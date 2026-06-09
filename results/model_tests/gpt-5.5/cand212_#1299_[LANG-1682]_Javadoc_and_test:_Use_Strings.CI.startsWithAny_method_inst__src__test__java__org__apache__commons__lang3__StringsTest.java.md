# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `c330b890b9164c6e98658030da3dbabaf90a5218`
- B: `f51f015e3deb2d205b2962fbaa253f6ef457f2a3`
- test: `src/test/java/org/apache/commons/lang3/StringsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Strings.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `9596`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2865, 'completion_tokens': 463, 'total_tokens': 3328}`

---

- 新增 `@Test` 方法 `testCaseInsensitiveStartsWithAny`，对应生产代码 `Strings.startsWithAny` 文档扩展为同时覆盖大小写不敏感场景。
- 不需要调整 import，现有 `assertFalse`、`assertTrue` 和 `@Test` 已满足新增测试方法使用。

```java
    /**
     * Expanding the existing test group {@link StringUtilsStartsEndsWithTest#testStartsWithAny()} to include case-insensitive cases
     */
    @Test
    public void testCaseInsensitiveStartsWithAny() {
        // LANG-1682
        assertFalse(Strings.CI.startsWithAny(null, (String[]) null));
        assertFalse(Strings.CI.startsWithAny(null, "aBc"));
        assertFalse(Strings.CI.startsWithAny("AbCxYz", (String[]) null));
        assertFalse(Strings.CI.startsWithAny("AbCxYz"));
        assertTrue(Strings.CI.startsWithAny("AbCxYz", "aBc"));
        assertTrue(Strings.CI.startsWithAny("AbCxYz", null, "XyZ", "aBc"));
        assertFalse(Strings.CI.startsWithAny("AbCxYz", null, "XyZ", "aBcD"));
        assertTrue(Strings.CI.startsWithAny("AbCxYz", ""));
        assertTrue(Strings.CI.startsWithAny("abcxyz", null, "XyZ", "ABCX"));
        assertTrue(Strings.CI.startsWithAny("ABCXYZ", null, "XyZ", "abc"));

        assertTrue(Strings.CI.startsWithAny("AbCxYz", new StringBuilder("XyZ"), new StringBuffer("aBc")));
        assertTrue(Strings.CI.startsWithAny(new StringBuffer("AbCxYz"), new StringBuilder("XyZ"), new StringBuffer("abc")));
    }
```