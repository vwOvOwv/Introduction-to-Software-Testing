# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `75a6aac07e7806ca73a42a2fe637273841262dfa`
- B: `9bf6b2fb41704f3a3eadd4816bdff3c4ec24604e`
- test: `src/test/java/org/apache/commons/lang3/ValidateTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Validate.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `75342`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 13669, 'completion_tokens': 405, 'total_tokens': 14074}`

---

- 新增 `shouldThrowIllegalArgumentExceptionWithNullSuperType`，覆盖 `Validate.isAssignableFrom` 在 `superType == null` 时改为抛出带 `"null type"` 默认消息的行为；无需调整 import。
- 新增 `shouldThrowIllegalArgumentExceptionWithNullType`，覆盖 `Validate.isAssignableFrom` 在 `type == null` 时改为抛出带 `"null type"` 默认消息的行为；无需调整 import。
- 新增 `shouldThrowIllegalArgumentExceptionWithNullTypes`，覆盖 `Validate.isAssignableFrom` 在两个参数均为 `null` 时改为抛出默认消息的行为；无需调整 import。

```java
@Test
void shouldThrowIllegalArgumentExceptionWithNullSuperType() {
    final IllegalArgumentException ex = assertThrows(
            IllegalArgumentException.class,
            () -> Validate.isAssignableFrom(null, String.class));

    assertEquals("Cannot assign a java.lang.String to a null type", ex.getMessage());
}

@Test
void shouldThrowIllegalArgumentExceptionWithNullType() {
    final IllegalArgumentException ex = assertThrows(
            IllegalArgumentException.class,
            () -> Validate.isAssignableFrom(List.class, null));

    assertEquals("Cannot assign a null type to a java.util.List", ex.getMessage());
}

@Test
void shouldThrowIllegalArgumentExceptionWithNullTypes() {
    final IllegalArgumentException ex = assertThrows(
            IllegalArgumentException.class,
            () -> Validate.isAssignableFrom(null, null));

    assertEquals("Cannot assign a null type to a null type", ex.getMessage());
}
```