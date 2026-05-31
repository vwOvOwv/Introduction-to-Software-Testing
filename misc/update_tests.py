#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用的 OpenAI 兼容模型测试更新脚本。"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from misc.update_tests_utils import (
    SYSTEM_PROMPT,
    _truncate,
    build_prompt_inputs,
    build_user_message,
    chat_completion,
    load_candidates,
)


DEFAULT_CANDIDATES = ROOT / "artifacts" / "lang_sample_candidates_filtered_full_verified_pass.json"
DEFAULT_OUT_DIR = ROOT / "artifacts" / "model_tests"

DEFAULT_API_BASE = os.environ.get("MODEL_API_BASE", "")
DEFAULT_MODEL = os.environ.get("MODEL_NAME", "")
DEFAULT_API_KEY = os.environ.get("MODEL_API_KEY", "")
DEFAULT_MAX_OUTPUT = int(os.environ.get("MODEL_MAX_OUTPUT_TOKENS", "8192"))
DEFAULT_CONTEXT_WARN = int(os.environ.get("MODEL_CONTEXT_CHARS_WARN", "180000"))
DEFAULT_MAX_CHARS = int(os.environ.get("MODEL_MAX_CHARS", "0"))
DEFAULT_TIMEOUT = int(os.environ.get("MODEL_TIMEOUT_SEC", "180"))
DEFAULT_CONTINUE_ON_LENGTH = True


def default_repo_path() -> Path:
    workspace_repo = ROOT / "commons-lang"
    if (workspace_repo / ".git").is_dir():
        return workspace_repo
    return ROOT.parent / "commons-lang"


def sanitize_name(value: str) -> str:
    safe = value.strip().replace("/", "_").replace("\\", "_").replace(":", "_")
    return safe or "model"


