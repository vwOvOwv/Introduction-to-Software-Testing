# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `1fc15b43d4b243262d6383d2e5a554a2158aa57f`
- B: `ee6c682ed5fa8c1b33aa1d52a1e2f088b0191b6b`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `36940`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9084, 'completion_tokens': 1549, 'total_tokens': 10633, 'prompt_tokens_details': {'cached_tokens': 8960}, 'completion_tokens_details': {'reasoning_tokens': 1185}, 'prompt_cache_hit_tokens': 8960, 'prompt_cache_miss_tokens': 124}`

---

- 新增 `testAnyNull` 测试方法，验证新增的 `anyNull` 方法在各种传入组合下的布尔返回值（与生产 diff 新增方法匹配）。
- 新增 `testAllNull` 测试方法，验证新增的 `allNull` 方法在各种传入组合下的布尔返回值。
- 无需调整 `import`，因为所需的 `assertTrue`、`assertFalse` 静态导入已存在。

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