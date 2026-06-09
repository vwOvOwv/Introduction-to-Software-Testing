# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `51ad9f989dda1e5c7f9487d1477c82ea003a864a`
- B: `ff415c8f8f213d40a19f8dc9ac037050ef497bf8`
- test: `src/test/java/org/apache/commons/lang3/stream/StreamsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/stream/Streams.java']`
- old_test_mode: `methods`
- user_chars: `13310`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3477, 'completion_tokens': 566, 'total_tokens': 4043}`

---

- 新增 `testNullSafeStreamNotNull`：覆盖新增公开方法 `Streams.nullSafeStream(Collection)` 会过滤非 null 集合中的 null 元素。
- 新增 `testNullSafeStreamNull`：覆盖 `Streams.nullSafeStream(null)` 返回空流。
- 新增 `testToStreamNotNull`：覆盖新增公开方法 `Streams.toStream(Collection)` 对非 null 集合委托为普通 stream。
- 新增 `testToStreamNull`：覆盖 `Streams.toStream(null)` 返回空流。
- 不需要调整 import：现有测试已使用 `@Test`、`Arrays`、`List`、`Collectors` 和 `assertEquals`。

```java
    @Test
    public void testNullSafeStreamNotNull() {
        assertEquals(2, Streams.nullSafeStream(Arrays.asList("A", "B")).collect(Collectors.toList()).size());
        assertEquals(2, Streams.nullSafeStream(Arrays.asList(null, "A", null, "B", null)).collect(Collectors.toList()).size());
        assertEquals(0, Streams.nullSafeStream(Arrays.asList(null, null)).collect(Collectors.toList()).size());
    }

    @Test
    public void testNullSafeStreamNull() {
        final List<String> input = null;
        assertEquals(0, Streams.nullSafeStream(input).collect(Collectors.toList()).size());
    }

    @Test
    public void testToStreamNotNull() {
        assertEquals(2, Streams.toStream(Arrays.asList("A", "B")).collect(Collectors.toList()).size());
    }

    @Test
    public void testToStreamNull() {
        final List<String> input = null;
        assertEquals(0, Streams.toStream(input).collect(Collectors.toList()).size());
    }
```