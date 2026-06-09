# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `6e0c4f9cc9df28853afc025d33ca6512b292926f`
- B: `e7d001f1b77c382f99ee7fe01d8563d8219697df`
- test: `src/test/java/org/apache/commons/lang3/RegExUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RegExUtils.java']`
- old_test_mode: `methods`
- user_chars: `6040`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2063, 'completion_tokens': 851, 'total_tokens': 2914}`

---

- 将删除旧的 `testRemovePattern_StringString`，因为 `removePattern(String, String)` 已被标记为 deprecated，并新增了 `removePattern(CharSequence, String)` 重载。
- 将新增 `testRemovePattern`，显式以 `CharSequence` 调用新 API，覆盖原有断言。
- 将新增 `testRemovePatternDeprecated`，保留对 deprecated `String` 重载的兼容性测试。
- 不需要调整 import。

```java
// DELETE_TESTS_START
testRemovePattern_StringString
// DELETE_TESTS_END

    @Test
    public void testRemovePattern() {
        assertNull(RegExUtils.removePattern((CharSequence) null, ""));
        assertEquals("any", RegExUtils.removePattern((CharSequence) "any", (String) null));

        assertEquals("", RegExUtils.removePattern((CharSequence) "", ""));
        assertEquals("", RegExUtils.removePattern((CharSequence) "", ".*"));
        assertEquals("", RegExUtils.removePattern((CharSequence) "", ".+"));

        assertEquals("AB", RegExUtils.removePattern((CharSequence) "A<__>\n<__>B", "<.*>"));
        assertEquals("AB", RegExUtils.removePattern((CharSequence) "A<__>\\n<__>B", "<.*>"));
        assertEquals("", RegExUtils.removePattern((CharSequence) "<A>x\\ny</A>", "<A>.*</A>"));
        assertEquals("", RegExUtils.removePattern((CharSequence) "<A>\nxy\n</A>", "<A>.*</A>"));

        assertEquals("ABC123", RegExUtils.removePattern((CharSequence) "ABCabc123", "[a-z]"));
    }

    @Test
    public void testRemovePatternDeprecated() {
        assertNull(RegExUtils.removePattern(null, ""));
        assertEquals("any", RegExUtils.removePattern("any", (String) null));

        assertEquals("", RegExUtils.removePattern("", ""));
        assertEquals("", RegExUtils.removePattern("", ".*"));
        assertEquals("", RegExUtils.removePattern("", ".+"));

        assertEquals("AB", RegExUtils.removePattern("A<__>\n<__>B", "<.*>"));
        assertEquals("AB", RegExUtils.removePattern("A<__>\\n<__>B", "<.*>"));
        assertEquals("", RegExUtils.removePattern("<A>x\\ny</A>", "<A>.*</A>"));
        assertEquals("", RegExUtils.removePattern("<A>\nxy\n</A>", "<A>.*</A>"));

        assertEquals("ABC123", RegExUtils.removePattern("ABCabc123", "[a-z]"));
    }
```