## 项目说明

本仓库用于 **commons-lang** 上的实验：根据 PR 在 **A→B** 的生产代码与测试 diff，调用 **DeepSeek** 生成/更新 JUnit 测试，并在 **B** 提交上用 Maven 做聚焦验证。

被测仓库默认路径：`../commons-lang`（即 `final_homework/commons-lang`，需为 git 克隆）。

```bash
git clone https://github.com/apache/commons-lang.git
```

实验结果见 **`results.md`**（135 条全量汇总）与 **`artifacts/sample_runs/`**（每条样本的 `deepseek_output.md`、`generated.java`、`run_report.json`）。

---

## 环境准备

| 依赖 | 说明 |
| --- | --- |
| **JDK** | 建议 17+（与 commons-lang 当前分支一致） |
| **Maven** | 需在 PATH 中；Windows 请用 `where.exe mvn` 检查（PowerShell 里 `where mvn` 不是查 PATH） |
| **git** | 用于 `checkout` / `show` / `diff` |
| **Python 3** | 运行脚本，仅标准库（DeepSeek 调用除外） |
| **`DEEPSEEK_API_KEY`** | 批量实验与单条生成时必需 |

PowerShell 示例：

```powershell
cd Introduction-to-Software-Testing
$env:DEEPSEEK_API_KEY = "sk-..."
where.exe mvn
where.exe git
```

---

## 样本与数据流

```
scan_lang_samples.py          → artifacts/lang_sample_candidates.json
filter_lang_candidates.py     → artifacts/lang_sample_candidates_filtered.json（135 条）
verify_lang_candidates.py     → artifacts/lang_sample_verify_report.json
run_sample_experiment.py      → artifacts/sample_runs/candNNN_<B前12位>/
scripts/build_results_md.py   → results.md
```

- **A**：`B` 的第一父提交（`B~1`），旧测试必须存在于 A。
- **B**：PR 合并后提交；Maven 在该版本上跑 `-Dtest=<TestClass> test`。
- 候选列表：`artifacts/lang_sample_candidates_filtered.json`（`count_kept: 135`）。

---

## 快速开始（批量实验）

```powershell
cd Introduction-to-Software-Testing

# 修改 key.py，写入你的 DeepSeek API Key
# DEEPSEEK_API_KEY = "sk-..."

# 跑全部 135 条（耗时长、消耗 API）
python run_sample_experiment.py

# 中断后续跑（跳过已有 deepseek_output + generated + run_report）
python run_sample_experiment.py --resume

# 只重算 generated.java + Maven（不调 API，应用最新合并逻辑）
python run_sample_experiment.py --resync-generated

# 试跑前 N 条
python run_sample_experiment.py --limit 5

# 从第 N 条继续
python run_sample_experiment.py --start 124 --resume

# 根据各目录 run_report 重新生成 results.md
python scripts/build_results_md.py
```

**注意：** `run_sample_experiment.py` **没有** `--run-all` 参数（该参数在 `update_tests_deepseek.py` 中）。不传 `--limit` 即处理 filtered JSON 中的全部候选。

---

## 流水线要点（与早期 6 条手工样本的区别）

1. **Prompt**：向模型提供生产 diff、A 上相关 `@Test` 方法（非整份 B 生产文件）；要求只输出需修改的测试**方法**。
2. **合并**：以 **A** 上完整测试类为底，将模型输出的方法替换/插入；再调用 `finalize_merged_test_class()`：
   - 从 **B** 补齐缺失的 `import`；
   - 若代码引用了某嵌套类型，用 **B** 上同名 `static class` 等定义**替换或插入**（一层嵌套；深层嵌套如 cand006 仍可能编译失败）。
3. **验证**：`run_single_maven_test.py` 在 **B** 上执行 `mvn -q -Dtest=<TestClass> test`；Windows 下通过 `shutil.which("mvn")` 解析 `mvn.cmd` 完整路径。
4. **容错**：单条合并/Maven 异常会记录在对应 `run_report.json` 中并**继续下一条**；每处理一条即刷新该条结果文件。

