#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量实验：对候选样本调用 update_tests_deepseek.py，再 run_single_maven_test.py 验证。

默认从 artifacts/lang_sample_candidates_filtered.json 读取 137 条（严格配对、已清洗）。
可选仅跑 Maven 验证报告中 status=pass 的条目（--only-verified-pass）。

用法：
  set DEEPSEEK_API_KEY=sk-...
  python run_sample_experiment.py
  python run_sample_experiment.py --limit 5
  python run_sample_experiment.py --resume
  python run_sample_experiment.py --resync-generated
  python run_sample_experiment.py --only-verified-pass
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent / "commons-lang"
ARTIFACTS = ROOT / "artifacts" / "sample_runs"
DEFAULT_CANDIDATES = ROOT / "artifacts" / "lang_sample_candidates_filtered.json"
DEFAULT_VERIFY_REPORT = ROOT / "artifacts" / "lang_sample_verify_report.json"
UPDATE_SCRIPT = ROOT / "update_tests_deepseek.py"
RUN_SCRIPT = ROOT / "run_single_maven_test.py"

DEFAULT_NOTE_TEMPLATE = (
    "只输出需要修改的 @Test / @ParameterizedTest 方法的完整方法体（含注解），"
    "不要输出整个测试类（除非该类极短）。保持类名 {selector} 与原有 package 不变。"
    "对照生产代码 diff 与测试 diff 调整断言。"
)


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    return subprocess.run(
        command,
        cwd=str(ROOT),
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )


def extract_java(markdown_text: str) -> str:
    fenced = re.findall(r"```(?:java)?\s*(.*?)```", markdown_text, flags=re.DOTALL)
    if fenced:
        return "\n\n".join(block.strip() for block in fenced) + "\n"
    marker = "\n---\n\n"
    body = markdown_text.split(marker, 1)[1] if marker in markdown_text else markdown_text
    return body.strip() + "\n"


def build_generated_java(
    markdown_text: str,
    *,
    repo: Path,
    a: str,
    b: str,
    test_path: str,
    sync_from_b: bool = True,
) -> str:
    """从 DeepSeek 回复得到可编译的完整测试类（方法级输出会合并进 A 上旧类）。"""
    from update_tests_deepseek import _git_show, finalize_merged_test_class, merge_patch_into_test_class

    patch = extract_java(markdown_text)
    if re.search(r"\bclass\s+[A-Za-z_]\w*", patch):
        merged = patch.strip() + "\n"
    else:
        base = _git_show(repo, a, test_path)
        merged = merge_patch_into_test_class(base, patch)
    if sync_from_b:
        reference = _git_show(repo, b, test_path)
        merged = finalize_merged_test_class(merged, reference_source=reference)
    return merged


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
        title = (c.get("subject") or "")[:120]
        samples.append(
            {
                "id": idx,
                "b_short": b[:12],
                "title": title,
                "a": c["a"],
                "b": b,
                "prod": prod_path,
                "target_test": test_path,
                "input_test": test_path,
                "selector": selector,
                "pr_hint": c.get("pr_hint"),
                "note": DEFAULT_NOTE_TEMPLATE.format(selector=selector),
            }
        )
        if limit is not None and len(samples) >= limit:
            break
    return samples


def sample_run_dir(sample: dict) -> Path:
    """cand001_<b_short>，避免仅用序号时与不同批次混淆。"""
    return ARTIFACTS / f"cand{sample['id']:03d}_{sample['b_short']}"


def process_sample(
    sample: dict,
    *,
    resume: bool,
    skip_maven: bool,
    resync_generated: bool = False,
) -> dict[str, object]:
    sample_dir = sample_run_dir(sample)
    sample_dir.mkdir(parents=True, exist_ok=True)
    deepseek_md = sample_dir / "deepseek_output.md"
    generated_java = sample_dir / "generated.java"
    run_report = sample_dir / "run_report.json"

    entry: dict[str, object] = dict(sample)
    entry["sample_dir"] = str(sample_dir)

    if resync_generated and deepseek_md.is_file():
        generated_java.write_text(
            build_generated_java(
                deepseek_md.read_text(encoding="utf-8"),
                repo=REPO,
                a=str(sample["a"]),
                b=str(sample["b"]),
                test_path=str(sample["input_test"]),
            ),
            encoding="utf-8",
        )
        entry["resync_generated"] = True
        entry["generated"] = True
        entry["generated_java"] = str(generated_java)
        java_source = generated_java.read_text(encoding="utf-8")
        entry["generated_class_name_present"] = str(sample["selector"]) in java_source
    elif resume and deepseek_md.is_file() and generated_java.is_file():
        entry["update_skipped"] = True
        entry["generated"] = True
        entry["generated_java"] = str(generated_java)
        java_source = generated_java.read_text(encoding="utf-8")
        entry["generated_class_name_present"] = str(sample["selector"]) in java_source
    else:
        update_command = [
            sys.executable,
            str(UPDATE_SCRIPT),
            "--repo",
            str(REPO),
            "--a",
            str(sample["a"]),
            "--b",
            str(sample["b"]),
            "--test",
            str(sample["input_test"]),
            "--prod",
            str(sample["prod"]),
            "--out",
            str(deepseek_md),
            "--note",
            str(sample["note"]),
        ]
        update_result = run_command(update_command)
        entry["update_exit_code"] = update_result.returncode
        entry["update_stdout_tail"] = update_result.stdout[-2000:]
        entry["update_stderr_tail"] = update_result.stderr[-4000:]

        if update_result.returncode != 0 or not deepseek_md.is_file():
            entry["generated"] = False
            return entry

        generated_java.write_text(
            build_generated_java(
                deepseek_md.read_text(encoding="utf-8"),
                repo=REPO,
                a=str(sample["a"]),
                b=str(sample["b"]),
                test_path=str(sample["input_test"]),
            ),
            encoding="utf-8",
        )
        java_source = generated_java.read_text(encoding="utf-8")
        entry["generated"] = True
        entry["generated_java"] = str(generated_java)
        entry["generated_class_name_present"] = str(sample["selector"]) in java_source

    if skip_maven:
        entry["run_skipped"] = True
        return entry

    if resume and run_report.is_file() and not resync_generated:
        entry["run_skipped"] = True
        entry["run_report"] = str(run_report)
        entry["run_report_exists"] = True
        payload = json.loads(run_report.read_text(encoding="utf-8"))
        maven = payload.get("maven") or {}
        entry["maven_returncode"] = maven.get("returncode")
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
        maven = payload.get("maven") or {}
        entry["maven_returncode"] = maven.get("returncode")
        entry["maven_stdout_tail"] = maven.get("stdout", "")[-2000:]
        entry["maven_stderr_tail"] = maven.get("stderr", "")[-3000:]

    return entry


