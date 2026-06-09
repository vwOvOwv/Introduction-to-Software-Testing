# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `30dcb8de48393338deca5bfe68f251008f4d31d0`
- B: `0b70b01a9f1d9664bb5eac737175f58f06979b60`
- test: `src/test/java/org/apache/commons/lang3/EnumUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/EnumUtils.java']`
- old_test_mode: `methods`
- user_chars: `7905`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2561, 'completion_tokens': 1306, 'total_tokens': 3867}`

---

- 修改 `test_isEnum` 为 `test_isValidEnum`，对应生产代码中 `isValidEnum` 改为委托 `getEnum` 的实现但保持大小写敏感语义。
- 修改 `test_isEnum_nullClass` 为 `test_isValidEnum_nullClass`，对应 `isValidEnum(null, ...)` 仍应抛出 `NullPointerException`。
- 新增 `test_isValidEnumIgnoreCase`，覆盖新增的大小写不敏感校验方法 `isValidEnumIgnoreCase`。
- 新增 `test_isValidEnumIgnoreCase_nullClass`，覆盖 `isValidEnumIgnoreCase` 传入空 enum class 的异常行为。
- 新增 `test_getEnum_nonEnumClass`，覆盖 `getEnum` 在非 enum class 上返回 `null` 的行为。
- 新增 `test_getEnumIgnoreCase`，覆盖新增的大小写不敏感枚举获取方法 `getEnumIgnoreCase`。
- 新增 `test_getEnumIgnoreCase_nonEnumClass`，覆盖 `getEnumIgnoreCase` 在非 enum class 上返回 `null` 的行为。
- 新增 `test_getEnumIgnoreCase_nullClass`，覆盖 `getEnumIgnoreCase` 传入空 enum class 的异常行为。
- 不需要调整 import。

```java
    @Test
    public void test_isValidEnum() {
        assertTrue(EnumUtils.isValidEnum(Traffic.class, "RED"));
        assertTrue(EnumUtils.isValidEnum(Traffic.class, "AMBER"));
        assertTrue(EnumUtils.isValidEnum(Traffic.class, "GREEN"));
        assertFalse(EnumUtils.isValidEnum(Traffic.class, "PURPLE"));
        assertFalse(EnumUtils.isValidEnum(Traffic.class, null));
    }

    @Test(expected=NullPointerException.class)
    public void test_isValidEnum_nullClass() {
        EnumUtils.isValidEnum(null, "PURPLE");
    }

    @Test
    public void test_isValidEnumIgnoreCase() {
        assertTrue(EnumUtils.isValidEnumIgnoreCase(Traffic.class, "red"));
        assertTrue(EnumUtils.isValidEnumIgnoreCase(Traffic.class, "Amber"));
        assertTrue(EnumUtils.isValidEnumIgnoreCase(Traffic.class, "grEEn"));
        assertFalse(EnumUtils.isValidEnumIgnoreCase(Traffic.class, "purple"));
        assertFalse(EnumUtils.isValidEnumIgnoreCase(Traffic.class, null));
    }

    @Test(expected=NullPointerException.class)
    public void test_isValidEnumIgnoreCase_nullClass() {
        EnumUtils.isValidEnumIgnoreCase(null, "PURPLE");
    }

    @Test
    public void test_getEnum_nonEnumClass() {
        final Class rawType = Object.class;
        assertNull(EnumUtils.getEnum(rawType, "rawType"));
    }

    @Test
    public void test_getEnumIgnoreCase() {
        assertEquals(Traffic.RED, EnumUtils.getEnumIgnoreCase(Traffic.class, "red"));
        assertEquals(Traffic.AMBER, EnumUtils.getEnumIgnoreCase(Traffic.class, "Amber"));
        assertEquals(Traffic.GREEN, EnumUtils.getEnumIgnoreCase(Traffic.class, "grEEn"));
        assertNull(EnumUtils.getEnumIgnoreCase(Traffic.class, "purple"));
        assertNull(EnumUtils.getEnumIgnoreCase(Traffic.class, null));
    }

    @Test
    public void test_getEnumIgnoreCase_nonEnumClass() {
        final Class rawType = Object.class;
        assertNull(EnumUtils.getEnumIgnoreCase(rawType, "rawType"));
    }

    @Test(expected=NullPointerException.class)
    public void test_getEnumIgnoreCase_nullClass() {
        EnumUtils.getEnumIgnoreCase((Class<Traffic>) null, "PURPLE");
    }
```