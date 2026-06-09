#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare LLM-generated tests with human-written tests on structure and assertions."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from misc.update_tests_utils import extract_test_methods


ROOT = Path(__file__).resolve().parent
DEFAULT_SAMPLE_RUNS = ROOT / "artifacts" / "sample_runs"
DEFAULT_CANDIDATES = ROOT / "artifacts" / "lang_sample_candidates_filtered_full_verified_pass.json"
DEFAULT_OUT_DIR = ROOT / "artifacts" / "analysis"


ASSERT_RE = re.compile(
    r"\b(?:(?:Assertions|Assert)\.)?"
    r"(assert[A-Z][A-Za-z0-9_]*|assertThat|fail)\s*\("
)
EXCEPTION_ASSERT_RE = re.compile(
    r"\b(?:(?:Assertions|Assert)\.)?"
    r"(assertThrows|assertThrowsExactly|assertThatThrownBy|assertThatExceptionOfType|assertThatCode)\s*\("
)
TEST_EXPECTED_RE = re.compile(r"@Test\s*\([^)]*\bexpected\s*=")
LOWEST_SECTION_NOTE = (
    "Each model contributes up to 10 non-perfect Maven-pass samples; "
    "if fewer rows are shown, the remaining samples are perfect matches for this metric."
)


def default_repo_path() -> Path:
    workspace_repo = ROOT / "commons-lang"
    if (workspace_repo / ".git").is_dir():
        return workspace_repo
    return ROOT.parent / "commons-lang"


def git_show(repo: Path, revision: str, relpath: str) -> str:
    relpath = relpath.replace("\\", "/")
    proc = subprocess.run(
        ["git", "-C", str(repo), "show", f"{revision}:{relpath}"],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip())
    return proc.stdout


