# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `648eebba22d6398a01b0924975bedced8469ac80`
- B: `eaa9269ac80c2a957cabed0c46173149a4137c24`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `8845`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2939, 'completion_tokens': 3877, 'total_tokens': 6816, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2900}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2555}`

---

- 将修改 @Test 方法 `testWrap_StringChar`：移除 `wrap(null, null)` 相关断言，并将 `wrap("\"ab\"", '\"')` 和 `wrap("'abcd'", '\'')` 的期望值修正为不重复包裹的格式（与 `wrapIfMissing` 行为保持一致）。
- 将新增 @Test 方法 `testWrapIfMissing_StringChar`：覆盖新增的 `StringUtils.wrapIfMissing(String, char)` 方法的常见场景与边界。
- 将新增 @Test 方法 `testWrapIfMissing_StringString`：覆盖新增的 `StringUtils.wrapIfMissing(String, String)` 方法的常见场景与边界。
- 无需调整 import 语句。

```java
@Test
public void testWrap_StringChar() {
    assertNull(StringUtils.wrap(null, '\0'));
    assertNull(StringUtils.wrap(null, '1'));

    assertEquals("", StringUtils.wrap("", '\0'));
    assertEquals("xabx", StringUtils.wrap("ab", 'x'));
    assertEquals("\"ab\"", StringUtils.wrap("ab", '\"'));
    assertEquals("\"ab\"", StringUtils.wrap("\"ab\"", '\"'));
    assertEquals("'ab'", StringUtils.wrap("ab", '\''));
    assertEquals("'abcd'", StringUtils.wrap("'abcd'", '\''));
    assertEquals("'\"abcd\"'", StringUtils.wrap("\"abcd\"", '\''));
    assertEquals("\"'abcd'\"", StringUtils.wrap("'abcd'", '\"'));
}

@Test
public void testWrapIfMissing_StringChar() {
    assertNull(StringUtils.wrapIfMissing(null, '\0'));
    assertNull(StringUtils.wrapIfMissing(null, '1'));

    assertEquals("", StringUtils.wrapIfMissing("", '\0'));
    assertEquals("xabx", StringUtils.wrapIfMissing("ab", 'x'));
    assertEquals("\"ab\"", StringUtils.wrapIfMissing("ab", '\"'));
    assertEquals("\"ab\"", StringUtils.wrapIfMissing("\"ab\"", '\"'));
    assertEquals("'ab'", StringUtils.wrapIfMissing("ab", '\''));
    assertEquals("'abcd'", StringUtils.wrapIfMissing("'abcd'", '\''));
    assertEquals("'\"abcd\"'", StringUtils.wrapIfMissing("\"abcd\"", '\''));
    assertEquals("\"'abcd'\"", StringUtils.wrapIfMissing("'abcd'", '\"'));
    assertEquals("/x/", StringUtils.wrapIfMissing("x", '/'));
    assertEquals("/x/y/z/", StringUtils.wrapIfMissing("x/y/z", '/'));
    assertEquals("/x/y/z/", StringUtils.wrapIfMissing("/x/y/z", '/'));
    assertEquals("/x/y/z/", StringUtils.wrapIfMissing("x/y/z/", '/'));
    assertEquals("/", StringUtils.wrapIfMissing("/", '/'));
}

@Test
public void testWrapIfMissing_StringString() {
    assertNull(StringUtils.wrapIfMissing(null, "\0"));
    assertNull(StringUtils.wrapIfMissing(null, "1"));

    assertEquals("", StringUtils.wrapIfMissing("", "\0"));
    assertEquals("xabx", StringUtils.wrapIfMissing("ab", "x"));
    assertEquals("\"ab\"", StringUtils.wrapIfMissing("ab", "\""));
    assertEquals("\"ab\"", StringUtils.wrapIfMissing("\"ab\"", "\""));
    assertEquals("'ab'", StringUtils.wrapIfMissing("ab", "\'"));
    assertEquals("'abcd'", StringUtils.wrapIfMissing("'abcd'", "\'"));
    assertEquals("'\"abcd\"'", StringUtils.wrapIfMissing("\"abcd\"", "\'"));
    assertEquals("\"'abcd'\"", StringUtils.wrapIfMissing("'abcd'", "\""));
    assertEquals("/x/", StringUtils.wrapIfMissing("x", "/"));
    assertEquals("/x/y/z/", StringUtils.wrapIfMissing("x/y/z", "/"));
    assertEquals("/x/y/z/", StringUtils.wrapIfMissing("/x/y/z", "/"));
    assertEquals("/x/y/z/", StringUtils.wrapIfMissing("x/y/z/", "/"));
    assertEquals("/", StringUtils.wrapIfMissing("/", "/"));
    assertEquals("ab/ab", StringUtils.wrapIfMissing("/", "ab"));
    assertEquals("ab/ab", StringUtils.wrapIfMissing("ab/ab", "ab"));
}
```