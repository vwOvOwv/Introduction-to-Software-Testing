#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


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


@dataclass
class CandidateTest:
    test_file: str
    method_name: str
    reason: str
    class_name: str


def run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )


def git_show(repo: Path, revision: str, relpath: str) -> str:
    result = run_command(["git", "show", f"{revision}:{relpath}"], cwd=repo)
    if result.returncode != 0:
        raise RuntimeError(f"git show 失败: {relpath}\n{result.stderr.strip()}")
    return result.stdout


def git_diff_name_status(repo: Path, a: str, b: str, pathspec: str) -> list[dict[str, str]]:
    result = run_command(
        ["git", "diff", "--name-status", "--find-renames", f"{a}..{b}", "--", pathspec],
        cwd=repo,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git diff --name-status 失败\n{result.stderr.strip()}")

    rows: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("R") or status.startswith("C"):
            if len(parts) >= 3:
                rows.append({"status": status[0], "old_path": parts[1], "new_path": parts[2]})
            continue
        if len(parts) >= 2:
            rows.append({"status": status, "old_path": parts[1], "new_path": parts[1]})
    return rows


def git_changed_main_files(repo: Path, a: str, b: str) -> list[str]:
    rows = git_diff_name_status(repo, a, b, "src/main/java")
    paths: list[str] = []
    for row in rows:
        path = row["new_path"] if row["status"] != "D" else row["old_path"]
        if path.endswith(".java"):
            paths.append(path)
    return sorted(set(paths))


def read_file_if_exists(repo: Path, revision: str, path: str) -> str | None:
    result = run_command(["git", "show", f"{revision}:{path}"], cwd=repo)
    if result.returncode != 0:
        return None
    return result.stdout


def extract_class_name(source: str, fallback_path: str) -> str:
    match = re.search(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)\b", source)
    if match:
        return match.group(1)
    return Path(fallback_path).stem


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


def reduce_to_single_test(source: str, target_method_name: str) -> str:
    methods = extract_test_methods(source)
    if target_method_name not in methods:
        raise ValueError(f"未在测试类中找到目标测试方法: {target_method_name}")

    reduced = source
    removable = [method for name, method in methods.items() if name != target_method_name]
    for method in sorted(removable, key=lambda item: item.start_offset, reverse=True):
        reduced = reduced[:method.start_offset] + reduced[method.end_offset:]
    return reduced


def normalize_method_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def discover_candidate_tests(repo: Path, a: str, b: str) -> list[CandidateTest]:
    rows = git_diff_name_status(repo, a, b, "src/test/java")
    candidates: list[CandidateTest] = []

    for row in rows:
        status = row["status"]
        old_path = row["old_path"]
        new_path = row["new_path"]
        if not old_path.endswith(".java"):
            continue

        source_a = read_file_if_exists(repo, a, old_path)
        source_b = read_file_if_exists(repo, b, new_path)
        if not source_a:
            continue

        class_name = extract_class_name(source_a, old_path)
        methods_a = extract_test_methods(source_a)
        methods_b = extract_test_methods(source_b) if source_b else {}

        if status == "D":
            for method_name in sorted(methods_a):
                candidates.append(CandidateTest(old_path, method_name, "deleted_file", class_name))
            continue

        for method_name, method_a in sorted(methods_a.items()):
            method_b = methods_b.get(method_name)
            if method_b is None:
                candidates.append(CandidateTest(old_path, method_name, "deleted_method", class_name))
                continue
            if normalize_method_text(method_a.text) != normalize_method_text(method_b.text):
                candidates.append(CandidateTest(old_path, method_name, "modified_method", class_name))

    return candidates


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_json_if_exists(path: Path) -> dict | None:
    if not path.is_file():
        return None
    return load_json(path)


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def run_python_script(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return run_command([sys.executable, *command], cwd=cwd)


def build_test_selector(class_name: str, method_name: str) -> str:
    return f"{class_name}#{method_name}"


def extract_java_from_deepseek_output(markdown_text: str) -> str:
    marker = "\n---\n\n"
    content = markdown_text.split(marker, 1)[1] if marker in markdown_text else markdown_text
    fenced = re.findall(r"```(?:java)?\s*(.*?)```", content, flags=re.DOTALL)
    if fenced:
        return fenced[0].strip() + "\n"
    return content.strip() + "\n"


def ensure_git_repo(repo: Path) -> None:
    if not (repo / ".git").exists():
        raise ValueError(f"不是 git 仓库根目录: {repo}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="比较 A/B 两个版本的测试用例，确认失效测试，并调用 DeepSeek 生成更新版本后复测。",
    )
    parser.add_argument("--repo", type=Path, required=True, help="Java Maven 仓库根目录")
    parser.add_argument("--a", required=True, help="旧版本 A")
    parser.add_argument("--b", required=True, help="新版本 B")
    parser.add_argument(
        "--run-script",
        type=Path,
        default=Path("run_single_maven_test.py"),
        help="单测执行脚本路径，默认 run_single_maven_test.py",
    )
    parser.add_argument(
        "--update-script",
        type=Path,
        default=Path("update_tests_deepseek.py"),
        help="DeepSeek 更新脚本路径，默认 update_tests_deepseek.py",
    )
    parser.add_argument(
        "--report-file",
        type=Path,
        default=Path("artifacts/orchestrate_test_updates_report.json"),
        help="最终报告输出路径",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=Path("artifacts/orchestrate_test_updates"),
        help="临时产物目录",
    )
    parser.add_argument(
        "--maven-arg",
        action="append",
        default=[],
        help="传给 run_single_maven_test.py 的附加 Maven 参数，可重复指定",
    )
    parser.add_argument(
        "--max-tests",
        type=int,
        default=None,
        help="仅处理前 N 个候选测试点，用于试跑",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只发现候选测试点 T，不执行后续步骤",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    repo = args.repo.resolve()
    run_script = args.run_script.resolve()
    update_script = args.update_script.resolve()
    report_file = args.report_file if args.report_file.is_absolute() else repo / args.report_file
    report_file = report_file.resolve()
    work_dir = args.work_dir if args.work_dir.is_absolute() else repo / args.work_dir
    work_dir = work_dir.resolve()

    ensure_git_repo(repo)
    if not run_script.is_file():
        raise ValueError(f"找不到 run script: {run_script}")
    if not update_script.is_file():
        raise ValueError(f"找不到 update script: {update_script}")

    candidate_tests = discover_candidate_tests(repo, args.a, args.b)
    if args.max_tests is not None:
        candidate_tests = candidate_tests[:args.max_tests]

    changed_prod_files = git_changed_main_files(repo, args.a, args.b)

    report: dict = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "repo": str(repo),
        "a": args.a,
        "b": args.b,
        "changed_prod_files": changed_prod_files,
        "candidates_T": [asdict(item) for item in candidate_tests],
        "confirmed_invalid_T_prime": [],
        "updated_results_T_double_prime": [],
    }

    if args.dry_run:
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(str(report_file))
        return 0

    for candidate in candidate_tests:
        candidate_id = safe_name(f"{candidate.class_name}__{candidate.method_name}")
        candidate_dir = work_dir / candidate_id
        old_test_source = git_show(repo, args.a, candidate.test_file)
        reduced_old_test_source = reduce_to_single_test(old_test_source, candidate.method_name)
        old_test_file = candidate_dir / "old" / Path(candidate.test_file).name
        write_text(old_test_file, reduced_old_test_source)

        run_report_path = candidate_dir / "run_old_report.json"
        run_command_args = [
            str(run_script),
            "--repo",
            str(repo),
            "--ref",
            args.b,
            "--target-test-path",
            candidate.test_file,
            "--replacement-test-file",
            str(old_test_file),
            "--test-selector",
            build_test_selector(candidate.class_name, candidate.method_name),
            "--report-file",
            str(run_report_path),
        ]
        for maven_arg in args.maven_arg:
            run_command_args.append(f"--maven-arg={maven_arg}")

        run_old_process = run_python_script(run_command_args, cwd=repo.parent)
        run_old_report = load_json_if_exists(run_report_path)

        candidate_record = {
            **asdict(candidate),
            "run_old_exit_code": run_old_process.returncode,
            "run_old_report": str(run_report_path),
            "run_old_stdout": run_old_process.stdout,
            "run_old_stderr": run_old_process.stderr,
            "run_old_report_exists": run_old_report is not None,
        }

        if run_old_process.returncode == 0:
            continue

        report["confirmed_invalid_T_prime"].append(candidate_record)

        deepseek_output_path = candidate_dir / "deepseek_output.md"
        note = (
            f"请只更新测试方法 {candidate.method_name}，保持类名 {candidate.class_name} 和方法名 {candidate.method_name} 不变，"
            "并确保输出完整测试类源码。"
        )
        update_command_args = [
            str(update_script),
            "--repo",
            str(repo),
            "--a",
            args.a,
            "--b",
            args.b,
            "--test",
            candidate.test_file,
            "--out",
            str(deepseek_output_path),
            "--note",
            note,
        ]
        for prod_file in changed_prod_files:
            update_command_args.extend(["--prod", prod_file])

        update_process = run_python_script(update_command_args, cwd=repo.parent)
        updated_record = {
            **candidate_record,
            "deepseek_exit_code": update_process.returncode,
            "deepseek_output": str(deepseek_output_path),
            "deepseek_stdout": update_process.stdout,
            "deepseek_stderr": update_process.stderr,
        }

        if update_process.returncode != 0 or not deepseek_output_path.is_file():
            report["updated_results_T_double_prime"].append(updated_record)
            continue

        generated_markdown = deepseek_output_path.read_text(encoding="utf-8")
        generated_java = extract_java_from_deepseek_output(generated_markdown)
        reduced_generated_java = reduce_to_single_test(generated_java, candidate.method_name)
        generated_test_file = candidate_dir / "generated" / Path(candidate.test_file).name
        write_text(generated_test_file, reduced_generated_java)

        run_new_report_path = candidate_dir / "run_updated_report.json"
        run_new_command_args = [
            str(run_script),
            "--repo",
            str(repo),
            "--ref",
            args.b,
            "--target-test-path",
            candidate.test_file,
            "--replacement-test-file",
            str(generated_test_file),
            "--test-selector",
            build_test_selector(candidate.class_name, candidate.method_name),
            "--report-file",
            str(run_new_report_path),
        ]
        for maven_arg in args.maven_arg:
            run_new_command_args.append(f"--maven-arg={maven_arg}")

        run_new_process = run_python_script(run_new_command_args, cwd=repo.parent)
        updated_record.update(
            {
                "generated_test_file": str(generated_test_file),
                "run_updated_exit_code": run_new_process.returncode,
                "run_updated_report": str(run_new_report_path),
                "run_updated_success": run_new_process.returncode == 0,
                "run_updated_stdout": run_new_process.stdout,
                "run_updated_stderr": run_new_process.stderr,
                "run_updated_report_exists": run_new_report_path.is_file(),
            }
        )
        report["updated_results_T_double_prime"].append(updated_record)

    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(report_file))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())