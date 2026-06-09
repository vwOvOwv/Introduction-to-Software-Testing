# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cc54667ce1ee7d4cbddd836d14467d1569b4057f`
- B: `526a03a8701f85e422786f0a4d1fadd3f0c249c1`
- test: `src/test/java/org/apache/commons/lang3/time/DateUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DateUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `93081`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 24767, 'completion_tokens': 295, 'total_tokens': 25062}`

---

- 新增 `testFailedTimeZonePatternDoesNotPoisonNextPatternInstant`：覆盖 `parseDateWithLeniency` 在每次模式尝试前恢复默认时区，防止失败的含时区模式污染后续无时区模式；无需调整 import。

```java
    @Test
    public void testFailedTimeZonePatternDoesNotPoisonNextPatternInstant() throws Exception {
        final String input = "+0500 01/01/2024";

        final Date baseline = DateUtils.parseDate(input, "'+0500 'MM/dd/yyyy");
        assertNotNull(baseline, "baseline parse must succeed");

        final Date poisoned = DateUtils.parseDate(input, "Z 'X' MM/dd/yyyy", "'+0500 'MM/dd/yyyy");
        assertNotNull(poisoned, "poisoning sequence parse must succeed via the second pattern");

        assertEquals(baseline.getTime(), poisoned.getTime(),
                "Calendar TZ leaked from a failed prior pattern must not affect the instant produced by a subsequent TZ-less pattern");
    }
```