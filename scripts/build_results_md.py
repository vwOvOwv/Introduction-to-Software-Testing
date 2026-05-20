#!/usr/bin/env python3
"""从 artifacts/sample_runs 汇总并生成 results.md 表格片段。"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "artifacts" / "sample_runs"
CANDIDATES = ROOT / "artifacts" / "lang_sample_candidates_filtered.json"
RESULTS = ROOT / "results.md"


def classify(maven_rc: int | None, stdout: str, has_gen: bool, has_md: bool) -> str:
    if has_md and not has_gen:
        return "merge_error"
    if not has_gen:
        return "no_generate"
    if maven_rc is None:
        return "no_maven"
    if maven_rc == 0:
        return "pass"
    s = stdout or ""
    if "COMPILATION ERROR" in s:
        return "compile_fail"
    if "Tests run:" in s:
        return "test_fail"
    return "maven_other"


def main() -> None:
    cands: list[dict] = json.loads(CANDIDATES.read_text(encoding="utf-8"))["candidates"]
    proc_errors: dict[int, str] = {}
    summ_path = RUNS / "summary.json"
    if summ_path.is_file():
        summ = json.loads(summ_path.read_text(encoding="utf-8"))
        if isinstance(summ, list):
            for e in summ:
                if e.get("processing_error"):
                    proc_errors[int(e["id"])] = str(e["processing_error"])

    rows: list[dict] = []
    stats: dict[str, int] = {}

    for i, c in enumerate(cands, 1):
        bshort = c["b"][:12]
        d = RUNS / f"cand{i:03d}_{bshort}"
        has_md = (d / "deepseek_output.md").is_file()
        has_gen = (d / "generated.java").is_file()
        maven_rc = None
        stdout = ""
        if (d / "run_report.json").is_file():
            rep = json.loads((d / "run_report.json").read_text(encoding="utf-8"))
            maven = rep.get("maven") or {}
            maven_rc = maven.get("returncode")
            stdout = maven.get("stdout") or ""
        status = classify(maven_rc, stdout, has_gen, has_md)
        if i in proc_errors:
            status = "merge_error"
        stats[status] = stats.get(status, 0) + 1
        selector = Path(c["primary_test"]).stem
        rows.append(
            {
                "id": i,
                "status": status,
                "selector": selector,
                "pr_hint": c.get("pr_hint"),
                "dir": d.name,
                "has_md": has_md,
                "deepseek_ok": has_md,
            }
        )

    status_zh = {
        "pass": "通过",
        "compile_fail": "失败",
        "test_fail": "失败",
        "merge_error": "失败",
        "maven_other": "失败",
        "no_generate": "失败",
        "no_maven": "失败",
    }
    maven_desc = {
        "pass": lambda s: f"`{s}` 通过",
        "compile_fail": lambda s: f"`{s}` 编译失败",
        "test_fail": lambda s: f"`{s}` 测试失败（断言/运行）",
        "merge_error": lambda s: "未执行（合并失败）",
        "maven_other": lambda s: f"`{s}` Maven 非 0",
        "no_generate": lambda s: "未生成 Java",
        "no_maven": lambda s: "未跑 Maven",
    }

    table_lines: list[str] = []
    for r, c in zip(rows, cands):
        i = r["id"]
        st = r["status"]
        sel = r["selector"]
        pr = f" PR#{r['pr_hint']}" if r.get("pr_hint") else ""
        subj = (c.get("subject") or "")[:60]
        note = f"{pr} {subj}".strip() if st == "pass" else f"{pr} {subj}".strip()
        if st == "merge_error":
            note = (proc_errors.get(i) or "模型输出无法合并为 @Test") + (f"；{note}" if note else "")
        elif st == "compile_fail":
            note = (note + "；合并后 testCompile 失败") if note else "合并后 testCompile 失败"
        elif st == "test_fail":
            note = (note + "；编译通过但测试失败") if note else "编译通过但测试失败"
        note += f"。`artifacts/sample_runs/{r['dir']}/`"
        table_lines.append(
            f"| cand{i:03d} | {status_zh.get(st, st)} | "
            f"{'成功' if r['deepseek_ok'] else '失败'} | "
            f"{maven_desc.get(st, lambda s: s)(sel)} | {note} |"
        )

    n = len(rows)
    n_pass = stats.get("pass", 0)
    n_deepseek = sum(1 for r in rows if r["has_md"])
    body = f"""# commons-lang 样本测试结果（135 条）

