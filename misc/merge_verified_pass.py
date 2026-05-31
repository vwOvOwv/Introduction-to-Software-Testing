#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge candidates that pass in one or more Maven verification reports."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATES = ROOT / "artifacts" / "lang_sample_candidates_filtered_full.json"
DEFAULT_REPORTS = [
    ROOT / "artifacts" / "lang_sample_verify_report_full_jdk8.json",
    ROOT / "artifacts" / "lang_sample_verify_report_full_jdk17.json",
]
DEFAULT_OUT = ROOT / "artifacts" / "lang_sample_candidates_filtered_full_verified_pass.json"


def report_label(path: Path) -> str:
    stem = path.stem
    prefix = "lang_sample_verify_report_full_"
    return stem[len(prefix) :] if stem.startswith(prefix) else stem


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"找不到文件: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="合并多个 verify report 中 status=pass 的候选样本")
    parser.add_argument("-i", "--input", type=Path, default=DEFAULT_CANDIDATES, help="候选 JSON")
    parser.add_argument(
        "-r",
        "--report",
        type=Path,
        action="append",
        default=None,
        help="验证报告 JSON；可重复传入。默认合并 full_jdk8 与 full_jdk17",
    )
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUT, help="输出候选 JSON")
    args = parser.parse_args()

    candidate_path = args.input.resolve()
    report_paths = [p.resolve() for p in (args.report or DEFAULT_REPORTS)]
    output_path = args.output.resolve()

    payload = load_json(candidate_path)
    candidates: list[dict] = payload.get("candidates", [])
    if not candidates:
        print(f"错误：{candidate_path} 中 candidates 为空", file=sys.stderr)
        return 2

    pass_sources: dict[str, list[str]] = {}
    report_summaries: list[dict[str, object]] = []

    for report_path in report_paths:
        report = load_json(report_path)
        label = report_label(report_path)
        results: dict[str, dict] = report.get("results", {})
        counts = Counter(r.get("status", "<missing>") for r in results.values())

        for b, result in results.items():
            if result.get("status") == "pass":
                pass_sources.setdefault(b, []).append(label)

        report_summaries.append(
            {
                "path": str(report_path),
                "label": label,
                "total": len(results),
                "status_counts": dict(sorted(counts.items())),
            }
        )

    kept: list[dict] = []
    missing_in_candidates = 0
    candidate_b = {c.get("b") for c in candidates}
    for b in pass_sources:
        if b not in candidate_b:
            missing_in_candidates += 1

    for candidate in candidates:
        b = candidate.get("b")
        if b not in pass_sources:
            continue
        kept.append(
            {
                **candidate,
                "verified_pass_sources": pass_sources[b],
            }
        )

    out_payload = {
        **{k: v for k, v in payload.items() if k != "candidates"},
        "filter": f"{payload.get('filter', 'candidates')} + verified_pass_union",
        "verify_reports": report_summaries,
        "count_input": len(candidates),
        "count_kept": len(kept),
        "count_rejected_by_verify": len(candidates) - len(kept),
        "count_pass_not_in_candidates": missing_in_candidates,
        "candidates": kept,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(out_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"输入候选: {len(candidates)}", file=sys.stderr)
    for summary in report_summaries:
        print(
            f"{summary['label']}: total={summary['total']} status={summary['status_counts']}",
            file=sys.stderr,
        )
    print(f"合并保留: {len(kept)}", file=sys.stderr)
    if missing_in_candidates:
        print(f"警告：{missing_in_candidates} 个 pass B 不在候选 JSON 中", file=sys.stderr)
    print(f"已写入: {output_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
