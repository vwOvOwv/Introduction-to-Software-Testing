# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `93701c9ad764e94968d6ae290f935f46b10eb68c`
- B: `055c20ab982090d48cf216e3a37055d2e668c538`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `methods`
- user_chars: `13882`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3880, 'completion_tokens': 592, 'total_tokens': 4472, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 439}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 3496}`

---

- 修改 `testShuffleBoolean` 方法：将调用 `ArrayUtils.removeAllOccurences` 替换为 `ArrayUtils.removeAllOccurrences`，以匹配生产代码中新增的正确方法名。

```java
    @Test
    public void testShuffleBoolean() {
        final boolean[] array1 = new boolean[]{true, false, true, true, false, false, true, false, false, true};
        final boolean[] array2 = ArrayUtils.clone(array1);

        ArrayUtils.shuffle(array1, new Random(SEED));
        assertFalse(Arrays.equals(array1, array2));
        assertEquals(5, ArrayUtils.removeAllOccurrences(array1, true).length);
    }
```