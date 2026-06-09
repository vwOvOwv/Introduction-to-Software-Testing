# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `4cf3dc8c8f4ab9c353de64e79c4de113eec93473`
- B: `0e2ebd347c4a4afd6c4cf539678d2a23d3df9570`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `305493`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 77588, 'completion_tokens': 791, 'total_tokens': 78379, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 495}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 77204}`

---

- 新增 `testContainsDoubleNaN` 方法：对应生产代码修改后支持在 `contains` 中匹配 `Double.NaN` 的兼容性测试。
- 新增 `testIndexOfDoubleNaN` 方法：对应生产代码修改后支持在 `indexOf` 中匹配 `Double.NaN` 的兼容性测试。
- 无需新增或删除 import 语句，已有 `import static org.junit.jupiter.api.Assertions.assertTrue;` 等足以支持新方法。

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