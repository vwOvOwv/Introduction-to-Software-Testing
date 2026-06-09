# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `3da149382fcc8c8880cc96aba2c93cc575cc4970`
- B: `680f9d5492e2c9c27e5c1178744a9edf36a0272b`
- test: `src/test/java/org/apache/commons/lang3/builder/ToStringBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/ToStringBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `63017`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 15850, 'completion_tokens': 615, 'total_tokens': 16465, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 485}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 15466}`

---

- 新增 `testAppendAsObjectToStringNullPointerException` 测试方法，以验证调用 `appendAsObjectToString(null)` 抛出 `NullPointerException` 且之后 `toString()` 可正常执行；该测试对应于测试 diff 中新增的测试。
- 无需调整 import，因为 `assertThrows` 已存在。

```java
@Test
public void testAppendAsObjectToStringNullPointerException() {
    ToStringBuilder builder = new ToStringBuilder(1);
    assertThrows(NullPointerException.class, () -> builder.appendAsObjectToString(null));
    builder.toString();
}
```