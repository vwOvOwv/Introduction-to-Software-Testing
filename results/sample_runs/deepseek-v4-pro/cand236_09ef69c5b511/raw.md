# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `bd4066eba88a772c06394d818d87aedca8bea53c`
- B: `09ef69c5b51115300da6df43690cd455d83c8027`
- test: `src/test/java/org/apache/commons/lang3/text/WordUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/WordUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `23962`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6392, 'completion_tokens': 600, 'total_tokens': 6992, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 488}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 6008}`

---

- 新增 @Test 方法 `testLANG1397`，以覆盖生产代码 `wrap` 方法中处理 `Integer.MAX_VALUE` 时溢出的修复。无需调整 import。

```java
@Test
public void testLANG1397() throws Exception {
    // Prior to fix, this was throwing StringIndexOutOfBoundsException
    WordUtils.wrap("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa "
        + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa "
        + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", Integer.MAX_VALUE);
}
```