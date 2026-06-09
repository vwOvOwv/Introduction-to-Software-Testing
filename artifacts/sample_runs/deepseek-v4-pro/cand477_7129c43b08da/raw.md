# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `5d4916933d6259f1e698662bc7e85ed4db461d61`
- B: `7129c43b08da58e1c907dd2b90bb58e7a09bf85c`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `17261`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 4908, 'completion_tokens': 3920, 'total_tokens': 8828, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2044}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 4524}`

---

- 根据测试 diff，需将 `testReplacePattern` 重命名为 `testReplacePattern_StringStringString`，方法体不变。
- 将 `testRemovePattern` 重命名为 `testRemovePattern_StringString`，方法体不变。
- 将 `testReplaceAll` 重命名为 `testReplaceAll_StringStringString`，方法体不变。
- 将 `testReplaceFirst` 重命名为 `testReplaceFirst_StringStringString`，方法体不变。
- 将 `testRemoveAll` 重命名为 `testRemoveAll_StringString`，方法体不变。
- 将 `testRemoveFirst` 重命名为 `testRemoveFirst_StringString`，方法体不变。
- 无需调整 import，因为测试中未直接使用 `RegExUtils`。

```java
// DELETE_TESTS_START
testReplacePattern
testRemovePattern
testReplaceAll
testReplaceFirst
testRemoveAll
testRemoveFirst
// DELETE_TESTS_END

    @Test
    public void testReplacePattern_StringStringString() {
        assertNull(StringUtils.replacePattern(null, "", ""));
        assertEquals("any", StringUtils.replacePattern("any", null, ""));
        assertEquals("any", StringUtils.replacePattern("any", "", null));

        assertEquals("zzz", StringUtils.replacePattern("", "", "zzz"));
        assertEquals("zzz", StringUtils.replacePattern("", ".*", "zzz"));
        assertEquals("", StringUtils.replacePattern("", ".+", "zzz"));

        assertEquals("z", StringUtils.replacePattern("<__>\n<__>", "<.*>", "z"));
        assertEquals("z", StringUtils.replacePattern("<__>\\n<__>", "<.*>", "z"));
        assertEquals("X", StringUtils.replacePattern("<A>\nxy\n</A>", "<A>.*</A>", "X"));

        assertEquals("ABC___123", StringUtils.replacePattern("ABCabc123", "[a-z]", "_"));
        assertEquals("ABC_123", StringUtils.replacePattern("ABCabc123", "[^A-Z0-9]+", "_"));
        assertEquals("ABC123", StringUtils.replacePattern("ABCabc123", "[^A-Z0-9]+", ""));
        assertEquals("Lorem_ipsum_dolor_sit",
                     StringUtils.replacePattern("Lorem ipsum  dolor   sit", "( +)([a-z]+)", "_$2"));
    }

    @Test
    public void testRemovePattern_StringString() {
        assertNull(StringUtils.removePattern(null, ""));
        assertEquals("any", StringUtils.removePattern("any", null));

        assertEquals("", StringUtils.removePattern("", ""));
        assertEquals("", StringUtils.removePattern("", ".*"));
        assertEquals("", StringUtils.removePattern("", ".+"));

        assertEquals("AB", StringUtils.removePattern("A<__>\n<__>B", "<.*>"));
        assertEquals("AB", StringUtils.removePattern("A<__>\\n<__>B", "<.*>"));
        assertEquals("", StringUtils.removePattern("<A>x\\ny</A>", "<A>.*</A>"));
        assertEquals("", StringUtils.removePattern("<A>\nxy\n</A>", "<A>.*</A>"));

        assertEquals("ABC123", StringUtils.removePattern("ABCabc123", "[a-z]"));
    }

    @Test
    public void testReplaceAll_StringStringString() {
        assertNull(StringUtils.replaceAll(null, "", ""));

        assertEquals("any", StringUtils.replaceAll("any", null, ""));
        assertEquals("any", StringUtils.replaceAll("any", "", null));

        assertEquals("zzz", StringUtils.replaceAll("", "", "zzz"));
        assertEquals("zzz", StringUtils.replaceAll("", ".*", "zzz"));
        assertEquals("", StringUtils.replaceAll("", ".+", "zzz"));
        assertEquals("ZZaZZbZZcZZ", StringUtils.replaceAll("abc", "", "ZZ"));

        assertEquals("z\nz", StringUtils.replaceAll("<__>\n<__>", "<.*>", "z"));
        assertEquals("z", StringUtils.replaceAll("<__>\n<__>", "(?s)<.*>", "z"));

        assertEquals("ABC___123", StringUtils.replaceAll("ABCabc123", "[a-z]", "_"));
        assertEquals("ABC_123", StringUtils.replaceAll("ABCabc123", "[^A-Z0-9]+", "_"));
        assertEquals("ABC123", StringUtils.replaceAll("ABCabc123", "[^A-Z0-9]+", ""));
        assertEquals("Lorem_ipsum_dolor_sit",
                     StringUtils.replaceAll("Lorem ipsum  dolor   sit", "( +)([a-z]+)", "_$2"));

        try {
            StringUtils.replaceAll("any", "{badRegexSyntax}", "");
            fail("StringUtils.replaceAll expecting PatternSyntaxException");
        } catch (final PatternSyntaxException ex) {
            // empty
        }
    }

    @Test
    public void testReplaceFirst_StringStringString() {
        assertNull(StringUtils.replaceFirst(null, "", ""));

        assertEquals("any", StringUtils.replaceFirst("any", null, ""));
        assertEquals("any", StringUtils.replaceFirst("any", "", null));

        assertEquals("zzz", StringUtils.replaceFirst("", "", "zzz"));
        assertEquals("zzz", StringUtils.replaceFirst("", ".*", "zzz"));
        assertEquals("", StringUtils.replaceFirst("", ".+", "zzz"));
        assertEquals("ZZabc", StringUtils.replaceFirst("abc", "", "ZZ"));

        assertEquals("z\n<__>", StringUtils.replaceFirst("<__>\n<__>", "<.*>", "z"));
        assertEquals("z", StringUtils.replaceFirst("<__>\n<__>", "(?s)<.*>", "z"));

        assertEquals("ABC_bc123", StringUtils.replaceFirst("ABCabc123", "[a-z]", "_"));
        assertEquals("ABC_123abc", StringUtils.replaceFirst("ABCabc123abc", "[^A-Z0-9]+", "_"));
        assertEquals("ABC123abc", StringUtils.replaceFirst("ABCabc123abc", "[^A-Z0-9]+", ""));
        assertEquals("Lorem_ipsum  dolor   sit",
                     StringUtils.replaceFirst("Lorem ipsum  dolor   sit", "( +)([a-z]+)", "_$2"));

        try {
            StringUtils.replaceFirst("any", "{badRegexSyntax}", "");
            fail("StringUtils.replaceFirst expecting PatternSyntaxException");
        } catch (final PatternSyntaxException ex) {
            // empty
        }
    }

    @Test
    public void testRemoveAll_StringString() {
        assertNull(StringUtils.removeAll(null, ""));
        assertEquals("any", StringUtils.removeAll("any", null));

        assertEquals("any", StringUtils.removeAll("any", ""));
        assertEquals("", StringUtils.removeAll("any", ".*"));
        assertEquals("", StringUtils.removeAll("any", ".+"));
        assertEquals("", StringUtils.removeAll("any", ".?"));

        assertEquals("A\nB", StringUtils.removeAll("A<__>\n<__>B", "<.*>"));
        assertEquals("AB", StringUtils.removeAll("A<__>\n<__>B", "(?s)<.*>"));
        assertEquals("ABC123", StringUtils.removeAll("ABCabc123abc", "[a-z]"));

        try {
            StringUtils.removeAll("any", "{badRegexSyntax}");
            fail("StringUtils.removeAll expecting PatternSyntaxException");
        } catch (final PatternSyntaxException ex) {
            // empty
        }
    }

    @Test
    public void testRemoveFirst_StringString() {
        assertNull(StringUtils.removeFirst(null, ""));
        assertEquals("any", StringUtils.removeFirst("any", null));

        assertEquals("any", StringUtils.removeFirst("any", ""));
        assertEquals("", StringUtils.removeFirst("any", ".*"));
        assertEquals("", StringUtils.removeFirst("any", ".+"));
        assertEquals("bc", StringUtils.removeFirst("abc", ".?"));

        assertEquals("A\n<__>B", StringUtils.removeFirst("A<__>\n<__>B", "<.*>"));
        assertEquals("AB", StringUtils.removeFirst("A<__>\n<__>B", "(?s)<.*>"));
        assertEquals("ABCbc123", StringUtils.removeFirst("ABCabc123", "[a-z]"));
        assertEquals("ABC123abc", StringUtils.removeFirst("ABCabc123abc", "[a-z]+"));

        try {
            StringUtils.removeFirst("any", "{badRegexSyntax}");
            fail("StringUtils.removeFirst expecting PatternSyntaxException");
        } catch (final PatternSyntaxException ex) {
            // empty
        }
    }
```