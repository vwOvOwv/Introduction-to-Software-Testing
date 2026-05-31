#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按两层规则清洗 1_scan.py 生成的 JSON。

第一层（subject）剔除：
  - Revert
  - Merge branch / 合并噪音
  - 纯格式/重构类标题
  - 标题像「只加测试」

第二层（配对）：
  - 仅保留严格同名配对 Foo.java <-> FooTest.java（同包）
  - 拒绝「仅 1 main + 1 test 但类名不对应」的凑对

用法：
  python 2_filter.py
  python 2_filter.py -i artifacts/lang_sample_candidates.json -o artifacts/lang_sample_candidates_filtered.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_IN = ROOT / "artifacts" / "lang_sample_candidates.json"
DEFAULT_OUT = ROOT / "artifacts" / "lang_sample_candidates_filtered.json"
DEFAULT_REJECTED = ROOT / "artifacts" / "lang_sample_candidates_rejected.json"

# 第一层：subject 命中任一则剔除（不区分大小写）
SUBJECT_REJECT: list[tuple[str, re.Pattern[str]]] = [
    ("revert", re.compile(r"\brevert\b", re.I)),
    ("merge_branch", re.compile(r"merge branch\b", re.I)),
    ("merge_remote", re.compile(r"merge remote-tracking", re.I)),
    ("merge_pull_noise", re.compile(r"^merge pull request #\d+ from", re.I)),
    ("empty_lines", re.compile(r"replace\s+2x\s+empty\s+lines|empty\s+lines?\s+with", re.I)),
    ("use_expression", re.compile(r"^use expression\b", re.I)),
    ("sort_members", re.compile(r"^sort members\b", re.I)),
    ("rename_internal", re.compile(r"^rename internal\b", re.I)),
    ("javadoc_only", re.compile(r"^better javadoc\b|^javadoc\b", re.I)),
    ("use_jre_constants", re.compile(r"^use jre constants\b", re.I)),
    ("typos_format", re.compile(r"^fix typos\b|^fix typo\b", re.I)),
    ("add_more_tests", re.compile(r"\badd more tests\b", re.I)),
    ("add_tests_only", re.compile(r"^add tests?\s+for\b", re.I)),
    ("only_test_changes", re.compile(r"^add test\b.*\bfor\b", re.I)),
]

PR_RE = re.compile(r"#(\d+)\b")


def strict_name_pair(main: str, test: str) -> bool:
    """Foo.java 与同包 FooTest.java。"""
    main, test = main.replace("\\", "/"), test.replace("\\", "/")
    mp, tp = Path(main), Path(test)
    if mp.stem + "Test" != tp.stem:
        return False
    try:
        main_pkg = mp.relative_to("src/main/java").parent
        test_pkg = tp.relative_to("src/test/java").parent
    except ValueError:
        return False
    return main_pkg == test_pkg


def pick_strict_pair(main_files: list[str], test_files: list[str]) -> tuple[str, str] | None:
    for main in main_files:
        for test in test_files:
            if strict_name_pair(main, test):
                return main, test
    return None


def layer1_reject_reason(subject: str) -> str | None:
    for name, pat in SUBJECT_REJECT:
        if pat.search(subject):
            return f"layer1:{name}"
    return None


def layer2_reject_reason(main_files: list[str], test_files: list[str]) -> str | None:
    if not pick_strict_pair(main_files, test_files):
        mains = ", ".join(Path(p).name for p in main_files)
        tests = ", ".join(Path(p).name for p in test_files)
        return f"layer2:no_strict_pair ({mains} vs {tests})"
    return None


def filter_candidates(candidates: list[dict]) -> tuple[list[dict], list[dict]]:
    kept: list[dict] = []
    rejected: list[dict] = []

    for c in candidates:
        subject = c.get("subject", "")
        r1 = layer1_reject_reason(subject)
        if r1:
            rejected.append({**c, "reject_reason": r1})
            continue
        r2 = layer2_reject_reason(c.get("main_files", []), c.get("test_files", []))
        if r2:
            rejected.append({**c, "reject_reason": r2})
            continue
        pair = pick_strict_pair(c["main_files"], c["test_files"])
        enriched = {
            **c,
            "primary_main": pair[0],
            "primary_test": pair[1],
            "primary_main_name": Path(pair[0]).name,
            "primary_test_name": Path(pair[1]).name,
        }
        pr = PR_RE.search(subject)
        if pr:
            enriched["pr_hint"] = int(pr.group(1))
        kept.append(enriched)

    return kept, rejected


def print_table(items: list[dict], *, title: str, limit: int) -> None:
    print(f"\n=== {title} ({len(items)} 条，显示前 {min(limit, len(items))} 条) ===\n")
    for i, c in enumerate(items[:limit], 1):
        pr = f" #{c['pr_hint']}" if c.get("pr_hint") else ""
        print(
            f"{i:3}. score={c.get('score', '?'):>2}  B={c['b'][:12]}  "
            f"{c.get('primary_main_name', '?')} <-> {c.get('primary_test_name', '?')}{pr}\n"
            f"     {c['subject'][:95]}\n"
            f"     A={c['a']}\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="清洗 lang_sample_candidates.json（两层规则）")
    parser.add_argument("-i", "--input", type=Path, default=DEFAULT_IN)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--rejected", type=Path, default=DEFAULT_REJECTED, help="剔除条目 JSON")
    parser.add_argument("--top", type=int, default=50, help="终端打印保留条数")
    parser.add_argument("--show-rejected", type=int, default=15, help="终端打印剔除条数样例")
    args = parser.parse_args()

    if not args.input.is_file():
        print(f"错误：找不到输入文件 {args.input}", file=sys.stderr)
        return 2

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    candidates: list[dict] = payload.get("candidates", [])
    kept, rejected = filter_candidates(candidates)

    out_payload = {
        **{k: v for k, v in payload.items() if k != "candidates"},
        "filter": "layer1_subject + layer2_strict_Foo_FooTest",
        "count_input": len(candidates),
        "count_kept": len(kept),
        "count_rejected": len(rejected),
        "candidates": kept,
    }
    rej_payload = {
        "count": len(rejected),
        "rejected": rejected,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.rejected.write_text(json.dumps(rej_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 简要统计剔除原因
    from collections import Counter

    reasons = Counter(r["reject_reason"].split(" (")[0] for r in rejected)
    print(
        f"输入 {len(candidates)} 条 → 保留 {len(kept)} 条，剔除 {len(rejected)} 条\n"
        f"已写入:\n  {args.output}\n  {args.rejected}\n\n剔除原因统计:",
        file=sys.stderr,
    )
    for reason, n in reasons.most_common():
        print(f"  {reason}: {n}", file=sys.stderr)

    print_table(kept, title="保留", limit=args.top)
    if args.show_rejected:
        print_table(
            [{**r, "primary_main_name": Path(r["main_files"][0]).name if r.get("main_files") else "?",
              "primary_test_name": Path(r["test_files"][0]).name if r.get("test_files") else "?"} for r in rejected],
            title="剔除（样例）",
            limit=args.show_rejected,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