「通过」= `maven.returncode == 0`，**不**保证与 PR 金标准测试 diff 完全一致（见 `results.md` 结论）。

---

## Python 脚本

### `run_sample_experiment.py`（主入口）

- **功能**：读取 `lang_sample_candidates_filtered.json`，对每条候选调用 `update_tests_deepseek.py` → 合并为 `generated.java` → `run_single_maven_test.py`，逐个写入 `artifacts/sample_runs/candNNN_*/run_report.json`。
- **产物目录**：`artifacts/sample_runs/cand001_07914b39281e/`（`NNN` 为 filtered 列表序号，`07914b39281e` 为 B 的 hash 前 12 位）。
- **常用参数**：`--limit`、`--start`、`--resume`、`--resync-generated`、`--skip-maven`、`--only-verified-pass`。

### `update_tests_deepseek.py`

- **功能**：构造 compact prompt，调用 DeepSeek；单条 `--index N` 或批量 `--run-all`（输出到 `artifacts/deepseek_tests/` 或 `--out`）。
- **示例**：
  ```powershell
  python update_tests_deepseek.py --index 1          # dry-run 第 1 条
  python update_tests_deepseek.py --index 1 --out artifacts/sample_runs/...
  python update_tests_deepseek.py --run-all --limit 5
  ```
- **环境变量**：~~`DEEPSEEK_API_KEY`~~；可选 `DEEPSEEK_MAX_OUTPUT_TOKENS`（默认 8192）。

### `run_single_maven_test.py`

- **功能**：`git checkout` 到 `--ref`，用本地文件覆盖仓库内测试类，运行聚焦 Surefire 测试，写 JSON 报告，并 `git restore` 测试文件。
- **示例**：
  ```powershell
  python run_single_maven_test.py --repo ..\commons-lang --ref <B> `
    --target-test-path src/test/java/.../FooTest.java `
    --replacement-test-file artifacts\sample_runs\cand001_...\generated.java `
    --test-selector FooTest --maven-arg=-q
  ```

### `scan_lang_samples.py` / `filter_lang_candidates.py` / `verify_lang_candidates.py`

- **功能**：从 git 历史扫描 PR 候选 → 清洗（subject、Foo/FooTest 配对）→ 在 B 上 `mvn -Dtest=...` 预验证，生成 filtered 列表与 verify 报告。
- **一般只需在扩充样本池时重跑**；日常实验直接用 `lang_sample_candidates_filtered.json`。

### `orchestrate_test_updates.py`

- **功能**：测试方法抽取、`merge_patch_into_test_class`、`finalize_merged_test_class` 等库函数；被 `update_tests_deepseek.py` 与 `run_sample_experiment.py` 引用。

### `scripts/build_results_md.py`

- **功能**：扫描 `artifacts/sample_runs/cand*/run_report.json`，统计通过/编译失败/测试失败/合并失败，生成 **`results.md`**。

---

## 结果解读（135 条实验概况）

详见 **`results.md`**。

## 已知限制

- 模型默认只输出 `@Test` / `@ParameterizedTest` **方法**；大改测试结构（重命名内部辅助方法、大量新增嵌套类）时，即使补 import 也可能编译或语义失败。
- `extract_test_methods` / 嵌套类同步均为启发式，复杂 Java 格式可能边界识别错误。
- 若只跑了部分 `--start`/`--limit` 批次，全量统计请以各 `candNNN_*/run_report.json` 或运行 `build_results_md.py` 为准。
- Maven 依赖本机 `~/.m2` 与网络；未配置私服镜像时首次构建较慢。

---

## 相关文件

| 路径 | 说明 |
| --- | --- |
| `results.md` | 135 条实验汇总表与结论 |
| `artifacts/lang_sample_candidates_filtered.json` | 当前实验样本池 |
| `artifacts/sample_runs/candNNN_*/run_report.json` | 最近一次批量运行的机器可读单条结果 |
