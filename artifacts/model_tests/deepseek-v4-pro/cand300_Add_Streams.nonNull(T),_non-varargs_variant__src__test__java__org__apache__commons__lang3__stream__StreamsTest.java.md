# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `45ad8976cb94010bcc36688f885fbf119f146252`
- B: `64736630706adf9e2cbb482fbfcbdc81a9dc02f7`
- test: `src/test/java/org/apache/commons/lang3/stream/StreamsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/stream/Streams.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `15014`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 4067, 'completion_tokens': 4017, 'total_tokens': 8084, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 3676}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 3683}`

---

我们需要更新旧测试以适应 B 上生产代码的变更：新增的 `nonNull(E)` 重载会使原有的 `nonNull(Collection)` 调用产生歧义，因此需要修改 `testNullSafeStreamNotNull` 和 `testNullSafeStreamNull`；同时，按测试 diff 的指引，新增测试方法 `testNonNull`。无需调整 import。

```java
    @Test
    public void testNullSafeStreamNotNull() {
        assertEquals(2, Streams.<String>nonNull(Arrays.asList("A", "B")).collect(Collectors.toList()).size());
        assertEquals(2, Streams.<String>nonNull(Arrays.asList(null, "A", null, "B", null)).collect(Collectors.toList()).size());
        assertEquals(0, Streams.<String>nonNull(Arrays.asList(null, null)).collect(Collectors.toList()).size());
    }

    @Test
    public void testNullSafeStreamNull() {
        final List<String> input = null;
        assertEquals(0, Streams.<String>nonNull(input).collect(Collectors.toList()).size());
    }

    @Test
    public void testNonNull() {
        assertEquals(0, Streams.nonNull().collect(Collectors.toList()).size());
        assertEquals(1, Streams.nonNull("A").collect(Collectors.toList()).size());
        assertEquals(1, Streams.nonNull("A", null).collect(Collectors.toList()).size());
        assertEquals(1, Streams.nonNull(null, "A").collect(Collectors.toList()).size());
    }
```