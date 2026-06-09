# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9bc57f7fed72c09468588f2f5ac5d5d503bc845c`
- B: `6b81f9e6cf42eae235c7ab505d967f60a42d7d66`
- test: `src/test/java/org/apache/commons/lang3/RegExUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RegExUtils.java']`
- old_test_mode: `methods`
- user_chars: `8692`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2788, 'completion_tokens': 1015, 'total_tokens': 3803}`

---

- 新增 `testReplacePattern`，用于覆盖新增的 `replacePattern(CharSequence, String, String)` 重载，并通过 `(CharSequence)` 强制选择新 API。
- 将旧的 `testReplacePattern_StringStringString` 替换为 `testReplacePatternDeprecated`，继续覆盖已废弃的 `replacePattern(String, String, String)` 行为。
- 不需要调整 import。

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