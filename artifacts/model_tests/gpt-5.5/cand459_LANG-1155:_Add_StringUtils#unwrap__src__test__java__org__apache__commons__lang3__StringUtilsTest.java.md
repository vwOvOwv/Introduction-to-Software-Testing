# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `d79e43216faba4b3e73536915bfddc550cc0f20f`
- B: `ff4497aff8cc9de4e0b2c6e5e23e5b6550f76f29`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `8976`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2776, 'completion_tokens': 995, 'total_tokens': 3771}`

---

- 修改/重命名 `testUnwrapString_String` 为 `testUnwrap_StringString`，补充 `wrapToken` 为 `null`/空串时返回原字符串的断言，并去除重复断言。
- 修改/重命名 `testUnwrapString_Char` 为 `testUnwrap_StringChar`，补充未完整包裹、空字符以及边界字符场景的断言以匹配新的 `unwrap` 行为。
- 不需要调整 import。

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