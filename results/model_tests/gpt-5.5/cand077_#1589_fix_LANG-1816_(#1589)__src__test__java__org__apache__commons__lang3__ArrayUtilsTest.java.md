# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9bca5d09c6d16a5524a3cd1d38305687ad7fdca4`
- B: `52c06bea2f2b6c277c517dc9f5bb0d62d17e073c`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `methods`
- user_chars: `5958`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2017, 'completion_tokens': 294, 'total_tokens': 2311}`

---

- 修改 `testIndexOfDoubleNaN`：生产代码新增了 `double` 容差重载对 `NaN` 的专门查找逻辑，因此补充断言覆盖 `ArrayUtils.indexOf(double[], double, double)` 对 `NaN`、正负无穷的行为；无需调整 import。

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
```