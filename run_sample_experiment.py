#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT / "commons-lang"
ARTIFACTS = ROOT / "artifacts" / "sample_runs"
UPDATE_SCRIPT = ROOT / "update_tests_deepseek.py"
RUN_SCRIPT = ROOT / "run_single_maven_test.py"
FIXED_PATH = "/usr/bin:/bin:/usr/local/bin"


SAMPLES = [
    {
        "id": 1,
        "title": "NaN bypass in primitive double range validators",
        "a": "4b09471db039085a3114f79ece97ca7fd9bd6f1e",
        "b": "864dd6ea887fd394f15e3b55203d6f52f717373b",
        "prod": "src/main/java/org/apache/commons/lang3/Validate.java",
        "target_test": "src/test/java/org/apache/commons/lang3/ValidateDoublesTest.java",
        "input_test": "src/test/java/org/apache/commons/lang3/ValidateTest.java",
        "selector": "ValidateDoublesTest",
        "note": "A 中不存在 ValidateDoublesTest.java。请基于旧测试类 ValidateTest.java 和生产代码 diff，生成一个完整的 JUnit 5 测试类，类名必须为 ValidateDoublesTest，包名必须为 org.apache.commons.lang3，聚焦 primitive double range validators 对 NaN 的新行为。输出只保留完整 Java 测试类源码。",
    },
    {
        "id": 2,
        "title": "TimedSemaphore.shutdown() must wake blocked threads",
        "a": "58ba515e4b083f658ef2087df36284a9cd539b31",
        "b": "5914a8e80a547301b76bf8ef691053e4dfc901a7",
        "prod": "src/main/java/org/apache/commons/lang3/concurrent/TimedSemaphore.java",
        "target_test": "src/test/java/org/apache/commons/lang3/concurrent/TimedSemaphoreTest.java",
        "input_test": "src/test/java/org/apache/commons/lang3/concurrent/TimedSemaphoreTest.java",
        "selector": "TimedSemaphoreTest",
        "note": "请输出完整测试类源码，并保留类名 TimedSemaphoreTest。重点覆盖 shutdown() 唤醒 acquire() 阻塞线程的行为。",
    },
    {
        "id": 3,
        "title": "Two fixes in RandomStringUtils.random(...)",
        "a": "e63927afd575ba22f41a1d5b23b2d85745e82d24",
        "b": "313d877d57abefdbb1ad0c42781bf719b83d5a35",
        "prod": "src/main/java/org/apache/commons/lang3/RandomStringUtils.java",
        "target_test": "src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java",
        "input_test": "src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java",
        "selector": "RandomStringUtilsTest",
        "note": "请输出完整测试类源码，并保留类名 RandomStringUtilsTest。重点覆盖这次 random(...) 修复对应的新边界行为。",
    },
    {
        "id": 4,
        "title": "StringUtils.joins() OOME / index check",
        "a": "b64542b5537b699f456cc8facf5e6481140dafaa",
        "b": "19b59ffddbde0db1405c2cf4df8413ccee189be0",
        "prod": "src/main/java/org/apache/commons/lang3/StringUtils.java",
        "target_test": "src/test/java/org/apache/commons/lang3/StringUtilsJoinExceptionTest.java",
        "input_test": "src/test/java/org/apache/commons/lang3/StringUtilsJoinExceptionTest.java",
        "selector": "StringUtilsJoinExceptionTest",
        "note": "请输出完整测试类源码，并保留类名 StringUtilsJoinExceptionTest。重点覆盖 joins() 的 OOME 和 index check 修复行为。",
    },
    {
        "id": 5,
        "title": "NumberUtils.createNumber Float shortcut / exact",
        "a": "1dd7cb14c233140a8e76ba5441b6360a239a98dc",
        "b": "5904c573ffacaa5d8836ffc2b346f400c8901ed1",
        "prod": "src/main/java/org/apache/commons/lang3/math/NumberUtils.java",
        "target_test": "src/test/java/org/apache/commons/lang3/math/NumberUtilsTest.java",
        "input_test": "src/test/java/org/apache/commons/lang3/math/NumberUtilsTest.java",
        "selector": "NumberUtilsTest",
        "note": "请输出完整测试类源码，并保留类名 NumberUtilsTest。重点覆盖 createNumber 对 Float shortcut 和精确解析的修复。",
    },
    {
        "id": 6,
        "title": "FailableConsumer.accept(...) overload",
        "a": "d0fb835fd93357238cbd29b0b1fbcfb84d856464",
        "b": "eb202b0b905ac3bbea742f1aad426f5a6c7d604d",
        "prod": "src/main/java/org/apache/commons/lang3/function/FailableConsumer.java",
        "target_test": "src/test/java/org/apache/commons/lang3/function/FailableConsumerTest.java",
        "input_test": "src/test/java/org/apache/commons/lang3/function/FailableConsumerTest.java",
        "selector": "FailableConsumerTest",
        "note": "请输出完整测试类源码，并保留类名 FailableConsumerTest。重点覆盖 accept(...) 新增 overload 的行为。",
    },
]


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PATH"] = FIXED_PATH
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
        return fenced[0].strip() + "\n"
    marker = "\n---\n\n"
    body = markdown_text.split(marker, 1)[1] if marker in markdown_text else markdown_text
    return body.strip() + "\n"


def main() -> int:
    if not os.environ.get("DEEPSEEK_API_KEY", "").strip():
        print("DEEPSEEK_API_KEY is required", file=sys.stderr)
        return 2

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    summary: list[dict[str, object]] = []

    for sample in SAMPLES:
        sample_dir = ARTIFACTS / f"sample{sample['id']}"
        sample_dir.mkdir(parents=True, exist_ok=True)
        deepseek_md = sample_dir / "deepseek_output.md"
        generated_java = sample_dir / "generated.java"
        run_report = sample_dir / "run_report.json"

        entry: dict[str, object] = dict(sample)

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
            summary.append(entry)
            continue

        generated_java.write_text(extract_java(deepseek_md.read_text(encoding="utf-8")), encoding="utf-8")
        java_source = generated_java.read_text(encoding="utf-8")
        entry["generated"] = True
        entry["generated_java"] = str(generated_java)
        entry["generated_class_name_present"] = str(sample["selector"]) in java_source

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
            entry["maven_stderr_tail"] = maven.get("stderr", "")[-4000:]

        summary.append(entry)

    summary_path = ARTIFACTS / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())