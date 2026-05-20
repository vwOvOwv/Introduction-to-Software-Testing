#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 git 取「B 上生产代码 + A 上旧测试」，调用 DeepSeek（OpenAI 兼容接口）生成更新后的测试。

依赖：仅标准库。API Key 默认从 key.py 中的 DEEPSEEK_API_KEY 导入。

样本来源：artifacts/lang_sample_candidates_filtered.json（Maven 验证通过的 135 条）。

示例：
  python update_tests_deepseek.py
    （无参数 = 第 1 条候选 --dry-run，只打印 prompt）
  python update_tests_deepseek.py --index 3
  python update_tests_deepseek.py --run-all
  python update_tests_deepseek.py --run-all --limit 5

  自定义单条：--a --b --test --prod
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import traceback
import urllib.error
import urllib.request
from collections import OrderedDict
from pathlib import Path
from typing import Any

from orchestrate_test_updates import TestMethod, extract_test_methods

try:
    from key import DEEPSEEK_API_KEY
except ImportError:
    DEEPSEEK_API_KEY = ""

# ---------------------------------------------------------------------------
# DeepSeek OpenAI 兼容接口
# ---------------------------------------------------------------------------
DEFAULT_API_BASE = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"
_ROOT = Path(__file__).resolve().parent


def _default_repo_path() -> Path:
    workspace_repo = _ROOT / "commons-lang"
    if (workspace_repo / ".git").is_dir():
        return workspace_repo
    parent_repo = _ROOT.parent / "commons-lang"
    return parent_repo


_DEFAULT_REPO = _default_repo_path()
_DEFAULT_CANDIDATES = _ROOT / "artifacts" / "lang_sample_candidates_filtered.json"

# diff 过短时，除 diff 外再附上 B 上受影响方法的完整方法体
_MIN_DIFF_CHARS_FOR_CONTEXT = 1200
# 粗算：1 token ≈ 3 字符（中英文混合）；deepseek-chat 上下文约 64k token 量级，仅作告警
_EST_CONTEXT_CHARS_WARN = int(os.environ.get("DEEPSEEK_CONTEXT_CHARS_WARN", "180000"))
# 默认输出 token 上限（可用环境变量加大；部分账号支持 8k~32k）
_DEFAULT_MAX_OUTPUT = int(os.environ.get("DEEPSEEK_MAX_OUTPUT_TOKENS", "8192"))

SYSTEM_PROMPT = """你是一位资深的 Java 单元测试专家，擅长使用 JUnit 5 和 Mockito。
任务：给定生产代码的 git diff、必要时 B 上受影响的生产方法实现、以及 A 上需修改的旧测试方法，请更新测试使其在 B 上可编译且断言通过。

输出格式（必须遵守）：
1. 先用 Markdown 无序列表说明：将新增或修改哪些 @Test / @ParameterizedTest 方法（写出方法名），以及是否需要调整 import；每条一句话对照生产/测试 diff。
2. 再给出一个 Java 代码块：
    - 若需要修改文件头 import，请把“完整目标 import 区块”放在代码块最前面，并用以下标记包裹：
      // IMPORTS_START
      import ...;
      import ...;
      // IMPORTS_END
    - 若只需新增 import，也可以仅在代码块最前面直接给出 import 语句；不要输出 package。
    - 其后只输出需修改的测试方法的完整方法（含注解、签名、方法体）。
    - 不要输出整个测试类，除非类很短（约 <80 行）或必须整体替换。
3. 保持原有 package 与测试类名；除 import 和必要的测试方法外，不要输出无关内容；不要寒暄。"""

_IMPORT_BLOCK_START = "// IMPORTS_START"
_IMPORT_BLOCK_END = "// IMPORTS_END"
_IMPORT_BLOCK_RE = re.compile(
    rf"{re.escape(_IMPORT_BLOCK_START)}\s*(.*?)\s*{re.escape(_IMPORT_BLOCK_END)}",
    flags=re.DOTALL,
)


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
    """max_chars 为 None 或 <=0 时不截断。"""
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
    """side: 'new' (+) 或 'old' (-)。"""
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
            elif line.startswith("-"):
                pass
        else:
            if line.startswith("-") and not line.startswith("--"):
                lines_out.add(cur)
                cur += 1
            elif line.startswith(" "):
                cur += 1
            elif line.startswith("+"):
                pass
    return lines_out


