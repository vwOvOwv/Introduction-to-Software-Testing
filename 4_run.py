#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量实验：用通用 OpenAI 兼容模型生成测试，然后合并并跑 Maven。"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def default_repo_path() -> Path:
    workspace_repo = ROOT / "commons-lang"
    if (workspace_repo / ".git").is_dir():
        return workspace_repo
    return ROOT.parent / "commons-lang"


REPO = default_repo_path()
ARTIFACTS = ROOT / "artifacts" / "sample_runs"
DEFAULT_CANDIDATES = ROOT / "artifacts" / "lang_sample_candidates_filtered_full_verified_pass.json"
UPDATE_SCRIPT = ROOT / "misc" / "update_tests.py"
RUN_SCRIPT = ROOT / "misc" / "run_single_maven_test.py"


def sanitize_name(value: str) -> str:
    safe = value.strip().replace("/", "_").replace("\\", "_").replace(":", "_")
    return safe or "model"


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(ROOT),
        env=os.environ.copy(),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )


def git_show(repo: Path, revision: str, relpath: str) -> str:
    result = run_command(["git", "-C", str(repo), "show", f"{revision}:{relpath}"])
    if result.returncode != 0:
        raise RuntimeError(f"git show 失败: {relpath}\nstderr:\n{result.stderr.strip()}")
    return result.stdout


def extract_maven_run_report(report: dict[str, object]) -> dict[str, object]:
    maven = report.get("maven")
    if isinstance(maven, dict):
        return maven
    command_history = report.get("command_history")
    if isinstance(command_history, list):
        for item in command_history:
            if isinstance(item, dict) and item.get("name") == "maven":
                return item
    return {}


def extract_setup_error(report: dict[str, object]) -> str | None:
    value = report.get("setup_error")
    return value if isinstance(value, str) and value else None


def test_selector_from_path(test_path: str) -> str:
    return Path(test_path.replace("\\", "/")).stem


def load_verified_pass_b_hashes(report_path: Path) -> set[str]:
    if not report_path.is_file():
        return set()
    data = json.loads(report_path.read_text(encoding="utf-8"))
    out: set[str] = set()
    for b, rec in (data.get("results") or {}).items():
        if rec.get("status") == "pass":
            out.add(b)
    return out


def candidates_to_samples(
    candidates: list[dict],
    *,
    only_pass_b: set[str] | None,
    start: int,
    limit: int | None,
) -> list[dict]:
    samples: list[dict] = []
    for idx, c in enumerate(candidates, start=1):
        if idx < start:
            continue
        b = c["b"]
        if only_pass_b is not None and b not in only_pass_b:
            continue
        test_path = c.get("primary_test") or c["test_files"][0]
        prod_path = c.get("primary_main") or c["main_files"][0]
        selector = test_selector_from_path(test_path)
        samples.append(
            {
                "id": idx,
                "b_short": b[:12],
                "a": c["a"],
                "b": b,
                "prod": prod_path,
                "target_test": test_path,
                "input_test": test_path,
                "selector": selector,
                "pr_hint": c.get("pr_hint"),
                "subject": c.get("subject", ""),
            }
        )
        if limit is not None and len(samples) >= limit:
            break
    return samples


def sample_run_dir(sample: dict, model: str) -> Path:
    return ARTIFACTS / sanitize_name(model) / f"cand{sample['id']:03d}_{sample['b_short']}"


def parse_model_output_path(stdout: str) -> Path | None:
    for line in reversed([line.strip() for line in stdout.splitlines() if line.strip()]):
        p = Path(line)
        if p.is_file():
            return p
    return None


def build_generated_java_from_markdown(
    markdown_text: str,
    *,
    repo: Path,
    a: str,
    b: str,
    test_path: str,
) -> str:
    from misc.update_tests_utils import (
        _git_show,
        _looks_like_full_test_class,
        extract_java_from_markdown,
        finalize_merged_test_class,
        merge_patch_into_test_class,
    )

    patch = extract_java_from_markdown(markdown_text)

    base = _git_show(repo, a, test_path)
    if _looks_like_full_test_class(patch, expected_class_name=test_selector_from_path(test_path)):
        merged = patch.strip() + "\n"
    else:
        merged = merge_patch_into_test_class(base, patch)
    reference = _git_show(repo, b, test_path)
    return finalize_merged_test_class(merged, reference_source=reference)