def print_summary(summary: list[dict[str, object]]) -> None:
    n_gen = sum(1 for e in summary if e.get("generated"))
    n_maven_ok = sum(1 for e in summary if e.get("maven_returncode") == 0)
    n_fail_gen = sum(1 for e in summary if e.get("generated") is False)
    n_proc_err = sum(1 for e in summary if e.get("processing_error"))
    n_fail_mvn = sum(
        1
        for e in summary
        if e.get("generated") and not e.get("run_skipped") and e.get("maven_returncode") not in (0, None)
    )
    print("\n========== 实验汇总 ==========", file=sys.stderr)
    print(f"  处理条数: {len(summary)}", file=sys.stderr)
    print(f"  DeepSeek 生成成功: {n_gen}", file=sys.stderr)
    print(f"  生成失败: {n_fail_gen}", file=sys.stderr)
    if n_proc_err:
        print(f"  合并/处理异常: {n_proc_err}", file=sys.stderr)
    print(f"  Maven returncode=0: {n_maven_ok}", file=sys.stderr)
    print(f"  Maven 非 0（已生成）: {n_fail_mvn}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="批量 DeepSeek 改测试 + Maven 验证")
    parser.add_argument(
        "--candidates",
        type=Path,
        default=DEFAULT_CANDIDATES,
        help=f"过滤后的候选 JSON（默认 {DEFAULT_CANDIDATES.name}）",
    )
    parser.add_argument(
        "--only-verified-pass",
        action="store_true",
        help="仅处理 verify_lang_candidates 报告中 status=pass 的 B",
    )
    parser.add_argument("--verify-report", type=Path, default=DEFAULT_VERIFY_REPORT)
    parser.add_argument("--limit", type=int, default=None, help="最多处理多少条")
    parser.add_argument("--start", type=int, default=1, help="从候选列表第几条开始（1-based）")
    parser.add_argument("--resume", action="store_true", help="跳过已有 deepseek_output / run_report 的步骤")
    parser.add_argument(
        "--resync-generated",
        action="store_true",
        help="用已有 deepseek_output.md 按当前规则重生成 generated.java 并重跑 Maven（不调 API）",
    )
    parser.add_argument("--skip-maven", action="store_true", help="只调 DeepSeek，不跑 Maven")
    parser.add_argument(
        "--output-summary",
        type=Path,
        default=ARTIFACTS / "summary.json",
        help="汇总 JSON 路径",
    )
    args = parser.parse_args()

    if not os.environ.get("DEEPSEEK_API_KEY", "").strip():
        print("错误：请设置环境变量 DEEPSEEK_API_KEY", file=sys.stderr)
        return 2

    if not args.candidates.is_file():
        print(f"错误：找不到 {args.candidates}", file=sys.stderr)
        return 2
    payload = json.loads(args.candidates.read_text(encoding="utf-8"))
    candidates: list[dict] = payload.get("candidates", [])
    only_pass: set[str] | None = None
    if args.only_verified_pass:
        only_pass = load_verified_pass_b_hashes(args.verify_report)
        print(f"仅 verified pass: {len(only_pass)} 条（报告 {args.verify_report}）", file=sys.stderr)
    samples = candidates_to_samples(
        candidates,
        only_pass_b=only_pass,
        start=args.start,
        limit=args.limit,
    )
    print(f"待处理样本: {len(samples)} 条（来源 {args.candidates.name}）", file=sys.stderr)

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    summary: list[dict[str, object]] = []
    args.output_summary.parent.mkdir(parents=True, exist_ok=True)
    n_errors = 0

    def write_summary() -> None:
        args.output_summary.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

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
                resync_generated=args.resync_generated,
            )
        except Exception as exc:  # noqa: BLE001
            n_errors += 1
            entry = dict(sample)
            entry["sample_dir"] = str(sample_run_dir(sample))
            entry["generated"] = False
            entry["processing_error"] = f"{type(exc).__name__}: {exc}"
            print(f"  本条异常（已跳过，继续下一条）: {exc}", file=sys.stderr, flush=True)
        summary.append(entry)
        write_summary()

    print_summary(summary)
    if n_errors:
        print(f"  处理异常条数: {n_errors}", file=sys.stderr)
    print(args.output_summary, file=sys.stdout)
    return 1 if n_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
