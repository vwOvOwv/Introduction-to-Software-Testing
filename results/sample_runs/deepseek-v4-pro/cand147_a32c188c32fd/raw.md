# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `c42806cfa03979023e1a683edd0a221c51e6789c`
- B: `a32c188c32fd0c4a8149bcda524d704dd609da6e`
- test: `src/test/java/org/apache/commons/lang3/FunctionsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Functions.java']`
- old_test_mode: `methods`
- user_chars: `13185`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3925, 'completion_tokens': 1316, 'total_tokens': 5241, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1088}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 3541}`

---

- 修改 `testAsSupplier` 方法：将多行 lambda 简化为单行，保持原有断言逻辑不变，以兼容生产代码中对 `asSupplier` 实现的简化（现在内部委托给 `get(pSupplier)`，行为相同）。无需调整 import，已有测试所需静态导入已在文件中。

```java
@Test
public void testAsSupplier() {
    FailureOnOddInvocations.invocation = 0;
    final FailableSupplier<FailureOnOddInvocations, Throwable> failableSupplier = () -> new FailureOnOddInvocations();
    final Supplier<FailureOnOddInvocations> supplier = Functions.asSupplier(failableSupplier);
    UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () -> supplier.get());
    final Throwable cause = e.getCause();
    assertNotNull(cause);
    assertTrue(cause instanceof SomeException);
    assertEquals("Odd Invocation: 1", cause.getMessage());
    final FailureOnOddInvocations instance = supplier.get();
    assertNotNull(instance);
}
```