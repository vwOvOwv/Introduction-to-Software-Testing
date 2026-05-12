# commons-lang 回归测试选择（RTS）实验样本

仓库本地路径：`final_homework/commons-lang`（Apache `apache/commons-lang`）。

**用法说明**

- **B**：变更后提交（在该版本上跑测试）。
- **A**：`B` 的第一父提交 `B~1`（在本机已用 `git rev-parse B~1` 核对）。
- **金标准相关测试**：本 PR 中改动的测试类路径，用于计算召回（「至少应被选中」）。
- 空白列留给你们填实验结果。

---

## 样本总表

| 编号 |                            PR                             | 标题（摘要）                                        | B（完整 hash）                             | A（B 的父提交）                            | 生产代码（`src/main/java`）                               | 金标准相关测试（`src/test/java`）                            | `mvn test` 在 B 上通过 | GPT 选中集合包含金标准 | 备注 |
| :--: | :-------------------------------------------------------: | :-------------------------------------------------- | :----------------------------------------- | :----------------------------------------- | :-------------------------------------------------------- | :----------------------------------------------------------- | :--------------------: | :--------------------: | :--- |
|  1   | [#1640](https://github.com/apache/commons-lang/pull/1640) | NaN bypass in primitive double range validators     | `864dd6ea887fd394f15e3b55203d6f52f717373b` | `4b09471db039085a3114f79ece97ca7fd9bd6f1e` | `org/apache/commons/lang3/Validate.java`                  | `org/apache/commons/lang3/ValidateDoublesTest.java`          |                        |                        |      |
|  2   | [#1639](https://github.com/apache/commons-lang/pull/1639) | TimedSemaphore.shutdown() must wake blocked threads | `5914a8e80a547301b76bf8ef691053e4dfc901a7` | `58ba515e4b083f658ef2087df36284a9cd539b31` | `org/apache/commons/lang3/concurrent/TimedSemaphore.java` | `org/apache/commons/lang3/concurrent/TimedSemaphoreTest.java` |                        |                        |      |
|  3   | [#1638](https://github.com/apache/commons-lang/pull/1638) | Two fixes in RandomStringUtils.random(...)          | `313d877d57abefdbb1ad0c42781bf719b83d5a35` | `e63927afd575ba22f41a1d5b23b2d85745e82d24` | `org/apache/commons/lang3/RandomStringUtils.java`         | `org/apache/commons/lang3/RandomStringUtilsTest.java`        |                        |                        |      |
|  4   | [#1636](https://github.com/apache/commons-lang/pull/1636) | StringUtils.joins() OOME / index check              | `19b59ffddbde0db1405c2cf4df8413ccee189be0` | `b64542b5537b699f456cc8facf5e6481140dafaa` | `org/apache/commons/lang3/StringUtils.java`               | `org/apache/commons/lang3/StringUtilsJoinExceptionTest.java` |                        |                        |      |
|  5   | [#1635](https://github.com/apache/commons-lang/pull/1635) | NumberUtils.createNumber Float shortcut / exact     | `5904c573ffacaa5d8836ffc2b346f400c8901ed1` | `1dd7cb14c233140a8e76ba5441b6360a239a98dc` | `org/apache/commons/lang3/math/NumberUtils.java`          | `org/apache/commons/lang3/math/NumberUtilsTest.java`         |                        |                        |      |
|  6   | [#1641](https://github.com/apache/commons-lang/pull/1641) | FailableConsumer.accept(...) overload               | `eb202b0b905ac3bbea742f1aad426f5a6c7d604d` | `d0fb835fd93357238cbd29b0b1fbcfb84d856464` | `org/apache/commons/lang3/function/FailableConsumer.java` | `org/apache/commons/lang3/function/FailableConsumerTest.java` |                        |                        |      |

---

## 常用命令（复制后把 `B` 换成上表 hash）

```bash
cd ./commons-lang
git checkout B
mvn -q test

# 变更文件列表（写进报告）
git diff --name-only B~1 B

# 给 GPT 的 diff（可按路径再缩小）
git diff B~1 B
```

**Surefire 只跑金标准测试类（示例，编号 1）：**

```bash
mvn -q test -Dtest=ValidateDoublesTest
```

---

## 若你们更换了本地 `B`（例如 rebase 过）

请在本机重新计算 **A**：

```bash
git rev-parse <B的hash>~1
```

将上表 **A** 列更新为输出结果即可。