# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `2f67045b9647de10ea5d01d8d1e98ac7de3e1cfb`
- B: `7ef106b23772995e4307f84afd1bee4e2337ce0c`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `146330`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 36096, 'completion_tokens': 533, 'total_tokens': 36629}`

---

- 新增辅助内部类 `TestClass`，用于覆盖新增的泛型 `ArrayUtils.nullToEmpty(T[], Class<T[]>)` 方法的数组类型。
- 新增 `testNullToEmptyGenericNull`，断言 `null` 泛型数组会按传入数组类型返回长度为 0 的非空数组。
- 新增 `testNullToEmptyGenericEmpty`，断言非 `null` 的空泛型数组会原样返回。
- 新增 `testNullToEmptyGeneric`，断言非空泛型数组会原样返回。
- 新增 `testNullToEmptyGenericNullType`，断言 `type` 参数为 `null` 时抛出 `IllegalArgumentException`。
- 不需要调整 import，现有 `org.junit.Test` 与 `static org.junit.Assert.*` 已满足新增测试。

```java
    private class TestClass {
    }

    @Test
    public void testNullToEmptyGenericNull() {
        final TestClass[] output = ArrayUtils.nullToEmpty(null, TestClass[].class);

        assertNotNull(output);
        assertEquals(0, output.length);
    }

    @Test
    public void testNullToEmptyGenericEmpty() {
        final TestClass[] input = new TestClass[]{};
        final TestClass[] output = ArrayUtils.nullToEmpty(input, TestClass[].class);

        assertSame(input, output);
    }

    @Test
    public void testNullToEmptyGeneric() {
        final TestClass[] input = new TestClass[]{new TestClass(), new TestClass()};
        final TestClass[] output = ArrayUtils.nullToEmpty(input, TestClass[].class);

        assertSame(input, output);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testNullToEmptyGenericNullType() {
        final TestClass[] input = new TestClass[]{};
        ArrayUtils.nullToEmpty(input, null);
    }
```