def process_sample(
    sample: dict,
    *,
    resume: bool,
    skip_maven: bool,
    api_base: str,
    model: str,
    api_key: str,
) -> dict[str, object]:
    sample_dir = sample_run_dir(sample, model)
    sample_dir.mkdir(parents=True, exist_ok=True)
    raw_md = sample_dir / "raw.md"
    old_test_java = sample_dir / "old_test.java"
    generated_java = sample_dir / "generated.java"
    run_report = sample_dir / "run_report.json"

    entry: dict[str, object] = dict(sample)
    entry["sample_dir"] = str(sample_dir)
    old_test_java.write_text(git_show(REPO, str(sample["a"]), str(sample["input_test"])), encoding="utf-8")
    entry["old_test_extracted"] = True
    entry["old_test_path"] = str(old_test_java)

    if raw_md.is_file() and not resume:
        raw_md.unlink()

    if not raw_md.is_file():
        update_cmd = [
            sys.executable,
            str(UPDATE_SCRIPT),
            "--index",
            str(sample["id"]),
            "--candidates",
            str(DEFAULT_CANDIDATES),
            "--api-base",
            api_base,
            "--model",
            model,
            "--api-key",
            api_key,
        ]
        update_result = run_command(update_cmd)
        entry["update_exit_code"] = update_result.returncode
        entry["update_stdout_tail"] = update_result.stdout[-2000:]
        entry["update_stderr_tail"] = update_result.stderr[-4000:]
        if update_result.returncode != 0:
            entry["generated"] = False
            run_report.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            return entry
        model_md = parse_model_output_path(update_result.stdout)
        if model_md is None:
            entry["generated"] = False
            entry["processing_error"] = "无法从模型脚本输出中定位结果文件"
            run_report.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            return entry
        raw_md.write_text(model_md.read_text(encoding="utf-8"), encoding="utf-8")
        entry["raw_md"] = str(raw_md)
        entry["model_output"] = str(model_md)
    else:
        entry["raw_md"] = str(raw_md)
        entry["model_output"] = str(raw_md)

    if not generated_java.is_file() or not resume:
        generated_java.write_text(
            build_generated_java_from_markdown(
                raw_md.read_text(encoding="utf-8"),
                repo=REPO,
                a=str(sample["a"]),
                b=str(sample["b"]),
                test_path=str(sample["input_test"]),
            ),
            encoding="utf-8",
        )
    entry["generated"] = True
    entry["generated_java"] = str(generated_java)
    entry["generated_class_name_present"] = str(sample["selector"]) in generated_java.read_text(encoding="utf-8")

    if skip_maven:
        entry["run_skipped"] = True
        run_report.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return entry

    if resume and run_report.is_file():
        entry["run_skipped"] = True
        entry["run_report"] = str(run_report)
        entry["run_report_exists"] = True
        payload = json.loads(run_report.read_text(encoding="utf-8"))
        maven = extract_maven_run_report(payload)
        entry["maven_returncode"] = maven.get("returncode")
        entry["maven_stdout_tail"] = (maven.get("stdout") or "")[-2000:]
        entry["maven_stderr_tail"] = (maven.get("stderr") or "")[-3000:]
        return entry

    run_test_command = [
        sys.executable,
        str(RUN_SCRIPT),
        "--repo",
        str(REPO),
        "--ref",
        str(sample["b"]),
        "--target-test-path",
        str(sample["target_test"]),
        "--replacement-test-file",
        str(generated_java),
        "--test-selector",
        str(sample["selector"]),
        "--report-file",
        str(run_report),
        "--maven-arg=-q",
    ]
    run_result = run_command(run_test_command)
    entry["run_exit_code"] = run_result.returncode
    entry["run_stdout_tail"] = run_result.stdout[-2000:]
    entry["run_stderr_tail"] = run_result.stderr[-4000:]
    entry["run_report"] = str(run_report)
    entry["run_report_exists"] = run_report.is_file()

    if run_report.is_file():
        payload = json.loads(run_report.read_text(encoding="utf-8"))
        maven = extract_maven_run_report(payload)
        entry["maven_returncode"] = maven.get("returncode")
        entry["maven_stdout_tail"] = (maven.get("stdout") or "")[-2000:]
        entry["maven_stderr_tail"] = (maven.get("stderr") or "")[-3000:]
        setup_error = extract_setup_error(payload)
        if setup_error:
            entry["run_setup_error"] = setup_error

    run_report.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return entry


