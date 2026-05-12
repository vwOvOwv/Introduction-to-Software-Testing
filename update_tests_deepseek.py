#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 git 取「B 上生产代码 + A 上旧测试」，调用 DeepSeek（OpenAI 兼容接口）生成更新后的测试。

依赖：仅标准库。需设置环境变量 DEEPSEEK_API_KEY。

示例（在 final_homework 目录下，--repo 默认同级 commons-lang，可省略）：
  # 不传任何参数 = 默认「--sample 1 --dry-run」（只打印 prompt，不调 API）
  python update_tests_deepseek.py

  set DEEPSEEK_API_KEY=sk-...
  python update_tests_deepseek.py --sample 1

  python update_tests_deepseek.py --repo commons-lang ^
    --a 4b09471db039085a3114f79ece97ca7fd9bd6f1e ^
    --b 864dd6ea887fd394f15e3b55203d6f52f717373b ^
    --test src/test/java/org/apache/commons/lang3/ValidateDoublesTest.java ^
    --prod src/main/java/org/apache/commons/lang3/Validate.java
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import traceback
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# DeepSeek OpenAI 兼容接口
# ---------------------------------------------------------------------------
DEFAULT_API_BASE = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"
# 脚本位于 final_homework/ 时，默认同目录下的 commons-lang 克隆
_DEFAULT_REPO = Path(__file__).resolve().parent / "commons-lang"

SYSTEM_PROMPT = """你是一位资深的 Java 单元测试专家，擅长使用 JUnit 5 和 Mockito。
任务：给定一个代码变更（git diff 或变更后的方法实现）以及一个针对旧版本代码编写的 JUnit 测试方法（该测试在旧版本上通过，但在新版本上会失败），请你更新这个测试方法，使其能够在新版本代码上编译通过并成功运行（断言通过）。
输出：请只给出「修改后的完整测试类」Java 源码（保持原有包名与类名），必要时可简短说明关键断言改动；不要输出与代码无关的寒暄。"""


@dataclass(frozen=True)
class Sample:
    id: int
    title: str
    a: str
    b: str
    prod: str  # repo-relative path
    test: str  # repo-relative path


# 与 samples.md 中总表一致（路径相对于 commons-lang 仓库根目录）
# 注意：测试路径在提交 A 的 tree 中必须已存在（不能选「仅在 B 新建测试文件」的 PR，否则 git show A:... 失败）。
PRESET_SAMPLES: list[Sample] = [
    Sample(1, "LANG-1816 ArrayUtils NaN (#1589)", "9bca5d09c6d16a5524a3cd1d38305687ad7fdca4", "52c06bea2f2b6c277c517dc9f5bb0d62d17e073c",
           "src/main/java/org/apache/commons/lang3/ArrayUtils.java",
           "src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java"),
    Sample(2, "TimedSemaphore shutdown", "58ba515e4b083f658ef2087df36284a9cd539b31", "5914a8e80a547301b76bf8ef691053e4dfc901a7",
           "src/main/java/org/apache/commons/lang3/concurrent/TimedSemaphore.java",
           "src/test/java/org/apache/commons/lang3/concurrent/TimedSemaphoreTest.java"),
    Sample(3, "RandomStringUtils.random fixes", "e63927afd575ba22f41a1d5b23b2d85745e82d24", "313d877d57abefdbb1ad0c42781bf719b83d5a35",
           "src/main/java/org/apache/commons/lang3/RandomStringUtils.java",
           "src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java"),
    Sample(4, "LANG-1823 LocaleUtils '#' (#1630)", "0745c26dac9ac76086f10c302d252a71bf4a68c5", "3df7f4440e7447bc55e95400ec511323e708c652",
           "src/main/java/org/apache/commons/lang3/LocaleUtils.java",
           "src/test/java/org/apache/commons/lang3/LocaleUtilsTest.java"),
    Sample(5, "NumberUtils.createNumber", "1dd7cb14c233140a8e76ba5441b6360a239a98dc", "5904c573ffacaa5d8836ffc2b346f400c8901ed1",
           "src/main/java/org/apache/commons/lang3/math/NumberUtils.java",
           "src/test/java/org/apache/commons/lang3/math/NumberUtilsTest.java"),
    Sample(6, "ArchUtils ppc64le (#1625)", "23a730b8ed392ba424cc275df793dcae88f4cebe", "bb675e1127adb7f7c8d8687667bc11779d8e75eb",
           "src/main/java/org/apache/commons/lang3/ArchUtils.java",
           "src/test/java/org/apache/commons/lang3/ArchUtilsTest.java"),
]


