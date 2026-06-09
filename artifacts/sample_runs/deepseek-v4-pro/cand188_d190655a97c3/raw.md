# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `2433cd393e6e4185031377665104ac09b75f99c5`
- B: `d190655a97c33c886997b9570697f432e7d3a21a`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `33047`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 8102, 'completion_tokens': 1183, 'total_tokens': 9285, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 806}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 7718}`

---

- 新增 `testAnyNotNull` 测试方法，验证生产代码新增的 `ObjectUtils.anyNotNull(Object...)` 方法的各种边界情况。
- 新增 `testAllNotNull` 测试方法，验证生产代码新增的 `ObjectUtils.allNotNull(Object...)` 方法的各种边界情况。
- 无需新增或修改 `import`，已有的 `assertFalse` 和 `assertTrue` 静态导入已满足需求。

```java
/**
 * Tests {@link ObjectUtils#anyNotNull(Object...)}.
 */
@Test
public void testAnyNotNull() {
    assertFalse(ObjectUtils.anyNotNull());
    assertFalse(ObjectUtils.anyNotNull((Object) null));
    assertFalse(ObjectUtils.anyNotNull((Object[]) null));
    assertFalse(ObjectUtils.anyNotNull(null, null, null));

    assertTrue(ObjectUtils.anyNotNull(FOO));
    assertTrue(ObjectUtils.anyNotNull(null, FOO, null));
    assertTrue(ObjectUtils.anyNotNull(null, null, null, null, FOO, BAR));
}

/**
 * Tests {@link ObjectUtils#allNotNull(Object...)}.
 */
@Test
public void testAllNotNull() {
    assertFalse(ObjectUtils.allNotNull((Object) null));
    assertFalse(ObjectUtils.allNotNull((Object[]) null));
    assertFalse(ObjectUtils.allNotNull(null, null, null));
    assertFalse(ObjectUtils.allNotNull(null, FOO, BAR));
    assertFalse(ObjectUtils.allNotNull(FOO, BAR, null));
    assertFalse(ObjectUtils.allNotNull(FOO, BAR, null, FOO, BAR));

    assertTrue(ObjectUtils.allNotNull());
    assertTrue(ObjectUtils.allNotNull(FOO));
    assertTrue(ObjectUtils.allNotNull(FOO, BAR, 1, Boolean.TRUE, new Object(), new Object[]{}));
}
```