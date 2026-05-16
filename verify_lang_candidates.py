#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对 filter 后的候选样本，在 commons-lang 的 B 提交上跑聚焦 Maven 测试（第五层快速验证）。

  python verify_lang_candidates.py
  python verify_lang_candidates.py --limit 5          # 先试 5 条
  python verify_lang_candidates.py --resume           # 跳过已验证条目
  python verify_lang_candidates.py --index 3          # 只验 JSON 里第 3 条（1-based）

输出：artifacts/lang_sample_verify_report.json
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_REPO = ROOT.parent / "commons-lang"
DEFAULT_IN = ROOT / "artifacts" / "lang_sample_candidates_filtered.json"
DEFAULT_OUT = ROOT / "artifacts" / "lang_sample_verify_report.json"


def resolve_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"PATH 中找不到: {name}")
    return path


def run(
    cmd: list[str],
    *,
    cwd: Path,
    timeout: int | None,
) -> tuple[int, str, str, bool]:
    """返回 (returncode, stdout, stderr, timed_out)。"""
    try:
        p = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return p.returncode, p.stdout, p.stderr, False
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") if isinstance(e.stdout, str) else ""
        err = (e.stderr or "") if isinstance(e.stderr, str) else ""
        return -1, out, err + "\n[TIMEOUT]", True


def test_selector_from_path(test_path: str) -> str:
    return Path(test_path.replace("\\", "/")).stem


def load_report(path: Path) -> dict:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"results": {}}


def save_report(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify_one(
    repo: Path,
    cand: dict,
    *,
    git_exe: str,
    mvn_exe: str,
    timeout_sec: int,
    maven_quiet: bool,
) -> dict:
    b = cand["b"]
    test_path = cand.get("primary_test") or cand["test_files"][0]
    selector = test_selector_from_path(test_path)
    t0 = time.perf_counter()

    entry: dict = {
        "b": b,
        "a": cand.get("a"),
        "subject": cand.get("subject"),
        "pr_hint": cand.get("pr_hint"),
        "primary_main": cand.get("primary_main"),
        "primary_test": test_path,
        "test_selector": selector,
        "verified_at": datetime.now(timezone.utc).isoformat(),
    }

    co_rc, co_out, co_err, co_to = run(
        [git_exe, "checkout", "--detach", b],
        cwd=repo,
        timeout=120,
    )
    entry["git_checkout"] = {
        "returncode": co_rc,
        "timed_out": co_to,
        "stderr_tail": co_err[-1500:],
    }
    if co_rc != 0 or co_to:
        entry["status"] = "checkout_failed"
        entry["elapsed_sec"] = round(time.perf_counter() - t0, 2)
        return entry

    mvn_cmd = [mvn_exe, "test", f"-Dtest={selector}"]
    if maven_quiet:
        mvn_cmd.insert(1, "-q")

    mvn_rc, mvn_out, mvn_err, mvn_to = run(mvn_cmd, cwd=repo, timeout=timeout_sec)
    entry["maven"] = {
        "command": mvn_cmd,
        "returncode": mvn_rc,
        "timed_out": mvn_to,
        "stdout_tail": mvn_out[-2000:],
        "stderr_tail": mvn_err[-3000:],
    }
    entry["elapsed_sec"] = round(time.perf_counter() - t0, 2)

    if mvn_to:
        entry["status"] = "timeout"
    elif mvn_rc == 0:
        entry["status"] = "pass"
    else:
        entry["status"] = "fail"

    return entry


def print_summary(results: list[dict]) -> None:
    from collections import Counter

    c = Counter(r["status"] for r in results)
    print("\n========== 验证汇总 ==========", file=sys.stderr)
    for k in ("pass", "fail", "timeout", "checkout_failed"):
        if c[k]:
            print(f"  {k}: {c[k]}", file=sys.stderr)
    print(f"  合计: {len(results)}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="在 B 提交上批量 mvn test -Dtest=... 验证候选样本")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("-i", "--input", type=Path, default=DEFAULT_IN)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--limit", type=int, default=None, help="最多验证多少条（用于试跑）")
    parser.add_argument("--index", type=int, default=None, help="只验证第 N 条（1-based，对 candidates 数组）")
    parser.add_argument("--resume", action="store_true", help="跳过报告中已有结果的 B")
    parser.add_argument("--timeout", type=int, default=600, help="单次 mvn 超时秒数（默认 600）")
    parser.add_argument("--no-quiet", action="store_true", help="mvn 不加 -q（输出更全）")
    args = parser.parse_args()

    repo = args.repo.resolve()
    if not (repo / ".git").is_dir():
        print(f"错误：不是 git 仓库: {repo}", file=sys.stderr)
        return 2
    try:
        git_exe = resolve_tool("git")
        mvn_exe = resolve_tool("mvn")
    except RuntimeError as e:
        print(f"错误：{e}", file=sys.stderr)
        return 2

    if not args.input.is_file():
        print(f"错误：找不到 {args.input}", file=sys.stderr)
        return 2

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    candidates: list[dict] = payload.get("candidates", [])
    if not candidates:
        print("错误：输入 JSON 无 candidates", file=sys.stderr)
        return 2

    report = load_report(args.output)
    results_map: dict[str, dict] = report.get("results", {})
    if args.index is not None:
        if not (1 <= args.index <= len(candidates)):
            print(f"错误：--index 须在 1..{len(candidates)}", file=sys.stderr)
            return 2
        candidates = [candidates[args.index - 1]]

    # 记录验证开始时的 HEAD，结束后尽量恢复
    head_rc, head_out, _, _ = run([git_exe, "rev-parse", "HEAD"], cwd=repo, timeout=30)
    original_head = head_out.strip() if head_rc == 0 else None

    processed = 0
    batch_results: list[dict] = []

    try:
        for i, cand in enumerate(candidates, 1):
            b = cand["b"]
            if args.resume and b in results_map:
                print(f"[跳过] {i}: B={b[:12]} 已有结果 status={results_map[b].get('status')}", file=sys.stderr)
                continue
            if args.limit is not None and processed >= args.limit:
                break

            selector = test_selector_from_path(
                cand.get("primary_test") or cand["test_files"][0]
            )
            pr = f" #{cand['pr_hint']}" if cand.get("pr_hint") else ""
            print(
                f"[{i}/{len(candidates)}] B={b[:12]}{pr}  -Dtest={selector} …",
                file=sys.stderr,
                flush=True,
            )

            entry = verify_one(
                repo,
                cand,
                git_exe=git_exe,
                mvn_exe=mvn_exe,
                timeout_sec=args.timeout,
                maven_quiet=not args.no_quiet,
            )
            results_map[b] = entry
            batch_results.append(entry)

            mark = entry["status"].upper()
            print(
                f"        -> {mark}  ({entry['elapsed_sec']}s)",
                file=sys.stderr,
                flush=True,
            )

            report = {
                "repo": str(repo),
                "input": str(args.input.resolve()),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "timeout_sec": args.timeout,
                "results": results_map,
            }
            save_report(args.output, report)
            processed += 1

    finally:
        if original_head:
            run([git_exe, "checkout", "--detach", original_head], cwd=repo, timeout=120)

    all_results = list(results_map.values())
    print_summary(all_results)
    print(f"报告: {args.output}", file=sys.stderr)

    n_pass = sum(1 for r in all_results if r.get("status") == "pass")
    return 0 if n_pass == len(all_results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