def _line_to_method_name(source: str, line_no: int, methods: dict[str, TestMethod]) -> str | None:
    """1-based line_no。"""
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


def _methods_for_diff_lines(source: str, line_numbers: set[int], *, test_file: bool) -> dict[str, str]:
    if not line_numbers:
        return {}
    if test_file:
        all_m = extract_test_methods(source)
    else:
        all_m = _extract_prod_methods(source)
    hit: dict[str, str] = {}
    for ln in line_numbers:
        name = _line_to_method_name(source, ln, all_m)
        if name and name not in hit:
            hit[name] = all_m[name].text
    return hit


def _extract_prod_methods(source: str) -> dict[str, TestMethod]:
    """从生产类源码中提取方法（启发式，按签名 + 大括号匹配）。"""
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


def _infer_test_method_names_from_diff(test_diff: str) -> set[str]:
    names: set[str] = set()
    for line in test_diff.splitlines():
        if not line or line[0] not in "+-":
            continue
        body = line[1:]
        for m in re.finditer(r"\b(void|boolean|int|long|String)\s+(\w+)\s*\(", body):
            names.add(m.group(2))
        for m in re.finditer(r"@(?:Parameterized)?Test\b", body):
            pass
    return names


def _replace_import_section(base_source: str, import_lines: list[str]) -> str:
    """用给定 import 区块替换文件头 import 区域。"""
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


def _extract_import_block(source: str) -> list[str] | None:
    match = _IMPORT_BLOCK_RE.search(source)
    if not match:
        return None
    lines = [line.strip() for line in match.group(1).splitlines() if line.strip()]
    return [line for line in lines if line.startswith("import ")]


def _apply_import_patch(base_source: str, patch_source: str) -> str:
    """应用补丁中的 import 变更：优先替换完整 import 区块，否则只增量添加。"""
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


def _looks_like_full_test_class(source: str, *, expected_class_name: str | None) -> bool:
    if expected_class_name and re.search(rf"\bclass\s+{re.escape(expected_class_name)}\b", source):
        return True
    return source.lstrip().startswith("package ")


