# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `8efbb7df05d879dec15433e87a51392810936da5`
- B: `4ff5e2b9f98e5ca9dd105a2d08477e0371ae8832`
- test: `src/test/java/org/apache/commons/lang3/concurrent/UncheckedFutureTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/UncheckedFuture.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `7398`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2115, 'completion_tokens': 1052, 'total_tokens': 3167, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 923}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1731}`

---

- 将新增 `testMap` 方法，对应生产代码新增的 `UncheckedFuture.map` 静态方法。
- 无需修改、删除其他已有测试方法。
- 无需调整 import，当前文件已包含所需依赖。

```java
@Test
public void testMap() {
    final List<String> expected = Arrays.asList("Y", "Z");
    final List<Future<String>> input = Arrays.asList(new TestFuture<>("Y"), new TestFuture<>("Z"));
    assertEquals(expected, UncheckedFuture.map(input).map(UncheckedFuture::get).collect(Collectors.toList()));
}
```