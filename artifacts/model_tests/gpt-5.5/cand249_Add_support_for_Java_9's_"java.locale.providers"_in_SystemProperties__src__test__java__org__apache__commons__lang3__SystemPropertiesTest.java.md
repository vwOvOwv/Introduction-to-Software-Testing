# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cdcd915d02b089a62f607670e46b05b475da0050`
- B: `16c34b222d6a16849798e3345174ca9f0ebc430d`
- test: `src/test/java/org/apache/commons/lang3/SystemPropertiesTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/SystemProperties.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `14940`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3882, 'completion_tokens': 797, 'total_tokens': 4679}`

---

- 新增 `testGetJavaLocaleProviders`，对应新增的 `SystemProperties.getJavaLocaleProviders()` 与 `JAVA_LOCALE_PROVIDERS` 常量，并在 Java 9+ 环境下断言默认值为 `null`。
- 新增 `testGetBoolean`，覆盖新增的 `SystemProperties.getBoolean(String, boolean)` 对存在属性和缺省值的处理。
- 新增 `testGetInt`，覆盖新增的 `SystemProperties.getInt(String, int)` 对存在属性和缺省值的处理。
- 新增 `testGetLong`，覆盖新增的 `SystemProperties.getLong(String, long)` 对存在属性和缺省值的处理。
- 需要调整 import，新增 `assertEquals` 与 `assumeTrue` 的静态导入。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.Test;
// IMPORTS_END

@Test
public void testGetJavaLocaleProviders() {
    assumeTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_9));
    // default is null
    assertNull(SystemProperties.getJavaLocaleProviders(), SystemProperties.getJavaVersion());
}

@Test
public void testGetBoolean() {
    final String key = RandomStringUtils.random(10);
    final String absentKey = RandomStringUtils.random(10);
    assertNull(System.getProperty(absentKey));
    try {
        System.setProperty(key, Boolean.toString(Boolean.TRUE));
        assertEquals(Boolean.TRUE, SystemProperties.getBoolean(key, false));
        assertEquals(Boolean.TRUE, SystemProperties.getBoolean(absentKey, Boolean.TRUE));
        assertEquals(false, SystemProperties.getBoolean(absentKey, false));
    } finally {
        System.clearProperty(key);
    }
}

@Test
public void testGetInt() {
    final String key = RandomStringUtils.random(10);
    final String absentKey = RandomStringUtils.random(10);
    assertNull(System.getProperty(absentKey));
    try {
        System.setProperty(key, Integer.toString(Integer.MAX_VALUE));
        assertEquals(Integer.MAX_VALUE, SystemProperties.getInt(key, 0));
        assertEquals(Integer.MAX_VALUE, SystemProperties.getInt(absentKey, Integer.MAX_VALUE));
        assertEquals(0, SystemProperties.getInt(absentKey, 0));
    } finally {
        System.clearProperty(key);
    }
}

@Test
public void testGetLong() {
    final String key = RandomStringUtils.random(10);
    final String absentKey = RandomStringUtils.random(10);
    assertNull(System.getProperty(absentKey));
    try {
        System.setProperty(key, Long.toString(Long.MAX_VALUE));
        assertEquals(Long.MAX_VALUE, SystemProperties.getLong(key, 0));
        assertEquals(Long.MAX_VALUE, SystemProperties.getLong(absentKey, Long.MAX_VALUE));
        assertEquals(0, SystemProperties.getLong(absentKey, 0));
    } finally {
        System.clearProperty(key);
    }
}
```