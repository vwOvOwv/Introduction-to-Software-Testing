# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `5d4916933d6259f1e698662bc7e85ed4db461d61`
- B: `7129c43b08da58e1c907dd2b90bb58e7a09bf85c`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `17261`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 4805, 'completion_tokens': 2011, 'total_tokens': 6816}`

---

- 修改 `testReplacePattern` 为 `testReplacePattern_StringStringString`，对应 `StringUtils.replacePattern` 已废弃并委托到 `RegExUtils.replacePattern`，测试内容保持兼容行为断言。
- 修改 `testRemovePattern` 为 `testRemovePattern_StringString`，对应 `StringUtils.removePattern` 已废弃并委托到 `RegExUtils.removePattern`，测试内容保持兼容行为断言。
- 修改 `testReplaceAll` 为 `testReplaceAll_StringStringString`，对应 `StringUtils.replaceAll` 已废弃并委托到 `RegExUtils.replaceAll`，测试内容保持兼容行为断言。
- 修改 `testReplaceFirst` 为 `testReplaceFirst_StringStringString`，对应 `StringUtils.replaceFirst` 已废弃并委托到 `RegExUtils.replaceFirst`，测试内容保持兼容行为断言。
- 修改 `testRemoveAll` 为 `testRemoveAll_StringString`，对应 `StringUtils.removeAll` 已废弃并委托到 `RegExUtils.removeAll`，测试内容保持兼容行为断言。
- 修改 `testRemoveFirst` 为 `testRemoveFirst_StringString`，对应 `StringUtils.removeFirst` 已废弃且签名不变，测试内容保持兼容行为断言。
- 不需要调整 import。

```java
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
```