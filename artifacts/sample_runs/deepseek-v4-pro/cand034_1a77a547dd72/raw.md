# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `4f9be0faabe494f1f9a2000df288d79d9ab6663b`
- B: `1a77a547dd72e82a8967e462406436a1c2e341a2`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `36940`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9084, 'completion_tokens': 931, 'total_tokens': 10015, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 567}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 8700}`

---

- 新增 `testAnyNull` 测试方法，对应生产代码新增的 `ObjectUtils.anyNull` 方法。
- 新增 `testAllNull` 测试方法，对应生产代码新增的 `ObjectUtils.allNull` 方法。
- 无需调整 import，现有测试已导入所有必需的断言方法；无需删除任何旧测试方法。

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