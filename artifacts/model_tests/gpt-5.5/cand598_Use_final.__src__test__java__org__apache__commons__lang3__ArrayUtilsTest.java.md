# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `d5196e7fe47b3121c4d18f90164ca66979d5fd80`
- B: `764b9bba528487fb575b84766998086c24bb1f48`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `methods`
- user_chars: `5629`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1876, 'completion_tokens': 508, 'total_tokens': 2384}`

---

- 修改 `testContainsDoubleNaN`：对照测试 diff，仅将局部数组变量改为 `final`，无需调整 import。
- 修改 `testContainsFloatNaN`：对照测试 diff，仅将局部数组变量改为 `final`，无需调整 import。
- 修改 `testIndexOfDoubleNaN`：对照测试 diff，仅将局部数组变量改为 `final`，无需调整 import。
- 修改 `testIndexOfFloatNaN`：对照测试 diff，仅将局部数组变量改为 `final`，无需调整 import。

```java
@Test
public void testContainsDoubleNaN() {
    final double[] a = new double[] { Double.NEGATIVE_INFINITY, Double.NaN, Double.POSITIVE_INFINITY };
    assertTrue(ArrayUtils.contains(a, Double.POSITIVE_INFINITY));
    assertTrue(ArrayUtils.contains(a, Double.NEGATIVE_INFINITY));
    assertTrue(ArrayUtils.contains(a, Double.NaN));
}

@Test
public void testContainsFloatNaN() {
    final float[] array = new float[] { Float.NEGATIVE_INFINITY, Float.NaN, Float.POSITIVE_INFINITY };
    assertTrue(ArrayUtils.contains(array, Float.POSITIVE_INFINITY));
    assertTrue(ArrayUtils.contains(array, Float.NEGATIVE_INFINITY));
    assertTrue(ArrayUtils.contains(array, Float.NaN));
}

@Test
public void testIndexOfDoubleNaN() {
    final double[] array = new double[] { Double.NEGATIVE_INFINITY, Double.NaN, Double.POSITIVE_INFINITY, Double.NaN };
    assertEquals(0, ArrayUtils.indexOf(array, Double.NEGATIVE_INFINITY));
    assertEquals(1, ArrayUtils.indexOf(array, Double.NaN));
    assertEquals(2, ArrayUtils.indexOf(array, Double.POSITIVE_INFINITY));

}

@Test
public void testIndexOfFloatNaN() {
    final float[] array = new float[] { Float.NEGATIVE_INFINITY, Float.NaN, Float.POSITIVE_INFINITY, Float.NaN };
    assertEquals(0, ArrayUtils.indexOf(array, Float.NEGATIVE_INFINITY));
    assertEquals(1, ArrayUtils.indexOf(array, Float.NaN));
    assertEquals(2, ArrayUtils.indexOf(array, Float.POSITIVE_INFINITY));
}
```