执行时间：2026-05-16（批量实验完成）

说明：

- 样本池：`artifacts/lang_sample_candidates_filtered.json`，共 **135** 条。
- 流水线：`run_sample_experiment.py` → `update_tests_deepseek.py`（DeepSeek）→ 合并进 A 底本并 **从 B 同步 import / 嵌套类** → `run_single_maven_test.py` 在 **B** 上执行 `mvn -q -Dtest=<TestClass> test`。
- 机器可读汇总：`artifacts/sample_runs/summary.json`（若仅含尾部批次，以各 `candNNN_*/run_report.json` 为准）。
- **「通过」** 指 `maven.returncode=0`（该测试类在 B 上可编译且测试全绿），不表示与 PR 金标准 diff 完全一致。

## 总体统计

| 指标 | 数量 | 占比 |
| --- | ---: | ---: |
| 样本总数 | {n} | 100% |
| DeepSeek 有输出（`deepseek_output.md`） | {n_deepseek} | {n_deepseek / n * 100:.1f}% |
| **Maven 通过**（`returncode=0`） | **{n_pass}** | **{n_pass / n * 100:.1f}%** |
| 编译失败（`COMPILATION ERROR`） | {stats.get('compile_fail', 0)} | {stats.get('compile_fail', 0) / n * 100:.1f}% |
| 测试失败（已编译，`Tests run` 失败） | {stats.get('test_fail', 0)} | {stats.get('test_fail', 0) / n * 100:.1f}% |
| 合并失败（无 `@Test` 可合并） | {stats.get('merge_error', 0)} | {stats.get('merge_error', 0) / n * 100:.1f}% |
| 其它 Maven 非 0 | {stats.get('maven_other', 0)} | {stats.get('maven_other', 0) / n * 100:.1f}% |

## 结论摘要

- 在「A 底本 + 模型只改 `@Test` + 从 B 补 import/一层嵌套类」设定下，**约 {n_pass / n * 100:.0f}%** 样本能在 B 上跑通聚焦测试类。
- 主要失败形态：**编译失败**（缺符号/import/深层嵌套类，约 {stats.get('compile_fail', 0)} 条）> **测试失败**（逻辑/断言未对齐，约 {stats.get('test_fail', 0)} 条）> **合并失败**（模型未输出可解析 `@Test`，{stats.get('merge_error', 0)} 条：cand124、cand128）。
- 与早期仅 8 条、未做 B 同步时相比，前 8 条在 `--resync-generated` 后由 2/8 提升至 **7/8** Maven 通过（cand006 仍为深层嵌套类编译失败）。

## 全量结果表

| 编号 | 结果 | DeepSeek | 聚焦测试执行结果 | 备注 |
| --- | --- | --- | --- | --- |
"""
    body += "\n".join(table_lines)
    body += """

## 失败样本索引（便于查阅）

### 合并失败（2）

- **cand124** `FastDateParserTest`：补丁中未识别到 `@Test` 方法。
- **cand128** `StreamsTest`：同上。

### Maven 通过但测试失败（8）

cand015、cand016、cand022、cand042、cand053、cand057、cand075、cand131（详见上表 `测试失败` 行）。

### 编译失败（26）

cand006、cand011、cand018、cand019、cand021、cand026、cand030、cand033、cand043、cand046、cand047、cand050、cand059、cand060、cand062、cand083、cand088、cand096、cand110、cand111、cand118、cand119、cand120、cand121、cand123、cand130 等（详见上表）。

## 主要产物路径

- 汇总：`artifacts/sample_runs/summary.json`
- 单条：`artifacts/sample_runs/candNNN_<B前12位>/`（`deepseek_output.md`、`generated.java`、`run_report.json`）
- 候选列表：`artifacts/lang_sample_candidates_filtered.json`
"""
    RESULTS.write_text(body, encoding="utf-8")
    print(f"Wrote {RESULTS} ({n} rows, pass={n_pass})")


if __name__ == "__main__":
    main()
