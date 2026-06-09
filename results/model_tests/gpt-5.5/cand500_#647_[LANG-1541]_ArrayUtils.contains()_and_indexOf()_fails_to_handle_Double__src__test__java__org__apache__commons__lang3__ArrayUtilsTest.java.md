# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `4cf3dc8c8f4ab9c353de64e79c4de113eec93473`
- B: `0e2ebd347c4a4afd6c4cf539678d2a23d3df9570`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `305493`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 74741, 'completion_tokens': 345, 'total_tokens': 75086, 'prompt_tokens_details': {'cached_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 48}}`

---

- 新增 `testContainsDoubleNaN`：对应 `ArrayUtils.indexOf(double[], double, int)` 现在支持 `NaN` 匹配，从而 `contains(double[], NaN)` 也应返回 true。
- 新增 `testIndexOfDoubleNaN`：对应生产代码新增 `Double.isNaN` 分支，断言查找 `NaN` 返回第一个 `NaN` 的索引。
- 不需要调整 import：现有 `assertTrue`、`assertEquals` 和 `@Test` import 已覆盖新增测试。

```java
@Test
public void testContainsDoubleNaN() {
    double[] a = new double[] { Double.NEGATIVE_INFINITY, Double.NaN, Double.POSITIVE_INFINITY };
    assertTrue(ArrayUtils.contains(a, Double.POSITIVE_INFINITY));
    assertTrue(ArrayUtils.contains(a, Double.NEGATIVE_INFINITY));
    assertTrue(ArrayUtils.contains(a, Double.NaN));
}

@Test
public void testIndexOfDoubleNaN() {
    double[] array = new double[] { Double.NEGATIVE_INFINITY, Double.NaN, Double.POSITIVE_INFINITY, Double.NaN };
    assertEquals(0, ArrayUtils.indexOf(array, Double.NEGATIVE_INFINITY));
    assertEquals(1, ArrayUtils.indexOf(array, Double.NaN));
    assertEquals(2, ArrayUtils.indexOf(array, Double.POSITIVE_INFINITY));
}
```