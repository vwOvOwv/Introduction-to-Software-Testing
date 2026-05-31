#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import getpass
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CommandResult:
    command: list[str]
    cwd: str
    env: dict[str, str]
    returncode: int
    stdout: str
    stderr: str


def build_manual_env(cwd: Path, repo: Path) -> dict[str, str]:
    java_path = shutil.which("java")
    path_entries = ["/usr/local/bin", "/usr/bin", "/bin"]
    if java_path:
        java_home = Path(java_path).resolve().parent.parent
        path_entries.insert(0, str(java_home / "bin"))
    env: dict[str, str] = {
        # "HOME": str(Path.home()),
        # "LANG": "zh_CN.UTF-8",
        # "LC_ALL": "zh_CN.UTF-8",
        # "LOGNAME": getpass.getuser(),
        "PATH": ":".join(path_entries),
        "PWD": os.path.relpath(cwd, start=repo),
        "JAVA_HOME": str(java_home),
        # "TERM": "xterm-256color",
        # "USER": getpass.getuser(),
    }
    if java_home is not None:
        env["JAVA_HOME"] = str(java_home)
    return env


def run_command(command: list[str], cwd: Path, repo: Path) -> CommandResult:
    env = build_manual_env(cwd, repo)
    process = subprocess.run(
        command,
        cwd=str(cwd),
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    return CommandResult(
        command=command,
        cwd=str(cwd),
        env=env,
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


def normalize_path_text(value: str, repo: Path, temp_root: Path) -> str:
    candidate = Path(value)
    try:
        relative_to_temp = str(candidate.resolve().relative_to(temp_root.resolve()))
        return "${tmp}/" + relative_to_temp
    except Exception:  # noqa: BLE001
        pass
    
    try:
        return "./" + str(candidate.resolve().relative_to(repo.resolve()))
    except Exception:
        return os.path.abspath(value)

def normalize_command(command: list[str], repo: Path, temp_root: Path) -> list[str]:
    normalized: list[str] = []
    for index, token in enumerate(command):
        if os.path.isabs(token):
            normalized.append(normalize_path_text(token, repo, temp_root))
        else:
            normalized.append(token)
    return normalized


def normalize_env_value(value: str, repo: Path, temp_root: Path) -> str:
    if os.pathsep in value:
        return os.pathsep.join(
            normalize_path_text(part, repo, temp_root) if part and os.path.isabs(part) else part
            for part in value.split(os.pathsep)
        )
    if os.path.isabs(value):
        return normalize_path_text(value, repo, temp_root)
    return value


def normalize_env(env: dict[str, str], cwd: Path, repo: Path, temp_root: Path) -> dict[str, str]:
    normalized = dict(env)
    normalized["PWD"] = normalize_path_text(str(cwd), repo, temp_root)
    for key in ("HOME", "JAVA_HOME"):
        if key in normalized:
            normalized[key] = normalize_env_value(normalized[key], repo, temp_root)
    if "PATH" in normalized:
        normalized["PATH"] = normalize_env_value(normalized["PATH"], repo, temp_root)
    return dict(sorted(normalized.items()))


def command_history_entry(name: str, result: CommandResult, repo: Path, temp_root: Path) -> dict[str, object]:
    cwd = normalize_path_text(result.cwd, repo, temp_root)
    return {
        "name": name,
        "cwd": cwd,
        "env": normalize_env(result.env, Path(result.cwd), repo, temp_root),
        "command": normalize_command(result.command, repo, temp_root),
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def checkout_ref(repo: Path, git_ref: str) -> CommandResult:
    return run_command([resolve_git_executable(), "checkout", "--detach", git_ref], cwd=repo, repo=repo)


def add_worktree(repo: Path, worktree_dir: Path, git_ref: str) -> CommandResult:
    return run_command(
        [resolve_git_executable(), "worktree", "add", "--detach", str(worktree_dir), git_ref],
        cwd=repo,
        repo=repo,
    )


def remove_worktree(repo: Path, worktree_dir: Path) -> CommandResult:
    return run_command(
        [resolve_git_executable(), "worktree", "remove", "--force", str(worktree_dir)],
        cwd=repo,
        repo=repo,
    )


def overwrite_test_file(source_file: Path, destination_file: Path) -> None:
    destination_file.parent.mkdir(parents=True, exist_ok=True)
    destination_file.write_text(source_file.read_text(encoding="utf-8"), encoding="utf-8")


def discard_changes(repo: Path, target_path: str | None) -> list[CommandResult]:
    commands: list[list[str]] = []
    if target_path:
        commands.append([
            resolve_git_executable(),
            "restore",
            "--source=HEAD",
            "--staged",
            "--worktree",
            "--",
            target_path,
        ])
    else:
        commands.append([resolve_git_executable(), "restore", "--source=HEAD", "--staged", "--worktree", "."])

    return [run_command(command, cwd=repo, repo=repo) for command in commands]


def resolve_git_executable() -> str:
    path = shutil.which("git")
    if not path:
        raise RuntimeError("PATH 中找不到 git，请安装 Git 或配置环境变量")
    return path


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
    worktree_remove_result: CommandResult | None = None
    worktree_path: Path | None = None
    setup_error: str | None = None
    active_repo = repo
    active_destination_test_file = destination_test_file
    command_history: list[dict[str, object]] = []

    try:
        require_git_repo(repo)
        require_existing_file(replacement_test_file, "replacement test file")
        ensure_tool_exists("git")
        resolve_mvn_executable()

        worktree_root = Path(tempfile.gettempdir()) / "sample_runs"
        worktree_root.mkdir(parents=True, exist_ok=True)
        worktree_path = Path(
            tempfile.mkdtemp(prefix=f"run-{Path(target_test_path).stem}-", dir=str(worktree_root))
        )
        checkout_result = add_worktree(repo, worktree_path, args.ref)
        if checkout_result.returncode != 0:
            return 1

        active_repo = worktree_path
        active_destination_test_file = active_repo / Path(target_test_path)

        overwrite_test_file(replacement_test_file, active_destination_test_file)

        maven_command = build_maven_command(args.test_selector, args.maven_arg)
        maven_result = run_command(maven_command, cwd=active_repo, repo=repo)
        return 0 if maven_result.returncode == 0 else maven_result.returncode
    except Exception as exc:  # noqa: BLE001
        setup_error = f"{type(exc).__name__}: {exc}"
        return 1
    finally:
        restore_target = None if args.discard_all_tracked_changes else target_test_path
        if checkout_result is not None and checkout_result.returncode == 0:
            restore_results = discard_changes(active_repo, restore_target)
        if worktree_path is not None and checkout_result is not None and checkout_result.returncode == 0:
            worktree_remove_result = remove_worktree(repo, worktree_path)

        if checkout_result is not None:
            command_history.append(command_history_entry("checkout", checkout_result, repo, worktree_root))
        if maven_result is not None:
            command_history.append(command_history_entry("maven", maven_result, repo, worktree_root))
        for index, item in enumerate(restore_results, start=1):
            history_name = "restore" if len(restore_results) == 1 else f"restore_{index}"
            command_history.append(command_history_entry(history_name, item, repo, worktree_root))
        if worktree_remove_result is not None:
            command_history.append(command_history_entry("worktree_remove", worktree_remove_result, repo, worktree_root))

        payload = {"command_history": command_history}
        if setup_error:
            payload["setup_error"] = setup_error
        write_report(report_file, payload)


if __name__ == "__main__":
    sys.exit(main())
