# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9c0379850b869e3a02320f9a5149eaad2c4cb76b`
- B: `7cfa8a932869b98c3737f4ed41312d92eb50d636`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `148246`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 37980, 'completion_tokens': 2721, 'total_tokens': 40701, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1849}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 37596}`

---

- 修改 `testCaseFunctions` 方法，新增对 `capitalize` 和 `uncapitalize` 方法的 `StringBuilder`、`StringBuffer`、`CharBuffer` 参数测试，以验证方法可接受多种 `CharSequence` 实现。

```java
    public void testCaseFunctions() {
        assertEquals(null, StringUtils.upperCase(null));
        assertEquals(null, StringUtils.upperCase(null, Locale.ENGLISH));
        assertEquals(null, StringUtils.lowerCase(null));
        assertEquals(null, StringUtils.lowerCase(null, Locale.ENGLISH));
        assertEquals(null, StringUtils.capitalize(null));
        assertEquals(null, StringUtils.uncapitalize(null));

        assertEquals("capitalize(empty-string) failed",
                     "", StringUtils.capitalize("") );
        assertEquals("capitalize(single-char-string) failed",
                "X", StringUtils.capitalize("x") );
        assertEquals("capitalize(single-char-string) failed",
                "X", StringUtils.capitalize(new StringBuilder("x")) );
        assertEquals("capitalize(single-char-string) failed",
                "X", StringUtils.capitalize(new StringBuffer("x")) );
        assertEquals("capitalize(single-char-string) failed",
                "X", StringUtils.capitalize(CharBuffer.wrap("x")) );
        
        assertEquals("uncapitalize(String) failed",
                     FOO_UNCAP, StringUtils.uncapitalize(FOO_CAP) );
        assertEquals("uncapitalize(empty-string) failed",
                     "", StringUtils.uncapitalize("") );
        assertEquals("uncapitalize(single-char-string) failed",
                "x", StringUtils.uncapitalize("X") );
        assertEquals("uncapitalize(single-char-string) failed",
                "x", StringUtils.uncapitalize(new StringBuilder("X")) );
        assertEquals("uncapitalize(single-char-string) failed",
                "x", StringUtils.uncapitalize(new StringBuffer("X")) );
        assertEquals("uncapitalize(single-char-string) failed",
                "x", StringUtils.uncapitalize(CharBuffer.wrap("X")) );
                     
        // reflection type of tests: Sentences.
        assertEquals("uncapitalize(capitalize(String)) failed",
                     SENTENCE_UNCAP, StringUtils.uncapitalize(StringUtils.capitalize(SENTENCE_UNCAP)) );
        assertEquals("capitalize(uncapitalize(String)) failed",
                     SENTENCE_CAP, StringUtils.capitalize(StringUtils.uncapitalize(SENTENCE_CAP)) );

        // reflection type of tests: One word.
        assertEquals("uncapitalize(capitalize(String)) failed",
                     FOO_UNCAP, StringUtils.uncapitalize(StringUtils.capitalize(FOO_UNCAP)) );
        assertEquals("capitalize(uncapitalize(String)) failed",
                     FOO_CAP, StringUtils.capitalize(StringUtils.uncapitalize(FOO_CAP)) );

        assertEquals("upperCase(String) failed",
                     "FOO TEST THING", StringUtils.upperCase("fOo test THING") );
        assertEquals("upperCase(empty-string) failed",
                     "", StringUtils.upperCase("") );
        assertEquals("lowerCase(String) failed",
                     "foo test thing", StringUtils.lowerCase("fOo test THING") );
        assertEquals("lowerCase(empty-string) failed",
                     "", StringUtils.lowerCase("") );

        assertEquals("upperCase(String, Locale) failed",
                     "FOO TEST THING", StringUtils.upperCase("fOo test THING", Locale.ENGLISH) );
        assertEquals("upperCase(empty-string, Locale) failed",
                     "", StringUtils.upperCase("", Locale.ENGLISH) );
        assertEquals("lowerCase(String, Locale) failed",
                     "foo test thing", StringUtils.lowerCase("fOo test THING", Locale.ENGLISH) );
        assertEquals("lowerCase(empty-string, Locale) failed",
                     "", StringUtils.lowerCase("", Locale.ENGLISH) );
    }
```