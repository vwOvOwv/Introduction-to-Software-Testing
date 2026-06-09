# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `f43534ec04d4c4bae666033e2041ecde21c19a56`
- B: `744a8c30c6e49962b5b0b9fc14a2cccbefdd1cd9`
- test: `src/test/java/org/apache/commons/lang3/RegExUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RegExUtils.java']`
- old_test_mode: `methods`
- user_chars: `19518`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5584, 'completion_tokens': 2440, 'total_tokens': 8024}`

---

- 新增 `testRemoveAll`，覆盖新增的 `removeAll(CharSequence, Pattern)` 重载并通过强转避免调用已废弃的 `String` 重载。
- 新增 `testRemoveAllDeprecated`，保留旧 `removeAll(String, Pattern)` 行为断言以对应生产代码中被标记为 deprecated 的兼容方法。
- 删除旧的 `testRemoveAll_StringPattern`，其职责被新的 CharSequence 与 deprecated 两个测试拆分。
- 新增 `testRemoveFirst`，覆盖新增的 `removeFirst(CharSequence, Pattern)` 重载并通过强转选择新 API。
- 新增 `testRemoveFirstDeprecated`，保留旧 `removeFirst(String, Pattern)` 行为断言。
- 删除旧的 `testRemoveFirst_StringPattern`，其职责被新的 CharSequence 与 deprecated 两个测试拆分。
- 新增 `testReplaceFirst`，覆盖签名变更后的 `replaceFirst(CharSequence, Pattern, String)`。
- 新增 `testReplaceFirstDeprecated`，保留旧 `replaceFirst(String, Pattern, String)` 兼容方法断言。
- 删除旧的 `testReplaceFirst_StringPatternString`，其职责被新的 CharSequence 与 deprecated 两个测试拆分。
- 不需要调整 import，现有 `Pattern`、`Test` 和断言静态导入即可满足新增测试。

```java
// DELETE_TESTS_START
testRemoveAll_StringPattern
testRemoveFirst_StringPattern
testReplaceFirst_StringPatternString
// DELETE_TESTS_END

    @Test
    public void testRemoveAll() {
        assertNull(RegExUtils.removeAll((CharSequence) null, Pattern.compile("")));
        assertEquals("any", RegExUtils.removeAll((CharSequence) "any", (Pattern) null));

        assertEquals("any", RegExUtils.removeAll((CharSequence) "any", Pattern.compile("")));
        assertEquals("", RegExUtils.removeAll((CharSequence) "any", Pattern.compile(".*")));
        assertEquals("", RegExUtils.removeAll((CharSequence) "any", Pattern.compile(".+")));
        assertEquals("", RegExUtils.removeAll((CharSequence) "any", Pattern.compile(".?")));

        assertEquals("A\nB", RegExUtils.removeAll((CharSequence) "A<__>\n<__>B", Pattern.compile("<.*>")));
        assertEquals("AB", RegExUtils.removeAll((CharSequence) "A<__>\n<__>B", Pattern.compile("(?s)<.*>")));
        assertEquals("ABC123", RegExUtils.removeAll((CharSequence) "ABCabc123abc", Pattern.compile("[a-z]")));

        assertEquals("AB", RegExUtils.removeAll((CharSequence) "A<__>\n<__>B", Pattern.compile("<.*>", Pattern.DOTALL)));
        assertEquals("AB", RegExUtils.removeAll((CharSequence) "A<__>\\n<__>B", Pattern.compile("<.*>")));
        assertEquals("", RegExUtils.removeAll((CharSequence) "<A>x\\ny</A>", Pattern.compile("<A>.*</A>")));
        assertEquals("", RegExUtils.removeAll((CharSequence) "<A>\nxy\n</A>", Pattern.compile("<A>.*</A>", Pattern.DOTALL)));
    }

    @Test
    public void testRemoveAllDeprecated() {
        assertNull(RegExUtils.removeAll(null, Pattern.compile("")));
        assertEquals("any", RegExUtils.removeAll("any", (Pattern) null));

        assertEquals("any", RegExUtils.removeAll("any", Pattern.compile("")));
        assertEquals("", RegExUtils.removeAll("any", Pattern.compile(".*")));
        assertEquals("", RegExUtils.removeAll("any", Pattern.compile(".+")));
        assertEquals("", RegExUtils.removeAll("any", Pattern.compile(".?")));

        assertEquals("A\nB", RegExUtils.removeAll("A<__>\n<__>B", Pattern.compile("<.*>")));
        assertEquals("AB", RegExUtils.removeAll("A<__>\n<__>B", Pattern.compile("(?s)<.*>")));
        assertEquals("ABC123", RegExUtils.removeAll("ABCabc123abc", Pattern.compile("[a-z]")));

        assertEquals("AB", RegExUtils.removeAll("A<__>\n<__>B", Pattern.compile("<.*>", Pattern.DOTALL)));
        assertEquals("AB", RegExUtils.removeAll("A<__>\\n<__>B", Pattern.compile("<.*>")));
        assertEquals("", RegExUtils.removeAll("<A>x\\ny</A>", Pattern.compile("<A>.*</A>")));
        assertEquals("", RegExUtils.removeAll("<A>\nxy\n</A>", Pattern.compile("<A>.*</A>", Pattern.DOTALL)));
    }

    @Test
    public void testRemoveFirst() {
        assertNull(RegExUtils.removeFirst((CharSequence) null, Pattern.compile("")));
        assertEquals("any", RegExUtils.removeFirst((CharSequence) "any", (Pattern) null));

        assertEquals("any", RegExUtils.removeFirst((CharSequence) "any", Pattern.compile("")));
        assertEquals("", RegExUtils.removeFirst((CharSequence) "any", Pattern.compile(".*")));
        assertEquals("", RegExUtils.removeFirst((CharSequence) "any", Pattern.compile(".+")));
        assertEquals("bc", RegExUtils.removeFirst((CharSequence) "abc", Pattern.compile(".?")));

        assertEquals("A\n<__>B", RegExUtils.removeFirst((CharSequence) "A<__>\n<__>B", Pattern.compile("<.*>")));
        assertEquals("AB", RegExUtils.removeFirst((CharSequence) "A<__>\n<__>B", Pattern.compile("(?s)<.*>")));
        assertEquals("ABCbc123", RegExUtils.removeFirst((CharSequence) "ABCabc123", Pattern.compile("[a-z]")));
        assertEquals("ABC123abc", RegExUtils.removeFirst((CharSequence) "ABCabc123abc", Pattern.compile("[a-z]+")));
    }

    @Test
    public void testRemoveFirstDeprecated() {
        assertNull(RegExUtils.removeFirst(null, Pattern.compile("")));
        assertEquals("any", RegExUtils.removeFirst("any", (Pattern) null));

        assertEquals("any", RegExUtils.removeFirst("any", Pattern.compile("")));
        assertEquals("", RegExUtils.removeFirst("any", Pattern.compile(".*")));
        assertEquals("", RegExUtils.removeFirst("any", Pattern.compile(".+")));
        assertEquals("bc", RegExUtils.removeFirst("abc", Pattern.compile(".?")));

        assertEquals("A\n<__>B", RegExUtils.removeFirst("A<__>\n<__>B", Pattern.compile("<.*>")));
        assertEquals("AB", RegExUtils.removeFirst("A<__>\n<__>B", Pattern.compile("(?s)<.*>")));
        assertEquals("ABCbc123", RegExUtils.removeFirst("ABCabc123", Pattern.compile("[a-z]")));
        assertEquals("ABC123abc", RegExUtils.removeFirst("ABCabc123abc", Pattern.compile("[a-z]+")));
    }

    @Test
    public void testReplaceFirst() {
        assertNull(RegExUtils.replaceFirst((CharSequence) null, Pattern.compile(""), ""));

        assertEquals("any", RegExUtils.replaceFirst((CharSequence) "any", (Pattern) null, ""));
        assertEquals("any", RegExUtils.replaceFirst((CharSequence) "any", Pattern.compile(""), null));

        assertEquals("zzz", RegExUtils.replaceFirst((CharSequence) "", Pattern.compile(""), "zzz"));
        assertEquals("zzz", RegExUtils.replaceFirst((CharSequence) "", Pattern.compile(".*"), "zzz"));
        assertEquals("", RegExUtils.replaceFirst((CharSequence) "", Pattern.compile(".+"), "zzz"));
        assertEquals("ZZabc", RegExUtils.replaceFirst((CharSequence) "abc", Pattern.compile(""), "ZZ"));

        assertEquals("z\n<__>", RegExUtils.replaceFirst((CharSequence) "<__>\n<__>", Pattern.compile("<.*>"), "z"));
        assertEquals("z", RegExUtils.replaceFirst((CharSequence) "<__>\n<__>", Pattern.compile("(?s)<.*>"), "z"));

        assertEquals("ABC_bc123", RegExUtils.replaceFirst((CharSequence) "ABCabc123", Pattern.compile("[a-z]"), "_"));
        assertEquals("ABC_123abc", RegExUtils.replaceFirst((CharSequence) "ABCabc123abc", Pattern.compile("[^A-Z0-9]+"), "_"));
        assertEquals("ABC123abc", RegExUtils.replaceFirst((CharSequence) "ABCabc123abc", Pattern.compile("[^A-Z0-9]+"), ""));
        assertEquals("Lorem_ipsum  dolor   sit", RegExUtils.replaceFirst((CharSequence) "Lorem ipsum  dolor   sit", Pattern.compile("( +)([a-z]+)"), "_$2"));
    }

    @Test
    public void testReplaceFirstDeprecated() {
        assertNull(RegExUtils.replaceFirst(null, Pattern.compile(""), ""));

        assertEquals("any", RegExUtils.replaceFirst("any", (Pattern) null, ""));
        assertEquals("any", RegExUtils.replaceFirst("any", Pattern.compile(""), null));

        assertEquals("zzz", RegExUtils.replaceFirst("", Pattern.compile(""), "zzz"));
        assertEquals("zzz", RegExUtils.replaceFirst("", Pattern.compile(".*"), "zzz"));
        assertEquals("", RegExUtils.replaceFirst("", Pattern.compile(".+"), "zzz"));
        assertEquals("ZZabc", RegExUtils.replaceFirst("abc", Pattern.compile(""), "ZZ"));

        assertEquals("z\n<__>", RegExUtils.replaceFirst("<__>\n<__>", Pattern.compile("<.*>"), "z"));
        assertEquals("z", RegExUtils.replaceFirst("<__>\n<__>", Pattern.compile("(?s)<.*>"), "z"));

        assertEquals("ABC_bc123", RegExUtils.replaceFirst("ABCabc123", Pattern.compile("[a-z]"), "_"));
        assertEquals("ABC_123abc", RegExUtils.replaceFirst("ABCabc123abc", Pattern.compile("[^A-Z0-9]+"), "_"));
        assertEquals("ABC123abc", RegExUtils.replaceFirst("ABCabc123abc", Pattern.compile("[^A-Z0-9]+"), ""));
        assertEquals("Lorem_ipsum  dolor   sit", RegExUtils.replaceFirst("Lorem ipsum  dolor   sit", Pattern.compile("( +)([a-z]+)"), "_$2"));
    }
```