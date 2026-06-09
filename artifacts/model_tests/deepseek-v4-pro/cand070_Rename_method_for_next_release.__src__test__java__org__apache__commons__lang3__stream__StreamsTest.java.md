# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9f0f3c838b00354009f265b7d0fcefd6f1dec454`
- B: `46b15a2ecb05bdc281bc6109bb2db99b566d4a10`
- test: `src/test/java/org/apache/commons/lang3/stream/StreamsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/stream/Streams.java']`
- old_test_mode: `methods`
- user_chars: `3752`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1427, 'completion_tokens': 615, 'total_tokens': 2042, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 400}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1043}`

---

- 修改 `testNullSafeStreamNotNull` 和 `testNullSafeStreamNull` 方法，将 `Streams.nullSafeStream(...)` 调用更新为 `Streams.nonNull(...)`，以匹配生产代码中将方法重命名为 `nonNull` 的变更；无需新增或删除 import 或其它方法。

```java
@Test
public void testNullSafeStreamNotNull() {
    assertEquals(2, Streams.nonNull(Arrays.asList("A", "B")).collect(Collectors.toList()).size());
    assertEquals(2, Streams.nonNull(Arrays.asList(null, "A", null, "B", null)).collect(Collectors.toList()).size());
    assertEquals(0, Streams.nonNull(Arrays.asList(null, null)).collect(Collectors.toList()).size());
}

@Test
public void testNullSafeStreamNull() {
    final List<String> input = null;
    assertEquals(0, Streams.nonNull(input).collect(Collectors.toList()).size());
}
```