def print_summary(summary: list[dict[str, object]]) -> None:
    n_gen = sum(1 for e in summary if e.get("generated"))
    n_maven_ok = sum(1 for e in summary if e.get("maven_returncode") == 0)
    n_fail_gen = sum(1 for e in summary if e.get("generated") is False)
    n_proc_err = sum(1 for e in summary if e.get("processing_error"))
    n_setup_err = sum(1 for e in summary if e.get("run_setup_error"))
    n_fail_mvn = sum(
        1
        for e in summary
        if e.get("generated") and not e.get("run_skipped") and e.get("maven_returncode") not in (0, None)
    )
    print("\n========== 实验汇总 ==========", file=sys.stderr)
    print(f"  处理条数: {len(summary)}", file=sys.stderr)
    print(f"  模型生成成功: {n_gen}", file=sys.stderr)
    print(f"  生成失败: {n_fail_gen}", file=sys.stderr)
    if n_proc_err:
        print(f"  合并/处理异常: {n_proc_err}", file=sys.stderr)
    if n_setup_err:
        print(f"  Maven 启动异常: {n_setup_err}", file=sys.stderr)
    print(f"  Maven returncode=0: {n_maven_ok}", file=sys.stderr)
    print(f"  Maven 非 0（已生成）: {n_fail_mvn}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="批量模型改测试 + Maven 验证")
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES, help=f"候选 JSON（默认 {DEFAULT_CANDIDATES.name}）")
    parser.add_argument("--verify-report", type=Path, default=ROOT / "artifacts" / "lang_sample_verify_report_full_jdk8.json")
    parser.add_argument("--only-verified-pass", action="store_true", help="仅处理 verify 报告中 status=pass 的 B")
    parser.add_argument("--limit", type=int, default=None, help="最多处理多少条")
    parser.add_argument("--start", type=int, default=1, help="从候选列表第几条开始（1-based）")
    parser.add_argument("--resume", action="store_true", help="跳过已有 raw.md / generated.java / run_report 的步骤")
    parser.add_argument("--skip-maven", action="store_true", help="只调模型，不跑 Maven")
    parser.add_argument("--api-base", required=True, help="OpenAI 兼容 API Base URL")
    parser.add_argument("--model", required=True, help="模型名")
    parser.add_argument("--api-key", required=True, help="API Key")
    args = parser.parse_args()

    if not args.candidates.is_file():
        print(f"错误：找不到 {args.candidates}", file=sys.stderr)
        return 2

    payload = json.loads(args.candidates.read_text(encoding="utf-8"))
    candidates: list[dict] = payload.get("candidates", [])
    only_pass: set[str] | None = None
    if args.only_verified_pass:
        only_pass = load_verified_pass_b_hashes(args.verify_report)
        print(f"仅 verified pass: {len(only_pass)} 条（报告 {args.verify_report}）", file=sys.stderr)

    samples = candidates_to_samples(candidates, only_pass_b=only_pass, start=args.start, limit=args.limit)
    print(f"待处理样本: {len(samples)} 条（来源 {args.candidates.name}）", file=sys.stderr)

    output_root = ARTIFACTS / sanitize_name(args.model)
    output_root.mkdir(parents=True, exist_ok=True)
    print(f"输出目录: {output_root}", file=sys.stderr)
    summary: list[dict[str, object]] = []
    n_errors = 0

    for i, sample in enumerate(samples, 1):
        pr = f" PR#{sample['pr_hint']}" if sample.get("pr_hint") else ""
        print(
            f"[{i}/{len(samples)}] cand{sample['id']:03d}{pr}  {sample['selector']}  B={sample['b'][:12]}",
            file=sys.stderr,
            flush=True,
        )
        try:
            entry = process_sample(
                sample,
                resume=args.resume,
                skip_maven=args.skip_maven,
                api_base=args.api_base,
                model=args.model,
                api_key=args.api_key,
            )
        except Exception as exc:  # noqa: BLE001
            n_errors += 1
            entry = dict(sample)
            entry["sample_dir"] = str(sample_run_dir(sample, args.model))
            entry["generated"] = False
            entry["processing_error"] = f"{type(exc).__name__}: {exc}"
            print(f"  本条异常（已跳过，继续下一条）: {exc}", file=sys.stderr, flush=True)
        summary.append(entry)

    print_summary(summary)
    if n_errors:
        print(f"  处理异常条数: {n_errors}", file=sys.stderr)
    return 1 if n_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
