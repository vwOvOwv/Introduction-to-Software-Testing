# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9bca5d09c6d16a5524a3cd1d38305687ad7fdca4`
- B: `52c06bea2f2b6c277c517dc9f5bb0d62d17e073c`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `methods`
- user_chars: `5958`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2001, 'completion_tokens': 3992, 'total_tokens': 5993, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 3341}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1617}`

---

- 修改 `testIndexOfDoubleNaN` 方法：新增对 `Double.NEGATIVE_INFINITY`、`Double.NaN`、`Double.POSITIVE_INFINITY` 使用 tolerance `0` 的 `indexOf` 断言。
- 修改 `testIndexOfDoubleTolerance` 方法：在 `null` 和空数组测试后新增对 `Double.NaN` 使用 tolerance `0` 的 `indexOf` 断言。
- 修改 `testContainsDoubleNaN` 方法：新增对无穷和 NaN 使用 tolerance `0.1` 的 `contains` 断言。
- 无需调整 import。

```java
    @Test
    void testIndexOfDoubleNaN() {
        final double[] array = { Double.NEGATIVE_INFINITY, Double.NaN, Double.POSITIVE_INFINITY, Double.NaN };
        assertEquals(0, ArrayUtils.indexOf(array, Double.NEGATIVE_INFINITY));
        assertEquals(0, ArrayUtils.indexOf(array, Double.NEGATIVE_INFINITY, (double) 0));
        assertEquals(1, ArrayUtils.indexOf(array, Double.NaN));
        assertEquals(1, ArrayUtils.indexOf(array, Double.NaN, (double) 0));
        assertEquals(2, ArrayUtils.indexOf(array, Double.POSITIVE_INFINITY));
        assertEquals(2, ArrayUtils.indexOf(array, Double.POSITIVE_INFINITY, (double) 0));
    }

    @Test
    void testIndexOfDoubleTolerance() {
        double[] array = null;
        assertEquals(-1, ArrayUtils.indexOf(array, (double) 0, (double) 0));
        assertEquals(-1, ArrayUtils.indexOf(array, Double.NaN, (double) 0));
        array = new double[0];
        assertEquals(-1, ArrayUtils.indexOf(array, (double) 0, (double) 0));
        assertEquals(-1, ArrayUtils.indexOf(array, Double.NaN, (double) 0));
        array = new double[]{0, 1, 2, 3, 0};
        assertEquals(0, ArrayUtils.indexOf(array, 0, 0.3));
        assertEquals(2, ArrayUtils.indexOf(array, 2.2, 0.35));
    }

    @Test
    void testContainsDoubleNaN() {
        final double[] a = new double[] { 1, 2, Double.NaN, 3, Double.POSITIVE_INFINITY, Double.NEGATIVE_INFINITY };
        assertTrue(ArrayUtils.contains(a, Double.POSITIVE_INFINITY));
        assertTrue(ArrayUtils.contains(a, Double.NEGATIVE_INFINITY));
        assertTrue(ArrayUtils.contains(a, Double.NaN));
        assertTrue(ArrayUtils.contains(a, Double.POSITIVE_INFINITY, 0.1));
        assertTrue(ArrayUtils.contains(a, Double.NEGATIVE_INFINITY, 0.1));
        assertTrue(ArrayUtils.contains(a, Double.NaN, 0.1));
    }
```