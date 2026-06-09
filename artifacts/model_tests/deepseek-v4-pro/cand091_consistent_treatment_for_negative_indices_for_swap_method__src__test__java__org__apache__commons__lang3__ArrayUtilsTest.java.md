# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `f431270c59b6d4558da8dff625a7738591a0d541`
- B: `5b7608d1549989d92dd159392c19d9ba8ce0e62e`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `methods`
- user_chars: `46536`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 15779, 'completion_tokens': 5929, 'total_tokens': 21708, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 4306}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 15395}`

---

- 将新增测试逻辑到 `testSwapCharRange`、`testSwapFloatRange`、`testSwapDoubleRange`、`testSwapIntRange`、`testSwapLongRange` 和 `testSwapObjectRange` 方法中，以覆盖越界索引和无操作行为，替代原本预期抛出 `ArrayIndexOutOfBoundsException` 的测试。
- 将删除以下 12 个 `@Test` 方法：`testSwapCharOutOfRange`、`testSwapCharOutOfRangeLen`、`testSwapFloatOutOfRange`、`testSwapFloatOutOfRangeLen`、`testSwapDoubleOutOfRange`、`testSwapDoubleOutOfRangeLen`、`testSwapIntOutOfRange`、`testSwapIntOutOfRangeLen`、`testSwapLongOutOfRange`、`testSwapLongOutOfRangeLen`、`testSwapObjectOutOfRange`、`testSwapObjectOutOfRangeLen`，因为生产代码不再抛出异常。
- import 无需调整，原有测试基类已包含所需依赖。

```java
// DELETE_TESTS_START
testSwapCharOutOfRange
testSwapCharOutOfRangeLen
testSwapFloatOutOfRange
testSwapFloatOutOfRangeLen
testSwapDoubleOutOfRange
testSwapDoubleOutOfRangeLen
testSwapIntOutOfRange
testSwapIntOutOfRangeLen
testSwapLongOutOfRange
testSwapLongOutOfRangeLen
testSwapObjectOutOfRange
testSwapObjectOutOfRangeLen
// DELETE_TESTS_END

@Test
public void testSwapCharRange() {
    char[] array = new char[] {1, 2, 3, 4};
    ArrayUtils.swap(array, 0, 2, 1);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    assertEquals(4, array[3]);

    array = new char[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 3);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    
    array = new char[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2, 2);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
}

@Test
public void testSwapFloatRange() {
    float[] array = new float[] {1, 2, 3, 4};
    ArrayUtils.swap(array, 0, 2, 1);
    assertEquals(3, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(1, array[2], 0);
    assertEquals(4, array[3], 0);

    array = new float[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 3);
    assertEquals(1, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(3, array[2], 0);
    
    array = new float[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2, 2);
    assertEquals(3, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(1, array[2], 0);
}

@Test
public void testSwapDoubleRange() {
    double[] array = new double[] {1, 2, 3, 4};
    ArrayUtils.swap(array, 0, 2, 1);
    assertEquals(3, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(1, array[2], 0);
    assertEquals(4, array[3], 0);

    array = new double[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 3);
    assertEquals(1, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(3, array[2], 0);
    
    array = new double[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2, 2);
    assertEquals(3, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(1, array[2], 0);
}

@Test
public void testSwapIntRange() {
    int[] array = new int[] {1, 2, 3, 4};
    ArrayUtils.swap(array, 0, 2, 1);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    assertEquals(4, array[3]);
    
    array = new int[] {1, 2, 3};
    ArrayUtils.swap(array, 3, 0);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    
    array = new int[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2, 2);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
}

@Test
public void testSwapLongRange() {
    long[] array = new long[] {1, 2, 3, 4};
    ArrayUtils.swap(array, 0, 2, 1);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    assertEquals(4, array[3]);
    
    array = new long[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 3);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    
    array = new long[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2, 2);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
}

@Test
public void testSwapObjectRange() {
    String[] array = new String[] {"1", "2", "3", "4"};
    ArrayUtils.swap(array, 0, 2, 1);
    assertEquals("3", array[0]);
    assertEquals("2", array[1]);
    assertEquals("1", array[2]);
    assertEquals("4", array[3]);

    array = new String[] {"1", "2", "3", "4"};
    ArrayUtils.swap(array, -1, 2, 3);
    assertEquals("3", array[0]);
    assertEquals("4", array[1]);
    assertEquals("1", array[2]);
    assertEquals("2", array[3]);

    array = new String[] {"1", "2", "3", "4", "5"};
    ArrayUtils.swap(array, -3, 2, 3);
    assertEquals("3", array[0]);
    assertEquals("4", array[1]);
    assertEquals("5", array[2]);
    assertEquals("2", array[3]);
    assertEquals("1", array[4]);
}
```