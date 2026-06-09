# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `80f198826443bec65bf032e729d40c3b6cb2a665`
- B: `c3d65461a327b98ce5f582c45a48b6bb2b21d03d`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `125385`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 30977, 'completion_tokens': 762, 'total_tokens': 31739}`

---

- 新增 `@Test testWrap_StringChar`：覆盖生产代码新增的 `StringUtils.wrap(String, char)` 对 `null`、空串、`\0` 以及不同包裹字符的行为；无需调整 import。
- 新增 `@Test testWrap_StringString`：覆盖生产代码新增的 `StringUtils.wrap(String, String)` 对 `null`、空串、空包裹串以及不同包裹字符串的行为；无需调整 import。

```java
    @Test
    public void testWrap_StringChar() {
        assertNull(StringUtils.wrap(null, null));
        assertNull(StringUtils.wrap(null, '\0'));
        assertNull(StringUtils.wrap(null, '1'));

        assertEquals(null, StringUtils.wrap(null, null));
        assertEquals("", StringUtils.wrap("", '\0'));
        assertEquals("xabx", StringUtils.wrap("ab", 'x'));
        assertEquals("\"ab\"", StringUtils.wrap("ab", '\"'));
        assertEquals("\"\"ab\"\"", StringUtils.wrap("\"ab\"", '\"'));
        assertEquals("'ab'", StringUtils.wrap("ab", '\''));
        assertEquals("''abcd''", StringUtils.wrap("'abcd'", '\''));
        assertEquals("'\"abcd\"'", StringUtils.wrap("\"abcd\"", '\''));
        assertEquals("\"'abcd'\"", StringUtils.wrap("'abcd'", '\"'));
    }

    @Test
    public void testWrap_StringString() {
        assertNull(StringUtils.wrap(null, null));
        assertNull(StringUtils.wrap(null, ""));
        assertNull(StringUtils.wrap(null, "1"));

        assertEquals(null, StringUtils.wrap(null, null));
        assertEquals("", StringUtils.wrap("", ""));
        assertEquals("ab", StringUtils.wrap("ab", null));
        assertEquals("xabx", StringUtils.wrap("ab", "x"));
        assertEquals("\"ab\"", StringUtils.wrap("ab", "\""));
        assertEquals("\"\"ab\"\"", StringUtils.wrap("\"ab\"", "\""));
        assertEquals("'ab'", StringUtils.wrap("ab", "'"));
        assertEquals("''abcd''", StringUtils.wrap("'abcd'", "'"));
        assertEquals("'\"abcd\"'", StringUtils.wrap("\"abcd\"", "'"));
        assertEquals("\"'abcd'\"", StringUtils.wrap("'abcd'", "\""));
    }
```