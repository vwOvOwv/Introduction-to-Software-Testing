## 项目说明

使用前需安装 JDK 与 maven，并克隆仓库 `commons-lang`。
```
git clone https://github.com/apache/commons-lang.git
```

本仓库包含用于生成并验证 AI 提示产物（基于 DeepSeek/OpenAI）的实验脚本与样本数据。有关运行与结果请参见 `artifacts/sample_runs/` 与 `results.md`。

Python 脚本汇总（功能 / 使用 / 已知缺陷）

- `update_tests_deepseek.py`
	- 功能：基于给定的仓库提交（A、B）与旧测试文件（来自 A），构建给 DeepSeek（OpenAI 兼容接口）的 prompt，调用 API 以生成针对 B 的更新后完整测试类源码；支持单样本或批量运行并把输出写为 `deepseek_output.md`。
	- 使用：
		- 干跑（只打印 prompt，不调 API）：`python update_tests_deepseek.py`
		- 指定样本：`python update_tests_deepseek.py --sample 1`
		- 指定仓库/提交/测试：参见脚本顶部示例，或使用 `--repo/--a/--b/--test/--prod` 参数。
	- 已知缺陷/注意事项：
		- 需设置环境变量 `DEEPSEEK_API_KEY` 才能实际调用 API；默认运行不调用时为 dry-run。
		- 要求指定的测试文件必须在 A 提交中存在（`git show A:<path>`），否则会报错并跳过该样本。
		- 对 API 返回的解析较为直接（基于围栏 ```java 提取或 marker 分割），若 DeepSeek 返回非预期格式（缺少围栏、包含额外注释）可能导致提取失败或生成不完整 Java 源码。
		- 对 HTTP/JSON 错误有抛出但恢复能力有限（会终止当前样本）；对网络异常、超大返回、非 JSON 响应有明确错误信息但未实现重试策略。

- `run_single_maven_test.py`
	- 功能：切换至指定 git 版本、把本地替换测试文件覆盖到仓库中指定路径、仅运行聚焦的 Surefire 测试（`-Dtest=<selector>`），并将执行报告写入 JSON。
	- 使用示例：
		```bash
		python run_single_maven_test.py --repo /path/to/commons-lang --ref <commit> \
			--target-test-path src/test/java/…/FooTest.java \
			--replacement-test-file /tmp/generated.java --test-selector FooTest --maven-arg -q
		```
	- 已知缺陷/注意事项：
		- 要求 `--repo` 必须是一个 git 仓库根目录（检测 `.git`），否则抛出异常并退出。
		- 依赖外部命令 `git` 与 `mvn` 存在于 PATH；脚本没有对 Maven 配置做容错（例如私服、环境差异）。
		- 覆盖测试文件后会尽量恢复（`git restore`），但在异常情况下仍可能留下工作树改动；有 `--discard-all-tracked-changes` 选项来强制丢弃全部 tracked 改动。

- `orchestrate_test_updates.py`
	- 功能：辅助发现候选测试方法、从 A/B diff 中挑选变更的生产代码文件和相关旧测试，提取测试方法、将候选方法归约为单一测试、并提供运行外部脚本（如 `update_tests_deepseek.py` 与 `run_single_maven_test.py`）的编排工具函数。
	- 使用：作为库/脚本被调用以进行更复杂的样本批量处理；包含对测试类方法抽取、差异文件识别等工具函数。
	- 已知缺陷/注意事项：
		- 对于解析 Java 源的正则和括号匹配存在启发式实现，复杂或非常规格式的测试类可能导致方法抽取失败或方法边界识别错误。
		- 依赖 `git show` / `git diff` 输出，若仓库状态或路径不匹配会抛出错误并中断流程。
		- 在查找外部脚本路径时，如果找不到会抛出 `ValueError`，上层调用需捕获并处理。

- `run_sample_experiment.py`
	- 功能：驱动 SAMPLES 列表（样本 1–6），调用 `update_tests_deepseek.py` 生成候选测试（写为 `artifacts/sample_runs/sampleN/deepseek_output.md`）、提取 Java 源写为 `generated.java`，随后调用 `run_single_maven_test.py` 在指定 B 提交上执行聚焦测试并收集报告，最终汇总 `artifacts/sample_runs/summary.json`。
	- 使用：`DEEPSEEK_API_KEY` 必需用于实际调用 API；直接运行将依次处理样本并输出摘要路径。
	- 已知缺陷/注意事项：
		- 当 `update_tests_deepseek.py` 生成的 `deepseek_output.md` 格式不符合预期（如缺少代码围栏）时，`extract_java()` 的提取逻辑可能失败或产生不完整源码，导致后续 Maven 编译失败（样本 5 的情形）。
		- 该脚本强制了一个固定 `PATH`（`FIXED_PATH`），可能影响用户环境中 `git`/`mvn` 等可执行文件的查找；在非标准环境下需注意该常量。

---

若需我把这些内容拆成更详尽的用法示例（例如每个脚本的全部 CLI 参数说明与典型命令行案例），或为 `update_tests_deepseek.py` 增加更鲁棒的 Java 提取规则/重试策略，我可以继续实现并运行简单验证。