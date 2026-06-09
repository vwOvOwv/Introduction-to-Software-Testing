# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `54facb4fd93c2ff59b3096c6e64b9be1b3c9cd88`
- B: `633ce604968078151e03363d5c67042af74310e3`
- test: `src/test/java/org/apache/commons/lang3/text/WordUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/WordUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `24083`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6287, 'completion_tokens': 484, 'total_tokens': 6771}`

---

- 修改 `testContainsAllWords_StringString`：生产方法参数从 `String` 扩展为 `CharSequence`，且任一搜索词为 `blank/null` 时立即返回 `false`，因此新增包含正文单词 `"null"` 且搜索词数组中存在 `null` 的断言以覆盖新行为。
- 不需要调整 import：现有 `assertFalse/assertTrue` 与 `@Test` 导入仍可用。

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
    assertFalse(WordUtils.containsAllWords("lorem ipsum null dolor sit amet", "ipsum", null, "lorem", "dolor"));
    assertFalse(WordUtils.containsAllWords("ab", "b"));
    assertFalse(WordUtils.containsAllWords("ab", "z"));
}
```