# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9f0f3c838b00354009f265b7d0fcefd6f1dec454`
- B: `46b15a2ecb05bdc281bc6109bb2db99b566d4a10`
- test: `src/test/java/org/apache/commons/lang3/stream/StreamsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/stream/Streams.java']`
- old_test_mode: `methods`
- user_chars: `3752`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1403, 'completion_tokens': 264, 'total_tokens': 1667}`

---

- 修改 `testNullSafeStreamNotNull`：生产方法由 `Streams.nullSafeStream(...)` 重命名为 `Streams.nonNull(...)`，测试调用同步替换。
- 修改 `testNullSafeStreamNull`：空集合输入场景同样改为调用 `Streams.nonNull(...)`。
- import 无需调整：现有 `Arrays`、`List`、`Collectors`、JUnit 断言等导入仍适用。

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