def normalize_api_base(value: str) -> str:
    base = value.strip().rstrip("/")
    if base.endswith("/v1"):
        base = base[:-3]
    return base


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_one_update(
    repo: Path,
    a: str,
    b: str,
    test_path: str,
    prod_paths: list[str],
    title: str,
    *,
    dry_run: bool,
    api_key: str | None,
    api_base: str,
    model: str,
    dry_run_compact: bool,
) -> tuple[bool, str]:
    try:
        inputs = build_prompt_inputs(repo, a, b, test_path, prod_paths)
        prod_diff, tr_pd = _truncate(inputs["prod_diff"], DEFAULT_MAX_CHARS or None)
        prod_methods_b, tr_pm = _truncate(inputs["prod_methods_b"], DEFAULT_MAX_CHARS or None)
        test_diff, tr_td = _truncate(inputs["test_diff"], DEFAULT_MAX_CHARS or None)
        old_snip, tr_old = _truncate(inputs["old_test_snippet"], DEFAULT_MAX_CHARS or None)
        input_truncated = {
            "prod_diff": tr_pd,
            "prod_methods_b": tr_pm,
            "test_diff": tr_td,
            "old_test": tr_old,
        }

        user_msg = build_user_message(
            prod_diff=prod_diff,
            prod_methods_b=prod_methods_b,
            test_diff=test_diff,
            test_path=inputs["test_path"],
            old_test_snippet=old_snip,
            old_test_mode=inputs["old_test_mode"],
            optional_note=None,
        )

        est_tokens = (len(SYSTEM_PROMPT) + len(user_msg)) // 3
        if est_tokens * 3 > DEFAULT_CONTEXT_WARN:
            print(
                f"警告：估算输入约 {est_tokens} tokens（可能接近上下文上限）；"
                f"old_test_mode={inputs['old_test_mode']} truncated={input_truncated}",
                file=sys.stderr,
            )

        if dry_run:
            if dry_run_compact:
                print(
                    f"[dry-run] {title}: user {len(user_msg)} 字符 (~{est_tokens} tok) "
                    f"truncated={input_truncated} old_test_mode={inputs['old_test_mode']}",
                    file=sys.stderr,
                )
            else:
                print(f"\n========== {title} ==========\n")
                print("=== SYSTEM ===")
                print(SYSTEM_PROMPT)
                print("\n=== USER ===")
                print(user_msg)
            return True, f"(dry-run) {title}"

        if not (api_key or "").strip():
            return False, "未设置 MODEL_API_KEY（或未通过 --api-key 指定）"
        api_base = normalize_api_base(api_base)
        if not api_base:
            return False, "未设置 MODEL_API_BASE（或未通过 --api-base 指定）"
        if not model.strip():
            return False, "未设置 MODEL_NAME（或未通过 --model 指定）"

        print(
            f"调用模型: model={model} user_chars={len(user_msg)} old_test_mode={inputs['old_test_mode']} ({title})",
            file=sys.stderr,
        )
        content, payload = chat_completion(
            api_key=api_key.strip(),
            api_base=api_base,
            model=model.strip(),
            system=SYSTEM_PROMPT,
            user=user_msg,
            timeout_sec=DEFAULT_TIMEOUT,
            max_output_tokens=DEFAULT_MAX_OUTPUT,
            continue_on_length=DEFAULT_CONTINUE_ON_LENGTH,
        )
        fr = payload.get("_merged_finish_reason") or payload.get("choices", [{}])[0].get("finish_reason")
        usage = payload.get("usage") or {}

        safe_model = sanitize_name(model)
        out_dir = DEFAULT_OUT_DIR / safe_model
        out_dir.mkdir(parents=True, exist_ok=True)
        safe_test = test_path.replace("/", "__").replace("\\", "__")
        out_path = out_dir / f"{title.replace(' ', '_')}__{safe_test}.md"

        write_text(
            out_path,
            "# 模型输出\n\n"
            + f"- repo: `{repo}`\n"
            + f"- A: `{a}`\n"
            + f"- B: `{b}`\n"
            + f"- test: `{test_path}`\n"
            + f"- prod: `{prod_paths}`\n"
            + f"- old_test_mode: `{inputs['old_test_mode']}`\n"
            + f"- user_chars: `{len(user_msg)}`\n"
            + f"- input_truncated: `{input_truncated}`\n"
            + f"- api_base: `{api_base}`\n"
            + f"- model: `{model}`\n"
            + f"- max_output_tokens: `{DEFAULT_MAX_OUTPUT}`\n"
            + f"- finish_reason: `{fr}`\n"
            + (f"- usage: `{usage}`\n" if usage else "")
            + ("  （length 表示输出可能被截断，已尝试自动续写一轮）\n" if fr == "length" else "")
            + "\n---\n\n"
            + content,
        )
        return True, str(out_path)
    except Exception as exc:  # noqa: BLE001
        err = f"{type(exc).__name__}: {exc}"
        print(f"\n[失败] {title}\n{err}", file=sys.stderr)
        return False, err