def load_candidates(path: Path) -> dict[int, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {i: c for i, c in enumerate(payload.get("candidates", []), start=1)}


def discover_models(sample_runs: Path, requested: list[str] | None) -> list[str]:
    if requested:
        return requested
    return sorted(
        child.name
        for child in sample_runs.iterdir()
        if child.is_dir() and any(child.glob("cand*_*"))
    )


def candidate_id_from_dir(path: Path) -> int | None:
    match = re.match(r"cand(\d+)_", path.name)
    return int(match.group(1)) if match else None


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    if not union:
        return 1.0
    return len(left & right) / len(union)


def ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 1.0 if numerator == 0 else 0.0
    return numerator / denominator


def json_list(values: set[str]) -> str:
    return json.dumps(sorted(values), ensure_ascii=False)


def json_counter(counter: Counter[str]) -> str:
    return json.dumps(dict(sorted(counter.items())), ensure_ascii=False)


def method_names(source: str) -> set[str]:
    return set(extract_test_methods(source))


def test_method_texts(source: str) -> dict[str, str]:
    return {name: method.text for name, method in extract_test_methods(source).items()}


def normalize_method_text(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"//.*", "", text)
    return re.sub(r"\s+", " ", text).strip()


def modified_methods(old: dict[str, str], new: dict[str, str]) -> set[str]:
    modified: set[str] = set()
    for name in set(old) & set(new):
        if normalize_method_text(old[name]) != normalize_method_text(new[name]):
            modified.add(name)
    return modified


def assertion_distribution(source: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for match in ASSERT_RE.finditer(source):
        counts[match.group(1)] += 1
    return counts


def assertion_count(source: str) -> int:
    return sum(assertion_distribution(source).values())


def exception_assert_count(source: str) -> int:
    return len(EXCEPTION_ASSERT_RE.findall(source)) + len(TEST_EXPECTED_RE.findall(source))


def counter_keys_jaccard(left: Counter[str], right: Counter[str]) -> float:
    return jaccard(set(left), set(right))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_maven_pass(sample_dir: Path) -> bool:
    report_path = sample_dir / "run_report.json"
    if not report_path.is_file():
        return False
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return report.get("maven_returncode") == 0


def compare_one(
    *,
    model: str,
    cand_id: int,
    sample_dir: Path,
    candidate: dict[str, Any],
    repo: Path,
) -> dict[str, Any]:
    old_path = sample_dir / "old_test.java"
    llm_path = sample_dir / "generated.java"
    if not old_path.is_file() or not llm_path.is_file():
        return {
            "model": model,
            "cand_id": cand_id,
            "status": "missing_generated",
            "sample_dir": str(sample_dir),
        }

    test_path = candidate.get("primary_test") or candidate.get("test_files", [""])[0]
    try:
        human_source = git_show(repo, candidate["b"], test_path)
    except Exception as exc:  # noqa: BLE001
        return {
            "model": model,
            "cand_id": cand_id,
            "status": "human_test_unavailable",
            "sample_dir": str(sample_dir),
            "error": f"{type(exc).__name__}: {exc}",
        }

    old_source = read_text(old_path)
    llm_source = read_text(llm_path)

    old_method_texts = test_method_texts(old_source)
    llm_method_texts = test_method_texts(llm_source)
    human_method_texts = test_method_texts(human_source)

    old_methods = set(old_method_texts)
    llm_methods = set(llm_method_texts)
    human_methods = set(human_method_texts)

    llm_added = llm_methods - old_methods
    human_added = human_methods - old_methods
    llm_deleted = old_methods - llm_methods
    human_deleted = old_methods - human_methods
    llm_modified = modified_methods(old_method_texts, llm_method_texts)
    human_modified = modified_methods(old_method_texts, human_method_texts)

    llm_asserts = assertion_distribution(llm_source)
    human_asserts = assertion_distribution(human_source)

    row: dict[str, Any] = {
        "model": model,
        "cand_id": cand_id,
        "status": "ok",
        "sample_dir": str(sample_dir),
        "b": candidate.get("b", ""),
        "subject": candidate.get("subject", ""),
        "test_path": test_path,
        "test_method_count_llm": len(llm_methods),
        "test_method_count_human": len(human_methods),
        "test_method_name_overlap": len(llm_methods & human_methods),
        "test_method_name_jaccard": f"{jaccard(llm_methods, human_methods):.4f}",
        "added_test_count_llm": len(llm_added),
        "added_test_count_human": len(human_added),
        "added_test_overlap": len(llm_added & human_added),
        "added_test_name_jaccard": f"{jaccard(llm_added, human_added):.4f}",
        "deleted_test_count_llm": len(llm_deleted),
        "deleted_test_count_human": len(human_deleted),
        "deleted_test_overlap": len(llm_deleted & human_deleted),
        "deleted_test_name_jaccard": f"{jaccard(llm_deleted, human_deleted):.4f}",
        "modified_test_count_llm": len(llm_modified),
        "modified_test_count_human": len(human_modified),
        "modified_test_overlap": len(llm_modified & human_modified),
        "modified_test_name_jaccard": f"{jaccard(llm_modified, human_modified):.4f}",
        "assert_count_llm": sum(llm_asserts.values()),
        "assert_count_human": sum(human_asserts.values()),
        "assert_count_ratio": f"{ratio(sum(llm_asserts.values()), sum(human_asserts.values())):.4f}",
        "assert_type_distribution_llm": json_counter(llm_asserts),
        "assert_type_distribution_human": json_counter(human_asserts),
        "assert_type_jaccard": f"{counter_keys_jaccard(llm_asserts, human_asserts):.4f}",
        "exception_assert_count_llm": exception_assert_count(llm_source),
        "exception_assert_count_human": exception_assert_count(human_source),
        "added_tests_llm": json_list(llm_added),
        "added_tests_human": json_list(human_added),
        "deleted_tests_llm": json_list(llm_deleted),
        "deleted_tests_human": json_list(human_deleted),
        "modified_tests_llm": json_list(llm_modified),
        "modified_tests_human": json_list(human_modified),
    }
    return row


def mean(values: list[float]) -> str:
    if not values:
        return "0.0000"
    return f"{sum(values) / len(values):.4f}"


def has_added_tests(row: dict[str, Any]) -> bool:
    return int(row["added_test_count_llm"]) > 0 or int(row["added_test_count_human"]) > 0


def has_deleted_tests(row: dict[str, Any]) -> bool:
    return int(row["deleted_test_count_llm"]) > 0 or int(row["deleted_test_count_human"]) > 0


def has_modified_tests(row: dict[str, Any]) -> bool:
    return int(row["modified_test_count_llm"]) > 0 or int(row["modified_test_count_human"]) > 0


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_model: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_model.setdefault(row["model"], []).append(row)

    out: list[dict[str, Any]] = []
    for model, items in sorted(by_model.items()):
        ok = [r for r in items if r.get("status") == "ok"]
        added_applicable = [r for r in ok if has_added_tests(r)]
        deleted_applicable = [r for r in ok if has_deleted_tests(r)]
        modified_applicable = [r for r in ok if has_modified_tests(r)]
        out.append(
            {
                "model": model,
                "total_rows": len(items),
                "comparable_rows": len(ok),
                "added_applicable_rows": len(added_applicable),
                "deleted_applicable_rows": len(deleted_applicable),
                "modified_applicable_rows": len(modified_applicable),
                "mean_method_name_jaccard": mean([float(r["test_method_name_jaccard"]) for r in ok]),
                "mean_added_test_name_jaccard": mean([float(r["added_test_name_jaccard"]) for r in added_applicable]),
                "mean_deleted_test_name_jaccard": mean([float(r["deleted_test_name_jaccard"]) for r in deleted_applicable]),
                "mean_modified_test_name_jaccard": mean([float(r["modified_test_name_jaccard"]) for r in modified_applicable]),
                "mean_assert_count_ratio": mean([float(r["assert_count_ratio"]) for r in ok]),
                "mean_assert_type_jaccard": mean([float(r["assert_type_jaccard"]) for r in ok]),
                "mean_exception_assert_count_llm": mean([float(r["exception_assert_count_llm"]) for r in ok]),
                "mean_exception_assert_count_human": mean([float(r["exception_assert_count_human"]) for r in ok]),
            }
        )
    return out


def perfect_rate(rows: list[dict[str, Any]], field: str, predicate=None) -> str:
    ok = [r for r in rows if r.get("status") == "ok"]
    if predicate is not None:
        ok = [r for r in ok if predicate(r)]
    if not ok:
        return "0.0000"
    n = sum(1 for r in ok if float(r[field]) >= 0.9999)
    return f"{n / len(ok):.4f}"


def top_low_similarity_by_model(
    rows: list[dict[str, Any]],
    field: str,
    *,
    limit: int = 10,
    include_perfect: bool = False,
) -> list[dict[str, Any]]:
    by_model: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if row.get("status") != "ok":
            continue
        if not include_perfect and float(row[field]) >= 0.9999:
            continue
        by_model.setdefault(row["model"], []).append(row)

    out: list[dict[str, Any]] = []
    for _, items in sorted(by_model.items()):
        out.extend(sorted(items, key=lambda r: (float(r[field]), int(r["cand_id"])))[:limit])
    return out


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_report(path: Path, summary_rows: list[dict[str, Any]], sample_rows: list[dict[str, Any]]) -> None:
    by_model: dict[str, list[dict[str, Any]]] = {}
    for row in sample_rows:
        by_model.setdefault(row["model"], []).append(row)

    lines = [
        "# LLM vs Human Test Similarity",
        "",
        "This report compares each LLM-generated `generated.java` against the human-written test file in commit B. "
        "Only samples whose generated tests pass Maven (`maven_returncode == 0`) are included in the similarity averages.",
        "",
        "## Metrics",
        "",
        "- `method_name_jaccard`: Jaccard similarity between LLM and human test method names.",
        "- `added_test_name_jaccard`: Jaccard similarity between test method names added relative to `old_test.java`; summary averages exclude samples where neither side added tests.",
        "- `deleted_test_name_jaccard`: Jaccard similarity between test method names deleted relative to `old_test.java`; summary averages exclude samples where neither side deleted tests.",
        "- `modified_test_name_jaccard`: Jaccard similarity between same-named tests whose normalized method bodies changed relative to `old_test.java`; summary averages exclude samples where neither side modified tests.",
        "- `assert_count_ratio`: total LLM assertion count divided by human assertion count.",
        "- `assert_type_jaccard`: Jaccard similarity between assertion API types, such as `assertEquals` and `assertThrows`.",
        "",
        "## Summary",
        "",
        "| model | comparable_rows | added_applicable_rows | deleted_applicable_rows | modified_applicable_rows | method_name_jaccard | added_test_name_jaccard | deleted_test_name_jaccard | modified_test_name_jaccard | assert_count_ratio | assert_type_jaccard |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        lines.append(
            "| {model} | {comparable_rows} | {added_applicable_rows} | {deleted_applicable_rows} | "
            "{modified_applicable_rows} | {mean_method_name_jaccard} | {mean_added_test_name_jaccard} | "
            "{mean_deleted_test_name_jaccard} | {mean_modified_test_name_jaccard} | "
            "{mean_assert_count_ratio} | {mean_assert_type_jaccard} |".format(**row)
        )
    lines.append("")
    lines.append("## Perfect-Match Rates")
    lines.append("")
    lines.append("| model | method_name_jaccard = 1.0 | added_test_name_jaccard = 1.0 | deleted_test_name_jaccard = 1.0 | modified_test_name_jaccard = 1.0 | assert_type_jaccard = 1.0 |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for model, rows in sorted(by_model.items()):
        lines.append(
            f"| {model} | {perfect_rate(rows, 'test_method_name_jaccard')} | "
            f"{perfect_rate(rows, 'added_test_name_jaccard', has_added_tests)} | "
            f"{perfect_rate(rows, 'deleted_test_name_jaccard', has_deleted_tests)} | "
            f"{perfect_rate(rows, 'modified_test_name_jaccard', has_modified_tests)} | "
            f"{perfect_rate(rows, 'assert_type_jaccard')} |"
        )
    lines.append("")
    lines.append("## Lowest Method-Name Similarity Samples")
    lines.append("")
    lines.append(LOWEST_SECTION_NOTE)
    lines.append("")
    lines.append("| model | cand | method_name_jaccard | added_test_name_jaccard | deleted_test_name_jaccard | assert_count_ratio | subject |")
    lines.append("|---|---:|---:|---:|---:|---:|---|")
    for row in top_low_similarity_by_model(sample_rows, "test_method_name_jaccard"):
        subject = str(row.get("subject", "")).replace("|", "\\|")[:90]
        lines.append(
            f"| {row['model']} | {row['cand_id']} | {row['test_method_name_jaccard']} | "
            f"{row['added_test_name_jaccard']} | {row['deleted_test_name_jaccard']} | "
            f"{row['assert_count_ratio']} | {subject} |"
        )
    lines.append("")
    lines.append("## Lowest Added-Test Similarity Samples")
    lines.append("")
    lines.append(LOWEST_SECTION_NOTE)
    lines.append("")
    lines.append("| model | cand | added_test_name_jaccard | added_test_count_llm | added_test_count_human | subject |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for row in top_low_similarity_by_model(sample_rows, "added_test_name_jaccard"):
        subject = str(row.get("subject", "")).replace("|", "\\|")[:90]
        lines.append(
            f"| {row['model']} | {row['cand_id']} | {row['added_test_name_jaccard']} | "
            f"{row['added_test_count_llm']} | {row['added_test_count_human']} | {subject} |"
        )
    lines.append("")
    lines.append("## Lowest Deleted-Test Similarity Samples")
    lines.append("")
    lines.append(LOWEST_SECTION_NOTE)
    lines.append("")
    lines.append("| model | cand | deleted_test_name_jaccard | deleted_test_count_llm | deleted_test_count_human | subject |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for row in top_low_similarity_by_model(sample_rows, "deleted_test_name_jaccard"):
        subject = str(row.get("subject", "")).replace("|", "\\|")[:90]
        lines.append(
            f"| {row['model']} | {row['cand_id']} | {row['deleted_test_name_jaccard']} | "
            f"{row['deleted_test_count_llm']} | {row['deleted_test_count_human']} | {subject} |"
        )
    lines.append("")
    lines.append("## Lowest Modified-Test Similarity Samples")
    lines.append("")
    lines.append(LOWEST_SECTION_NOTE)
    lines.append("")
    lines.append("| model | cand | modified_test_name_jaccard | modified_test_count_llm | modified_test_count_human | subject |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for row in top_low_similarity_by_model(sample_rows, "modified_test_name_jaccard"):
        subject = str(row.get("subject", "")).replace("|", "\\|")[:90]
        lines.append(
            f"| {row['model']} | {row['cand_id']} | {row['modified_test_name_jaccard']} | "
            f"{row['modified_test_count_llm']} | {row['modified_test_count_human']} | {subject} |"
        )
    lines.append("")
    lines.append("## Lowest Assertion-Type Similarity Samples")
    lines.append("")
    lines.append(LOWEST_SECTION_NOTE)
    lines.append("")
    lines.append("| model | cand | assert_type_jaccard | assert_count_ratio | assert_count_llm | assert_count_human | subject |")
    lines.append("|---|---:|---:|---:|---:|---:|---|")
    for row in top_low_similarity_by_model(sample_rows, "assert_type_jaccard"):
        subject = str(row.get("subject", "")).replace("|", "\\|")[:90]
        lines.append(
            f"| {row['model']} | {row['cand_id']} | {row['assert_type_jaccard']} | "
            f"{row['assert_count_ratio']} | {row['assert_count_llm']} | "
            f"{row['assert_count_human']} | {subject} |"
        )
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- High structural similarity is expected for many samples because the task is test maintenance, not free-form test generation.")
    lines.append("- `assert_count_ratio > 1` means the LLM test contains more assertion calls than the human test; `< 1` means fewer.")
    lines.append("- These metrics are static. They do not prove behavioral equivalence; coverage-based comparison can be added later.")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare LLM generated tests with human B-version tests")
    parser.add_argument("--sample-runs", type=Path, default=DEFAULT_SAMPLE_RUNS)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--repo", type=Path, default=default_repo_path())
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--model", action="append", help="只分析指定模型目录；可重复")
    args = parser.parse_args()

    candidates = load_candidates(args.candidates)
    models = discover_models(args.sample_runs, args.model)
    rows: list[dict[str, Any]] = []
    skipped_non_pass = 0

    for model in models:
        model_dir = args.sample_runs / model
        for sample_dir in sorted(model_dir.glob("cand*_*")):
            cand_id = candidate_id_from_dir(sample_dir)
            if cand_id is None or cand_id not in candidates:
                continue
            if not is_maven_pass(sample_dir):
                skipped_non_pass += 1
                continue
            rows.append(
                compare_one(
                    model=model,
                    cand_id=cand_id,
                    sample_dir=sample_dir,
                    candidate=candidates[cand_id],
                    repo=args.repo,
                )
            )

    sample_fields = [
        "model",
        "cand_id",
        "status",
        "sample_dir",
        "b",
        "subject",
        "test_path",
        "test_method_count_llm",
        "test_method_count_human",
        "test_method_name_overlap",
        "test_method_name_jaccard",
        "added_test_count_llm",
        "added_test_count_human",
        "added_test_overlap",
        "added_test_name_jaccard",
        "deleted_test_count_llm",
        "deleted_test_count_human",
        "deleted_test_overlap",
        "deleted_test_name_jaccard",
        "modified_test_count_llm",
        "modified_test_count_human",
        "modified_test_overlap",
        "modified_test_name_jaccard",
        "assert_count_llm",
        "assert_count_human",
        "assert_count_ratio",
        "assert_type_distribution_llm",
        "assert_type_distribution_human",
        "assert_type_jaccard",
        "exception_assert_count_llm",
        "exception_assert_count_human",
        "added_tests_llm",
        "added_tests_human",
        "deleted_tests_llm",
        "deleted_tests_human",
        "modified_tests_llm",
        "modified_tests_human",
        "error",
    ]
    summary_rows = summarize(rows)
    summary_fields = [
        "model",
        "total_rows",
        "comparable_rows",
        "added_applicable_rows",
        "deleted_applicable_rows",
        "modified_applicable_rows",
        "mean_method_name_jaccard",
        "mean_added_test_name_jaccard",
        "mean_deleted_test_name_jaccard",
        "mean_modified_test_name_jaccard",
        "mean_assert_count_ratio",
        "mean_assert_type_jaccard",
        "mean_exception_assert_count_llm",
        "mean_exception_assert_count_human",
    ]

    write_csv(args.out_dir / "similarity_by_sample.csv", rows, sample_fields)
    write_csv(args.out_dir / "similarity_summary_by_model.csv", summary_rows, summary_fields)
    write_report(args.out_dir / "similarity_report.md", summary_rows, rows)

    print(f"分析模型: {', '.join(models)}")
    print(f"跳过非 Maven pass 样本: {skipped_non_pass}")
    print(f"逐样本相似度: {args.out_dir / 'similarity_by_sample.csv'}")
    print(f"模型相似度汇总: {args.out_dir / 'similarity_summary_by_model.csv'}")
    print(f"报告: {args.out_dir / 'similarity_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
