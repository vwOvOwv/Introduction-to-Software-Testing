# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `80f198826443bec65bf032e729d40c3b6cb2a665`
- B: `c3d65461a327b98ce5f582c45a48b6bb2b21d03d`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `125385`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 31612, 'completion_tokens': 2170, 'total_tokens': 33782, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1657}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 31228}`

---

- 新增 `testWrap_StringChar` 和 `testWrap_StringString` 两个 `@Test` 方法，对应生产代码新增的 `StringUtils.wrap(String, char)` 和 `StringUtils.wrap(String, String)` 方法。
- 无需新增或修改 import，现有 `import static org.junit.Assert.*` 已足够。
- 无需删除任何旧测试方法。

```java
// -----------------------------------------------------------------------

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