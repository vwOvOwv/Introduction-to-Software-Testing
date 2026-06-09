# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e81855a208c909f46e1bf346d7982bd77be13476`
- B: `7f7d4b881d78dcb8d5a0149965f934df268919d7`
- test: `src/test/java/org/apache/commons/lang3/ValidateTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Validate.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `82743`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 16269, 'completion_tokens': 164, 'total_tokens': 16433}`

---

- 新增 `shouldThrowExceptionWithGivenMessageContainingSpecialCharacterForFalseExpression`，对应生产代码将无 varargs 值时的消息处理从 `String.format` 改为原样返回以支持 `%` 等特殊字符；无需调整 import。

```java
@Test
void shouldThrowExceptionWithGivenMessageContainingSpecialCharacterForFalseExpression() {
    final IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> Validate.isTrue(false, "%"));
    assertEquals("%", ex.getMessage());
}
```