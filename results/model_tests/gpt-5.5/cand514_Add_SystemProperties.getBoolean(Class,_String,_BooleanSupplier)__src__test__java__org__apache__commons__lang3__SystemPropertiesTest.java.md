# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9cbf068672d7250b90d21c474ed70bfe271ba14e`
- B: `8b27dec0340e501fee098278d358d7ddd62ad2ad`
- test: `src/test/java/org/apache/commons/lang3/SystemPropertiesTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/SystemProperties.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `51143`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 11525, 'completion_tokens': 993, 'total_tokens': 12518}`

---

- 新增 `testGetBooleanClass`，覆盖生产代码新增的 `SystemProperties.getBoolean(Class<?>, String, BooleanSupplier)` 使用类简单名拼接系统属性键的行为。
- 新增 `testGetIntClass`，覆盖生产代码新增的 `SystemProperties.getInt(Class<?>, String, IntSupplier)` 使用类简单名拼接系统属性键的行为。
- 新增 `testGetLongClass`，覆盖生产代码新增的 `SystemProperties.getLong(Class<?>, String, LongSupplier)` 使用类简单名拼接系统属性键的行为。
- 不需要调整 import，现有断言、`@Test` 与同包 `RandomStringUtils` 均已可用。

```java
@Test
void testGetBooleanClass() {
    final String simpleName = SystemPropertiesTest.class.getSimpleName();
    final String key = RandomStringUtils.insecure().next(10);
    final String absentKey = RandomStringUtils.insecure().next(10);
    final String keyFull = simpleName + "." + key;
    final String absentKeyFull = simpleName + "." + absentKey;
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
    final String simpleName = SystemPropertiesTest.class.getSimpleName();
    final String key = RandomStringUtils.insecure().next(10);
    final String absentKey = RandomStringUtils.insecure().next(10);
    final String keyFull = simpleName + "." + key;
    final String absentKeyFull = simpleName + "." + absentKey;
    assertNull(System.getProperty(absentKeyFull));
    try {
        System.setProperty(keyFull, Integer.toString(Integer.MAX_VALUE));
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
    final String simpleName = SystemPropertiesTest.class.getSimpleName();
    final String key = RandomStringUtils.insecure().next(10);
    final String absentKey = RandomStringUtils.insecure().next(10);
    final String keyFull = simpleName + "." + key;
    final String absentKeyFull = simpleName + "." + absentKey;
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
```