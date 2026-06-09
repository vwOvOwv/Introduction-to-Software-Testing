# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ea47d47ea8ab89a8ab84488cac0d0ce030c28efd`
- B: `f43534ec04d4c4bae666033e2041ecde21c19a56`
- test: `src/test/java/org/apache/commons/lang3/RegExUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RegExUtils.java']`
- old_test_mode: `methods`
- user_chars: `12924`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3841, 'completion_tokens': 3677, 'total_tokens': 7518, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2607}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 3457}`

---

- 将删除旧测试方法 `testReplaceAll_StringPatternString`
- 将新增测试方法 `testReplaceAll`，以覆盖新的 `replaceAll(CharSequence, Pattern, String)` 方法
- 将新增测试方法 `testReplaceAllDeprecated`，以覆盖已弃用的 `replaceAll(String, Pattern, String)` 方法
- 无需调整 import，因为所有用到的类均已存在于当前测试类中

```java
// DELETE_TESTS_START
testReplaceAll_StringPatternString
// DELETE_TESTS_END

    @Test
    public void testReplaceAll() {
        assertNull(RegExUtils.replaceAll((CharSequence) null, Pattern.compile(""), ""));

        assertEquals("any", RegExUtils.replaceAll((CharSequence) "any", (Pattern) null, ""));
        assertEquals("any", RegExUtils.replaceAll((CharSequence) "any", Pattern.compile(""), null));

        assertEquals("zzz", RegExUtils.replaceAll((CharSequence) "", Pattern.compile(""), "zzz"));
        assertEquals("zzz", RegExUtils.replaceAll((CharSequence) "", Pattern.compile(".*"), "zzz"));
        assertEquals("", RegExUtils.replaceAll((CharSequence) "", Pattern.compile(".+"), "zzz"));
        assertEquals("ZZaZZbZZcZZ", RegExUtils.replaceAll((CharSequence) "abc", Pattern.compile(""), "ZZ"));

        assertEquals("z\nz", RegExUtils.replaceAll((CharSequence) "<__>\n<__>", Pattern.compile("<.*>"), "z"));
        assertEquals("z", RegExUtils.replaceAll((CharSequence) "<__>\n<__>", Pattern.compile("(?s)<.*>"), "z"));

        assertEquals("z", RegExUtils.replaceAll((CharSequence) "<__>\n<__>", Pattern.compile("<.*>", Pattern.DOTALL), "z"));
        assertEquals("z", RegExUtils.replaceAll((CharSequence) "<__>\\n<__>", Pattern.compile("<.*>"), "z"));
        assertEquals("X", RegExUtils.replaceAll((CharSequence) "<A>\nxy\n</A>", Pattern.compile("<A>.*</A>", Pattern.DOTALL), "X"));

        assertEquals("ABC___123", RegExUtils.replaceAll((CharSequence) "ABCabc123", Pattern.compile("[a-z]"), "_"));
        assertEquals("ABC_123", RegExUtils.replaceAll((CharSequence) "ABCabc123", Pattern.compile("[^A-Z0-9]+"), "_"));
        assertEquals("ABC123", RegExUtils.replaceAll((CharSequence) "ABCabc123", Pattern.compile("[^A-Z0-9]+"), ""));
        assertEquals("Lorem_ipsum_dolor_sit", RegExUtils.replaceAll((CharSequence) "Lorem ipsum  dolor   sit", Pattern.compile("( +)([a-z]+)"), "_$2"));
    }

    @Test
    public void testReplaceAllDeprecated() {
        assertNull(RegExUtils.replaceAll(null, Pattern.compile(""), ""));

        assertEquals("any", RegExUtils.replaceAll("any", (Pattern) null, ""));
        assertEquals("any", RegExUtils.replaceAll("any", Pattern.compile(""), null));

        assertEquals("zzz", RegExUtils.replaceAll("", Pattern.compile(""), "zzz"));
        assertEquals("zzz", RegExUtils.replaceAll("", Pattern.compile(".*"), "zzz"));
        assertEquals("", RegExUtils.replaceAll("", Pattern.compile(".+"), "zzz"));
        assertEquals("ZZaZZbZZcZZ", RegExUtils.replaceAll("abc", Pattern.compile(""), "ZZ"));

        assertEquals("z\nz", RegExUtils.replaceAll("<__>\n<__>", Pattern.compile("<.*>"), "z"));
        assertEquals("z", RegExUtils.replaceAll("<__>\n<__>", Pattern.compile("(?s)<.*>"), "z"));

        assertEquals("z", RegExUtils.replaceAll("<__>\n<__>", Pattern.compile("<.*>", Pattern.DOTALL), "z"));
        assertEquals("z", RegExUtils.replaceAll("<__>\\n<__>", Pattern.compile("<.*>"), "z"));
        assertEquals("X", RegExUtils.replaceAll("<A>\nxy\n</A>", Pattern.compile("<A>.*</A>", Pattern.DOTALL), "X"));

        assertEquals("ABC___123", RegExUtils.replaceAll("ABCabc123", Pattern.compile("[a-z]"), "_"));
        assertEquals("ABC_123", RegExUtils.replaceAll("ABCabc123", Pattern.compile("[^A-Z0-9]+"), "_"));
        assertEquals("ABC123", RegExUtils.replaceAll("ABCabc123", Pattern.compile("[^A-Z0-9]+"), ""));
        assertEquals("Lorem_ipsum_dolor_sit", RegExUtils.replaceAll("Lorem ipsum  dolor   sit", Pattern.compile("( +)([a-z]+)"), "_$2"));
    }
```