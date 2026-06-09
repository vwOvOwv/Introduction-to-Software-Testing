# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `495167a3922826b19b381c3151634d66ac85b9b4`
- B: `5b699d076518cbf2dddc286f65cb06d0873dae16`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `methods`
- user_chars: `30739`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7918, 'completion_tokens': 622, 'total_tokens': 8540}`

---

- 新增 `testGet`，覆盖新增的 `ArrayUtils.get(T[], int)` 在 `null` 数组、空数组、越界索引和有效索引下的返回值。
- 新增 `testGetDefault`，覆盖新增的 `ArrayUtils.get(T[], int, T)` 在默认值为 `null` 和非 `null` 时的越界与有效索引行为。
- 不需要调整 import，现有断言静态导入和同包 `StringUtils` 可直接使用。

```java
    @Test
    public void testGet() {
        assertNull(ArrayUtils.get(null, -1));
        assertNull(ArrayUtils.get(null, 0));
        assertNull(ArrayUtils.get(null, 1));
        final String[] array0 = {};
        assertNull(ArrayUtils.get(array0, -1));
        assertNull(ArrayUtils.get(array0, 0));
        assertNull(ArrayUtils.get(array0, 1));
        final String[] array1 = { StringUtils.EMPTY };
        assertEquals(null, ArrayUtils.get(array1, -1));
        assertEquals(StringUtils.EMPTY, ArrayUtils.get(array1, 0));
        assertEquals(null, ArrayUtils.get(array1, 1));
    }

    @Test
    public void testGetDefault() {
        // null default
        {
            assertNull(ArrayUtils.get(null, -1, null));
            assertNull(ArrayUtils.get(null, 0, null));
            assertNull(ArrayUtils.get(null, 1, null));
            final String[] array0 = {};
            assertNull(ArrayUtils.get(array0, -1, null));
            assertNull(ArrayUtils.get(array0, 0, null));
            assertNull(ArrayUtils.get(array0, 1, null));
            final String[] array1 = { StringUtils.EMPTY };
            assertEquals(null, ArrayUtils.get(array1, -1, null));
            assertEquals(StringUtils.EMPTY, ArrayUtils.get(array1, 0, null));
            assertEquals(null, ArrayUtils.get(array1, 1, null));
        }
        // non-null default
        {
            final String defaultValue = "defaultValue";
            final String[] array1 = { StringUtils.EMPTY };
            assertEquals(defaultValue, ArrayUtils.get(array1, -1, defaultValue));
            assertEquals(StringUtils.EMPTY, ArrayUtils.get(array1, 0, defaultValue));
            assertEquals(defaultValue, ArrayUtils.get(array1, 1, defaultValue));
        }
    }
```