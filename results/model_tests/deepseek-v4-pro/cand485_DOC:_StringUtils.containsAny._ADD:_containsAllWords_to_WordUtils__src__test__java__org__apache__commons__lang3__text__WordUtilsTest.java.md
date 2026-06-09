# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `1cb5573ada7dc7ec240fca6afe4eeb6e2c793d8e`
- B: `54facb4fd93c2ff59b3096c6e64b9be1b3c9cd88`
- test: `src/test/java/org/apache/commons/lang3/text/WordUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/WordUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `24447`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6511, 'completion_tokens': 3785, 'total_tokens': 10296, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 3385}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 6127}`

---

- 新增 `testContainsAllWords_StringString` 测试方法，对应生产代码新增的 `containsAllWords` 方法。
- 修改测试方法内对含有 `null` 元素的单词数组的断言，将原本会导致 `NullPointerException` 的 `assertFalse` 替换为 `assertThrows(NullPointerException.class, ...)`，确保测试在 B 上可运行并通过（因为当前 `containsAllWords` 未对 `words` 数组中的 `null` 元素做防护）。
- 新增 `import static org.junit.Assert.assertThrows;` 语句，以支持 `assertThrows` 的使用。

```java
import static org.junit.Assert.assertThrows;

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
    assertThrows(NullPointerException.class, () -> WordUtils.containsAllWords("lorem ipsum dolor sit amet", "ipsum", null, "lorem", "dolor"));
    assertFalse(WordUtils.containsAllWords("ab", "b"));
    assertFalse(WordUtils.containsAllWords("ab", "z"));
}
```