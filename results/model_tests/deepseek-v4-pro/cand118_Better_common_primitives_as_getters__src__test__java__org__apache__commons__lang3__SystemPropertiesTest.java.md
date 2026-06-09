# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `6cca6ff4a540b1811bec01934f9452761f7ef489`
- B: `7d7e8af45032f1f3a29a18888cd3b0ca6085a156`
- test: `src/test/java/org/apache/commons/lang3/SystemPropertiesTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/SystemProperties.java']`
- old_test_mode: `methods`
- user_chars: `8498`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2382, 'completion_tokens': 1722, 'total_tokens': 4104, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1046}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1998}`

---

- 修改 `testGetBoolean`：将 `getBoolean` 的第二个参数从基本类型 `boolean` 替换为 `BooleanSupplier` 的 lambda 表达式，并新增一个 `defaultIfAbsent` 为 `null` 的断言用例。
- 修改 `testGetInt`：将 `getInt` 的第二个参数从基本类型 `int` 替换为 `IntSupplier` 的 lambda 表达式，并新增一个 `defaultIfAbsent` 为 `null` 的断言用例。
- 修改 `testGetLong`：将 `getLong` 的第二个参数从基本类型 `long` 替换为 `LongSupplier` 的 lambda 表达式，并新增一个 `defaultIfAbsent` 为 `null` 的断言用例。
- 需要调整 import：添加 `java.util.function.BooleanSupplier`、`java.util.function.IntSupplier`、`java.util.function.LongSupplier`。

```java
// IMPORTS_START
import java.util.function.BooleanSupplier;
import java.util.function.IntSupplier;
import java.util.function.LongSupplier;
// IMPORTS_END

@Test
public void testGetBoolean() {
    final String key = RandomStringUtils.random(10);
    final String absentKey = RandomStringUtils.random(10);
    assertNull(System.getProperty(absentKey));
    try {
        System.setProperty(key, Boolean.toString(Boolean.TRUE));
        assertEquals(Boolean.TRUE, SystemProperties.getBoolean(key, () -> false));
        assertEquals(Boolean.TRUE, SystemProperties.getBoolean(absentKey, () -> Boolean.TRUE));
        assertEquals(false, SystemProperties.getBoolean(absentKey, () -> false));
        assertEquals(false, SystemProperties.getBoolean(absentKey, null));
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
        assertEquals(Integer.MAX_VALUE, SystemProperties.getInt(key, () -> 0));
        assertEquals(Integer.MAX_VALUE, SystemProperties.getInt(absentKey, () -> Integer.MAX_VALUE));
        assertEquals(0, SystemProperties.getInt(absentKey, () -> 0));
        assertEquals(0, SystemProperties.getInt(absentKey, null));
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
        assertEquals(Long.MAX_VALUE, SystemProperties.getLong(key, () -> 0));
        assertEquals(Long.MAX_VALUE, SystemProperties.getLong(absentKey, () -> Long.MAX_VALUE));
        assertEquals(0, SystemProperties.getLong(absentKey, () -> 0));
        assertEquals(0, SystemProperties.getLong(absentKey, null));
    } finally {
        System.clearProperty(key);
    }
}
```