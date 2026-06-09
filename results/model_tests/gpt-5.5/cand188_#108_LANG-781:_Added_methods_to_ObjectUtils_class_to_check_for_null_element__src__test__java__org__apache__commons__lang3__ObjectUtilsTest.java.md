# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `2433cd393e6e4185031377665104ac09b75f99c5`
- B: `d190655a97c33c886997b9570697f432e7d3a21a`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `33047`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7904, 'completion_tokens': 476, 'total_tokens': 8380}`

---

- 新增 `testAnyNotNull`：覆盖新增的 `ObjectUtils.anyNotNull(Object...)` 在空数组、`null` 数组、全 `null` 和包含非 `null` 元素时的返回值；无需调整 import。
- 新增 `testAllNotNull`：覆盖新增的 `ObjectUtils.allNotNull(Object...)` 在 `null` 数组、包含 `null`、空数组和全非 `null` 元素时的返回值；无需调整 import。

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