def _normalize_signature(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _split_java_params(params: str) -> list[str]:
    items: list[str] = []
    current: list[str] = []
    angle_depth = 0
    paren_depth = 0
    brace_depth = 0
    bracket_depth = 0
    for char in params:
        if char == "," and angle_depth == paren_depth == brace_depth == bracket_depth == 0:
            item = "".join(current).strip()
            if item:
                items.append(item)
            current = []
            continue
        current.append(char)
        if char == "<":
            angle_depth += 1
        elif char == ">":
            angle_depth = max(0, angle_depth - 1)
        elif char == "(":
            paren_depth += 1
        elif char == ")":
            paren_depth = max(0, paren_depth - 1)
        elif char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth = max(0, brace_depth - 1)
        elif char == "[":
            bracket_depth += 1
        elif char == "]":
            bracket_depth = max(0, bracket_depth - 1)
    tail = "".join(current).strip()
    if tail:
        items.append(tail)
    return items


def _normalize_param_types(params: str) -> str:
    normalized: list[str] = []
    for param in _split_java_params(params):
        item = re.sub(r"@\w+(?:\([^)]*\))?\s*", "", param).strip()
        item = re.sub(r"\bfinal\b\s*", "", item).strip()
        item = re.sub(r"\s+", " ", item)
        type_only = re.sub(r"\s+[A-Za-z_]\w*$", "", item).strip()
        normalized.append(type_only or item)
    return ", ".join(normalized)


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


def _line_start_offsets(lines: list[str]) -> list[int]:
    offsets: list[int] = []
    total = 0
    for line in lines:
        offsets.append(total)
        total += len(line)
    return offsets


def _line_brace_depths(lines: list[str]) -> list[int]:
    depths: list[int] = []
    depth = 0
    source = "".join(lines)
    line_no = 0
    next_line_start = len(lines[0]) if lines else 0
    brace_events: list[list[str]] = [[] for _ in lines]
    for index, char in _iter_code_chars(source):
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
    return depths


def _is_comment_only_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*") or stripped.startswith("*/")


def _is_modifier_only_line(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and bool(re.fullmatch(r"(?:public|protected|private|static|abstract|final)\s+", stripped + " "))


def _member_key_from_signature(signature: str) -> str | None:
    declaration_lines = []
    for line in signature.splitlines():
        stripped = line.strip()
        if not stripped or _is_comment_only_line(line) or stripped.startswith("@"):
            continue
        declaration_lines.append(stripped)
    declaration = " ".join(declaration_lines)
    method_matches = re.findall(r"([A-Za-z_]\w*)\s*\(([^()]*)\)", declaration, flags=re.DOTALL)
    method_match = method_matches[-1] if method_matches else None
    if method_match:
        name = method_match[0]
        params = _normalize_param_types(method_match[1])
        return f"method:{name}({params})"
    field_match = re.search(r"([A-Za-z_]\w*)\s*(?:=[^;]*)?;\s*$", declaration, flags=re.DOTALL)
    if field_match:
        return f"field:{field_match.group(1)}"
    return None


def _extract_class_members(source: str) -> dict[str, TestMethod]:
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
    depths = _line_brace_depths(lines)
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
                key = _member_key_from_signature(signature)
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
        key = _member_key_from_signature(signature)
        if key:
            members[key] = TestMethod(key, offsets[start_line], end_offset, source[offsets[start_line]:end_offset])
        while index < len(lines) and offsets[index] < end_offset:
            index += 1
    return members


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


def _extract_top_level_type_blocks(source: str) -> dict[str, TestMethod]:
    bounds = _find_outer_class_bounds(source)
    outer_name = bounds[0] if bounds else None
    lines = source.splitlines(keepends=True)
    offsets = _line_start_offsets(lines)
    depths = _line_brace_depths(lines)
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
        end_line = index
        while end_line + 1 < len(lines) and offsets[end_line] < body_end:
            end_line += 1
        blocks[name] = TestMethod(
            name=name,
            start_offset=offsets[start_line],
            end_offset=body_end + 1,
            text=source[offsets[start_line]:body_end + 1],
        )
        while index < len(lines) and offsets[index] < body_end + 1:
            index += 1
    return blocks


def _apply_top_level_type_blocks(base_source: str, patch_source: str) -> tuple[str, str]:
    patch_blocks = _extract_top_level_type_blocks(patch_source)
    if not patch_blocks:
        return base_source, patch_source

    result = base_source
    remaining = patch_source
    for block in patch_blocks.values():
        remaining = remaining.replace(block.text, "", 1)

    existing_blocks = _extract_top_level_type_blocks(result)
    bounds = _find_outer_class_bounds(result)
    outer_start = result.find(f"class {bounds[0]}") if bounds else result.rfind("}")
    for name, patch_block in sorted(
        patch_blocks.items(),
        key=lambda item: existing_blocks.get(item[0], item[1]).start_offset,
        reverse=True,
    ):
        if name in existing_blocks:
            current = existing_blocks[name]
            result = result[: current.start_offset] + patch_block.text.rstrip() + "\n\n" + result[current.end_offset :]
        else:
            insert_at = outer_start if outer_start is not None and outer_start >= 0 else len(result)
            result = result[:insert_at] + patch_block.text.rstrip() + "\n\n" + result[insert_at:]
        existing_blocks = _extract_top_level_type_blocks(result)
        bounds = _find_outer_class_bounds(result)
        outer_start = result.find(f"class {bounds[0]}") if bounds else result.rfind("}")
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


def _extract_patch_type_blocks(source: str) -> dict[str, TestMethod]:
    """提取补丁片段中的嵌套类型定义（class/interface/enum/record）。"""
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


def _remove_patch_import_block(source: str) -> str:
    source = _IMPORT_BLOCK_RE.sub("", source)
    lines = [line for line in source.splitlines(keepends=True) if not line.strip().startswith("import ")]
    return "".join(lines)


def _apply_patch_type_blocks(base_source: str, patch_source: str) -> tuple[str, str]:
    """应用补丁中的嵌套类型，并返回剩余未处理片段。"""
    patch_blocks = _extract_patch_type_blocks(patch_source)
    if not patch_blocks:
        return base_source, patch_source

    result = base_source
    existing_blocks = extract_nested_classes(result)
    remaining = patch_source
    for name, patch_block in sorted(
        patch_blocks.items(),
        key=lambda item: existing_blocks.get(item[0], item[1]).start_offset,
        reverse=True,
    ):
        remaining = remaining.replace(patch_block.text, "", 1)
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


def _apply_patch_member_snippet(base_source: str, patch_source: str) -> str:
    """把补丁中除 import、测试方法、嵌套类型外的剩余类成员片段插入测试类。"""
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
        existing_members = _extract_class_members(result)
    return result


def merge_patch_into_test_class(base_source: str, patch_source: str) -> str:
    """将模型输出的 import / 若干测试方法合并进 A 上的完整测试类。"""
    outer_class_name = _outer_class_name(base_source)
    if _looks_like_full_test_class(patch_source, expected_class_name=outer_class_name):
        return patch_source.strip() + "\n"
    base_m = extract_test_methods(base_source)
    patch_m = extract_test_methods(patch_source)
    if not patch_m:
        result = _apply_import_patch(base_source, patch_source)
        result, remaining = _apply_patch_type_blocks(result, patch_source)
        result = _apply_patch_member_snippet(result, remaining)
        if result != base_source:
            return result
        raise ValueError("补丁中未识别到任何 @Test 方法，也未包含可应用的 import，且非完整测试类")
    result = base_source
    for name in sorted(patch_m.keys(), key=lambda n: base_m.get(n, patch_m[n]).start_offset, reverse=True):
        pm = patch_m[name]
        if name in base_m:
            bm = base_m[name]
            result = result[: bm.start_offset] + pm.text + result[bm.end_offset :]
        else:
            # 新方法：插在最后一个 } 之前
            last_brace = result.rfind("}")
            if last_brace < 0:
                raise ValueError("基类中找不到类结束大括号")
            insert = "\n\n" + pm.text.rstrip() + "\n"
            result = result[:last_brace] + insert + result[last_brace:]
    result = _apply_import_patch(result, patch_source)
    result, remaining = _apply_patch_type_blocks(result, patch_source)
    return _apply_patch_member_snippet(result, remaining)


def _outer_class_name(source: str) -> str | None:
    bounds = _find_outer_class_bounds(source)
    return bounds[0] if bounds else None


def _extract_import_lines(source: str) -> list[str]:
    return [line.strip() for line in source.splitlines() if line.strip().startswith("import ")]


def _import_identity(import_line: str) -> tuple[str, str]:
    body = import_line.removeprefix("import ").removesuffix(";").strip()
    kind = "static" if body.startswith("static ") else "normal"
    target = body.removeprefix("static ").strip()
    return kind, target.rsplit(".", 1)[-1]


def _merge_import_lists(base_imports: list[str], preferred_imports: list[str]) -> list[str]:
    merged: list[str] = []
    seen: dict[tuple[str, str], int] = {}
    for import_line in base_imports + preferred_imports:
        key = _import_identity(import_line)
        if key in seen:
            merged[seen[key]] = import_line
        else:
            seen[key] = len(merged)
            merged.append(import_line)
    return merged


def merge_imports_from_reference(merged: str, reference: str) -> str:
    """把 B 上测试类有而合并结果缺的 import 补进文件头。"""
    return _replace_import_section(
        merged,
        _merge_import_lists(_extract_import_lines(merged), _extract_import_lines(reference)),
    )


_NESTED_CLASS_RE = re.compile(
    r"^\s*(?:@\w+(?:\([^)]*\))?\s*)*"
    r"(?:(?:public|protected|private|static|abstract|final)\s+)*(?:class|interface|enum|record)\s+(\w+)\b"
)


def extract_nested_classes(source: str) -> dict[str, TestMethod]:
    """提取测试类内嵌套类型（不含最外层 public class XxxTest）。"""
    return {
        key.split(":", 1)[1]: TestMethod(
            name=member.name,
            start_offset=member.start_offset,
            end_offset=member.end_offset,
            text=member.text,
        )
        for key, member in _extract_class_members(source).items()
        if key.startswith("type:")
    }


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


def _sync_recursive_nested_classes_from_reference(merged: str, reference: str) -> str:
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


def sync_nested_classes_from_reference(merged: str, reference: str) -> str:
    """若合并结果引用了某嵌套类型，用 B 上同名嵌套类定义替换或插入。"""
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


def finalize_merged_test_class(merged: str, *, reference_source: str) -> str:
    """合并模型补丁后，从 B 提交上的测试类补齐 import 与嵌套类型定义。"""
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
    old_test_full = _git_show(repo, a, test_path)
    prod_diff_parts: list[str] = []
    prod_method_parts: list[str] = []

    for p in prod_paths:
        d = _git_diff(repo, a, b, [p])
        prod_diff_parts.append(f"===== {p} =====\n{d}")
        prod_source_b = _git_show(repo, b, p)
        new_lines = _parse_diff_line_numbers(d, side="new")
        methods_b = _methods_for_diff_lines(prod_source_b, new_lines, test_file=False)
        # diff 片段过短或无法从 hunk 读懂时，附上 B 上受影响方法的完整方法体（非整文件）
        need_bodies = len(d.strip()) < _MIN_DIFF_CHARS_FOR_CONTEXT or bool(methods_b)
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
        old_test_snippet = "\n\n".join(
            f"// 方法: {n}\n{t}" for n, t in sorted(old_methods.items())
        )
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


def _chat_request(
    *,
    api_key: str,
    api_base: str,
    model: str,
    messages: list[dict[str, str]],
    timeout_sec: int,
    max_output_tokens: int | None,
) -> dict[str, Any]:
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


def deepseek_chat(
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
    messages: list[dict[str, str]] = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    payload = _chat_request(
        api_key=api_key,
        api_base=api_base,
        model=model,
        messages=messages,
        timeout_sec=timeout_sec,
        max_output_tokens=max_output_tokens,
    )
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
        payload2 = _chat_request(
            api_key=api_key,
            api_base=api_base,
            model=model,
            messages=messages,
            timeout_sec=timeout_sec,
            max_output_tokens=max_output_tokens,
        )
        choice2 = payload2["choices"][0]
        content = content + choice2["message"]["content"]
        payload = payload2
        finish_reason = choice2.get("finish_reason")
        if finish_reason == "length":
            print(
                "警告：续写后仍为 finish_reason=length，请增大 DEEPSEEK_MAX_OUTPUT_TOKENS 或 --max-output-tokens。",
                file=sys.stderr,
            )
    elif finish_reason == "length":
        print(
            "警告：finish_reason=length（未续写）。可增大 --max-output-tokens 或去掉 --no-continue-output。",
            file=sys.stderr,
        )

    payload.setdefault("_merged_finish_reason", finish_reason)
    return content, payload


def run_one_update(
    repo: Path,
    a: str,
    b: str,
    test_path: str,
    prod_paths: list[str],
    title: str,
    *,
    dry_run: bool,
    api_key: str | None,
    api_base: str,
    model: str,
    max_chars: int | None,
    max_output_tokens: int,
    continue_on_length: bool,
    note: str | None,
    timeout: int,
    out: Path | None,
    dry_run_compact: bool,
    verbose: bool,
) -> tuple[bool, str]:
    """
    执行单次「取 git → 拼 prompt → dry-run 或调 API → 写文件」。
    返回 (成功, 说明)：成功时说明为输出文件路径；失败时为错误摘要（单行优先）。
    """
    try:
        inputs = build_prompt_inputs(repo, a, b, test_path, prod_paths)
        prod_diff, tr_pd = _truncate(inputs["prod_diff"], max_chars)
        prod_methods_b, tr_pm = _truncate(inputs["prod_methods_b"], max_chars)
        test_diff, tr_td = _truncate(inputs["test_diff"], max_chars)
        old_snip, tr_old = _truncate(inputs["old_test_snippet"], max_chars)
        input_truncated = {
            "prod_diff": tr_pd,
            "prod_methods_b": tr_pm,
            "test_diff": tr_td,
            "old_test": tr_old,
        }

        user_msg = build_user_message(
            prod_diff=prod_diff,
            prod_methods_b=prod_methods_b,
            test_diff=test_diff,
            test_path=inputs["test_path"],
            old_test_snippet=old_snip,
            old_test_mode=inputs["old_test_mode"],
            optional_note=note,
        )

        est_tokens = (len(SYSTEM_PROMPT) + len(user_msg)) // 3
        if est_tokens * 3 > _EST_CONTEXT_CHARS_WARN:
            print(
                f"警告：估算输入约 {est_tokens} tokens（>{_EST_CONTEXT_CHARS_WARN // 3}k），可能触及模型上下文上限；"
                f"old_test_mode={inputs['old_test_mode']} truncated={input_truncated}",
                file=sys.stderr,
            )

        if dry_run:
            if dry_run_compact:
                print(
                    f"[dry-run] {title}: user {len(user_msg)} 字符 (~{est_tokens} tok) "
                    f"truncated={input_truncated} old_test_mode={inputs['old_test_mode']}",
                    file=sys.stderr,
                )
            else:
                print(f"\n========== {title} ==========\n")
                print("=== SYSTEM ===")
                print(SYSTEM_PROMPT)
                print("\n=== USER ===")
                print(user_msg)
            return True, f"(dry-run) {title}"

        if not (api_key or "").strip():
            return False, "未在 key.py 中设置 DEEPSEEK_API_KEY"

        print(
            f"调用 DeepSeek: model={model} user_chars={len(user_msg)} old_test_mode={inputs['old_test_mode']} ({title})",
            file=sys.stderr,
        )
        content, payload = deepseek_chat(
            api_key=api_key.strip(),
            api_base=api_base,
            model=model,
            system=SYSTEM_PROMPT,
            user=user_msg,
            timeout_sec=timeout,
            max_output_tokens=max_output_tokens,
            continue_on_length=continue_on_length,
        )
        fr = payload.get("_merged_finish_reason") or payload.get("choices", [{}])[0].get("finish_reason")
        usage = payload.get("usage") or {}

        out_path = out
        if out_path is None:
            out_dir = repo.parent / "artifacts" / "deepseek_tests"
            out_dir.mkdir(parents=True, exist_ok=True)
            safe = test_path.replace("/", "__").replace("\\", "__")
            out_path = out_dir / f"{title.replace(' ', '_')}__{safe}.md"

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            "# DeepSeek 输出\n\n"
            + f"- repo: `{repo}`\n"
            + f"- A: `{a}`\n"
            + f"- B: `{b}`\n"
            + f"- test: `{test_path}`\n"
            + f"- prod: `{prod_paths}`\n"
            + f"- old_test_mode: `{inputs['old_test_mode']}`\n"
            + f"- user_chars: `{len(user_msg)}`\n"
            + f"- input_truncated: `{input_truncated}`\n"
            + f"- max_output_tokens: `{max_output_tokens}`\n"
            + f"- finish_reason: `{fr}`\n"
            + (f"- usage: `{usage}`\n" if usage else "")
            + ("  （length 表示输出可能被截断，已尝试自动续写一轮）\n" if fr == "length" else "")
            + "\n---\n\n"
            + content,
            encoding="utf-8",
        )
        return True, str(out_path)
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
        print(f"\n[失败] {title}\n{err}", file=sys.stderr)
        if verbose:
            traceback.print_exc(file=sys.stderr)
        return False, err


def main() -> int:
    parser = argparse.ArgumentParser(
        description="用 DeepSeek 根据 A/B 提交更新 JUnit 测试（135 条已验证候选）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            f"候选列表默认：{_DEFAULT_CANDIDATES.name}\n"
            f"仓库默认：{_DEFAULT_REPO}\n"
            "  python update_tests_deepseek.py              # 第 1 条 dry-run\n"
            "  python update_tests_deepseek.py --index 5\n"
            "  python update_tests_deepseek.py --run-all\n"
            "  python update_tests_deepseek.py --run-all --limit 10 --resume"
        ),
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=_DEFAULT_REPO,
        help=f"commons-lang 仓库根目录（默认：{_DEFAULT_REPO}）",
    )
    parser.add_argument(
        "--candidates",
        type=Path,
        default=_DEFAULT_CANDIDATES,
        help="已验证候选 JSON（默认 lang_sample_candidates_filtered.json）",
    )
    parser.add_argument(
        "--index",
        type=int,
        default=None,
        help="只处理候选列表中的第 N 条（1-based，与 filtered.json 顺序一致）",
    )
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="依次处理候选 JSON 中的全部条目",
    )
    parser.add_argument("--limit", type=int, default=None, help="与 --run-all 联用：最多处理条数")
    parser.add_argument("--start", type=int, default=1, help="从候选列表第几条开始（1-based）")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="与 --run-all 联用：若 artifacts/deepseek_tests 中已有输出则跳过",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="失败时打印 traceback；--dry-run 时打印完整 prompt",
    )
    parser.add_argument("--a", help="旧提交 A（与 --b/--test/--prod 联用）")
    parser.add_argument("--b", help="新提交 B")
    parser.add_argument("--test", help="测试文件在仓库中的相对路径，如 src/test/java/.../FooTest.java")
    parser.add_argument("--prod", action="append", help="生产代码相对路径，可多次指定；与 --sample 互斥时必填")
    parser.add_argument("--note", default=None, help="可选：人工补充说明，写入用户消息")
    parser.add_argument("--api-base", default=os.environ.get("DEEPSEEK_API_BASE", DEFAULT_API_BASE))
    parser.add_argument("--model", default=os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL))
    parser.add_argument(
        "--max-chars",
        type=int,
        default=int(os.environ.get("DEEPSEEK_MAX_CHARS", "0")),
        help="输入每段最大字符数；0=不截断（推荐，compact prompt 通常够用）",
    )
    parser.add_argument(
        "--max-output-tokens",
        type=int,
        default=_DEFAULT_MAX_OUTPUT,
        help=f"API max_tokens（默认 {_DEFAULT_MAX_OUTPUT}，可用 DEEPSEEK_MAX_OUTPUT_TOKENS 覆盖）",
    )
    parser.add_argument(
        "--no-continue-output",
        action="store_true",
        help="输出为 length 时不自动续写第二轮",
    )
    parser.add_argument("--out", type=Path, default=None, help="将模型原始回复写入该文件（UTF-8）；与 --run-all 互斥（批量时自动命名）")
    parser.add_argument("--dry-run", action="store_true", help="只打印用户消息，不调 API")
    parser.add_argument("--timeout", type=int, default=180, help="HTTP 超时秒数")
    args = parser.parse_args()

    if args.run_all and args.index is not None:
        print("错误：--run-all 不能与 --index 同时使用", file=sys.stderr)
        return 2
    if args.run_all and (args.a or args.b or args.test or args.prod):
        print("错误：--run-all 不能与自定义 --a/--b/--test/--prod 同时使用", file=sys.stderr)
        return 2
    if args.run_all and args.out is not None:
        print("错误：--run-all 请省略 --out（每条结果自动写入 artifacts/deepseek_tests/）", file=sys.stderr)
        return 2

    if len(sys.argv) == 1:
        args.index = 1
        args.dry_run = True
        print(
            "提示：无参数 = 候选列表第 1 条 + --dry-run。\n"
            "      批量：python update_tests_deepseek.py --run-all\n"
            f"      候选文件：{args.candidates}",
            file=sys.stderr,
        )

    repo: Path = args.repo.resolve()
    if not (repo / ".git").is_dir():
        print("错误：--repo 不是 git 仓库根目录", file=sys.stderr)
        return 2

    api_key = (DEEPSEEK_API_KEY or "").strip() or None
    out_dir = _ROOT / "artifacts" / "deepseek_tests"

    def _run_candidate(idx: int, cand: dict) -> tuple[str, bool, str]:
        test_path = cand.get("primary_test") or cand["test_files"][0]
        prod_path = cand.get("primary_main") or cand["main_files"][0]
        pr = f" #{cand['pr_hint']}" if cand.get("pr_hint") else ""
        title = f"cand{idx:03d}{pr} {cand.get('subject', '')[:70]}"
        out_path = out_dir / f"cand{idx:03d}_{cand['b'][:12]}__{test_path.replace('/', '__')}.md"
        if args.resume and out_path.is_file() and not args.dry_run:
            return title, True, str(out_path)
        compact = args.dry_run and not args.verbose
        ok, msg = run_one_update(
            repo,
            cand["a"],
            cand["b"],
            test_path,
            [prod_path],
            title,
            dry_run=args.dry_run,
            api_key=api_key,
            api_base=args.api_base,
            model=args.model,
            max_chars=args.max_chars if args.max_chars > 0 else None,
            max_output_tokens=args.max_output_tokens,
            continue_on_length=not args.no_continue_output,
            note=args.note,
            timeout=args.timeout,
            out=out_path if args.run_all else args.out,
            dry_run_compact=compact,
            verbose=args.verbose,
        )
        return title, ok, msg

    if args.run_all or args.index is not None:
        try:
            all_cands = load_candidates(args.candidates.resolve())
        except (FileNotFoundError, ValueError) as e:
            print(f"错误：{e}", file=sys.stderr)
            return 2
        print(f"已加载候选 {len(all_cands)} 条 ← {args.candidates.name}", file=sys.stderr)

    if args.run_all:
        if not args.dry_run and not api_key:
            print("错误：--run-all 且非 --dry-run 时需在 key.py 中设置 DEEPSEEK_API_KEY", file=sys.stderr)
            return 2
        results: list[tuple[str, bool, str]] = []
        processed = 0
        for idx, cand in enumerate(all_cands, start=1):
            if idx < args.start:
                continue
            if args.limit is not None and processed >= args.limit:
                break
            title, ok, msg = _run_candidate(idx, cand)
            results.append((title, ok, msg))
            processed += 1
            if ok and not args.dry_run:
                print(msg)

        print("\n========== 汇总 ==========", file=sys.stderr)
        n_ok = sum(1 for _t, ok, _m in results if ok)
        for title, ok, msg in results:
            mark = "OK  " if ok else "FAIL"
            print(f"  [{mark}] {title}", file=sys.stderr)
            if not ok:
                print(f"        {(msg or '').split(chr(10), 1)[0][:500]}", file=sys.stderr)
        print(f"  成功 {n_ok} / {len(results)}", file=sys.stderr)
        return 0 if n_ok == len(results) else 1

    if args.index is not None:
        if not (1 <= args.index <= len(all_cands)):
            print(f"错误：--index 须在 1..{len(all_cands)}", file=sys.stderr)
            return 2
        cand = all_cands[args.index - 1]
        title, ok, msg = _run_candidate(args.index, cand)
        if not ok:
            print(msg, file=sys.stderr)
            return 1
        if not args.dry_run:
            print(msg)
        return 0

    if args.a and args.b and args.test and args.prod:
        a, b, test_path, prod_paths = args.a, args.b, args.test, list(args.prod)
        title = "custom"
    else:
        print(
            "错误：请指定 --index N、--run-all，或自定义 --a --b --test --prod。\n"
            f"  候选文件：{args.candidates}",
            file=sys.stderr,
        )
        return 2

    ok, msg = run_one_update(
        repo,
        a,
        b,
        test_path,
        prod_paths,
        title,
        dry_run=args.dry_run,
        api_key=api_key,
        api_base=args.api_base,
        model=args.model,
        max_chars=args.max_chars if args.max_chars > 0 else None,
        max_output_tokens=args.max_output_tokens,
        continue_on_length=not args.no_continue_output,
        note=args.note,
        timeout=args.timeout,
        out=args.out,
        dry_run_compact=False,
        verbose=args.verbose,
    )
    if not ok:
        print(msg, file=sys.stderr)
        return 1
    if not args.dry_run:
        print(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
