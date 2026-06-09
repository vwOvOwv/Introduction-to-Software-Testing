# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `6cca6ff4a540b1811bec01934f9452761f7ef489`
- B: `7d7e8af45032f1f3a29a18888cd3b0ca6085a156`
- test: `src/test/java/org/apache/commons/lang3/SystemPropertiesTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/SystemProperties.java']`
- old_test_mode: `methods`
- user_chars: `8498`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2349, 'completion_tokens': 663, 'total_tokens': 3012}`

---

- 修改 `testGetBoolean`：生产方法默认值参数由 `boolean` 改为 `BooleanSupplier`，测试改用 lambda，并新增 `null` 默认供应器断言。
- 修改 `testGetInt`：生产方法默认值参数由 `int` 改为 `IntSupplier`，测试改用 lambda，并新增 `null` 默认供应器断言。
- 修改 `testGetLong`：生产方法默认值参数由 `long` 改为 `LongSupplier`，测试改用 lambda，并新增 `null` 默认供应器断言。
- 不需要调整 import。

```java
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