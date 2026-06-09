#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analyze model experiment run reports.

Reads artifacts/sample_runs/<model>/candXXX_*/run_report.json and writes:
  - artifacts/analysis/model_summary.csv
  - artifacts/analysis/failure_breakdown.csv
  - artifacts/analysis/sample_results.csv
  - artifacts/analysis/report.md
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_SAMPLE_RUNS = ROOT / "artifacts" / "sample_runs"
DEFAULT_CANDIDATES = ROOT / "artifacts" / "lang_sample_candidates_filtered_full_verified_pass.json"
DEFAULT_OUT_DIR = ROOT / "artifacts" / "analysis"


@dataclass
class SampleResult:
    model: str
    cand_id: int
    sample_dir: str
    b: str = ""
    subject: str = ""
    selector: str = ""
    generated: bool = False
    update_exit_code: int | None = None
    run_exit_code: int | None = None
    maven_returncode: int | None = None
    status: str = "unknown"
    failure_category: str = ""
    failure_detail: str = ""


def load_candidates(path: Path) -> dict[int, dict[str, Any]]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {i: c for i, c in enumerate(payload.get("candidates", []), start=1)}


def discover_models(sample_runs: Path, requested: list[str] | None) -> list[str]:
    if requested:
        return requested
    if not sample_runs.is_dir():
        return []
    models: list[str] = []
    for child in sorted(sample_runs.iterdir()):
        if child.is_dir() and any(child.glob("cand*_*")):
            models.append(child.name)
    return models


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {"_json_error": f"{type(exc).__name__}: {exc}"}


def combined_error_text(report: dict[str, Any]) -> str:
    parts = [
        report.get("processing_error"),
        report.get("run_setup_error"),
        report.get("update_stdout_tail"),
        report.get("update_stderr_tail"),
        report.get("run_stdout_tail"),
        report.get("run_stderr_tail"),
        report.get("maven_stdout_tail"),
        report.get("maven_stderr_tail"),
    ]
    return "\n".join(str(p) for p in parts if p)


def classify_failure(report: dict[str, Any]) -> tuple[str, str]:
    text = combined_error_text(report)
    lower = text.lower()
    detail = " ".join(text.split())[-500:]

    if report.get("_json_error"):
        return "bad_report", report["_json_error"]
    if report.get("processing_error"):
        return "merge_or_processing_error", str(report.get("processing_error"))
    if report.get("run_setup_error"):
        return "setup_error", str(report.get("run_setup_error"))
    if report.get("generated") is False:
        if "insufficient balance" in lower or "http 402" in lower:
            return "api_insufficient_balance", detail
        if "connection reset" in lower:
            return "api_connection_reset", detail
        if "unexpected_eof_while_reading" in lower or "ssl:" in lower:
            return "api_ssl_eof", detail
        if "timeouterror" in lower or "timed out" in lower:
            return "api_timeout", detail
        http_match = re.search(r"HTTP\s+(\d+)", text)
        if http_match:
            return f"api_http_{http_match.group(1)}", detail
        if report.get("update_exit_code") is not None:
            return "model_update_failed", detail
        return "generation_failed", detail

    if report.get("maven_returncode") == 0:
        return "", ""

    if "compilation error" in lower or "compilation failure" in lower:
        if "cannot find symbol" in lower:
            return "compile_cannot_find_symbol", detail
        if "incompatible types" in lower:
            return "compile_incompatible_types", detail
        if "method " in lower and "cannot be applied" in lower:
            return "compile_method_mismatch", detail
        if "package " in lower and " does not exist" in lower:
            return "compile_missing_package", detail
        return "compile_error", detail
    if "there are test failures" in lower or "failures:" in lower or "assertion" in lower:
        return "test_failure", detail
    if "no tests were executed" in lower or "no tests matching pattern" in lower:
        return "no_tests_executed", detail
    if "apache-rat-plugin" in lower or "unapproved license" in lower:
        return "rat_license_check", detail
    if report.get("run_exit_code") is not None:
        return "maven_other_failure", detail
    return "unknown_failure", detail


