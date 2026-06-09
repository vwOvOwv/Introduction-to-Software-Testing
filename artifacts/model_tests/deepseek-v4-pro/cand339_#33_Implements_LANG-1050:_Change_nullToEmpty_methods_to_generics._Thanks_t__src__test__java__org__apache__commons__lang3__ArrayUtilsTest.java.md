# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `2f67045b9647de10ea5d01d8d1e98ac7de3e1cfb`
- B: `7ef106b23772995e4307f84afd1bee4e2337ce0c`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `146330`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 37003, 'completion_tokens': 1392, 'total_tokens': 38395, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 998}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 36619}`

---

- 新增内部类 `TestClass`，用于构造通用数组元素进行测试。
- 新增 `@Test` 方法 `testNullToEmptyGenericNull`，验证传入 `null` 数组时返回非空且长度为 0 的数组。
- 新增 `@Test` 方法 `testNullToEmptyGenericEmpty`，验证传入空数组时返回同一个引用（`assertSame`）。
- 新增 `@Test` 方法 `testNullToEmptyGeneric`，验证传入非空数组时返回同一个引用。
- 新增 `@Test` 方法 `testNullToEmptyGenericNullType`，使用 `expected=IllegalArgumentException.class` 验证传入 `null` 类型时抛出 `IllegalArgumentException`。
- 无需新增或调整 import。

```java
    private class TestClass{}

    @Test
    public void testNullToEmptyGenericNull() {
        TestClass[] output = ArrayUtils.nullToEmpty(null, TestClass[].class);

        assertTrue(output != null);
        assertTrue(output.length == 0);
    }

    @Test
    public void testNullToEmptyGenericEmpty() {
        TestClass[] input = new TestClass[]{};
        TestClass[] output = ArrayUtils.nullToEmpty(input, TestClass[].class);

        assertSame(input, output);
    }

    @Test
    public void testNullToEmptyGeneric() {
        TestClass[] input = new TestClass[]{new TestClass(), new TestClass()};
        TestClass[] output = ArrayUtils.nullToEmpty(input, TestClass[].class);

        assertSame(input, output);
    }

    @Test(expected=IllegalArgumentException.class)
    public void testNullToEmptyGenericNullType() {
        TestClass[] input = new TestClass[]{};
        ArrayUtils.nullToEmpty(input, null);
    }
```