def main() -> int:
    parser = argparse.ArgumentParser(
        description="用任意 OpenAI 兼容模型更新 JUnit 测试",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            f"候选列表默认：{DEFAULT_CANDIDATES.name}\n"
            "  python misc/update_tests.py --index 1 --dry-run\n"
            "  python misc/update_tests.py --run-all --limit 5 "
            "--api-base ... --model ... --api-key ...\n"
            "  python misc/update_tests.py --run-all --resume ..."
        ),
    )
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES, help="过滤后的候选 JSON")
    parser.add_argument("--index", type=int, default=None, help="只处理候选列表中的第 N 条（1-based）")
    parser.add_argument("--run-all", action="store_true", help="依次处理候选 JSON 中的全部条目")
    parser.add_argument("--limit", type=int, default=None, help="与 --run-all 联用：最多处理条数")
    parser.add_argument("--start", type=int, default=1, help="从候选列表第几条开始（1-based）")
    parser.add_argument("--resume", action="store_true", help="与 --run-all 联用：若 artifacts/model_tests 中已有输出则跳过")
    parser.add_argument("--api-base", default=DEFAULT_API_BASE, help="OpenAI 兼容 API Base URL")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型名")
    parser.add_argument("--api-key", default=DEFAULT_API_KEY, help="API Key")
    parser.add_argument("--dry-run", action="store_true", help="只打印用户消息，不调 API")
    args = parser.parse_args()

    if args.run_all and args.index is not None:
        print("错误：--run-all 不能与 --index 同时使用", file=sys.stderr)
        return 2

    if len(sys.argv) == 1:
        args.index = 1
        args.dry_run = True
        print(
            "提示：无参数 = 候选列表第 1 条 + --dry-run。\n"
            "      批量：python misc/update_tests.py --run-all\n"
            f"      候选文件：{args.candidates}",
            file=sys.stderr,
        )

    repo: Path = default_repo_path().resolve()
    if not (repo / ".git").is_dir():
        print("错误：找不到 commons-lang 仓库根目录", file=sys.stderr)
        return 2

    api_key = (args.api_key or "").strip() or None
    out_dir = DEFAULT_OUT_DIR

    def _run_candidate(idx: int, cand: dict) -> tuple[str, bool, str]:
        test_path = cand.get("primary_test") or cand["test_files"][0]
        prod_path = cand.get("primary_main") or cand["main_files"][0]
        pr = f" #{cand['pr_hint']}" if cand.get("pr_hint") else ""
        title = f"cand{idx:03d}{pr} {cand.get('subject', '')[:70]}"
        out_path = out_dir / sanitize_name(args.model or "model") / f"cand{idx:03d}_{cand['b'][:12]}__{test_path.replace('/', '__')}.md"
        if args.resume and out_path.is_file() and not args.dry_run:
            return title, True, str(out_path)
        compact = args.dry_run
        ok, msg = run_one_update(
            repo,
            cand["a"],
            cand["b"],
            test_path,
            [prod_path],
            title,
            dry_run=args.dry_run,
            api_key=api_key,
            api_base=args.api_base,
            model=args.model,
            dry_run_compact=compact,
        )
        return title, ok, msg

    if args.run_all or args.index is not None:
        try:
            all_cands = load_candidates(args.candidates.resolve())
        except (FileNotFoundError, ValueError) as exc:
            print(f"错误：{exc}", file=sys.stderr)
            return 2
        print(f"已加载候选 {len(all_cands)} 条 ← {args.candidates.name}", file=sys.stderr)

    if args.run_all:
        if not args.dry_run and not api_key:
            print("错误：--run-all 且非 --dry-run 时需通过 --api-key 或 MODEL_API_KEY 设置 API Key", file=sys.stderr)
            return 2
        results: list[tuple[str, bool, str]] = []
        processed = 0
        for idx, cand in enumerate(all_cands, start=1):
            if idx < args.start:
                continue
            if args.limit is not None and processed >= args.limit:
                break
            title, ok, msg = _run_candidate(idx, cand)
            results.append((title, ok, msg))
            processed += 1
            if ok and not args.dry_run:
                print(msg)

        print("\n========== 汇总 ==========", file=sys.stderr)
        n_ok = sum(1 for _t, ok, _m in results if ok)
        for title, ok, msg in results:
            mark = "OK  " if ok else "FAIL"
            print(f"  [{mark}] {title}", file=sys.stderr)
            if not ok:
                print(f"        {(msg or '').split(chr(10), 1)[0][:500]}", file=sys.stderr)
        print(f"  成功 {n_ok} / {len(results)}", file=sys.stderr)
        return 0 if n_ok == len(results) else 1

    if args.index is not None:
        if not (1 <= args.index <= len(all_cands)):
            print(f"错误：--index 须在 1..{len(all_cands)}", file=sys.stderr)
            return 2
        cand = all_cands[args.index - 1]
        title, ok, msg = _run_candidate(args.index, cand)
        if not ok:
            print(msg, file=sys.stderr)
            return 1
        if not args.dry_run:
            print(msg)
        return 0

    print(
        "错误：请指定 --index N 或 --run-all。\n"
        f"  候选文件：{args.candidates}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
