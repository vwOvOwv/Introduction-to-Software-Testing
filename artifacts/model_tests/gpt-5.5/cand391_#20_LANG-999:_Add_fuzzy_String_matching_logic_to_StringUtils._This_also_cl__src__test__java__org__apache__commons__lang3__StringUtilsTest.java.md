# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `287aba5b2eff81c0f7c62cb37a6adfc5e331f99f`
- B: `b78295b4faca2fd26024a26ef4638b0dce5d40a3`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `130442`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 31856, 'completion_tokens': 659, 'total_tokens': 32515}`

---

- 新增 `testGetFuzzyDistance`，对应生产代码新增 `StringUtils.getFuzzyDistance(CharSequence, CharSequence, Locale)` 的正常评分行为。
- 新增 `testGetFuzzyDistance_NullNullNull`，对应生产代码对 `term/query` 为 `null` 时抛出 `IllegalArgumentException`。
- 新增 `testGetFuzzyDistance_StringNullLoclae`，对应生产代码对 `query` 为 `null` 时抛出 `IllegalArgumentException`。
- 新增 `testGetFuzzyDistance_NullStringLocale`，对应生产代码对 `term` 为 `null` 时抛出 `IllegalArgumentException`。
- 新增 `testGetFuzzyDistance_StringStringNull`，对应生产代码对 `locale` 为 `null` 时抛出 `IllegalArgumentException`。
- 无需调整 import，旧测试文件已包含 `java.util.Locale`、`org.junit.Test` 和 `assertEquals` 静态导入。

```java
    @Test
    public void testGetFuzzyDistance() throws Exception {
        assertEquals(0, StringUtils.getFuzzyDistance("", "", Locale.ENGLISH));
        assertEquals(0, StringUtils.getFuzzyDistance("Workshop", "b", Locale.ENGLISH));
        assertEquals(1, StringUtils.getFuzzyDistance("Room", "o", Locale.ENGLISH));
        assertEquals(1, StringUtils.getFuzzyDistance("Workshop", "w", Locale.ENGLISH));
        assertEquals(2, StringUtils.getFuzzyDistance("Workshop", "ws", Locale.ENGLISH));
        assertEquals(4, StringUtils.getFuzzyDistance("Workshop", "wo", Locale.ENGLISH));
        assertEquals(3, StringUtils.getFuzzyDistance("Apache Software Foundation", "asf", Locale.ENGLISH));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testGetFuzzyDistance_NullNullNull() throws Exception {
        StringUtils.getFuzzyDistance(null, null, null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testGetFuzzyDistance_StringNullLoclae() throws Exception {
        StringUtils.getFuzzyDistance(" ", null, Locale.ENGLISH);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testGetFuzzyDistance_NullStringLocale() throws Exception {
        StringUtils.getFuzzyDistance(null, "clear", Locale.ENGLISH);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testGetFuzzyDistance_StringStringNull() throws Exception {
        StringUtils.getFuzzyDistance(" ", "clear", null);
    }
```