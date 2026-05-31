#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在 commons-lang 历史中批量扫描「适合做 LLM 改测试实验」的提交对 (A=B~1, B)。

硬性条件（与实验设计一致）：
  - 至少 1 个 src/main/java 下 .java 为 M（修改）
  - 至少 1 个 src/test/java 下 *Test.java 为 M（修改，非 A 新增）
  - 该测试文件在 A 的 tree 中存在（git cat-file -e A:path）
  - main 与 test 在 A..B 之间 diff 非空

用法：
  cd Introduction-to-Software-Testing
  python 1_scan.py

  或在 final_homework 根目录：
  python 1_scan.py
  python Introduction-to-Software-Testing\\1_scan.py --repo ..\\commons-lang
  python 1_scan.py --merges-only --max-files 10 --min-test-methods 1

依赖：Python 3.9+ 标准库 + 本机 git。
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

_DEFAULT_REPO = Path(__file__).resolve().parent.parent / "commons-lang"

MAIN_RE = re.compile(r"^src/main/java/.+\.java$")
TEST_RE = re.compile(r"^src/test/java/.+Test\.java$")


@dataclass
class Candidate:
    b: str
    a: str
    subject: str
    main_files: list[str]
    test_files: list[str]
    total_changed: int
    added_tests: list[str] = field(default_factory=list)
    score: int = 0

    def primary_pair(self) -> tuple[str, str] | None:
        """Heuristic: same basename Foo.java / FooTest.java if possible."""
        for main in self.main_files:
            stem = Path(main).stem
            want = f"src/test/java/{Path(main).relative_to('src/main/java').parent}/" f"{stem}Test.java"
            want = want.replace("\\", "/")
            if want in self.test_files:
                return main, want
        if len(self.main_files) == 1 and len(self.test_files) == 1:
            return self.main_files[0], self.test_files[0]
        return None


def _run(cmd: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def git(repo: Path, *args: str) -> str:
    p = _run(["git", "-C", str(repo), *args], cwd=repo)
    if p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}\n{p.stderr.strip()}")
    return p.stdout


def object_exists(repo: Path, rev: str, path: str) -> bool:
    p = _run(["git", "-C", str(repo), "cat-file", "-e", f"{rev}:{path}"], cwd=repo)
    return p.returncode == 0


def diff_nonempty(repo: Path, a: str, b: str, path: str) -> bool:
    p = _run(["git", "-C", str(repo), "diff", "--quiet", f"{a}..{b}", "--", path], cwd=repo)
    return p.returncode == 1


def parse_name_status(text: str) -> dict[str, list[str]]:
    added: list[str] = []
    modified: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status, path = parts[0], parts[-1]
        path = path.replace("\\", "/")
        if status.startswith("A"):
            added.append(path)
        elif status.startswith("M"):
            modified.append(path)
    return {"added": added, "modified": modified}


def score_candidate(
    *,
    mains: list[str],
    tests: list[str],
    added_tests: list[str],
    total_changed: int,
    max_files: int,
) -> int:
    s = 0
    if len(mains) == 1:
        s += 3
    if len(tests) == 1:
        s += 3
    if len(mains) <= 2 and len(tests) <= 2:
        s += 2
    if not added_tests:
        s += 2
    if total_changed <= max_files:
        s += 2
    pair = None
    c = Candidate("", "", "", mains, tests, total_changed, added_tests)
    if c.primary_pair():
        s += 4
    return s