def status_from_report(report: dict[str, Any], failure_category: str) -> str:
    if report.get("_json_error"):
        return "bad_report"
    if report.get("generated") is False:
        return "generation_failed"
    if report.get("generated") is True and report.get("maven_returncode") == 0:
        return "maven_pass"
    if report.get("generated") is True and report.get("maven_returncode") is not None:
        return "maven_fail"
    if report.get("run_skipped"):
        return "run_skipped"
    if failure_category:
        return "failed"
    return "unknown"


def candidate_id_from_dir(path: Path) -> int | None:
    match = re.match(r"cand(\d+)_", path.name)
    return int(match.group(1)) if match else None


def analyze_model(model_dir: Path, candidates: dict[int, dict[str, Any]]) -> list[SampleResult]:
    existing: dict[int, Path] = {}
    for sample_dir in model_dir.glob("cand*_*"):
        cand_id = candidate_id_from_dir(sample_dir)
        if cand_id is not None:
            existing[cand_id] = sample_dir

    ids = sorted(set(existing) | set(candidates))
    results: list[SampleResult] = []
    for cand_id in ids:
        sample_dir = existing.get(cand_id)
        candidate = candidates.get(cand_id, {})
        if sample_dir is None:
            results.append(
                SampleResult(
                    model=model_dir.name,
                    cand_id=cand_id,
                    sample_dir="",
                    b=candidate.get("b", ""),
                    subject=candidate.get("subject", ""),
                    selector=Path(candidate.get("primary_test", "")).stem,
                    status="no_dir",
                    failure_category="no_dir",
                )
            )
            continue

        report_path = sample_dir / "run_report.json"
        if not report_path.is_file():
            has_raw = (sample_dir / "raw.md").is_file()
            has_generated = (sample_dir / "generated.java").is_file()
            status = "merge_incomplete" if has_raw and not has_generated else "no_report"
            category = status
            results.append(
                SampleResult(
                    model=model_dir.name,
                    cand_id=cand_id,
                    sample_dir=str(sample_dir),
                    b=candidate.get("b", ""),
                    subject=candidate.get("subject", ""),
                    selector=Path(candidate.get("primary_test", "")).stem,
                    status=status,
                    failure_category=category,
                )
            )
            continue

        report = read_json(report_path)
        has_raw = (sample_dir / "raw.md").is_file()
        has_generated = (sample_dir / "generated.java").is_file()
        if has_raw and not has_generated and report.get("generated") is False:
            category, detail = "merge_incomplete", "raw.md exists, but generated.java is missing"
            status = "merge_incomplete"
        else:
            category, detail = classify_failure(report)
            status = status_from_report(report, category)
        results.append(
            SampleResult(
                model=model_dir.name,
                cand_id=cand_id,
                sample_dir=str(sample_dir),
                b=str(report.get("b") or candidate.get("b", "")),
                subject=str(report.get("subject") or candidate.get("subject", "")),
                selector=str(report.get("selector") or Path(candidate.get("primary_test", "")).stem),
                generated=bool(report.get("generated")),
                update_exit_code=report.get("update_exit_code"),
                run_exit_code=report.get("run_exit_code"),
                maven_returncode=report.get("maven_returncode"),
                status=status,
                failure_category=category,
                failure_detail=detail,
            )
        )
    return results


def summarize(results: list[SampleResult]) -> list[dict[str, Any]]:
    by_model: dict[str, list[SampleResult]] = {}
    for item in results:
        by_model.setdefault(item.model, []).append(item)

    rows: list[dict[str, Any]] = []
    for model, items in sorted(by_model.items()):
        total = len(items)
        generated = sum(1 for x in items if x.generated)
        maven_pass = sum(1 for x in items if x.status == "maven_pass")
        maven_fail = sum(1 for x in items if x.status == "maven_fail")
        generation_failed = sum(1 for x in items if x.status == "generation_failed")
        no_report = sum(1 for x in items if x.status == "no_report")
        merge_incomplete = sum(1 for x in items if x.status == "merge_incomplete")
        no_dir = sum(1 for x in items if x.status == "no_dir")
        setup_error = sum(1 for x in items if x.failure_category == "setup_error")
        compile_fail = sum(1 for x in items if x.failure_category.startswith("compile_"))
        test_fail = sum(1 for x in items if x.failure_category == "test_failure")
        rows.append(
            {
                "model": model,
                "total": total,
                "generated": generated,
                "generation_failed": generation_failed,
                "maven_pass": maven_pass,
                "maven_fail": maven_fail,
                "compile_fail": compile_fail,
                "test_fail": test_fail,
                "setup_error": setup_error,
                "merge_incomplete": merge_incomplete,
                "no_report": no_report,
                "no_dir": no_dir,
                "generation_success_rate": rate(generated, total),
                "maven_pass_rate": rate(maven_pass, total),
                "pass_given_generated": rate(maven_pass, generated),
            }
        )
    return rows