def _git_show(repo: Path, revision: str, relpath: str) -> str:
    relpath = relpath.replace("\\", "/")
    cmd = ["git", "-C", str(repo), "show", f"{revision}:{relpath}"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(
            f"git show 失败: {' '.join(cmd)}\nstderr:\n{p.stderr.strip()}\n"
            "提示：若提示 path 在 A 中不存在，说明该 PR 的测试类是 B 上新建的，"
            "不能作为「A 旧测试」；请换 --sample 或换 --test 为在 A 已存在的测试文件。"
        )
    return p.stdout


def _git_diff(repo: Path, a: str, b: str, paths: list[str]) -> str:
    cmd = ["git", "-C", str(repo), "diff", f"{a}..{b}", "--", *paths]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"git diff 失败: {' '.join(cmd)}\n{p.stderr.strip()}")
    return p.stdout


def _truncate(text: str, max_chars: int | None) -> tuple[str, bool]:
    if max_chars is None or len(text) <= max_chars:
        return text, False
    head = max_chars // 2
    tail = max_chars - head
    omitted = len(text) - head - tail
    merged = (
        text[:head]
        + f"\n\n... [省略 {omitted} 字符，可用 --max-chars 调大] ...\n\n"
        + text[-tail:]
    )
    return merged, True


def build_user_message(
    *,
    prod_after: str,
    old_test: str,
    diff_summary: str,
    optional_note: str | None,
) -> str:
    parts = [
        "输入：",
        "",
        "1. 变更后的生产代码（来自新版本提交 B）：",
        "```java",
        prod_after.rstrip(),
        "```",
        "",
        "2. 旧测试代码（来自旧版本提交 A，在新版本上会失败）：",
        "```java",
        old_test.rstrip(),
        "```",
        "",
        "3. 代码变更说明（git diff A..B，仅相关生产文件）：",
        "```diff",
        diff_summary.rstrip() if diff_summary.strip() else "(无 diff 输出)",
        "```",
    ]
    if optional_note:
        parts.extend(["", "4. 补充说明（人工）：", optional_note.strip()])
    return "\n".join(parts)


def deepseek_chat(
    *,
    api_key: str,
    api_base: str,
    model: str,
    system: str,
    user: str,
    timeout_sec: int = 120,
) -> tuple[str, dict[str, Any]]:
    url = api_base.rstrip("/") + "/v1/chat/completions"
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
    }
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {err_body}") from e
    payload = json.loads(raw)
    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"无法解析响应 JSON: {raw[:2000]}") from e
    return content, payload


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
    max_chars: int,
    note: str | None,
    timeout: int,
    out: Path | None,
    dry_run_compact: bool,
    verbose: bool,
) -> tuple[bool, str]:
    """
    执行单次「取 git → 拼 prompt → dry-run 或调 API → 写文件」。
    返回 (成功, 说明)：成功时说明为输出文件路径；失败时为错误摘要（单行优先）。
    """
    try:
        old_test = _git_show(repo, a, test_path)
        prod_chunks: list[str] = []
        for p in prod_paths:
            prod_chunks.append(f"===== 文件: {p} (提交 {b}) =====\n" + _git_show(repo, b, p))
        prod_after = "\n\n".join(prod_chunks)
        diff_summary = _git_diff(repo, a, b, prod_paths)

        prod_after, _ = _truncate(prod_after, max_chars)
        old_test, _ = _truncate(old_test, max_chars)
        diff_summary, _ = _truncate(diff_summary, max_chars)

        user_msg = build_user_message(
            prod_after=prod_after,
            old_test=old_test,
            diff_summary=diff_summary,
            optional_note=note,
        )

        if dry_run:
            if dry_run_compact:
                print(
                    f"[dry-run] {title}: 已构造 prompt，user 长度 {len(user_msg)} 字符",
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
            return False, "未设置 DEEPSEEK_API_KEY"

        print(f"调用 DeepSeek: model={model} base={api_base} ({title})", file=sys.stderr)
        content, _payload = deepseek_chat(
            api_key=api_key.strip(),
            api_base=api_base,
            model=model,
            system=SYSTEM_PROMPT,
            user=user_msg,
            timeout_sec=timeout,
        )

        out_path = out
        if out_path is None:
            out_dir = repo.parent / "artifacts" / "deepseek_tests"
            out_dir.mkdir(parents=True, exist_ok=True)
            safe = test_path.replace("/", "__").replace("\\", "__")
            out_path = out_dir / f"{title.replace(' ', '_')}__{safe}.md"

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            "# DeepSeek 输出\n\n"
            + f"- repo: `{repo}`\n"
            + f"- A: `{a}`\n"
            + f"- B: `{b}`\n"
            + f"- test: `{test_path}`\n"
            + f"- prod: `{prod_paths}`\n\n"
            + "---\n\n"
            + content,
            encoding="utf-8",
        )
        return True, str(out_path)
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
        print(f"\n[失败] {title}\n{err}", file=sys.stderr)
        if verbose:
            traceback.print_exc(file=sys.stderr)
        return False, err


