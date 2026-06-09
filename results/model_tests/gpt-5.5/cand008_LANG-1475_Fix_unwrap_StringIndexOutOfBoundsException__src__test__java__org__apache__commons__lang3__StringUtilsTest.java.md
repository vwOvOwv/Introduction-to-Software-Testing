# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e610367507d69947c752cf2659162afbde4ec7e8`
- B: `06aea7e74cfe4a1578cb76672f1562132090c205`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `165538`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 40582, 'completion_tokens': 723, 'total_tokens': 41305}`

---

- 修改 `testUnwrap_StringChar`：生产代码对长度为 1 的字符串不再 unwrap，并支持 `"aa"` 使用单字符 token unwrap 为空串，因此在该测试中补充对应断言；无需调整 import。
- 修改 `testUnwrap_StringString`：生产代码对长度为 1 的字符串不再 unwrap，并支持 `"aa"` 使用字符串 token unwrap 为空串，因此在该测试中补充对应断言；无需调整 import。

```java
@Test
public void testUnwrap_StringChar() {
    assertNull(StringUtils.unwrap(null, null));
    assertNull(StringUtils.unwrap(null, CharUtils.NUL));
    assertNull(StringUtils.unwrap(null, '1'));

    assertEquals("abc", StringUtils.unwrap("abc", null));
    assertEquals("a", StringUtils.unwrap("a", "a"));
    assertEquals("", StringUtils.unwrap("aa", "a"));
    assertEquals("abc", StringUtils.unwrap("\'abc\'", '\''));
    assertEquals("abc", StringUtils.unwrap("AabcA", 'A'));
    assertEquals("AabcA", StringUtils.unwrap("AAabcAA", 'A'));
    assertEquals("abc", StringUtils.unwrap("abc", 'b'));
    assertEquals("#A", StringUtils.unwrap("#A", '#'));
    assertEquals("A#", StringUtils.unwrap("A#", '#'));
    assertEquals("ABA", StringUtils.unwrap("AABAA", 'A'));
}

@Test
public void testUnwrap_StringString() {
    assertNull(StringUtils.unwrap(null, null));
    assertNull(StringUtils.unwrap(null, ""));
    assertNull(StringUtils.unwrap(null, "1"));

    assertEquals("abc", StringUtils.unwrap("abc", null));
    assertEquals("abc", StringUtils.unwrap("abc", ""));
    assertEquals("a", StringUtils.unwrap("a", "a"));
    assertEquals("", StringUtils.unwrap("aa", "a"));
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
```