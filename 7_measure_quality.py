#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Measure classic test-quality metrics for human and LLM tests."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_REPO = ROOT.parent / "commons-lang"
DEFAULT_SAMPLE_RUNS = ROOT / "artifacts" / "sample_runs"
DEFAULT_CANDIDATES = ROOT / "artifacts" / "lang_sample_candidates_filtered_full_verified_pass.json"
DEFAULT_OUT_DIR = ROOT / "artifacts" / "analysis"
DEFAULT_MAVEN_REPO_LOCAL = Path("/tmp/m2")

JACOCO_VERSION = "0.8.11"
PIT_VERSION = "1.15.8"
LOG_TAIL_CHARS = 12000


def classify_tool_failure(stdout: str, stderr: str) -> str:
    text = f"{stdout}\n{stderr}"
    lower = text.lower()
    if "there are test failures" in lower or "failed tests:" in lower:
        return "test_failure"
    if lower.count("-javaagent:") >= 2 and "jacoco" in lower:
        return "jacoco_agent_conflict"
    if "forked vm terminated without properly saying goodbye" in lower:
        return "forked_vm_crash"
    if "compilation failure" in lower or "compilation error" in lower:
        return "compilation_failure"
    if "no compiler is provided" in lower:
        return "missing_jdk"
    if "could not resolve" in lower or "could not find artifact" in lower:
        return "dependency_resolution"
    if "no tests were executed" in lower:
        return "no_tests_executed"
    if "no mutations found" in lower:
        return "no_mutations_found"
    if "timeout" in lower or "timed out" in lower:
        return "timeout"
    if "unsupported class file major version" in lower:
        return "java_version_mismatch"
    if "mojoexecutionexception" in lower:
        return "maven_plugin_execution"
    if "mojofailureexception" in lower:
        return "maven_plugin_failure"
    return "maven_other_failure"


def sanitize_name(value: str) -> str:
    return value.strip().replace("/", "_").replace("\\", "_").replace(":", "_") or "model"


def candidate_id_from_dir(path: Path) -> int | None:
    match = re.match(r"cand(\d+)_", path.name)
    return int(match.group(1)) if match else None


def class_name_from_path(path: str, root: str) -> str:
    value = path.replace("\\", "/")
    if value.startswith(root):
        value = value[len(root) :]
    if value.endswith(".java"):
        value = value[:-5]
    return value.strip("/").replace("/", ".")


def test_selector_from_path(path: str) -> str:
    return Path(path.replace("\\", "/")).stem