def failure_breakdown(results: list[SampleResult]) -> list[dict[str, Any]]:
    counter: Counter[tuple[str, str]] = Counter()
    totals: Counter[str] = Counter()
    for item in results:
        totals[item.model] += 1
        if item.failure_category:
            counter[(item.model, item.failure_category)] += 1
    rows: list[dict[str, Any]] = []
    for (model, category), count in sorted(counter.items()):
        rows.append(
            {
                "model": model,
                "failure_category": category,
                "count": count,
                "rate": rate(count, totals[model]),
            }
        )
    return rows


def rate(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return "0.0000"
    return f"{numerator / denominator:.4f}"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_report(path: Path, summary_rows: list[dict[str, Any]], breakdown_rows: list[dict[str, Any]]) -> None:
    lines = ["# Model Test Update Results", ""]
    lines.append("## Summary")
    lines.append("")
    lines.append(
        "| model | total | generated | maven_pass | maven_fail | "
        "generation_failed | merge_incomplete | pass_rate | pass_given_generated |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in summary_rows:
        lines.append(
            "| {model} | {total} | {generated} | {maven_pass} | {maven_fail} | "
            "{generation_failed} | {merge_incomplete} | {maven_pass_rate} | {pass_given_generated} |".format(**row)
        )
    lines.append("")
    lines.append("## Failure Breakdown")
    lines.append("")
    lines.append("| model | failure_category | count | rate |")
    lines.append("|---|---|---:|---:|")
    for row in breakdown_rows:
        lines.append("| {model} | {failure_category} | {count} | {rate} |".format(**row))
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze LLM test-update experiment results")
    parser.add_argument("--sample-runs", type=Path, default=DEFAULT_SAMPLE_RUNS)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--model", action="append", help="只分析指定模型目录；可重复")
    args = parser.parse_args()

    candidates = load_candidates(args.candidates)
    models = discover_models(args.sample_runs, args.model)
    if not models:
        print(f"没有找到模型结果目录: {args.sample_runs}")
        return 2

    all_results: list[SampleResult] = []
    for model in models:
        model_dir = args.sample_runs / model
        if not model_dir.is_dir():
            print(f"跳过不存在的模型目录: {model_dir}")
            continue
        all_results.extend(analyze_model(model_dir, candidates))

    summary_rows = summarize(all_results)
    breakdown_rows = failure_breakdown(all_results)
    sample_rows = [item.__dict__ for item in sorted(all_results, key=lambda x: (x.model, x.cand_id))]

    write_csv(
        args.out_dir / "model_summary.csv",
        summary_rows,
        [
            "model",
            "total",
            "generated",
            "generation_failed",
            "maven_pass",
            "maven_fail",
            "compile_fail",
            "test_fail",
            "setup_error",
            "merge_incomplete",
            "no_report",
            "no_dir",
            "generation_success_rate",
            "maven_pass_rate",
            "pass_given_generated",
        ],
    )
    write_csv(args.out_dir / "failure_breakdown.csv", breakdown_rows, ["model", "failure_category", "count", "rate"])
    write_csv(
        args.out_dir / "sample_results.csv",
        sample_rows,
        [
            "model",
            "cand_id",
            "sample_dir",
            "b",
            "subject",
            "selector",
            "generated",
            "update_exit_code",
            "run_exit_code",
            "maven_returncode",
            "status",
            "failure_category",
            "failure_detail",
        ],
    )
    write_report(args.out_dir / "report.md", summary_rows, breakdown_rows)

    print(f"分析模型: {', '.join(models)}")
    print(f"样本明细: {args.out_dir / 'sample_results.csv'}")
    print(f"模型汇总: {args.out_dir / 'model_summary.csv'}")
    print(f"失败分类: {args.out_dir / 'failure_breakdown.csv'}")
    print(f"报告: {args.out_dir / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
