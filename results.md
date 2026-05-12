# sample.md 样本测试结果

执行时间：2026-05-12

说明：

- 已使用 `update_tests_deepseek.py` 为各样本生成测试候选，并用 `run_single_maven_test.py` 在对应 `B` 提交上执行。
- 实际验证命令是聚焦测试类的 `mvn -q -Dtest=<TestClass> test`，不是整库 `mvn test`。
- 原始产物位于 `artifacts/sample_runs/`。

| 编号 | 结果 | `update_tests_deepseek.py` | 聚焦测试执行结果 | 备注 |
| --- | --- | --- | --- | --- |
| 1 | 通过 | 成功 | `ValidateDoublesTest` 通过 | `A` 中没有 `ValidateDoublesTest.java`，改用 `ValidateTest.java` 作为旧测试基底，并在提示中要求输出类名 `ValidateDoublesTest`。产物见 `artifacts/sample_runs/sample1/`。 |
| 2 | 通过 | 成功 | `TimedSemaphoreTest` 通过 | 产物见 `artifacts/sample_runs/sample2/`。Maven 返回码为 0。 |
| 3 | 通过 | 成功 | `RandomStringUtilsTest` 通过 | 产物见 `artifacts/sample_runs/sample3/`。Maven 返回码为 0。 |
| 4 | 通过 | 成功 | `LocaleUtilsTest` 通过 | 已基于更新后的样本定义重跑。`A`/`B` 使用 `LocaleUtilsTest.java` 作为测试类，生成成功，聚焦测试在 `B=3df7f4440e7447bc55e95400ec511323e708c652` 上返回码为 0。产物见 `artifacts/sample_runs/sample4_rerun/`。 |
| 5 | 失败 | 成功 | `NumberUtilsTest` 编译失败 | 首轮执行因为提取结果含代码围栏失败；修正提取后仍失败。2026-05-12 已基于更新后的 `update_tests_deepseek.py` 再次重跑，结果不变：模型生成的 Java 源码本身不完整，`sample5_rerun/generated.java` 末尾仍出现未结束字符串，Maven 编译报错。产物见 `artifacts/sample_runs/sample5/` 与 `artifacts/sample_runs/sample5_rerun/`。 |
| 6 | 通过 | 成功 | `ArchUtilsTest` 通过 | 已基于更新后的样本定义重跑。`A`/`B` 使用 `ArchUtilsTest.java` 作为测试类，生成成功，聚焦测试在 `B=bb675e1127adb7f7c8d8687667bc11779d8e75eb` 上返回码为 0。产物见 `artifacts/sample_runs/sample6_rerun/`。 |

## 关键信息

- 成功跑通的样本：1、2、3、4、6。
- 生成成功但测试失败的样本：5。
- 因脚本前提不满足而未进入生成/执行阶段的样本：无。

## 样本 1-4、6 补丁效果对比

- 样本 1：效果最好。AI 生成补丁虽然不是最小改动，而是重写了整个 `ValidateDoublesTest`，但它准确覆盖了金标准关心的核心行为，即 `inclusiveBetween` 和 `exclusiveBetween` 对 `Double.NaN` 的拒绝逻辑；同时还补充了带消息与不带消息、边界值和越界值场景。就回归测试价值看，属于命中缺陷本质、但生成范围偏大的补丁。
- 样本 2：部分命中。AI 补丁同样识别出“`shutdown()` 应唤醒阻塞在 `acquire()` 的线程”这一核心目标，也新增了相关并发测试，因此方向基本正确；但相比金标准，它缺少更强的防伪阳性设计，例如确认线程已进入 `WAITING`、避免依赖短周期定时任务自然唤醒，以及更严格的超时保护。因此它能覆盖问题主题，但检错能力弱于金标准。
- 样本 3：明显失配。金标准新增的是两个关键回归点：自定义 `chars` 数组不应误抛 `IllegalArgumentException`，以及只含被拒绝码点的区间应快速抛错而不是卡住。AI 生成补丁没有保留这两处新增测试，反而出现了整文件重写和代码围栏残留等明显偏差。虽然聚焦测试执行结果仍为通过，但这更说明补丁没有有效对齐该 PR 的真实测试意图，不能把“跑通”视为“覆盖正确”。
- 样本 4：部分命中。重跑后的金标准测试主要补了 `LocaleUtils.toLocale()` 对 `#` 变体和 JDK 特殊 locale 字符串的正向解析能力，例如 `th_TH_#Thai`、`th_TH_TH`、`ja_JP_JP` 及其带扩展后缀的形式。AI 生成补丁确实感知到了 `#` 相关特殊情况，在 `testParseAllLocales()` 中加入了例外分支；但它没有保留金标准新增的显式正向测试 `testLang1823()` 和 `testSpecialCases()`，因此更像是对同一问题域的弱覆盖，而不是对金标准改动的等价复现。
- 样本 6：部分命中且较接近金标准。金标准只新增了 `ppc64le` 相关断言，分别覆盖架构类型识别、非 32 位和 64 位判定三处。AI 生成补丁正确加入了 `ppc64le` 常量，并在 `testArch()` 中验证了它会被识别为 `PPC`；但它漏掉了 `is32Bit()` 和 `is64Bit()` 两组新增断言。因此它已经命中核心映射关系，但覆盖仍不完整。
- 总体结论：如果只看 `mvn -q -Dtest=<TestClass> test`，样本 1、2、3、4、6 都是成功；如果看与金标准测试修改的一致性，则可区分为“强命中（样本 1）”“部分命中但较弱（样本 2、4）”“部分命中且较接近（样本 6）”“明显失配（样本 3）”。因此，这批样本更适合同时从“能否运行”和“是否语义对齐金标准”两个维度评估，而不能只看通过率。

## 主要产物路径

- 汇总：`artifacts/sample_runs/summary.json`
- 样本 1：`artifacts/sample_runs/sample1/`
- 样本 2：`artifacts/sample_runs/sample2/`
- 样本 3：`artifacts/sample_runs/sample3/`
- 样本 4 重跑：`artifacts/sample_runs/sample4_rerun/`
- 样本 5 修正后执行报告：`artifacts/sample_runs/sample5/run_report_fixed.json`
- 样本 5 重跑执行报告：`artifacts/sample_runs/sample5_rerun/run_report.json`
- 样本 6 重跑：`artifacts/sample_runs/sample6_rerun/`
