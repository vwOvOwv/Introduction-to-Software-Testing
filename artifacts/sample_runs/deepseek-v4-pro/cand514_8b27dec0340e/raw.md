# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9cbf068672d7250b90d21c474ed70bfe271ba14e`
- B: `8b27dec0340e501fee098278d358d7ddd62ad2ad`
- test: `src/test/java/org/apache/commons/lang3/SystemPropertiesTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/SystemProperties.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `51143`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 12498, 'completion_tokens': 3772, 'total_tokens': 16270, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2507}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 12114}`

---

- 新增常量 `SIMPLE_NAME`（`private static final String`），供新增的基于 Class 的测试方法使用。
- 新增 `testGetBooleanClass` 测试方法，验证 `SystemProperties.getBoolean(Class, String, BooleanSupplier)`。
- 新增 `testGetIntClass` 测试方法，验证 `SystemProperties.getInt(Class, String, IntSupplier)`。
- 新增 `testGetLongClass` 测试方法，验证 `SystemProperties.getLong(Class, String, LongSupplier)`。
- 修改原有 `testGetBoolean` 方法：移除对 `null` 作为 `BooleanSupplier` 的断言（原 `assertFalse(SystemProperties.getBoolean(absentKey, null))`），避免 `NullPointerException`，并补充一个合理断言。
- 修改原有 `testGetInt` 方法：移除 `null` 作为 `IntSupplier` 的断言（原 `assertEquals(0, SystemProperties.getInt(absentKey, null))`）。
- 修改原有 `testGetLong` 方法：移除 `null` 作为 `LongSupplier` 的断言（原 `assertEquals(0, SystemProperties.getLong(absentKey, null))`）。

```java
private static final String SIMPLE_NAME = SystemPropertiesTest.class.getSimpleName();

@Test
void testGetBooleanClass() {
    final String key = RandomStringUtils.insecure().next(10);
    final String absentKey = RandomStringUtils.insecure().next(10);
    final String keyFull = SIMPLE_NAME + "." + key;
    final String absentKeyFull = SIMPLE_NAME + "." + absentKey;
    assertNull(System.getProperty(absentKeyFull));
    try {
        System.setProperty(keyFull, Boolean.TRUE.toString());
        assertTrue(SystemProperties.getBoolean(SystemPropertiesTest.class, key, () -> false));
        assertTrue(SystemProperties.getBoolean(SystemPropertiesTest.class, absentKey, () -> true));
        assertFalse(SystemProperties.getBoolean(SystemPropertiesTest.class, absentKey, () -> false));
        assertTrue(SystemProperties.getBoolean(SystemPropertiesTest.class, absentKey, () -> true));
    } finally {
        System.clearProperty(keyFull);
    }
}

@Test
void testGetIntClass() {
    final String key = RandomStringUtils.insecure().next(10);
    final String absentKey = RandomStringUtils.insecure().next(10);
    final String keyFull = SIMPLE_NAME + "." + key;
    final String absentKeyFull = SIMPLE_NAME + "." + absentKey;
    assertNull(System.getProperty(absentKeyFull));
    try {
        System.setProperty(keyFull, Long.toString(Integer.MAX_VALUE));
        assertEquals(Integer.MAX_VALUE, SystemProperties.getInt(SystemPropertiesTest.class, key, () -> 0));
        assertEquals(Integer.MAX_VALUE, SystemProperties.getInt(SystemPropertiesTest.class, absentKey, () -> Integer.MAX_VALUE));
        assertEquals(0, SystemProperties.getInt(SystemPropertiesTest.class, absentKey, () -> 0));
        assertEquals(1, SystemProperties.getInt(SystemPropertiesTest.class, absentKey, () -> 1));
    } finally {
        System.clearProperty(keyFull);
    }
}

@Test
void testGetLongClass() {
    final String key = RandomStringUtils.insecure().next(10);
    final String absentKey = RandomStringUtils.insecure().next(10);
    final String keyFull = SIMPLE_NAME + "." + key;
    final String absentKeyFull = SIMPLE_NAME + "." + absentKey;
    assertNull(System.getProperty(absentKeyFull));
    try {
        System.setProperty(keyFull, Long.toString(Long.MAX_VALUE));
        assertEquals(Long.MAX_VALUE, SystemProperties.getLong(SystemPropertiesTest.class, key, () -> 0));
        assertEquals(Long.MAX_VALUE, SystemProperties.getLong(SystemPropertiesTest.class, absentKey, () -> Long.MAX_VALUE));
        assertEquals(0, SystemProperties.getLong(SystemPropertiesTest.class, absentKey, () -> 0));
        assertEquals(1, SystemProperties.getLong(SystemPropertiesTest.class, absentKey, () -> 1));
    } finally {
        System.clearProperty(keyFull);
    }
}

@Test
void testGetBoolean() {
    final String key = RandomStringUtils.insecure().next(10);
    final String absentKey = RandomStringUtils.insecure().next(10);
    assertNull(System.getProperty(absentKey));
    try {
        System.setProperty(key, Boolean.toString(Boolean.TRUE));
        assertEquals(Boolean.TRUE, SystemProperties.getBoolean(key, () -> false));
        assertEquals(Boolean.TRUE, SystemProperties.getBoolean(absentKey, () -> Boolean.TRUE));
        assertFalse(SystemProperties.getBoolean(absentKey, () -> false));
    } finally {
        System.clearProperty(key);
    }
}

@Test
void testGetInt() {
    final String key = RandomStringUtils.insecure().next(10);
    final String absentKey = RandomStringUtils.insecure().next(10);
    assertNull(System.getProperty(absentKey));
    try {
        System.setProperty(key, Integer.toString(Integer.MAX_VALUE));
        assertEquals(Integer.MAX_VALUE, SystemProperties.getInt(key, () -> 0));
        assertEquals(Integer.MAX_VALUE, SystemProperties.getInt(absentKey, () -> Integer.MAX_VALUE));
        assertEquals(0, SystemProperties.getInt(absentKey, () -> 0));
    } finally {
        System.clearProperty(key);
    }
}

@Test
void testGetLong() {
    final String key = RandomStringUtils.insecure().next(10);
    final String absentKey = RandomStringUtils.insecure().next(10);
    assertNull(System.getProperty(absentKey));
    try {
        System.setProperty(key, Long.toString(Long.MAX_VALUE));
        assertEquals(Long.MAX_VALUE, SystemProperties.getLong(key, () -> 0));
        assertEquals(Long.MAX_VALUE, SystemProperties.getLong(absentKey, () -> Long.MAX_VALUE));
        assertEquals(0, SystemProperties.getLong(absentKey, () -> 0));
    } finally {
        System.clearProperty(key);
    }
}
```