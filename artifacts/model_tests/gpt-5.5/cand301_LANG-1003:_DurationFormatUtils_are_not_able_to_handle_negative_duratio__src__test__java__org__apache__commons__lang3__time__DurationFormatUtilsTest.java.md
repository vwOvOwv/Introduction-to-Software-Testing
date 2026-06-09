# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `358f139d1316df2b8efd7610afa3aa68d165334f`
- B: `64ef8a80224443c81dfb198cbc567e1b2b9356a2`
- test: `src/test/java/org/apache/commons/lang3/time/DurationFormatUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DurationFormatUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `36306`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 10361, 'completion_tokens': 701, 'total_tokens': 11062}`

---

- 新增 `testFormatNegativeDurationWords`，覆盖 `formatDurationWords` 通过 `formatDuration` 对负 duration 新增抛出 `IllegalArgumentException` 的行为；无需调整 import。
- 新增 `testFormatNegativeDurationHMS`，覆盖 `formatDurationHMS` 对负 duration 新增抛出 `IllegalArgumentException` 的行为；无需调整 import。
- 新增 `testFormatNegativeDurationISO`，覆盖 `formatDurationISO` 对负 duration 新增抛出 `IllegalArgumentException` 的行为；无需调整 import。
- 新增 `testFormatNegativeDuration`，覆盖 `formatDuration(long, String, boolean)` 对负 duration 新增抛出 `IllegalArgumentException` 的行为；无需调整 import。
- 新增 `testFormatPeriodISOStartGreaterEnd`，覆盖 `formatPeriodISO` 在 `startMillis > endMillis` 时新增抛出 `IllegalArgumentException` 的行为；无需调整 import。
- 新增 `testFormatPeriodeStartGreaterEnd`，覆盖 `formatPeriod` 在 `startMillis > endMillis` 时新增抛出 `IllegalArgumentException` 的行为；无需调整 import。

```java
@Test(expected = IllegalArgumentException.class)
public void testFormatNegativeDurationWords() throws Exception {
    DurationFormatUtils.formatDurationWords(-5000, true, true);
}

@Test(expected = IllegalArgumentException.class)
public void testFormatNegativeDurationHMS() throws Exception {
    DurationFormatUtils.formatDurationHMS(-5000);
}

@Test(expected = IllegalArgumentException.class)
public void testFormatNegativeDurationISO() throws Exception {
    DurationFormatUtils.formatDurationISO(-5000);
}

@Test(expected = IllegalArgumentException.class)
public void testFormatNegativeDuration() throws Exception {
    DurationFormatUtils.formatDuration(-5000, "S", true);
}

@Test(expected = IllegalArgumentException.class)
public void testFormatPeriodISOStartGreaterEnd() throws Exception {
    DurationFormatUtils.formatPeriodISO(5000, 2000);
}

@Test(expected = IllegalArgumentException.class)
public void testFormatPeriodeStartGreaterEnd() throws Exception {
    DurationFormatUtils.formatPeriod(5000, 2500, "yy/MM");
}
```