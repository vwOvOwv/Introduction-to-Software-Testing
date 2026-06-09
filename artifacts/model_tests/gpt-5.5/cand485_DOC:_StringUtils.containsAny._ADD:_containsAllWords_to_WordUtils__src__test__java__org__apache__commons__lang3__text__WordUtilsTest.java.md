# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `1cb5573ada7dc7ec240fca6afe4eeb6e2c793d8e`
- B: `54facb4fd93c2ff59b3096c6e64b9be1b3c9cd88`
- test: `src/test/java/org/apache/commons/lang3/text/WordUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/WordUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `24447`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6430, 'completion_tokens': 543, 'total_tokens': 6973}`

---

- 新增 `testContainsAllWords_StringString`：对应生产代码新增 `WordUtils.containsAllWords(String, String...)`，覆盖空值、空字符串、整词匹配和未匹配场景。
- 不需要调整 import：旧测试文件已存在 `assertFalse`、`assertTrue` 和 `@Test` 的导入。

```java
    @Test
    public void testContainsAllWords_StringString() {
        assertFalse(WordUtils.containsAllWords(null, (String) null));
        assertFalse(WordUtils.containsAllWords(null, ""));
        assertFalse(WordUtils.containsAllWords(null, "ab"));

        assertFalse(WordUtils.containsAllWords("", (String) null));
        assertFalse(WordUtils.containsAllWords("", ""));
        assertFalse(WordUtils.containsAllWords("", "ab"));

        assertFalse(WordUtils.containsAllWords("foo", (String) null));
        assertFalse(WordUtils.containsAllWords("bar", ""));
        assertFalse(WordUtils.containsAllWords("zzabyycdxx", "by"));
        assertTrue(WordUtils.containsAllWords("lorem ipsum dolor sit amet", "ipsum", "lorem", "dolor"));
        assertFalse(WordUtils.containsAllWords("lorem ipsum dolor sit amet", "ipsum", null, "lorem", "dolor"));
        assertFalse(WordUtils.containsAllWords("ab", "b"));
        assertFalse(WordUtils.containsAllWords("ab", "z"));
    }
```