def load_candidates(path: Path) -> dict[int, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {i: c for i, c in enumerate(payload.get("candidates", []), start=1)}


def discover_models(sample_runs: Path, requested: list[str] | None) -> list[str]:
    if requested:
        return [sanitize_name(x) for x in requested]
    return sorted(child.name for child in sample_runs.iterdir() if child.is_dir() and any(child.glob("cand*_*")))


def is_maven_pass(sample_dir: Path) -> bool:
    report_path = sample_dir / "run_report.json"
    if not report_path.is_file():
        return False
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return report.get("maven_returncode") == 0


def run_command(
    command: list[str],
    cwd: Path,
    timeout: int | None,
    *,
    java_home: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if java_home is not None:
        env["JAVA_HOME"] = str(java_home)
        env["PATH"] = f"{java_home / 'bin'}:{env.get('PATH', '')}"
    return subprocess.run(
        command,
        cwd=str(cwd),
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
    )


def resolve_java_home(value: Path | None) -> Path | None:
    candidates: list[Path] = []
    if value is not None:
        candidates.append(value)
    candidates.extend([Path.home() / "jdk8", Path.home() / "jdk-17"])
    for candidate in candidates:
        if (candidate / "bin" / "javac").is_file():
            return candidate
    return None


def resolve_mvn(value: Path | None) -> str:
    if value is not None:
        if value.is_file():
            return str(value)
        raise FileNotFoundError(f"mvn not found: {value}")
    found = shutil.which("mvn")
    if found:
        return found
    common = Path.home() / "apache-maven-3.9.9" / "bin" / "mvn"
    if common.is_file():
        return str(common)
    raise FileNotFoundError("mvn")


def export_ref_to_temp(repo: Path, ref: str) -> Path:
    root = Path(tempfile.gettempdir()) / "quality_runs"
    root.mkdir(parents=True, exist_ok=True)
    checkout = Path(tempfile.mkdtemp(prefix="quality-", dir=str(root)))

    archive = subprocess.Popen(
        ["git", "-C", str(repo), "archive", ref],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    tar = subprocess.Popen(
        ["tar", "-x", "-C", str(checkout)],
        stdin=archive.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if archive.stdout is not None:
        archive.stdout.close()
    _, tar_stderr = tar.communicate()
    _, archive_stderr = archive.communicate()
    if archive.returncode != 0 or tar.returncode != 0:
        shutil.rmtree(checkout, ignore_errors=True)
        detail = (archive_stderr or tar_stderr or b"").decode("utf-8", errors="replace").strip()
        raise RuntimeError(detail or f"failed to export {ref}")
    return checkout


def replace_test(worktree: Path, target_test_path: str, replacement: Path) -> None:
    dst = worktree / target_test_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(replacement.read_text(encoding="utf-8"), encoding="utf-8")


def parse_jacoco_counters(elements: list[ET.Element]) -> dict[str, float | int | str]:
    counters = {
        "INSTRUCTION": ("instruction", "instruction_coverage"),
        "BRANCH": ("branch", "branch_coverage"),
        "LINE": ("line", "line_coverage"),
        "METHOD": ("method", "method_coverage"),
    }
    out: dict[str, float | int | str] = {}
    totals = {key: [0, 0] for key in counters}
    for element in elements:
        for counter in element.findall("counter"):
            counter_type = counter.get("type")
            if counter_type not in counters:
                continue
            totals[counter_type][0] += int(counter.get("missed", "0"))
            totals[counter_type][1] += int(counter.get("covered", "0"))
    for counter_type, (prefix, ratio_name) in counters.items():
        missed, covered = totals[counter_type]
        total = missed + covered
        out[f"{prefix}_missed"] = missed
        out[f"{prefix}_covered"] = covered
        out[ratio_name] = covered / total if total else 0.0
    return out


def parse_jacoco_xml(path: Path, target_fqn: str) -> dict[str, float | int | str]:
    if not path.is_file():
        raise RuntimeError(f"missing JaCoCo XML: {path}")
    root = ET.parse(path).getroot()
    target_internal = target_fqn.replace(".", "/")
    classes = [
        element
        for element in root.findall(".//class")
        if element.get("name") == target_internal or str(element.get("name", "")).startswith(target_internal + "$")
    ]
    if classes:
        return parse_jacoco_counters(classes)
    return parse_jacoco_counters([root])


def ensure_jacoco_agent(worktree: Path, mvn: str, java_home: Path | None, maven_repo_local: Path) -> Path:
    agent = (
        maven_repo_local
        / "org"
        / "jacoco"
        / "org.jacoco.agent"
        / JACOCO_VERSION
        / f"org.jacoco.agent-{JACOCO_VERSION}-runtime.jar"
    )
    if agent.is_file():
        return agent
    result = run_command(
        [
            mvn,
            "-q",
            f"-Dmaven.repo.local={maven_repo_local}",
            "org.apache.maven.plugins:maven-dependency-plugin:3.6.1:get",
            f"-Dartifact=org.jacoco:org.jacoco.agent:{JACOCO_VERSION}:jar:runtime",
        ],
        worktree,
        300,
        java_home=java_home,
    )
    if result.returncode != 0 or not agent.is_file():
        raise RuntimeError(result.stdout[-LOG_TAIL_CHARS:] + result.stderr[-LOG_TAIL_CHARS:])
    return agent


def run_coverage(
    worktree: Path,
    mvn: str,
    java_home: Path | None,
    maven_repo_local: Path,
    test_selector: str,
    target_fqn: str,
    timeout: int,
) -> dict[str, Any]:
    agent = ensure_jacoco_agent(worktree, mvn, java_home, maven_repo_local)
    jacoco_exec = worktree / "target" / "jacoco.exec"
    test_command = [
        mvn,
        "-q",
        f"-Dmaven.repo.local={maven_repo_local}",
        "-Djacoco.skip=true",
        f"-DargLine=-javaagent:{agent}=destfile={jacoco_exec},append=false",
        f"-Dtest={test_selector}",
        "test",
    ]
    test_result = run_command(test_command, worktree, timeout, java_home=java_home)
    out: dict[str, Any] = {
        "coverage_returncode": test_result.returncode,
        "coverage_stdout_tail": test_result.stdout[-LOG_TAIL_CHARS:],
        "coverage_stderr_tail": test_result.stderr[-LOG_TAIL_CHARS:],
    }
    if test_result.returncode != 0:
        out["coverage_failure_category"] = classify_tool_failure(test_result.stdout, test_result.stderr)
        return out

    report_command = [
        mvn,
        "-q",
        f"-Dmaven.repo.local={maven_repo_local}",
        f"org.jacoco:jacoco-maven-plugin:{JACOCO_VERSION}:report",
    ]
    report_result = run_command(report_command, worktree, timeout, java_home=java_home)
    out["coverage_returncode"] = report_result.returncode
    out["coverage_stdout_tail"] = (test_result.stdout + "\n" + report_result.stdout)[-LOG_TAIL_CHARS:]
    out["coverage_stderr_tail"] = (test_result.stderr + "\n" + report_result.stderr)[-LOG_TAIL_CHARS:]
    if report_result.returncode == 0:
        out.update(parse_jacoco_xml(worktree / "target" / "site" / "jacoco" / "jacoco.xml", target_fqn))
    else:
        out["coverage_failure_category"] = classify_tool_failure(report_result.stdout, report_result.stderr)
    return out


def parse_mutations_xml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise RuntimeError(f"missing PIT mutations XML: {path}")
    root = ET.parse(path).getroot()
    total = 0
    detected = 0
    status_counts: dict[str, int] = {}
    for mutation in root.findall("mutation"):
        total += 1
        status = mutation.get("status", "UNKNOWN")
        status_counts[status] = status_counts.get(status, 0) + 1
        if mutation.get("detected") == "true":
            detected += 1
    return {
        "mutation_total": total,
        "mutation_detected": detected,
        "mutation_score": detected / total if total else 0.0,
        "mutation_status_counts": json.dumps(status_counts, ensure_ascii=False, sort_keys=True),
    }


def run_mutation(
    worktree: Path,
    mvn: str,
    java_home: Path | None,
    maven_repo_local: Path,
    test_fqn: str,
    target_fqn: str,
    timeout: int,
) -> dict[str, Any]:
    command = [
        mvn,
        "-q",
        f"-Dmaven.repo.local={maven_repo_local}",
        "test-compile",
        f"org.pitest:pitest-maven:{PIT_VERSION}:mutationCoverage",
        f"-DtargetTests={test_fqn}",
        f"-DtargetClasses={target_fqn}*",
        "-DoutputFormats=XML",
        "-DtimestampedReports=false",
        "-Dthreads=4",
    ]
    result = run_command(command, worktree, timeout, java_home=java_home)
    out: dict[str, Any] = {
        "mutation_returncode": result.returncode,
        "mutation_stdout_tail": result.stdout[-LOG_TAIL_CHARS:],
        "mutation_stderr_tail": result.stderr[-LOG_TAIL_CHARS:],
    }
    if result.returncode == 0:
        out.update(parse_mutations_xml(worktree / "target" / "pit-reports" / "mutations.xml"))
    else:
        out["mutation_failure_category"] = classify_tool_failure(result.stdout, result.stderr)
    return out


def prefixed(prefix: str, values: dict[str, Any]) -> dict[str, Any]:
    return {f"{prefix}_{k}": v for k, v in values.items()}


def fmt(value: Any) -> str:
    return f"{value:.4f}" if isinstance(value, float) else value


def add_comparison_fields(row: dict[str, Any]) -> None:
    for metric in ("line_coverage", "branch_coverage", "instruction_coverage", "method_coverage", "mutation_score"):
        try:
            human = float(row.get(f"human_{metric}", ""))
            llm = float(row.get(f"llm_{metric}", ""))
        except (TypeError, ValueError):
            continue
        row[f"{metric}_diff_llm_minus_human"] = llm - human
        row[f"{metric}_ratio_llm_to_human"] = 1.0 if human == 0 and llm == 0 else (llm / human if human else 0.0)


def measure_one(
    *,
    repo: Path,
    mvn: str,
    java_home: Path | None,
    maven_repo_local: Path,
    sample_dir: Path,
    candidate: dict[str, Any],
    skip_coverage: bool,
    skip_mutation: bool,
    coverage_timeout: int,
    mutation_timeout: int,
) -> dict[str, Any]:
    test_path = candidate.get("primary_test") or candidate.get("test_files", [""])[0]
    prod_path = candidate.get("primary_main") or candidate.get("main_files", [""])[0]
    test_selector = test_selector_from_path(test_path)
    test_fqn = class_name_from_path(test_path, "src/test/java/")
    target_fqn = class_name_from_path(prod_path, "src/main/java/")

    row: dict[str, Any] = {
        "b": candidate.get("b", ""),
        "subject": candidate.get("subject", ""),
        "test_path": test_path,
        "prod_path": prod_path,
        "test_selector": test_selector,
        "test_fqn": test_fqn,
        "target_fqn": target_fqn,
    }

    for variant in ("human", "llm"):
        checkout = export_ref_to_temp(repo, candidate["b"])
        try:
            if variant == "llm":
                replace_test(checkout, test_path, sample_dir / "generated.java")
            if not skip_coverage:
                row.update(
                    prefixed(
                        variant,
                        run_coverage(
                            checkout,
                            mvn,
                            java_home,
                            maven_repo_local,
                            test_selector,
                            target_fqn,
                            coverage_timeout,
                        ),
                    )
                )
            if not skip_mutation:
                row.update(
                    prefixed(
                        variant,
                        run_mutation(checkout, mvn, java_home, maven_repo_local, test_fqn, target_fqn, mutation_timeout),
                    )
                )
        finally:
            shutil.rmtree(checkout, ignore_errors=True)

    add_comparison_fields(row)
    return row


def row_key(row: dict[str, Any]) -> tuple[str, int]:
    return row["model"], int(row["cand_id"])


def load_existing_rows(path: Path) -> dict[tuple[str, int], dict[str, str]]:
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8", newline="") as fh:
        return {row_key(r): r for r in csv.DictReader(fh)}


def append_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.is_file()
    with path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        for row in rows:
            writer.writerow({k: fmt(v) for k, v in row.items()})


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: fmt(v) for k, v in row.items()})
    tmp.replace(path)


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def has_metric(row: dict[str, Any], field: str) -> bool:
    value = row.get(field)
    return value is not None and str(value) != ""


def has_coverage_metrics(row: dict[str, Any]) -> bool:
    return all(
        has_metric(row, f"{variant}_{metric}")
        for variant in ("human", "llm")
        for metric in ("line_coverage", "branch_coverage", "instruction_coverage", "method_coverage")
    )


def has_mutation_metrics(row: dict[str, Any]) -> bool:
    return all(has_metric(row, f"{variant}_mutation_score") for variant in ("human", "llm"))


def needs_resume_work(row: dict[str, Any], *, skip_coverage: bool, skip_mutation: bool) -> bool:
    if not row:
        return True
    if not skip_coverage:
        if not has_coverage_metrics(row):
            return True
    if not skip_mutation:
        if not has_mutation_metrics(row):
            return True
    return False


def merge_measurement_row(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    merged = dict(old)
    for key, value in new.items():
        if value is not None and str(value) != "":
            merged[key] = value
    for side in ("human", "llm"):
        for tool in ("coverage", "mutation"):
            if str(new.get(f"{side}_{tool}_returncode", "")) == "0":
                merged[f"{side}_{tool}_failure_category"] = ""
    if not new.get("error"):
        merged["error"] = ""
    add_comparison_fields(merged)
    backfill_failure_categories(merged)
    return merged


def backfill_failure_categories(row: dict[str, Any]) -> None:
    for side in ("human", "llm"):
        for tool in ("coverage", "mutation"):
            category_key = f"{side}_{tool}_failure_category"
            returncode = str(row.get(f"{side}_{tool}_returncode", ""))
            if returncode == "0":
                row[category_key] = ""
                continue
            if row.get(category_key) or returncode == "":
                continue
            row[category_key] = classify_tool_failure(
                str(row.get(f"{side}_{tool}_stdout_tail", "")),
                str(row.get(f"{side}_{tool}_stderr_tail", "")),
            )


def mean(values: list[float]) -> str:
    values = [v for v in values if v == v]
    return f"{sum(values) / len(values):.4f}" if values else ""


def write_summary(out_dir: Path, rows: list[dict[str, str]]) -> None:
    metrics = ("line_coverage", "branch_coverage", "instruction_coverage", "method_coverage", "mutation_score")
    by_model: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_model.setdefault(row["model"], []).append(row)

    summary_rows: list[dict[str, str]] = []
    for model, items in sorted(by_model.items()):
        row: dict[str, str] = {"model": model, "rows": str(len(items))}
        for metric in metrics:
            for variant in ("human", "llm"):
                key = f"{variant}_{metric}"
                vals = [float(x[key]) for x in items if x.get(key)]
                row[f"mean_{key}"] = mean(vals)
            diff_key = f"{metric}_diff_llm_minus_human"
            row[f"mean_{diff_key}"] = mean([float(x[diff_key]) for x in items if x.get(diff_key)])
        summary_rows.append(row)

    fieldnames = ["model", "rows"]
    for metric in metrics:
        fieldnames.extend(
            [
                f"mean_human_{metric}",
                f"mean_llm_{metric}",
                f"mean_{metric}_diff_llm_minus_human",
            ]
        )
    summary_path = out_dir / "quality_summary_by_model.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(summary_rows)

    lines = [
        "# Human vs LLM Test Quality",
        "",
        "This report compares Maven-pass LLM tests with the corresponding human tests at commit B.",
        "",
        "## Summary",
        "",
        "| model | rows | human_line | llm_line | human_branch | llm_branch | human_instruction | llm_instruction | human_method | llm_method | human_mutation | llm_mutation |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        lines.append(
            f"| {row['model']} | {row['rows']} | {row.get('mean_human_line_coverage', '')} | "
            f"{row.get('mean_llm_line_coverage', '')} | {row.get('mean_human_branch_coverage', '')} | "
            f"{row.get('mean_llm_branch_coverage', '')} | {row.get('mean_human_instruction_coverage', '')} | "
            f"{row.get('mean_llm_instruction_coverage', '')} | {row.get('mean_human_method_coverage', '')} | "
            f"{row.get('mean_llm_method_coverage', '')} | {row.get('mean_human_mutation_score', '')} | "
            f"{row.get('mean_llm_mutation_score', '')} |"
        )
    lines.append("")
    for tool in ("coverage", "mutation"):
        lines.append(f"## {tool.title()} Failure Breakdown")
        lines.append("")
        lines.append("| model | side | category | count |")
        lines.append("|---|---|---|---:|")
        for model, items in sorted(by_model.items()):
            for side in ("human", "llm"):
                counts: dict[str, int] = {}
                key = f"{side}_{tool}_failure_category"
                for item in items:
                    category = item.get(key, "")
                    if category:
                        counts[category] = counts.get(category, 0) + 1
                for category, count in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
                    lines.append(f"| {model} | {side} | {category} | {count} |")
        lines.append("")
    (out_dir / "quality_report.md").write_text("\n".join(lines), encoding="utf-8")


def fieldnames() -> list[str]:
    base = [
        "model",
        "cand_id",
        "sample_dir",
        "b",
        "subject",
        "test_path",
        "prod_path",
        "test_selector",
        "test_fqn",
        "target_fqn",
    ]
    per_variant = []
    for variant in ("human", "llm"):
        per_variant.extend(
            [
                f"{variant}_coverage_returncode",
                f"{variant}_coverage_failure_category",
                f"{variant}_line_coverage",
                f"{variant}_branch_coverage",
                f"{variant}_instruction_coverage",
                f"{variant}_method_coverage",
                f"{variant}_mutation_returncode",
                f"{variant}_mutation_failure_category",
                f"{variant}_mutation_score",
                f"{variant}_mutation_total",
                f"{variant}_mutation_detected",
                f"{variant}_mutation_status_counts",
                f"{variant}_coverage_stdout_tail",
                f"{variant}_coverage_stderr_tail",
                f"{variant}_mutation_stdout_tail",
                f"{variant}_mutation_stderr_tail",
            ]
        )
    comparisons = []
    for metric in ("line_coverage", "branch_coverage", "instruction_coverage", "method_coverage", "mutation_score"):
        comparisons.extend([f"{metric}_diff_llm_minus_human", f"{metric}_ratio_llm_to_human"])
    return base + per_variant + comparisons + ["error"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure coverage and mutation score for human vs LLM tests")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--sample-runs", type=Path, default=DEFAULT_SAMPLE_RUNS)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--mvn", type=Path, default=None, help="Maven executable path")
    parser.add_argument("--java-home", type=Path, default=None, help="JAVA_HOME with javac")
    parser.add_argument("--maven-repo-local", type=Path, default=DEFAULT_MAVEN_REPO_LOCAL)
    parser.add_argument("--model", action="append", help="只分析指定模型目录；可重复")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--skip-coverage", action="store_true")
    parser.add_argument("--skip-mutation", action="store_true")
    parser.add_argument("--coverage-timeout", type=int, default=300)
    parser.add_argument("--mutation-timeout", type=int, default=900)
    args = parser.parse_args()

    candidates = load_candidates(args.candidates)
    models = discover_models(args.sample_runs, args.model)
    mvn = resolve_mvn(args.mvn)
    java_home = resolve_java_home(args.java_home)
    out_path = args.out_dir / "quality_by_sample.csv"
    args.maven_repo_local.mkdir(parents=True, exist_ok=True)
    if not args.resume:
        for path in (
            out_path,
            args.out_dir / "quality_summary_by_model.csv",
            args.out_dir / "quality_report.md",
        ):
            path.unlink(missing_ok=True)
    existing_rows = load_existing_rows(out_path) if args.resume else {}
    updated_rows: dict[tuple[str, int], dict[str, Any]] = dict(existing_rows)
    processed = 0
    skipped = 0

    for model in models:
        model_dir = args.sample_runs / model
        for sample_dir in sorted(model_dir.glob("cand*_*")):
            cand_id = candidate_id_from_dir(sample_dir)
            if cand_id is None or cand_id < args.start or cand_id not in candidates:
                continue
            if args.limit is not None and processed >= args.limit:
                break
            if not is_maven_pass(sample_dir) or not (sample_dir / "generated.java").is_file():
                skipped += 1
                continue
            key = (model, cand_id)
            old_row = updated_rows.get(key, {})
            if args.resume and not needs_resume_work(
                old_row,
                skip_coverage=args.skip_coverage,
                skip_mutation=args.skip_mutation,
            ):
                skipped += 1
                continue
            row: dict[str, Any] = {
                "model": model,
                "cand_id": cand_id,
                "sample_dir": str(sample_dir),
            }
            run_skip_coverage = args.skip_coverage or (args.resume and has_coverage_metrics(old_row))
            run_skip_mutation = args.skip_mutation or (args.resume and has_mutation_metrics(old_row))
            print(f"[{processed + 1}] {model} cand{cand_id:03d}", flush=True)
            try:
                row.update(
                    measure_one(
                        repo=args.repo,
                        mvn=mvn,
                        java_home=java_home,
                        maven_repo_local=args.maven_repo_local,
                        sample_dir=sample_dir,
                        candidate=candidates[cand_id],
                        skip_coverage=run_skip_coverage,
                        skip_mutation=run_skip_mutation,
                        coverage_timeout=args.coverage_timeout,
                        mutation_timeout=args.mutation_timeout,
                    )
                )
            except Exception as exc:  # noqa: BLE001
                row["error"] = f"{type(exc).__name__}: {exc}"
            updated_rows[key] = merge_measurement_row(old_row, row)
            write_csv(
                out_path,
                [updated_rows[key] for key in sorted(updated_rows)],
                fieldnames(),
            )
            processed += 1
        if args.limit is not None and processed >= args.limit:
            break

    all_rows = read_rows(out_path)
    for row in all_rows:
        backfill_failure_categories(row)
    if all_rows:
        write_csv(out_path, all_rows, fieldnames())
        all_rows = read_rows(out_path)
    write_summary(args.out_dir, all_rows)
    print(f"处理样本: {processed}，跳过: {skipped}")
    print(f"逐样本质量指标: {out_path}")
    print(f"模型质量汇总: {args.out_dir / 'quality_summary_by_model.csv'}")
    print(f"报告: {args.out_dir / 'quality_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
