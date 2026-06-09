# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `8efbb7df05d879dec15433e87a51392810936da5`
- B: `4ff5e2b9f98e5ca9dd105a2d08477e0371ae8832`
- test: `src/test/java/org/apache/commons/lang3/concurrent/UncheckedFutureTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/UncheckedFuture.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `7398`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2066, 'completion_tokens': 194, 'total_tokens': 2260}`

---

- 新增 `testMap`：生产代码新增 `UncheckedFuture.map(Collection<Future<T>>)` 返回 `Stream<UncheckedFuture<T>>`，因此补充测试验证映射后的 `get()` 结果。
- 不需要调整 import：旧测试已包含 `Arrays`、`List`、`Future`、`Collectors` 以及断言所需 import。

```java
@Test
public void testMap() {
    final List<String> expected = Arrays.asList("Y", "Z");
    final List<Future<String>> input = Arrays.asList(new TestFuture<>("Y"), new TestFuture<>("Z"));
    assertEquals(expected, UncheckedFuture.map(input).map(UncheckedFuture::get).collect(Collectors.toList()));
}
```