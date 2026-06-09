# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `b4842f559f0d8b8b5a98a19b1f3795a42c1a2614`
- B: `242b815437b9a988c2ce9e980295ca8a9e302e7a`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `6419`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2119, 'completion_tokens': 860, 'total_tokens': 2979}`

---

- 修改 `@Test` 方法 `testReplaceAll_StringStringString` 为 `testReplaceAll`，并根据生产代码文档新增空正则对非空字符串的断言。
- 修改 `@Test` 方法 `testReplaceFirst_StringStringString` 为 `testReplaceFirst`，并根据生产代码文档新增空正则对非空字符串的断言。
- 不需要调整 import。

```java
    @Test
    public void testReplaceAll() {
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
    public void testReplaceFirst() {
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
```