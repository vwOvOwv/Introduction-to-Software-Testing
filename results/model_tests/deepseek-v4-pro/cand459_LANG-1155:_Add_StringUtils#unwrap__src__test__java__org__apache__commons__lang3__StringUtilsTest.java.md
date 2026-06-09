# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `d79e43216faba4b3e73536915bfddc550cc0f20f`
- B: `ff4497aff8cc9de4e0b2c6e5e23e5b6550f76f29`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `8976`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2837, 'completion_tokens': 3107, 'total_tokens': 5944, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2420}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2453}`

---

- 将删除旧测试方法 `testUnwrapString_String` 和 `testUnwrapString_Char`，因为它们的命名不符合更新后的规范，且断言已不完整。
- 将新增测试方法 `testUnwrap_StringString`，该方法重命名并补充了对 null 或空 wrapToken 的断言，与生产代码空 token 直接返回原始字符串的行为一致。
- 将新增测试方法 `testUnwrap_StringChar`，该方法重命名并添加了对非包裹字符、不完整包裹以及通过 null 调用 String 重载版本的新增断言，覆盖生产代码新增的边界情况。
- 无需调整 import，现有静态导入和 `StringUtils` 导入已满足需求。

```java
// DELETE_TESTS_START
testUnwrapString_String
testUnwrapString_Char
// DELETE_TESTS_END

    @Test
    public void testUnwrap_StringString() {
        assertNull(StringUtils.unwrap(null, null));
        assertNull(StringUtils.unwrap(null, ""));
        assertNull(StringUtils.unwrap(null, "1"));
        assertEquals("abc", StringUtils.unwrap("abc", null));
        assertEquals("abc", StringUtils.unwrap("abc", ""));
        assertEquals("abc", StringUtils.unwrap("\'abc\'", "\'"));
        assertEquals("abc", StringUtils.unwrap("\"abc\"", "\""));
        assertEquals("abc\"xyz", StringUtils.unwrap("\"abc\"xyz\"", "\""));
        assertEquals("abc\"xyz\"", StringUtils.unwrap("\"abc\"xyz\"\"", "\""));
        assertEquals("abc\'xyz\'", StringUtils.unwrap("\"abc\'xyz\'\"", "\""));
        assertEquals("\"abc\'xyz\'\"", StringUtils.unwrap("AA\"abc\'xyz\'\"AA", "AA"));
        assertEquals("\"abc\'xyz\'\"", StringUtils.unwrap("123\"abc\'xyz\'\"123", "123"));
        assertEquals("AA\"abc\'xyz\'\"", StringUtils.unwrap("AA\"abc\'xyz\'\"", "AA"));
        assertEquals("AA\"abc\'xyz\'\"AA", StringUtils.unwrap("AAA\"abc\'xyz\'\"AAA", "A"));
        assertEquals("\"abc\'xyz\'\"AA", StringUtils.unwrap("\"abc\'xyz\'\"AA", "AA"));
    }

    @Test
    public void testUnwrap_StringChar() {
        assertNull(StringUtils.unwrap(null, null));
        assertNull(StringUtils.unwrap(null, '\0'));
        assertNull(StringUtils.unwrap(null, '1'));
        assertEquals("abc", StringUtils.unwrap("abc", null));
        assertEquals("abc", StringUtils.unwrap("\'abc\'", '\''));
        assertEquals("abc", StringUtils.unwrap("AabcA", 'A'));
        assertEquals("AabcA", StringUtils.unwrap("AAabcAA", 'A'));
        assertEquals("abc", StringUtils.unwrap("abc", 'b'));
        assertEquals("#A", StringUtils.unwrap("#A", '#'));
        assertEquals("A#", StringUtils.unwrap("A#", '#'));
        assertEquals("ABA", StringUtils.unwrap("AABAA", 'A'));
    }
```