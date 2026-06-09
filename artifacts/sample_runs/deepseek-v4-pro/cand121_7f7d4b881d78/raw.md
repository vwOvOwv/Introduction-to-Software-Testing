# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e81855a208c909f46e1bf346d7982bd77be13476`
- B: `7f7d4b881d78dcb8d5a0149965f934df268919d7`
- test: `src/test/java/org/apache/commons/lang3/ValidateTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Validate.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `82743`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 16469, 'completion_tokens': 1008, 'total_tokens': 17477, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 879}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 16085}`

---

- 在 `IsTrue.WithMessage` 中新增测试方法 `shouldThrowExceptionWithGivenMessageContainingSpecialCharacterForFalseExpression`，验证当消息包含特殊字符（如 `%`）且无变参时，异常消息保留原文而不进行格式化。
- 无需修改现有测试方法或 import，其他测试行为与断言均保持兼容。

```java
@Test
void shouldThrowExceptionWithGivenMessageContainingSpecialCharacterForFalseExpression() {
    final IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> Validate.isTrue(false, "%"));
    assertEquals("%", ex.getMessage());
}
```