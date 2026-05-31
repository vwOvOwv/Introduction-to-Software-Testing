#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用的测试更新辅助函数：prompt、合并、OpenAI 兼容请求。"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from collections import OrderedDict
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent


TEST_ANNOTATIONS = {
    "Test",
    "ParameterizedTest",
    "RepeatedTest",
    "TestFactory",
    "TestTemplate",
}


@dataclass
class TestMethod:
    name: str
    start_offset: int
    end_offset: int
    text: str


def extract_test_methods(source: str) -> dict[str, TestMethod]:
    methods: dict[str, TestMethod] = {}
    lines = source.splitlines(keepends=True)
    offsets: list[int] = []
    total = 0
    for line in lines:
        offsets.append(total)
        total += len(line)

    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped.startswith("@"):
            index += 1
            continue

        annotation_start = index
        has_test_annotation = False
        scan_index = index
        while scan_index < len(lines):
            current = lines[scan_index].strip()
            if current.startswith("@"):
                annotation_name = current[1:].split("(", 1)[0].split(".")[-1]
                if annotation_name in TEST_ANNOTATIONS:
                    has_test_annotation = True
                scan_index += 1
                continue
            if current == "" or current.startswith("//"):
                scan_index += 1
                continue
            break

        if not has_test_annotation:
            index += 1
            continue

        signature_parts: list[str] = []
        body_start_line: int | None = None
        while scan_index < len(lines):
            signature_parts.append(lines[scan_index])
            if "{" in lines[scan_index]:
                body_start_line = scan_index
                break
            scan_index += 1

        if body_start_line is None:
            index += 1
            continue

        signature_text = "".join(signature_parts)
        matches = list(re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", signature_text))
        if not matches:
            index += 1
            continue
        method_name = matches[-1].group(1)

        start_offset = offsets[annotation_start]
        brace_depth = 0
        end_line = body_start_line
        found_body = False
        for line_index in range(body_start_line, len(lines)):
            for char in lines[line_index]:
                if char == "{":
                    brace_depth += 1
                    found_body = True
                elif char == "}":
                    brace_depth -= 1
                    if found_body and brace_depth == 0:
                        end_line = line_index
                        break
            if found_body and brace_depth == 0:
                break

        end_offset = offsets[end_line] + len(lines[end_line])
        methods[method_name] = TestMethod(
            name=method_name,
            start_offset=start_offset,
            end_offset=end_offset,
            text=source[start_offset:end_offset],
        )
        index = end_line + 1

    return methods


def load_candidates(path: Path) -> list[dict]:
    if not path.is_file():
        raise FileNotFoundError(f"找不到候选列表: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("candidates", [])
    if not items:
        raise ValueError(f"{path} 中 candidates 为空")
    return items


def _git_show(repo: Path, revision: str, relpath: str) -> str:
    relpath = relpath.replace("\\", "/")
    cmd = ["git", "-C", str(repo), "show", f"{revision}:{relpath}"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(
            f"git show 失败: {' '.join(cmd)}\nstderr:\n{p.stderr.strip()}\n"
            "提示：若提示 path 在 A 中不存在，说明该 PR 的测试类是 B 上新建的，"
            "不能作为「A 旧测试」；请换 --index 或换 --test 为在 A 已存在的测试文件。"
        )
    return p.stdout


def _git_diff(repo: Path, a: str, b: str, paths: list[str]) -> str:
    cmd = ["git", "-C", str(repo), "diff", f"{a}..{b}", "--", *paths]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"git diff 失败: {' '.join(cmd)}\n{p.stderr.strip()}")
    return p.stdout


def _truncate(text: str, max_chars: int | None) -> tuple[str, bool]:
    if max_chars is None or max_chars <= 0 or len(text) <= max_chars:
        return text, False
    head = max_chars // 2
    tail = max_chars - head
    omitted = len(text) - head - tail
    merged = (
        text[:head]
        + f"\n\n... [省略 {omitted} 字符，可用 --max-chars 调大] ...\n\n"
        + text[-tail:]
    )
    return merged, True


_HUNK_RE = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def _parse_diff_line_numbers(diff_text: str, *, side: str) -> set[int]:
    lines_out: set[int] = set()
    cur: int | None = None
    for line in diff_text.splitlines():
        if line.startswith("@@"):
            m = _HUNK_RE.match(line)
            if m:
                cur = int(m.group(2)) if side == "new" else int(m.group(1))
            continue
        if cur is None:
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue
        if side == "new":
            if line.startswith("+") and not line.startswith("++"):
                lines_out.add(cur)
                cur += 1
            elif line.startswith(" "):
                cur += 1
        else:
            if line.startswith("-") and not line.startswith("--"):
                lines_out.add(cur)
                cur += 1
            elif line.startswith(" "):
                cur += 1
    return lines_out


def _line_to_method_name(source: str, line_no: int, methods: dict[str, TestMethod]) -> str | None:
    offset = 0
    lines = source.splitlines(keepends=True)
    if line_no < 1 or line_no > len(lines):
        return None
    for i in range(line_no):
        offset += len(lines[i])
    for name, m in methods.items():
        if m.start_offset <= offset < m.end_offset:
            return name
    return None


def _extract_prod_methods(source: str) -> dict[str, TestMethod]:
    methods: dict[str, TestMethod] = {}
    lines = source.splitlines(keepends=True)
    offsets: list[int] = []
    total = 0
    for line in lines:
        offsets.append(total)
        total += len(line)

    sig_re = re.compile(
        r"^\s*(?:@\w+(?:\([^)]*\))?\s*)*(?:public|protected|private)\s+[\w<>,\[\].\s]+\s+(\w+)\s*\("
    )
    index = 0
    while index < len(lines):
        m = sig_re.match(lines[index])
        if not m:
            index += 1
            continue
        method_name = m.group(1)
        if method_name in methods:
            index += 1
            continue
        start_line = index
        scan = index
        body_start: int | None = None
        while scan < len(lines):
            if "{" in lines[scan]:
                body_start = scan
                break
            scan += 1
        if body_start is None:
            index += 1
            continue
        start_offset = offsets[start_line]
        brace_depth = 0
        end_line = body_start
        found = False
        for li in range(body_start, len(lines)):
            for ch in lines[li]:
                if ch == "{":
                    brace_depth += 1
                    found = True
                elif ch == "}":
                    brace_depth -= 1
                    if found and brace_depth == 0:
                        end_line = li
                        break
            if found and brace_depth == 0:
                break
        end_offset = offsets[end_line] + len(lines[end_line])
        methods[method_name] = TestMethod(
            name=method_name,
            start_offset=start_offset,
            end_offset=end_offset,
            text=source[start_offset:end_offset],
        )
        index = end_line + 1
    return methods


def _methods_for_diff_lines(source: str, line_numbers: set[int], *, test_file: bool) -> dict[str, str]:
    if not line_numbers:
        return {}
    all_m = extract_test_methods(source) if test_file else _extract_prod_methods(source)
    hit: dict[str, str] = {}
    for ln in line_numbers:
        name = _line_to_method_name(source, ln, all_m)
        if name and name not in hit:
            hit[name] = all_m[name].text
    return hit


def _infer_test_method_names_from_diff(test_diff: str) -> set[str]:
    names: set[str] = set()
    for line in test_diff.splitlines():
        if not line or line[0] not in "+-":
            continue
        body = line[1:]
        for m in re.finditer(r"\b(void|boolean|int|long|String)\s+(\w+)\s*\(", body):
            names.add(m.group(2))
    return names


_IMPORT_BLOCK_START = "// IMPORTS_START"
_IMPORT_BLOCK_END = "// IMPORTS_END"
_IMPORT_BLOCK_RE = re.compile(
    rf"{re.escape(_IMPORT_BLOCK_START)}\s*(.*?)\s*{re.escape(_IMPORT_BLOCK_END)}",
    flags=re.DOTALL,
)
_DELETE_TESTS_START = "// DELETE_TESTS_START"
_DELETE_TESTS_END = "// DELETE_TESTS_END"
_DELETE_TESTS_RE = re.compile(
    rf"{re.escape(_DELETE_TESTS_START)}\s*(.*?)\s*{re.escape(_DELETE_TESTS_END)}",
    flags=re.DOTALL,
)


def _normalize_param_types(params: str) -> str:
    parts = [p.strip() for p in params.split(",") if p.strip()]
    normalized: list[str] = []
    for item in parts:
        item = re.sub(r"@\w+(?:\([^)]*\))?\s*", "", item).strip()
        item = re.sub(r"\bfinal\b\s*", "", item).strip()
        item = re.sub(r"\s+", " ", item)
        type_only = re.sub(r"\s+[A-Za-z_]\w*$", "", item).strip()
        normalized.append(type_only or item)
    return ", ".join(normalized)


def _is_comment_only_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*") or stripped.startswith("*/")


def _is_modifier_only_line(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and bool(re.fullmatch(r"(?:public|protected|private|static|abstract|final)\s+", stripped + " "))


def _line_start_offsets(lines: list[str]) -> list[int]:
    offsets: list[int] = []
    total = 0
    for line in lines:
        offsets.append(total)
        total += len(line)
    return offsets


def _iter_code_chars(source: str, start: int = 0):
    in_line_comment = False
    in_block_comment = False
    in_string = False
    in_char = False
    escaped = False
    index = start
    while index < len(source):
        char = source[index]
        next_char = source[index + 1] if index + 1 < len(source) else ""
        if in_line_comment:
            if char == "\n":
                in_line_comment = False
            index += 1
            continue
        if in_block_comment:
            if char == "*" and next_char == "/":
                in_block_comment = False
                index += 2
                continue
            index += 1
            continue
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if in_char:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == "'":
                in_char = False
            index += 1
            continue
        if char == "/" and next_char == "/":
            in_line_comment = True
            index += 2
            continue
        if char == "/" and next_char == "*":
            in_block_comment = True
            index += 2
            continue
        if char == '"':
            in_string = True
            index += 1
            continue
        if char == "'":
            in_char = True
            index += 1
            continue
        yield index, char
        index += 1


_BRACE_MATCH_CACHE_MAX_SOURCES = 8
_BRACE_MATCH_CACHE: OrderedDict[str, dict[int, int]] = OrderedDict()


def _brace_match_cache_for(source: str) -> dict[int, int]:
    cache = _BRACE_MATCH_CACHE.get(source)
    if cache is not None:
        _BRACE_MATCH_CACHE.move_to_end(source)
        return cache
    cache = {}
    _BRACE_MATCH_CACHE[source] = cache
    if len(_BRACE_MATCH_CACHE) > _BRACE_MATCH_CACHE_MAX_SOURCES:
        _BRACE_MATCH_CACHE.popitem(last=False)
    return cache


def _find_matching_brace(source: str, open_offset: int) -> int:
    brace_cache = _brace_match_cache_for(source)
    cached_close = brace_cache.get(open_offset)
    if cached_close is not None:
        return cached_close
    depth = 0
    stack: list[int] = []
    in_line_comment = False
    in_block_comment = False
    in_string = False
    in_char = False
    escaped = False
    index = open_offset
    while index < len(source):
        char = source[index]
        next_char = source[index + 1] if index + 1 < len(source) else ""
        if in_line_comment:
            if char == "\n":
                in_line_comment = False
            index += 1
            continue
        if in_block_comment:
            if char == "*" and next_char == "/":
                in_block_comment = False
                index += 2
                continue
            index += 1
            continue
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if in_char:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == "'":
                in_char = False
            index += 1
            continue
        if char == "/" and next_char == "/":
            in_line_comment = True
            index += 2
            continue
        if char == "/" and next_char == "*":
            in_block_comment = True
            index += 2
            continue
        if char == '"':
            in_string = True
            index += 1
            continue
        if char == "'":
            in_char = True
            index += 1
            continue
        if char == "{":
            cached_close = brace_cache.get(index)
            if cached_close is not None:
                if depth == 0:
                    return cached_close
                index = cached_close + 1
                continue
            depth += 1
            stack.append(index)
        elif char == "}":
            if depth == 0:
                index += 1
                continue
            depth -= 1
            if stack:
                brace_cache[stack.pop()] = index
            if depth == 0:
                return index
        index += 1
    raise ValueError("找不到匹配的大括号")


def _find_outer_class_bounds(source: str) -> tuple[str, int, int] | None:
    type_decl_re = re.compile(
        r"^\s*(?:@\w+(?:\([^)]*\))?\s*)*"
        r"(?:(?:public|protected|private|static|abstract|final)\s+)*"
        r"class\s+(\w+)\b"
    )
    lines = source.splitlines(keepends=True)
    offsets = _line_start_offsets(lines)
    for index, line in enumerate(lines):
        if _is_comment_only_line(line):
            continue
        match = type_decl_re.match(line)
        if not match:
            continue
        open_offset = source.find("{", offsets[index])
        if open_offset < 0:
            continue
        close_offset = _find_matching_brace(source, open_offset)
        return match.group(1), open_offset, close_offset
    return None


def _outer_class_name(source: str) -> str | None:
    bounds = _find_outer_class_bounds(source)
    return bounds[0] if bounds else None


def _extract_import_lines(source: str) -> list[str]:
    return [line.strip() for line in source.splitlines() if line.strip().startswith("import ")]


def _extract_import_block(source: str) -> list[str] | None:
    match = _IMPORT_BLOCK_RE.search(source)
    if not match:
        return None
    lines = [line.strip() for line in match.group(1).splitlines() if line.strip()]
    return [line for line in lines if line.startswith("import ")]


def _replace_import_section(base_source: str, import_lines: list[str]) -> str:
    lines = base_source.splitlines(keepends=True)
    package_idx = -1
    first_import_idx = -1
    last_import_idx = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("package "):
            package_idx = i
        if stripped.startswith("import "):
            if first_import_idx < 0:
                first_import_idx = i
            last_import_idx = i
    if first_import_idx >= 0:
        start_idx = first_import_idx
        end_idx = last_import_idx + 1
    elif package_idx >= 0:
        start_idx = package_idx + 1
        end_idx = package_idx + 1
    else:
        start_idx = 0
        end_idx = 0
    while start_idx < len(lines) and not lines[start_idx].strip():
        start_idx += 1
    while end_idx < len(lines) and lines[end_idx].strip().startswith("import "):
        end_idx += 1
    while end_idx < len(lines) and not lines[end_idx].strip():
        end_idx += 1
    if not import_lines:
        replacement = "\n" if package_idx >= 0 else ""
    else:
        replacement = "\n" + "".join(f"{line}\n" for line in import_lines) + "\n"
    lines[start_idx:end_idx] = [replacement]
    return "".join(lines)


def _merge_import_lists(base_imports: list[str], preferred_imports: list[str]) -> list[str]:
    merged: list[str] = []
    seen: dict[tuple[str, str], int] = {}
    for import_line in base_imports + preferred_imports:
        body = import_line.removeprefix("import ").removesuffix(";").strip()
        kind = "static" if body.startswith("static ") else "normal"
        target = body.removeprefix("static ").strip()
        key = (kind, target.rsplit(".", 1)[-1])
        if key in seen:
            merged[seen[key]] = import_line
        else:
            seen[key] = len(merged)
            merged.append(import_line)
    return merged


def _apply_import_patch(base_source: str, patch_source: str) -> str:
    block_imports = _extract_import_block(patch_source)
    if block_imports is not None:
        return _replace_import_section(base_source, block_imports)
    patch_imports = _extract_import_lines(patch_source)
    if not patch_imports:
        return base_source
    existing = set(_extract_import_lines(base_source))
    to_add = [imp for imp in patch_imports if imp not in existing]
    if not to_add:
        return base_source
    merged_imports = _extract_import_lines(base_source) + to_add
    return _replace_import_section(base_source, merged_imports)


def _clean_delete_test_name(line: str) -> str | None:
    cleaned = line.strip()
    cleaned = re.sub(r"^(?:[-*]\s*)?(?://\s*)?", "", cleaned).strip()
    cleaned = cleaned.strip("` ,;")
    match = re.search(r"\b([A-Za-z_]\w*)\b", cleaned)
    return match.group(1) if match else None


def extract_delete_test_names(text: str) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()

    def add(name: str | None) -> None:
        if name and name not in seen:
            seen.add(name)
            names.append(name)

    for block in _DELETE_TESTS_RE.findall(text):
        for line in block.splitlines():
            add(_clean_delete_test_name(line))

    for match in re.finditer(r"(?:删除|移除|delete|remove)\s+`?([A-Za-z_]\w*)`?", text, flags=re.I):
        name = match.group(1)
        if name.startswith("test") or name.endswith("Test"):
            add(name)

    return names


def _remove_delete_tests_block(source: str) -> str:
    return _DELETE_TESTS_RE.sub("", source)


def _apply_delete_test_patch(base_source: str, patch_source: str) -> tuple[str, bool]:
    names = extract_delete_test_names(patch_source)
    if not names:
        return base_source, False
    methods = extract_test_methods(base_source)
    result = base_source
    changed = False
    for name in sorted(names, key=lambda n: methods.get(n, TestMethod(n, 0, 0, "")).start_offset, reverse=True):
        method = methods.get(name)
        if not method:
            continue
        result = result[: method.start_offset] + result[method.end_offset :]
        changed = True
    return result, changed


def _looks_like_full_test_class(source: str, *, expected_class_name: str | None) -> bool:
    if expected_class_name and re.search(rf"\bclass\s+{re.escape(expected_class_name)}\b", source):
        return True
    return source.lstrip().startswith("package ")


def _extract_test_method_blocks(source: str) -> dict[str, TestMethod]:
    methods: dict[str, TestMethod] = {}
    lines = source.splitlines(keepends=True)
    offsets: list[int] = []
    total = 0
    for line in lines:
        offsets.append(total)
        total += len(line)
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped.startswith("@"):
            index += 1
            continue
        annotation_start = index
        has_test_annotation = False
        scan_index = index
        while scan_index < len(lines):
            current = lines[scan_index].strip()
            if current.startswith("@"):
                annotation_name = current[1:].split("(", 1)[0].split(".")[-1]
                if annotation_name in {
                    "Test",
                    "ParameterizedTest",
                    "RepeatedTest",
                    "TestFactory",
                    "TestTemplate",
                }:
                    has_test_annotation = True
                scan_index += 1
                continue
            if current == "" or current.startswith("//"):
                scan_index += 1
                continue
            break
        if not has_test_annotation:
            index += 1
            continue
        signature_start = scan_index
        signature_parts: list[str] = []
        body_start_line: int | None = None
        while scan_index < len(lines):
            signature_parts.append(lines[scan_index])
            if "{" in lines[scan_index]:
                body_start_line = scan_index
                break
            scan_index += 1
        if body_start_line is None:
            index += 1
            continue
        signature_text = "".join(signature_parts)
        matches = list(re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", signature_text))
        if not matches:
            index += 1
            continue
        method_name = matches[-1].group(1)
        start_offset = offsets[annotation_start]
        brace_depth = 0
        end_line = body_start_line
        found_body = False
        for line_index in range(body_start_line, len(lines)):
            for char in lines[line_index]:
                if char == "{":
                    brace_depth += 1
                    found_body = True
                elif char == "}":
                    brace_depth -= 1
                    if found_body and brace_depth == 0:
                        end_line = line_index
                        break
            if found_body and brace_depth == 0:
                break
        end_offset = offsets[end_line] + len(lines[end_line])
        methods[method_name] = TestMethod(
            name=method_name,
            start_offset=start_offset,
            end_offset=end_offset,
            text=source[start_offset:end_offset],
        )
        index = end_line + 1
    return methods


def _extract_nested_classes(source: str) -> dict[str, TestMethod]:
    outer = _outer_class_name(source)
    if not outer:
        return {}
    class_match = re.search(rf"\bclass\s+{re.escape(outer)}\b", source)
    if not class_match:
        return {}
    body_start = source.find("{", class_match.end())
    if body_start < 0:
        return {}
    body_end = _find_matching_brace(source, body_start)
    lines = source.splitlines(keepends=True)
    offsets = _line_start_offsets(lines)
    depths: list[int] = []
    depth = 0
    source_all = "".join(lines)
    line_no = 0
    next_line_start = len(lines[0]) if lines else 0
    brace_events: list[list[str]] = [[] for _ in lines]
    for index, char in _iter_code_chars(source_all):
        while line_no + 1 < len(lines) and index >= next_line_start:
            line_no += 1
            next_line_start += len(lines[line_no])
        if char in "{}" and line_no < len(brace_events):
            brace_events[line_no].append(char)
    for line_index, line in enumerate(lines):
        depths.append(depth)
        for char in brace_events[line_index]:
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
    members: dict[str, TestMethod] = {}
    type_decl_re = re.compile(
        r"^\s*(?:@\w+(?:\([^)]*\))?\s*)*"
        r"(?:(?:public|protected|private|static|abstract|final)\s+)*"
        r"(?:class|interface|enum|record)\s+(\w+)\b"
    )
    index = 0
    while index < len(lines):
        if offsets[index] <= body_start or offsets[index] >= body_end or depths[index] != 1:
            index += 1
            continue
        stripped = lines[index].strip()
        if not stripped or _is_comment_only_line(lines[index]):
            index += 1
            continue
        start_line = index
        while start_line > 0 and depths[start_line - 1] == 1:
            prev = lines[start_line - 1]
            if not prev.strip() or prev.lstrip().startswith("@") or _is_comment_only_line(prev) or _is_modifier_only_line(prev):
                start_line -= 1
                continue
            break
        signature_end_line = index
        open_brace_offset: int | None = None
        while signature_end_line < len(lines) and offsets[signature_end_line] < body_end:
            if depths[signature_end_line] != 1:
                break
            line = lines[signature_end_line]
            type_match = type_decl_re.match(line)
            if type_match:
                open_brace_offset = source.find("{", offsets[signature_end_line], body_end)
                if open_brace_offset >= 0:
                    close_offset = _find_matching_brace(source, open_brace_offset)
                    end_offset = close_offset + 1
                    text = source[offsets[start_line]:end_offset]
                    key = f"type:{type_match.group(1)}"
                    members[key] = TestMethod(key, offsets[start_line], end_offset, text)
                    while index < len(lines) and offsets[index] < end_offset:
                        index += 1
                    break
            brace_pos = line.find("{")
            if brace_pos >= 0:
                open_brace_offset = offsets[signature_end_line] + brace_pos
                break
            if ";" in line:
                end_offset = offsets[signature_end_line] + line.rfind(";") + 1
                signature = source[offsets[start_line]:end_offset]
                key = None
                declaration_lines = []
                for sig_line in signature.splitlines():
                    stripped_sig = sig_line.strip()
                    if not stripped_sig or _is_comment_only_line(sig_line) or stripped_sig.startswith("@"):
                        continue
                    declaration_lines.append(stripped_sig)
                declaration = " ".join(declaration_lines)
                method_matches = re.findall(r"([A-Za-z_]\w*)\s*\(([^()]*)\)", declaration, flags=re.DOTALL)
                if method_matches:
                    method_name = method_matches[-1][0]
                    params = _normalize_param_types(method_matches[-1][1])
                    key = f"method:{method_name}({params})"
                else:
                    field_match = re.search(r"([A-Za-z_]\w*)\s*(?:=[^;]*)?;\s*$", declaration, flags=re.DOTALL)
                    if field_match:
                        key = f"field:{field_match.group(1)}"
                if key:
                    members[key] = TestMethod(key, offsets[start_line], end_offset, signature)
                index = signature_end_line + 1
                break
            signature_end_line += 1
        else:
            index += 1
            continue
        if open_brace_offset is None:
            continue
        close_offset = _find_matching_brace(source, open_brace_offset)
        end_offset = close_offset + 1
        signature = source[offsets[start_line]:open_brace_offset]
        declaration_lines = []
        for sig_line in signature.splitlines():
            stripped_sig = sig_line.strip()
            if not stripped_sig or _is_comment_only_line(sig_line) or stripped_sig.startswith("@"):
                continue
            declaration_lines.append(stripped_sig)
        declaration = " ".join(declaration_lines)
        method_matches = re.findall(r"([A-Za-z_]\w*)\s*\(([^()]*)\)", declaration, flags=re.DOTALL)
        if method_matches:
            method_name = method_matches[-1][0]
            params = _normalize_param_types(method_matches[-1][1])
            key = f"method:{method_name}({params})"
            members[key] = TestMethod(key, offsets[start_line], end_offset, source[offsets[start_line]:end_offset])
        while index < len(lines) and offsets[index] < end_offset:
            index += 1
    return members


def _extract_class_members(source: str) -> dict[str, TestMethod]:
    """Extract direct members of the outer class: methods, fields, and nested types."""
    return _extract_nested_classes(source)


def extract_nested_classes(source: str) -> dict[str, TestMethod]:
    return {
        key.split(":", 1)[1]: TestMethod(
            name=member.name,
            start_offset=member.start_offset,
            end_offset=member.end_offset,
            text=member.text,
        )
        for key, member in _extract_nested_classes(source).items()
        if key.startswith("type:")
    }


def _extract_top_level_type_blocks(source: str) -> dict[str, TestMethod]:
    bounds = _find_outer_class_bounds(source)
    outer_name = bounds[0] if bounds else None
    lines = source.splitlines(keepends=True)
    offsets = _line_start_offsets(lines)
    depths: list[int] = []
    depth = 0
    source_all = "".join(lines)
    line_no = 0
    next_line_start = len(lines[0]) if lines else 0
    brace_events: list[list[str]] = [[] for _ in lines]
    for index, char in _iter_code_chars(source_all):
        while line_no + 1 < len(lines) and index >= next_line_start:
            line_no += 1
            next_line_start += len(lines[line_no])
        if char in "{}" and line_no < len(brace_events):
            brace_events[line_no].append(char)
    for line_index, line in enumerate(lines):
        depths.append(depth)
        for char in brace_events[line_index]:
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
    type_re = re.compile(
        r"^\s*(?:@\w+(?:\([^)]*\))?\s*)*"
        r"(?:(?:public|protected|private|static|abstract|final)\s+)*"
        r"(?:class|interface|enum|record)\s+(\w+)\b"
    )
    blocks: dict[str, TestMethod] = {}
    index = 0
    while index < len(lines):
        if depths[index] != 0 or _is_comment_only_line(lines[index]):
            index += 1
            continue
        match = type_re.match(lines[index])
        if not match:
            index += 1
            continue
        name = match.group(1)
        if name == outer_name:
            index += 1
            continue
        body_start = source.find("{", offsets[index])
        if body_start < 0:
            index += 1
            continue
        body_end = _find_matching_brace(source, body_start)
        start_line = index
        while start_line > 0 and depths[start_line - 1] == 0:
            prev = lines[start_line - 1]
            if not prev.strip() or prev.lstrip().startswith("@") or _is_comment_only_line(prev) or _is_modifier_only_line(prev):
                start_line -= 1
                continue
            break
        blocks[name] = TestMethod(
            name=name,
            start_offset=offsets[start_line],
            end_offset=body_end + 1,
            text=source[offsets[start_line]:body_end + 1],
        )
        while index < len(lines) and offsets[index] < body_end + 1:
            index += 1
    return blocks


def _extract_patch_type_blocks(source: str) -> dict[str, TestMethod]:
    lines = source.splitlines(keepends=True)
    offsets: list[int] = []
    total = 0
    for line in lines:
        offsets.append(total)
        total += len(line)
    type_re = re.compile(
        r"^\s*(?:@\w+(?:\([^)]*\))?\s*)*"
        r"(?:(?:public|protected|private|static|abstract|final)\s+)*"
        r"(?:class|interface|enum|record)\s+(\w+)\b"
    )
    blocks: dict[str, TestMethod] = {}
    index = 0
    while index < len(lines):
        match = type_re.match(lines[index])
        if not match:
            index += 1
            continue
        name = match.group(1)
        if name in blocks:
            index += 1
            continue
        start_line = index
        scan = index
        body_start: int | None = None
        while scan < len(lines):
            if "{" in lines[scan]:
                body_start = scan
                break
            scan += 1
        if body_start is None:
            index += 1
            continue
        start_offset = offsets[start_line]
        brace_depth = 0
        end_line = body_start
        found = False
        for li in range(body_start, len(lines)):
            for ch in lines[li]:
                if ch == "{":
                    brace_depth += 1
                    found = True
                elif ch == "}":
                    brace_depth -= 1
                    if found and brace_depth == 0:
                        end_line = li
                        break
            if found and brace_depth == 0:
                break
        end_offset = offsets[end_line] + len(lines[end_line])
        blocks[name] = TestMethod(
            name=name,
            start_offset=start_offset,
            end_offset=end_offset,
            text=source[start_offset:end_offset],
        )
        index = end_line + 1
    return blocks


def _apply_patch_type_blocks(base_source: str, patch_source: str) -> tuple[str, str]:
    patch_blocks = _extract_patch_type_blocks(patch_source)
    if not patch_blocks:
        return base_source, patch_source
    result = base_source
    remaining = patch_source
    for block in patch_blocks.values():
        remaining = remaining.replace(block.text, "", 1)
    existing_blocks = extract_nested_classes(result)
    for name, patch_block in sorted(
        patch_blocks.items(),
        key=lambda item: existing_blocks.get(item[0], item[1]).start_offset,
        reverse=True,
    ):
        if name in existing_blocks:
            current = existing_blocks[name]
            result = result[: current.start_offset] + patch_block.text + result[current.end_offset :]
        else:
            last_brace = result.rfind("}")
            if last_brace < 0:
                raise ValueError("基类中找不到类结束大括号")
            insert = "\n\n" + patch_block.text.rstrip() + "\n"
            result = result[:last_brace] + insert + result[last_brace:]
        existing_blocks = extract_nested_classes(result)
    return result, remaining


def _extract_member_snippet_blocks(source: str) -> dict[str, TestMethod]:
    wrapped = "class __PatchWrapper__ {\n" + source.strip() + "\n}\n"
    members = _extract_class_members(wrapped)
    if not members:
        return {}
    prefix = len("class __PatchWrapper__ {\n")
    return {
        key: TestMethod(
            name=member.name,
            start_offset=max(0, member.start_offset - prefix),
            end_offset=max(0, member.end_offset - prefix),
            text=member.text,
        )
        for key, member in members.items()
        if not key.startswith("type:")
    }


def _apply_patch_member_snippet(base_source: str, patch_source: str) -> str:
    snippet = _remove_patch_import_block(patch_source)
    for method in sorted(extract_test_methods(patch_source).values(), key=lambda item: item.start_offset, reverse=True):
        snippet = snippet.replace(method.text, "", 1)
    snippet = snippet.strip()
    if not snippet:
        return base_source
    patch_members = _extract_member_snippet_blocks(snippet)
    if not patch_members:
        last_brace = base_source.rfind("}")
        if last_brace < 0:
            raise ValueError("基类中找不到类结束大括号")
        insert = "\n\n" + snippet.rstrip() + "\n"
        return base_source[:last_brace] + insert + base_source[last_brace:]
    result = base_source
    existing_members = _extract_class_members(result)
    for key, patch_member in sorted(
        patch_members.items(),
        key=lambda item: existing_members.get(item[0], item[1]).start_offset,
        reverse=True,
    ):
        if key in existing_members:
            current = existing_members[key]
            result = result[: current.start_offset] + patch_member.text.rstrip() + result[current.end_offset :]
        else:
            last_brace = result.rfind("}")
            if last_brace < 0:
                raise ValueError("基类中找不到类结束大括号")
            insert = "\n\n" + patch_member.text.rstrip() + "\n"
            result = result[:last_brace] + insert + result[last_brace:]
        existing_members = _extract_member_snippet_blocks(result)
    return result


def _remove_patch_import_block(source: str) -> str:
    source = _IMPORT_BLOCK_RE.sub("", source)
    lines = [line for line in source.splitlines(keepends=True) if not line.strip().startswith("import ")]
    return "".join(lines)


def merge_patch_into_test_class(base_source: str, patch_source: str) -> str:
    outer_class_name = _outer_class_name(base_source)
    if _looks_like_full_test_class(patch_source, expected_class_name=outer_class_name):
        return patch_source.strip() + "\n"
    result, deleted = _apply_delete_test_patch(base_source, patch_source)
    patch_source = _remove_delete_tests_block(patch_source)
    if deleted:
        result = _apply_import_patch(result, patch_source)
        base_source = result
    base_m = extract_test_methods(base_source)
    patch_m = extract_test_methods(patch_source)
    if not patch_m:
        if deleted and not (_extract_import_lines(patch_source) or _extract_import_block(patch_source) or _extract_patch_type_blocks(patch_source)):
            return base_source
        result = _apply_import_patch(base_source, patch_source)
        result, remaining = _apply_patch_type_blocks(result, patch_source)
        result = _apply_patch_member_snippet(result, remaining)
        if result != base_source or deleted:
            return result
        raise ValueError("补丁中未识别到任何 @Test 方法，也未包含可应用的 import，且非完整测试类")
    result = base_source
    for name in sorted(patch_m.keys(), key=lambda n: base_m.get(n, patch_m[n]).start_offset, reverse=True):
        pm = patch_m[name]
        if name in base_m:
            bm = base_m[name]
            result = result[: bm.start_offset] + pm.text + result[bm.end_offset :]
        else:
            last_brace = result.rfind("}")
            if last_brace < 0:
                raise ValueError("基类中找不到类结束大括号")
            insert = "\n\n" + pm.text.rstrip() + "\n"
            result = result[:last_brace] + insert + result[last_brace:]
    result = _apply_import_patch(result, patch_source)
    result, remaining = _apply_patch_type_blocks(result, patch_source)
    return _apply_patch_member_snippet(result, remaining)


def merge_imports_from_reference(merged: str, reference: str) -> str:
    return _replace_import_section(
        merged,
        _merge_import_lists(_extract_import_lines(merged), _extract_import_lines(reference)),
    )


def sync_nested_classes_from_reference(merged: str, reference: str) -> str:
    ref_nested = extract_nested_classes(reference)
    if not ref_nested:
        return merged
    result = merged
    for name, ref_block in sorted(ref_nested.items(), key=lambda item: item[1].start_offset, reverse=True):
        if name not in result:
            continue
        merged_nested = extract_nested_classes(result)
        if name in merged_nested:
            block = merged_nested[name]
            result = result[: block.start_offset] + ref_block.text.rstrip() + result[block.end_offset :]
        else:
            last_brace = result.rfind("}")
            if last_brace < 0:
                continue
            insert = "\n\n" + ref_block.text.rstrip() + "\n"
            result = result[:last_brace] + insert + result[last_brace:]
    return result


def _sync_recursive_nested_classes_from_reference(merged: str, reference: str) -> str:
    def _extract_nested_class_paths(source: str, *, _prefix: str = "", _base_offset: int = 0) -> dict[str, TestMethod]:
        blocks: dict[str, TestMethod] = {}
        for name, block in extract_nested_classes(source).items():
            path = f"{_prefix}.{name}" if _prefix else name
            absolute_block = TestMethod(
                name=path,
                start_offset=_base_offset + block.start_offset,
                end_offset=_base_offset + block.end_offset,
                text=block.text,
            )
            blocks[path] = absolute_block
            blocks.update(_extract_nested_class_paths(block.text, _prefix=path, _base_offset=absolute_block.start_offset))
        return blocks

    ref_paths = _extract_nested_class_paths(reference)
    if not ref_paths:
        return merged
    name_to_paths: dict[str, list[str]] = {}
    for path in ref_paths:
        simple_name = path.rsplit(".", 1)[-1]
        name_to_paths.setdefault(simple_name, []).append(path)
    result = merged
    for path, ref_block in sorted(ref_paths.items(), key=lambda item: item[0].count(".")):
        if "." not in path:
            continue
        simple_name = path.rsplit(".", 1)[-1]
        if len(name_to_paths.get(simple_name, [])) != 1 or simple_name not in result:
            continue
        merged_paths = _extract_nested_class_paths(result)
        if path in merged_paths:
            current = merged_paths[path]
            result = result[: current.start_offset] + ref_block.text.rstrip() + result[current.end_offset :]
            merged_paths = _extract_nested_class_paths(result)
            duplicates = [
                block
                for other_path, block in merged_paths.items()
                if other_path.rsplit(".", 1)[-1] == simple_name and other_path != path
            ]
            for block in sorted(duplicates, key=lambda item: item.start_offset, reverse=True):
                result = result[: block.start_offset] + result[block.end_offset :]
            continue
        parent_path = path.rsplit(".", 1)[0]
        parent_block = merged_paths.get(parent_path)
        if not parent_block:
            continue
        misplaced = [block for other_path, block in merged_paths.items() if other_path.rsplit(".", 1)[-1] == simple_name]
        for block in sorted(misplaced, key=lambda item: item.start_offset, reverse=True):
            result = result[: block.start_offset] + result[block.end_offset :]
        merged_paths = _extract_nested_class_paths(result)
        parent_block = merged_paths.get(parent_path)
        if not parent_block:
            continue
        insert_at = parent_block.end_offset - 1
        insert_text = "\n\n" + ref_block.text.rstrip() + "\n"
        result = result[:insert_at] + insert_text + result[insert_at:]
    return result


def _remove_dangling_annotations(source: str) -> str:
    return re.sub(
        r"(?m)^[ \t]*@\w+(?:\([^\n)]*\))?[ \t]*\n(?:[ \t]*\n)*(?=[ \t]*})",
        "",
        source,
    )


def _remove_invalid_split_modifiers(source: str) -> str:
    return re.sub(r"(?m)^[ \t]*final[ \t]*\n(?=[ \t]*interface\b)", "", source)


def finalize_merged_test_class(merged: str, *, reference_source: str) -> str:
    out = merge_imports_from_reference(merged, reference_source)
    ref_top_level = _extract_top_level_type_blocks(reference_source)
    out_top_level = _extract_top_level_type_blocks(out)
    outer_bounds = _find_outer_class_bounds(out)
    outer_name = outer_bounds[0] if outer_bounds else None
    outer_start = out.find(f"class {outer_name}") if outer_name else len(out)
    for name, ref_block in sorted(
        ref_top_level.items(),
        key=lambda item: out_top_level.get(item[0], item[1]).start_offset,
        reverse=True,
    ):
        if not re.search(rf"\b{re.escape(name)}\b", out):
            continue
        if name in out_top_level:
            current = out_top_level[name]
            out = out[: current.start_offset] + ref_block.text.rstrip() + "\n\n" + out[current.end_offset :]
        else:
            out = out[:outer_start] + ref_block.text.rstrip() + "\n\n" + out[outer_start:]
        out_top_level = _extract_top_level_type_blocks(out)
        outer_bounds = _find_outer_class_bounds(out)
        outer_name = outer_bounds[0] if outer_bounds else None
        outer_start = out.find(f"class {outer_name}") if outer_name else len(out)
    out = sync_nested_classes_from_reference(out, reference_source)
    out = _sync_recursive_nested_classes_from_reference(out, reference_source)
    out = _remove_dangling_annotations(out)
    out = _remove_invalid_split_modifiers(out)
    ref_members = _extract_class_members(reference_source)
    result_members = _extract_class_members(out)
    for key, ref_member in sorted(
        ref_members.items(),
        key=lambda item: result_members.get(item[0], item[1]).start_offset,
        reverse=True,
    ):
        if key.startswith("type:"):
            continue
        name = key.split(":", 1)[1].split("(", 1)[0]
        if not re.search(rf"\b{re.escape(name)}\b", out):
            continue
        if key in result_members:
            current = result_members[key]
            out = out[: current.start_offset] + ref_member.text.rstrip() + out[current.end_offset :]
        else:
            last_brace = out.rfind("}")
            if last_brace < 0:
                continue
            out = out[:last_brace] + "\n\n" + ref_member.text.rstrip() + "\n" + out[last_brace:]
        result_members = _extract_class_members(out)
    ref_tests = extract_test_methods(reference_source)
    out_tests = extract_test_methods(out)
    for name, method in sorted(out_tests.items(), key=lambda item: item[1].start_offset, reverse=True):
        if name in ref_tests:
            continue
        out = out[: method.start_offset] + out[method.end_offset :]
    return out


def build_prompt_inputs(
    repo: Path,
    a: str,
    b: str,
    test_path: str,
    prod_paths: list[str],
) -> dict[str, str]:
    min_diff_chars_for_context = int(os.environ.get("MODEL_MIN_DIFF_CHARS_FOR_CONTEXT", "1200"))
    old_test_full = _git_show(repo, a, test_path)
    prod_diff_parts: list[str] = []
    prod_method_parts: list[str] = []
    for p in prod_paths:
        d = _git_diff(repo, a, b, [p])
        prod_diff_parts.append(f"===== {p} =====\n{d}")
        prod_source_b = _git_show(repo, b, p)
        new_lines = _parse_diff_line_numbers(d, side="new")
        methods_b = _methods_for_diff_lines(prod_source_b, new_lines, test_file=False)
        need_bodies = len(d.strip()) < min_diff_chars_for_context or bool(methods_b)
        if need_bodies and methods_b:
            for name, text in sorted(methods_b.items()):
                prod_method_parts.append(f"===== {p} :: {name} (提交 B) =====\n{text}")
    test_diff = _git_diff(repo, a, b, [test_path])
    old_lines = _parse_diff_line_numbers(test_diff, side="old")
    old_methods = _methods_for_diff_lines(old_test_full, old_lines, test_file=True)
    if not old_methods:
        for n in _infer_test_method_names_from_diff(test_diff):
            tm = extract_test_methods(old_test_full)
            if n in tm:
                old_methods[n] = tm[n].text
    if old_methods:
        old_test_snippet = "\n\n".join(f"// 方法: {n}\n{t}" for n, t in sorted(old_methods.items()))
        old_test_mode = "methods"
    else:
        old_test_snippet = old_test_full
        old_test_mode = "full_class_fallback"
    return {
        "prod_diff": "\n\n".join(prod_diff_parts),
        "prod_methods_b": "\n\n".join(prod_method_parts),
        "test_diff": test_diff,
        "old_test_snippet": old_test_snippet,
        "old_test_mode": old_test_mode,
        "test_path": test_path,
    }


def build_user_message(
    *,
    prod_diff: str,
    prod_methods_b: str,
    test_diff: str,
    test_path: str,
    old_test_snippet: str,
    old_test_mode: str,
    optional_note: str | None,
) -> str:
    td = test_diff.strip() if test_diff.strip() else "(测试文件在 A..B 之间无 diff)"
    parts = [
        "输入（不包含 B 上整份 main 源文件；仅 diff 与必要时受影响方法体）：",
        "",
        "1. 生产代码变更（git diff A..B）：",
        "```diff",
        prod_diff.rstrip() if prod_diff.strip() else "(无)",
        "```",
    ]
    if prod_methods_b.strip():
        parts.extend(
            [
                "",
                "2. diff 涉及的生产方法完整实现（提交 B；当 diff 片段过短或缺少上下文时补充）：",
                "```java",
                prod_methods_b.rstrip(),
                "```",
            ]
        )
        step_old = 3
    else:
        step_old = 2
    parts.extend(
        [
            "",
            f"{step_old}. 测试文件「{test_path}」变更（git diff A..B；人类金标准，用于定位要改哪些 @Test）：",
            "```diff",
            td,
            "```",
            "",
            f"{step_old + 1}. 旧测试（提交 A，模式={old_test_mode}；在新版本 B 上会失败）：",
            "```java",
            old_test_snippet.rstrip(),
            "```",
        ]
    )
    if optional_note:
        parts.extend(["", f"{step_old + 2}. 补充说明：", optional_note.strip()])
    return "\n".join(parts)


SYSTEM_PROMPT = """你是一位资深的 Java 单元测试专家，擅长使用 JUnit 5 和 Mockito。
任务：给定生产代码的 git diff、必要时 B 上受影响的生产方法实现、以及 A 上需修改的旧测试方法，请更新测试使其在 B 上可编译且断言通过。

输出格式（必须遵守）：
1. 先用 Markdown 无序列表说明：将新增、修改或删除哪些 @Test / @ParameterizedTest 方法（写出方法名），以及是否需要调整 import；每条一句话对照生产/测试 diff。
2. 再给出一个 Java 代码块：
    - 若需要修改文件头 import，请把“完整目标 import 区块”放在代码块最前面，并用以下标记包裹：
      // IMPORTS_START
      import ...;
      import ...;
      // IMPORTS_END
    - 若需要删除旧测试方法，请在代码块中输出以下标记；每行一个方法名：
      // DELETE_TESTS_START
      testOldBehavior
      testRemovedApi
      // DELETE_TESTS_END
    - 若只需新增 import，也可以仅在代码块最前面直接给出 import 语句；不要输出 package。
    - 其后只输出需新增或修改的测试方法的完整方法（含注解、签名、方法体）。
    - 不要输出整个测试类，除非类很短（约 <80 行）或必须整体替换。
3. 保持原有 package 与测试类名；除 import 和必要的测试方法外，不要输出无关内容；不要寒暄。"""


def chat_completion(
    *,
    api_key: str,
    api_base: str,
    model: str,
    system: str,
    user: str,
    timeout_sec: int = 120,
    max_output_tokens: int | None = None,
    continue_on_length: bool = True,
) -> tuple[str, dict[str, Any]]:
    def _chat_request(*, messages: list[dict[str, str]]) -> dict[str, Any]:
        url = api_base.rstrip("/") + "/v1/chat/completions"
        body: dict[str, Any] = {"model": model, "messages": messages, "temperature": 0.2}
        if max_output_tokens is not None:
            body["max_tokens"] = max_output_tokens
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {e.code}: {err_body}") from e
        return json.loads(raw)

    messages: list[dict[str, str]] = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    payload = _chat_request(messages=messages)
    choice = payload["choices"][0]
    content = choice["message"]["content"]
    finish_reason = choice.get("finish_reason")
    if finish_reason == "length" and continue_on_length:
        print("警告：输出在 max_tokens 处截断，正在自动续写一轮…", file=sys.stderr)
        messages.append({"role": "assistant", "content": content})
        messages.append(
            {
                "role": "user",
                "content": (
                    "上一段输出因长度上限被截断。请从断开处继续，只补全剩余 Java（测试方法或说明），"
                    "不要重复已输出内容，不要寒暄。"
                ),
            }
        )
        payload2 = _chat_request(messages=messages)
        choice2 = payload2["choices"][0]
        content = content + choice2["message"]["content"]
        payload = payload2
        finish_reason = choice2.get("finish_reason")
    payload.setdefault("_merged_finish_reason", finish_reason)
    return content, payload


def extract_java_from_markdown(markdown_text: str) -> str:
    marker = "\n---\n\n"
    content = markdown_text.split(marker, 1)[1] if marker in markdown_text else markdown_text
    fenced = re.findall(r"```(?:java)?\s*(.*?)```", content, flags=re.DOTALL)
    if fenced:
        code = fenced[0].strip()
        if code:
            return code + "\n"
        if extract_delete_test_names(content):
            return content.strip() + "\n"
        return "\n"
    return content.strip() + "\n"
