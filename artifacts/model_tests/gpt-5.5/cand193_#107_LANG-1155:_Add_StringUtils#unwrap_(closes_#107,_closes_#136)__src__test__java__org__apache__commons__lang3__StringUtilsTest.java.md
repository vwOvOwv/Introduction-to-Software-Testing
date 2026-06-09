# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `a069c490e8119189fa2b43d3b597b79b3d42a367`
- B: `d79e43216faba4b3e73536915bfddc550cc0f20f`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `161067`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 39543, 'completion_tokens': 656, 'total_tokens': 40199}`

---

- 新增 `testUnwrapString_String`，对应生产代码新增 `StringUtils.unwrap(String, String)`，覆盖 null/空 token、单字符与多字符包裹、未正确包裹时返回原字符串等行为；无需调整 import。
- 新增 `testUnwrapString_Char`，对应生产代码新增 `StringUtils.unwrap(String, char)`，覆盖 null、`\0`、正常字符包裹以及重复边界字符的行为；无需调整 import。

```java
    @Test
    public void testUnwrapString_String() {
        assertNull(StringUtils.unwrap(null, null));
        assertNull(StringUtils.unwrap(null, ""));
        assertNull(StringUtils.unwrap(null, "1"));
        assertEquals("abc", StringUtils.unwrap("\'abc\'", "\'"));
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
    public void testUnwrapString_Char() {
        assertNull(StringUtils.unwrap(null, null));
        assertNull(StringUtils.unwrap(null, '\0'));
        assertNull(StringUtils.unwrap(null, '1'));
        assertEquals("abc", StringUtils.unwrap("\'abc\'", '\''));
        assertEquals("abc", StringUtils.unwrap("AabcA", 'A'));
        assertEquals("AabcA", StringUtils.unwrap("AAabcAA", 'A'));
    }
```