def scan(
    repo: Path,
    *,
    max_commits: int,
    merges_only: bool,
    max_files: int,
    require_pairable: bool,
) -> list[Candidate]:
    log_args = ["log", f"-{max_commits}", "--format=%H%x09%s"]
    if merges_only:
        log_args.insert(1, "--merges")
    lines = git(repo, *log_args).splitlines()

    out: list[Candidate] = []
    seen_b: set[str] = set()

    for line in lines:
        if "\t" not in line:
            continue
        b, subject = line.split("\t", 1)
        b = b.strip()
        if b in seen_b:
            continue
        seen_b.add(b)

        try:
            a = git(repo, "rev-parse", f"{b}~1").strip()
        except RuntimeError:
            continue

        try:
            ns = git(repo, "diff", "--name-status", f"{a}..{b}")
        except RuntimeError:
            continue

        parsed = parse_name_status(ns)
        all_paths = set(parsed["added"]) | set(parsed["modified"])
        total_changed = len(all_paths)

        if total_changed > max_files:
            continue

        mains = [p for p in parsed["modified"] if MAIN_RE.match(p)]
        tests_modified = [p for p in parsed["modified"] if TEST_RE.match(p)]
        tests_added = [p for p in parsed["added"] if TEST_RE.match(p)]

        if not mains or not tests_modified:
            continue

        valid_tests: list[str] = []
        for tp in tests_modified:
            if not object_exists(repo, a, tp):
                continue
            if not diff_nonempty(repo, a, b, tp):
                continue
            valid_tests.append(tp)

        if not valid_tests:
            continue

        valid_mains: list[str] = []
        for mp in mains:
            if not object_exists(repo, a, mp):
                continue
            if not diff_nonempty(repo, a, b, mp):
                continue
            valid_mains.append(mp)

        if not valid_mains:
            continue

        cand = Candidate(
            b=b,
            a=a,
            subject=subject.strip(),
            main_files=valid_mains,
            test_files=valid_tests,
            total_changed=total_changed,
            added_tests=tests_added,
        )
        cand.score = score_candidate(
            mains=valid_mains,
            tests=valid_tests,
            added_tests=tests_added,
            total_changed=total_changed,
            max_files=max_files,
        )

        if require_pairable and cand.primary_pair() is None:
            continue

        out.append(cand)

    out.sort(key=lambda c: (-c.score, c.total_changed, c.b))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="扫描 commons-lang 中适合做「A 旧测试 + B 新代码」实验的提交对")
    parser.add_argument("--repo", type=Path, default=_DEFAULT_REPO, help=f"commons-lang 根目录（默认 {_DEFAULT_REPO}）")
    parser.add_argument("--max-commits", type=int, default=800, help="扫描最近多少条 git log（默认 800）")
    parser.add_argument("--merges-only", action="store_true", help="只扫描 merge commit（更接近 PR 合入点）")
    parser.add_argument("--max-files", type=int, default=12, help="A..B 变更文件总数上限（默认 12）")
    parser.add_argument(
        "--require-pairable",
        action="store_true",
        help="要求存在 Foo.java 与 FooTest.java 同名配对（更省心）",
    )
    parser.add_argument("-o", "--output", type=Path, default=None, help="写出 JSON（默认只打印表格）")
    parser.add_argument("--top", type=int, default=40, help="终端最多打印多少条（默认 40）")
    args = parser.parse_args()

    repo = args.repo.resolve()
    if not (repo / ".git").is_dir():
        print(f"错误：不是 git 仓库: {repo}", file=sys.stderr)
        return 2

    print(f"扫描 {repo} （最近 {args.max_commits} 条" + (" merge" if args.merges_only else "") + "）…", file=sys.stderr)
    candidates = scan(
        repo,
        max_commits=args.max_commits,
        merges_only=args.merges_only,
        max_files=args.max_files,
        require_pairable=args.require_pairable,
    )
    print(f"找到 {len(candidates)} 个候选（已按推荐度 score 排序）\n", file=sys.stderr)

    rows: list[dict] = []
    for i, c in enumerate(candidates[: args.top], 1):
        pair = c.primary_pair()
        pair_s = f"{Path(pair[0]).name} <-> {Path(pair[1]).name}" if pair else "(多文件，需人工选)"
        flag = " +新测试" if c.added_tests else ""
        print(
            f"{i:3}. score={c.score:2}  B={c.b[:12]}  files={c.total_changed:2}{flag}\n"
            f"     {c.subject[:90]}\n"
            f"     main: {', '.join(Path(p).name for p in c.main_files[:3])}"
            f"{'...' if len(c.main_files) > 3 else ''}\n"
            f"     test: {', '.join(Path(p).name for p in c.test_files[:3])}"
            f"{'...' if len(c.test_files) > 3 else ''}\n"
            f"     推荐配对: {pair_s}\n"
            f"     A={c.a}\n"
        )
        d = asdict(c)
        d["primary_main"], d["primary_test"] = (pair if pair else (None, None))
        rows.append(d)

    if args.output:
        payload = {
            "repo": str(repo),
            "scan_args": {
                "max_commits": args.max_commits,
                "merges_only": args.merges_only,
                "max_files": args.max_files,
                "require_pairable": args.require_pairable,
            },
            "count": len(candidates),
            "candidates": [asdict(c) for c in candidates],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"已写入 {args.output}（共 {len(candidates)} 条）", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
