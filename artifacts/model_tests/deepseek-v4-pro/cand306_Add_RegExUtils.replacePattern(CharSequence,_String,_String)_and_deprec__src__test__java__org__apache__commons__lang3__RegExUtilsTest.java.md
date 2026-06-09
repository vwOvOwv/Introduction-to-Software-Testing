# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9bc57f7fed72c09468588f2f5ac5d5d503bc845c`
- B: `6b81f9e6cf42eae235c7ab505d967f60a42d7d66`
- test: `src/test/java/org/apache/commons/lang3/RegExUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RegExUtils.java']`
- old_test_mode: `methods`
- user_chars: `8692`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2826, 'completion_tokens': 2075, 'total_tokens': 4901, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1216}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2442}`

---

- 删除旧测试方法 `testReplacePattern_StringStringString`，因为生产代码新增了 `replacePattern(CharSequence, String, String)` 重载，导致旧版本签名调用存在歧义，无法编译。
- 新增 `testReplacePattern` 方法，使用 `(CharSequence)` 强制转换调用新的 `CharSequence` 版本，以验证新重载的行为。
- 新增 `testReplacePatternDeprecated` 方法，保留对已标记 `@Deprecated` 的 `replacePattern(String, String, String)` 的调用，确保旧版行为不受影响。
- 无需调整 import 语句，`CharSequence` 来自 `java.lang` 包，已默认可用。

```java
// DELETE_TESTS_START
testReplacePattern_StringStringString
// DELETE_TESTS_END

@Test
public void testReplacePattern() {
    assertNull(RegExUtils.replacePattern((CharSequence) null, "", ""));
    assertEquals("any", RegExUtils.replacePattern((CharSequence) "any", (String) null, ""));
    assertEquals("any", RegExUtils.replacePattern((CharSequence) "any", "", null));

    assertEquals("zzz", RegExUtils.replacePattern((CharSequence) "", "", "zzz"));
    assertEquals("zzz", RegExUtils.replacePattern((CharSequence) "", ".*", "zzz"));
    assertEquals("", RegExUtils.replacePattern((CharSequence) "", ".+", "zzz"));

    assertEquals("z", RegExUtils.replacePattern((CharSequence) "<__>\n<__>", "<.*>", "z"));
    assertEquals("z", RegExUtils.replacePattern((CharSequence) "<__>\\n<__>", "<.*>", "z"));
    assertEquals("X", RegExUtils.replacePattern((CharSequence) "<A>\nxy\n</A>", "<A>.*</A>", "X"));

    assertEquals("ABC___123", RegExUtils.replacePattern((CharSequence) "ABCabc123", "[a-z]", "_"));
    assertEquals("ABC_123", RegExUtils.replacePattern((CharSequence) "ABCabc123", "[^A-Z0-9]+", "_"));
    assertEquals("ABC123", RegExUtils.replacePattern((CharSequence) "ABCabc123", "[^A-Z0-9]+", ""));
    assertEquals("Lorem_ipsum_dolor_sit", RegExUtils.replacePattern((CharSequence) "Lorem ipsum  dolor   sit", "( +)([a-z]+)", "_$2"));
}

@Test
public void testReplacePatternDeprecated() {
    assertNull(RegExUtils.replacePattern(null, "", ""));
    assertEquals("any", RegExUtils.replacePattern("any", (String) null, ""));
    assertEquals("any", RegExUtils.replacePattern("any", "", null));

    assertEquals("zzz", RegExUtils.replacePattern("", "", "zzz"));
    assertEquals("zzz", RegExUtils.replacePattern("", ".*", "zzz"));
    assertEquals("", RegExUtils.replacePattern("", ".+", "zzz"));

    assertEquals("z", RegExUtils.replacePattern("<__>\n<__>", "<.*>", "z"));
    assertEquals("z", RegExUtils.replacePattern("<__>\\n<__>", "<.*>", "z"));
    assertEquals("X", RegExUtils.replacePattern("<A>\nxy\n</A>", "<A>.*</A>", "X"));

    assertEquals("ABC___123", RegExUtils.replacePattern("ABCabc123", "[a-z]", "_"));
    assertEquals("ABC_123", RegExUtils.replacePattern("ABCabc123", "[^A-Z0-9]+", "_"));
    assertEquals("ABC123", RegExUtils.replacePattern("ABCabc123", "[^A-Z0-9]+", ""));
    assertEquals("Lorem_ipsum_dolor_sit", RegExUtils.replacePattern("Lorem ipsum  dolor   sit", "( +)([a-z]+)", "_$2"));
}
```