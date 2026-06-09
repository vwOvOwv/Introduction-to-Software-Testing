# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `8d360ae70732ae26d961f76da5a98c44ac5931c6`
- B: `aadd8e172eb22fb593fbaa454075677656fad111`
- test: `src/test/java/org/apache/commons/lang3/time/DurationFormatUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DurationFormatUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `34861`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9940, 'completion_tokens': 452, 'total_tokens': 10392}`

---

- 新增 `@Test` 方法 `testLANG981`，对应生产代码 `lexx` 在遇到未闭合单引号字面量时新增抛出 `IllegalArgumentException` 的行为。
- 不需要调整 import，复用现有 `org.junit.Test` 导入即可。

```java
    @Test(expected = IllegalArgumentException.class)
    public void testLANG981() {
        DurationFormatUtils.lexx("'yMdHms''S");
    }
```