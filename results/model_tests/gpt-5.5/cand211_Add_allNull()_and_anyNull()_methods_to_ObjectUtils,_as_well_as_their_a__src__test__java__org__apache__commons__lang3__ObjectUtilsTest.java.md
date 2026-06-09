# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `1fc15b43d4b243262d6383d2e5a554a2158aa57f`
- B: `ee6c682ed5fa8c1b33aa1d52a1e2f088b0191b6b`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `36940`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 8841, 'completion_tokens': 437, 'total_tokens': 9278}`

---

- 新增 `testAnyNull`：覆盖生产代码新增的 `ObjectUtils.anyNull(Object...)`，验证包含 `null` 时为 `true`、全非空或空参数时为 `false`。
- 新增 `testAllNull`：覆盖生产代码新增的 `ObjectUtils.allNull(Object...)`，验证空参数、数组为 `null` 或全为 `null` 时为 `true`，存在非空值时为 `false`。
- import 无需调整：旧测试已包含 `assertTrue`、`assertFalse` 和 `@Test` 所需 import。

```java
/**
 * Tests {@link ObjectUtils#anyNull(Object...)}.
 */
@Test
public void testAnyNull() {
    assertTrue(ObjectUtils.anyNull((Object) null));
    assertTrue(ObjectUtils.anyNull(null, null, null));
    assertTrue(ObjectUtils.anyNull(null, FOO, BAR));
    assertTrue(ObjectUtils.anyNull(FOO, BAR, null));
    assertTrue(ObjectUtils.anyNull(FOO, BAR, null, FOO, BAR));

    assertFalse(ObjectUtils.anyNull());
    assertFalse(ObjectUtils.anyNull(FOO));
    assertFalse(ObjectUtils.anyNull(FOO, BAR, 1, Boolean.TRUE, new Object(), new Object[]{}));
}

/**
 * Tests {@link ObjectUtils#allNull(Object...)}.
 */
@Test
public void testAllNull() {
    assertTrue(ObjectUtils.allNull());
    assertTrue(ObjectUtils.allNull((Object) null));
    assertTrue(ObjectUtils.allNull((Object[]) null));
    assertTrue(ObjectUtils.allNull(null, null, null));

    assertFalse(ObjectUtils.allNull(FOO));
    assertFalse(ObjectUtils.allNull(null, FOO, null));
    assertFalse(ObjectUtils.allNull(null, null, null, null, FOO, BAR));
}
```