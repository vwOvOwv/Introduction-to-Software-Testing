#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import shlex
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class CommandResult:
    command: list[str]
    cwd: str
    returncode: int
    stdout: str
    stderr: str


def run_command(command: list[str], cwd: Path) -> CommandResult:
    process = subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    return CommandResult(
        command=command,
        cwd=str(cwd),
        returncode=process.returncode,
        stdout=process.stdout,
        stderr=process.stderr,
    )


def require_git_repo(repo: Path) -> None:
    if not (repo / ".git").exists():
        raise ValueError(f"不是 git 仓库根目录: {repo}")


def require_existing_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise ValueError(f"{label} 不存在: {path}")


def ensure_tool_exists(tool_name: str) -> None:
    if shutil.which(tool_name) is None:
        raise RuntimeError(f"找不到可执行文件: {tool_name}")


def write_report(report_path: Path, payload: dict) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def checkout_ref(repo: Path, git_ref: str) -> CommandResult:
    return run_command(["git", "checkout", "--detach", git_ref], cwd=repo)


def overwrite_test_file(source_file: Path, destination_file: Path) -> None:
    destination_file.parent.mkdir(parents=True, exist_ok=True)
    destination_file.write_text(source_file.read_text(encoding="utf-8"), encoding="utf-8")


def discard_changes(repo: Path, target_path: str | None) -> list[CommandResult]:
    commands: list[list[str]] = []
    if target_path:
        commands.append(["git", "restore", "--source=HEAD", "--staged", "--worktree", "--", target_path])
    else:
        commands.append(["git", "restore", "--source=HEAD", "--staged", "--worktree", "."])

    return [run_command(command, cwd=repo) for command in commands]


def resolve_mvn_executable() -> str:
    path = shutil.which("mvn")
    if not path:
        raise RuntimeError("PATH 中找不到 mvn，请安装 Maven 或配置环境变量")
    return path


def build_maven_command(test_selector: str, extra_args: list[str]) -> list[str]:
    command = [resolve_mvn_executable(), *extra_args, f"-Dtest={test_selector}", "test"]
    return command


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="切换到指定版本，覆盖一个 Maven/JUnit 测试文件，只运行该测试，并记录结果。",
    )
    parser.add_argument("--repo", type=Path, required=True, help="Java Maven 仓库根目录")
    parser.add_argument("--ref", required=True, help="目标 git 版本，可为 commit/tag/branch")
    parser.add_argument(
        "--target-test-path",
        required=True,
        help="仓库内待覆盖的测试文件相对路径，例如 src/test/java/com/acme/FooTest.java",
    )
    parser.add_argument(
        "--replacement-test-file",
        type=Path,
        required=True,
        help="本地替换测试文件路径，内容会覆盖到 target-test-path",
    )
    parser.add_argument(
        "--test-selector",
        required=True,
        help="Surefire 测试选择器，例如 FooTest 或 FooTest#testBar",
    )
    parser.add_argument(
        "--report-file",
        type=Path,
        default=Path("artifacts/test-run-report.json"),
        help="结果报告输出路径，默认 artifacts/test-run-report.json",
    )
    parser.add_argument(
        "--maven-arg",
        action="append",
        default=[],
        help="附加 Maven 参数，可重复指定，例如 --maven-arg=-q",
    )
    parser.add_argument(
        "--discard-all-tracked-changes",
        action="store_true",
        help="运行完成后丢弃整个仓库当前版本上的所有 tracked 改动；默认只还原 target-test-path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    repo = args.repo.resolve()
    replacement_test_file = args.replacement_test_file.resolve()
    report_file = args.report_file if args.report_file.is_absolute() else repo / args.report_file
    report_file = report_file.resolve()
    target_test_path = args.target_test_path.replace("\\", "/")
    destination_test_file = repo / Path(target_test_path)

    checkout_result: CommandResult | None = None
    maven_result: CommandResult | None = None
    restore_results: list[CommandResult] = []
    failure_message: str | None = None

    try:
        require_git_repo(repo)
        require_existing_file(replacement_test_file, "replacement test file")
        ensure_tool_exists("git")
        resolve_mvn_executable()

        checkout_result = checkout_ref(repo, args.ref)
        if checkout_result.returncode != 0:
            failure_message = "git checkout 失败"
            return 1

        overwrite_test_file(replacement_test_file, destination_test_file)

        maven_command = build_maven_command(args.test_selector, args.maven_arg)
        maven_result = run_command(maven_command, cwd=repo)
        return 0 if maven_result.returncode == 0 else maven_result.returncode
    except Exception as exc:  # noqa: BLE001
        failure_message = str(exc)
        return 1
    finally:
        restore_target = None if args.discard_all_tracked_changes else target_test_path
        if checkout_result is not None and checkout_result.returncode == 0:
            restore_results = discard_changes(repo, restore_target)

        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "repo": str(repo),
            "ref": args.ref,
            "target_test_path": target_test_path,
            "replacement_test_file": str(replacement_test_file),
            "test_selector": args.test_selector,
            "maven_args": args.maven_arg,
            "discard_all_tracked_changes": args.discard_all_tracked_changes,
            "checkout": asdict(checkout_result) if checkout_result else None,
            "maven": asdict(maven_result) if maven_result else None,
            "restore": [asdict(item) for item in restore_results],
            "failure_message": failure_message,
            "maven_command_shell": shlex.join(build_maven_command(args.test_selector, args.maven_arg)),
        }
        write_report(report_file, payload)


if __name__ == "__main__":
    sys.exit(main())