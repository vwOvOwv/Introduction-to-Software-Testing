# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cda703ccb891290208f28bc6afb2abfaea7a6c8d`
- B: `3a35c53c6c9a3b9a1feedaf39b72e405ecaf9df8`
- test: `src/test/java/org/apache/commons/lang3/time/DurationUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DurationUtils.java']`
- old_test_mode: `methods`
- user_chars: `4005`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1401, 'completion_tokens': 218, 'total_tokens': 1619}`

---

- 新增 `testZeroIfNull`：对应生产代码新增 `DurationUtils.zeroIfNull(Duration)`，验证 `null` 返回 `Duration.ZERO`，非空值原样返回；无需调整 import。

```java
    @Test
    public void testZeroIfNull() {
        assertEquals(Duration.ZERO, DurationUtils.zeroIfNull(null));
        assertEquals(Duration.ofDays(1), DurationUtils.zeroIfNull(Duration.ofDays(1)));
    }
```