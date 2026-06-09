# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `36217ee164239391c672fdfc8f5bd080beab5c4b`
- B: `cc6beb2d05347fba64d933906ae2b712b1a43302`
- test: `src/test/java/org/apache/commons/lang3/reflect/TypeUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/reflect/TypeUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `47291`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 11780, 'completion_tokens': 1345, 'total_tokens': 13125, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1226}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 11396}`

---

- 新增一个 @Test 方法 `testLANG1348()`，用于验证递归类型参数 `T extends Enum<T>` 的 `toString` 输出为 `"T extends java.lang.Enum<T>"`。无需调整 import 或修改其他现有测试方法。

```java
@Test
public void testLANG1348() throws Exception {
    final Method method = Enum.class.getMethod("valueOf", Class.class, String.class);
    Assert.assertEquals("T extends java.lang.Enum<T>", TypeUtils.toString(method.getGenericReturnType()));
}
```