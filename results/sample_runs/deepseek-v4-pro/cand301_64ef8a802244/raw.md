# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `358f139d1316df2b8efd7610afa3aa68d165334f`
- B: `64ef8a80224443c81dfb198cbc567e1b2b9356a2`
- test: `src/test/java/org/apache/commons/lang3/time/DurationFormatUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DurationFormatUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `36306`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 10433, 'completion_tokens': 1817, 'total_tokens': 12250, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1426}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 10049}`

---

- 新增 @Test 方法：`testFormatNegativeDurationWords`，覆盖 `formatDurationWords` 负值检查。
- 新增 @Test 方法：`testFormatNegativeDurationHMS`，覆盖 `formatDurationHMS` 负值检查。
- 新增 @Test 方法：`testFormatNegativeDurationISO`，覆盖 `formatDurationISO` 负值检查。
- 新增 @Test 方法：`testFormatNegativeDuration`，覆盖 `formatDuration(String, boolean)` 重载的负值检查。
- 新增 @Test 方法：`testFormatPeriodISOStartGreaterEnd`，覆盖 `formatPeriodISO` 起止顺序检查。
- 新增 @Test 方法：`testFormatPeriodeStartGreaterEnd`，覆盖 `formatPeriod` 起止顺序检查。
- 无需调整 import，无需删除旧测试方法。

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