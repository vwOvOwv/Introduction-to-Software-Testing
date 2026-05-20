# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `9cbf068672d7250b90d21c474ed70bfe271ba14e`
- B: `8b27dec0340e501fee098278d358d7ddd62ad2ad`
- test: `src/test/java/org/apache/commons/lang3/SystemPropertiesTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/SystemProperties.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `51421`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 12558, 'completion_tokens': 977, 'total_tokens': 13535, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 12302}`

---

- 新增 `SIMPLE_NAME` 常量字段，用于构造 `SimpleClassName.Key` 格式的键。
- 新增 `testGetBooleanClass()` 测试方法，测试 `getBoolean(Class, String, BooleanSupplier)` 方法。
- 新增 `testGetIntClass()` 测试方法，测试 `getInt(Class, String, IntSupplier)` 方法。
- 新增 `testGetLongClass()` 测试方法，测试 `getLong(Class, String, LongSupplier)` 方法。
- 无需调整 import，因为 `BooleanSupplier`、`IntSupplier`、`LongSupplier` 均在 `java.util.function` 包中，而旧测试已导入 `java.util.function.Supplier`，但未导入这些特定接口，需新增 import。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.util.function.BooleanSupplier;
import java.util.function.IntSupplier;
import java.util.function.LongSupplier;
import java.util.function.Supplier;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.ThrowingSupplier;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junitpioneer.jupiter.SetSystemProperty;
import org.junitpioneer.jupiter.SetSystemProperty.SetSystemProperties;
// IMPORTS_END

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
```