def main() -> int:
    parser = argparse.ArgumentParser(
        description="用 DeepSeek 根据 A/B 提交更新 JUnit 测试（commons-lang 预设样本）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "最简调用（仓库在 final_homework/commons-lang）：\n"
            "  python update_tests_deepseek.py\n"
            "    （无参数 = 默认 --sample 1 --dry-run，仅打印 prompt）\n"
            "  python update_tests_deepseek.py --sample 1 --dry-run\n"
            "  python update_tests_deepseek.py --sample 1\n"
            "  python update_tests_deepseek.py --run-all\n"
            "    （依次跑样本 1–6；失败跳过继续；非 dry-run 需 DEEPSEEK_API_KEY）\n"
            "  python update_tests_deepseek.py --run-all --dry-run\n"
            "  python update_tests_deepseek.py --run-all --dry-run --verbose\n"
            f"默认 --repo：{_DEFAULT_REPO}"
        ),
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=_DEFAULT_REPO,
        help=f"commons-lang 仓库根目录（默认：{_DEFAULT_REPO}）",
    )
    parser.add_argument("--sample", type=int, choices=range(1, 7), help="使用 samples.md 中的预设样本编号 1–6")
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="依次运行预设样本 1–6；单条失败打印错误后继续下一条，最后输出汇总",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="与 --run-all 联用：失败时打印完整 traceback；--run-all --dry-run 时打印每条完整 prompt",
    )
    parser.add_argument("--a", help="旧提交 A（与 --b/--test/--prod 联用）")
    parser.add_argument("--b", help="新提交 B")
    parser.add_argument("--test", help="测试文件在仓库中的相对路径，如 src/test/java/.../FooTest.java")
    parser.add_argument("--prod", action="append", help="生产代码相对路径，可多次指定；与 --sample 互斥时必填")
    parser.add_argument("--note", default=None, help="可选：人工补充说明，写入用户消息")
    parser.add_argument("--api-base", default=os.environ.get("DEEPSEEK_API_BASE", DEFAULT_API_BASE))
    parser.add_argument("--model", default=os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL))
    parser.add_argument("--max-chars", type=int, default=120_000, help="对过长正文截断的总字符上限（单段拼接前分别截断）")
    parser.add_argument("--out", type=Path, default=None, help="将模型原始回复写入该文件（UTF-8）；与 --run-all 互斥（批量时自动命名）")
    parser.add_argument("--dry-run", action="store_true", help="只打印用户消息，不调 API")
    parser.add_argument("--timeout", type=int, default=180, help="HTTP 超时秒数")
    args = parser.parse_args()

    if args.run_all and args.sample is not None:
        print("错误：--run-all 不能与 --sample 同时使用", file=sys.stderr)
        return 2
    if args.run_all and (args.a or args.b or args.test or args.prod):
        print("错误：--run-all 不能与自定义 --a/--b/--test/--prod 同时使用", file=sys.stderr)
        return 2
    if args.run_all and args.out is not None:
        print("错误：--run-all 请省略 --out（每条结果自动写入 artifacts/deepseek_tests/）", file=sys.stderr)
        return 2

    # 仅传入脚本名、无任何参数时：默认样本 1 + dry-run，避免误消耗 API
    if len(sys.argv) == 1:
        args.sample = 1
        args.dry_run = True
        print(
            "提示：未传入任何参数，已默认使用 --sample 1 --dry-run（只打印 prompt）。\n"
            "      正式调用 DeepSeek：设置 DEEPSEEK_API_KEY 后执行\n"
            "      python update_tests_deepseek.py --sample 1\n"
            "      或批量：python update_tests_deepseek.py --run-all",
            file=sys.stderr,
        )

    repo: Path = args.repo.resolve()
    if not (repo / ".git").is_dir():
        print("错误：--repo 不是 git 仓库根目录", file=sys.stderr)
        return 2

    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip() or None

    if args.run_all:
        if not args.dry_run and not api_key:
            print("错误：--run-all 且非 --dry-run 时需设置环境变量 DEEPSEEK_API_KEY", file=sys.stderr)
            return 2
        results: list[tuple[str, bool, str]] = []
        for s in PRESET_SAMPLES:
            title = f"sample{s.id} {s.title}"
            compact = args.dry_run and not args.verbose
            ok, msg = run_one_update(
                repo,
                s.a,
                s.b,
                s.test,
                [s.prod],
                title,
                dry_run=args.dry_run,
                api_key=api_key,
                api_base=args.api_base,
                model=args.model,
                max_chars=args.max_chars,
                note=args.note,
                timeout=args.timeout,
                out=None,
                dry_run_compact=compact,
                verbose=args.verbose,
            )
            results.append((title, ok, msg))
            if ok and not args.dry_run:
                print(msg)

        print("\n========== 汇总 ==========", file=sys.stderr)
        n_ok = sum(1 for _t, ok, _m in results if ok)
        for title, ok, msg in results:
            mark = "OK  " if ok else "FAIL"
            print(f"  [{mark}] {title}", file=sys.stderr)
            if not ok:
                first = (msg or "").split("\n", 1)[0]
                print(f"        {first[:500]}", file=sys.stderr)
        print(f"  成功 {n_ok} / {len(results)}", file=sys.stderr)
        return 0 if n_ok == len(results) else 1

    if args.sample is not None:
        s = next(x for x in PRESET_SAMPLES if x.id == args.sample)
        a, b, test_path, prod_paths = s.a, s.b, s.test, [s.prod]
        title = f"sample{s.id} {s.title}"
    elif args.a and args.b and args.test and args.prod:
        a, b, test_path, prod_paths = args.a, args.b, args.test, list(args.prod)
        title = "custom"
    else:
        print(
            "错误：请指定预设样本或自定义提交。\n"
            "  预设：python update_tests_deepseek.py --sample 1 [--dry-run]\n"
            "  批量：python update_tests_deepseek.py --run-all [--dry-run]\n"
            "  自定义：需同时提供 --a --b --test 与至少一个 --prod\n"
            "  仓库路径：默认使用脚本同目录下的 commons-lang；可显式传入 --repo 路径。",
            file=sys.stderr,
        )
        return 2

    ok, msg = run_one_update(
        repo,
        a,
        b,
        test_path,
        prod_paths,
        title,
        dry_run=args.dry_run,
        api_key=api_key,
        api_base=args.api_base,
        model=args.model,
        max_chars=args.max_chars,
        note=args.note,
        timeout=args.timeout,
        out=args.out,
        dry_run_compact=False,
        verbose=args.verbose,
    )
    if not ok:
        print(msg, file=sys.stderr)
        return 1
    if not args.dry_run:
        print(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
