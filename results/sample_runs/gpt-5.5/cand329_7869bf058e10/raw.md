# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `b0cd0eabd1e3c8274fd0cbbdabb05855ed0c32ff`
- B: `7869bf058e10be7684d4ba6f58346527b692f63a`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `155465`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 38992, 'completion_tokens': 3139, 'total_tokens': 42131}`

---

- 新增 `testReverseBooleanRange`，对应生产代码新增 `reverse(boolean[], int, int)` 的区间反转能力。
- 新增 `testReverseByteRange`，对应生产代码新增 `reverse(byte[], int, int)` 的区间反转能力。
- 新增 `testReverseCharRange`，对应生产代码新增 `reverse(char[], int, int)` 的区间反转能力。
- 新增 `testReverseDoubleRange`，对应生产代码新增 `reverse(double[], int, int)` 的区间反转能力。
- 新增 `testReverseFloatRange`，对应生产代码新增 `reverse(float[], int, int)` 的区间反转能力。
- 新增 `testReverseIntRange`，对应生产代码新增 `reverse(int[], int, int)` 的区间反转能力。
- 新增 `testReverseLongRange`，对应生产代码新增 `reverse(long[], int, int)` 的区间反转能力。
- 新增 `testReverseShortRange`，对应生产代码新增 `reverse(short[], int, int)` 的区间反转能力。
- 新增 `testReverseObjectRange`，对应生产代码新增 `reverse(Object[], int, int)` 的区间反转能力。
- 不需要调整 import，现有 `org.junit.Test` 与断言静态导入已满足新增测试。

```java
@Test
public void testReverseBooleanRange() {
    boolean[] array = new boolean[] {false, false, true};
    // The whole array
    ArrayUtils.reverse(array, 0, 3);
    assertTrue(array[0]);
    assertFalse(array[1]);
    assertFalse(array[2]);
    // a range
    array = new boolean[] {false, false, true};
    ArrayUtils.reverse(array, 0, 2);
    assertFalse(array[0]);
    assertFalse(array[1]);
    assertTrue(array[2]);
    // a range with a negative start
    array = new boolean[] {false, false, true};
    ArrayUtils.reverse(array, -1, 3);
    assertTrue(array[0]);
    assertFalse(array[1]);
    assertFalse(array[2]);
    // a range with a large stop idnex
    array = new boolean[] {false, false, true};
    ArrayUtils.reverse(array, -1, array.length + 1000);
    assertTrue(array[0]);
    assertFalse(array[1]);
    assertFalse(array[2]);
    // null
    array = null;
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(null, array);
}

@Test
public void testReverseByteRange() {
    byte[] array = new byte[] {1, 2, 3};
    // The whole array
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // a range
    array = new byte[] {1, 2, 3};
    ArrayUtils.reverse(array, 0, 2);
    assertEquals(2, array[0]);
    assertEquals(1, array[1]);
    assertEquals(3, array[2]);
    // a range with a negative start
    array = new byte[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, 3);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // a range with a large stop idnex
    array = new byte[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, array.length + 1000);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // null
    array = null;
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(null, array);
}

@Test
public void testReverseCharRange() {
    char[] array = new char[] {1, 2, 3};
    // The whole array
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // a range
    array = new char[] {1, 2, 3};
    ArrayUtils.reverse(array, 0, 2);
    assertEquals(2, array[0]);
    assertEquals(1, array[1]);
    assertEquals(3, array[2]);
    // a range with a negative start
    array = new char[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, 3);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // a range with a large stop idnex
    array = new char[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, array.length + 1000);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // null
    array = null;
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(null, array);
}

@Test
public void testReverseDoubleRange() {
    double[] array = new double[] {1, 2, 3};
    // The whole array
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(3, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(1, array[2], 0);
    // a range
    array = new double[] {1, 2, 3};
    ArrayUtils.reverse(array, 0, 2);
    assertEquals(2, array[0], 0);
    assertEquals(1, array[1], 0);
    assertEquals(3, array[2], 0);
    // a range with a negative start
    array = new double[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, 3);
    assertEquals(3, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(1, array[2], 0);
    // a range with a large stop idnex
    array = new double[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, array.length + 1000);
    assertEquals(3, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(1, array[2], 0);
    // null
    array = null;
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(null, array);
}

@Test
public void testReverseFloatRange() {
    float[] array = new float[] {1, 2, 3};
    // The whole array
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(3, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(1, array[2], 0);
    // a range
    array = new float[] {1, 2, 3};
    ArrayUtils.reverse(array, 0, 2);
    assertEquals(2, array[0], 0);
    assertEquals(1, array[1], 0);
    assertEquals(3, array[2], 0);
    // a range with a negative start
    array = new float[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, 3);
    assertEquals(3, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(1, array[2], 0);
    // a range with a large stop idnex
    array = new float[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, array.length + 1000);
    assertEquals(3, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(1, array[2], 0);
    // null
    array = null;
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(null, array);
}

@Test
public void testReverseIntRange() {
    int[] array = new int[] {1, 2, 3};
    // The whole array
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // a range
    array = new int[] {1, 2, 3};
    ArrayUtils.reverse(array, 0, 2);
    assertEquals(2, array[0]);
    assertEquals(1, array[1]);
    assertEquals(3, array[2]);
    // a range with a negative start
    array = new int[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, 3);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // a range with a large stop idnex
    array = new int[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, array.length + 1000);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // null
    array = null;
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(null, array);
}

@Test
public void testReverseLongRange() {
    long[] array = new long[] {1, 2, 3};
    // The whole array
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // a range
    array = new long[] {1, 2, 3};
    ArrayUtils.reverse(array, 0, 2);
    assertEquals(2, array[0]);
    assertEquals(1, array[1]);
    assertEquals(3, array[2]);
    // a range with a negative start
    array = new long[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, 3);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // a range with a large stop idnex
    array = new long[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, array.length + 1000);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // null
    array = null;
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(null, array);
}

@Test
public void testReverseShortRange() {
    short[] array = new short[] {1, 2, 3};
    // The whole array
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // a range
    array = new short[] {1, 2, 3};
    ArrayUtils.reverse(array, 0, 2);
    assertEquals(2, array[0]);
    assertEquals(1, array[1]);
    assertEquals(3, array[2]);
    // a range with a negative start
    array = new short[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, 3);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // a range with a large stop idnex
    array = new short[] {1, 2, 3};
    ArrayUtils.reverse(array, -1, array.length + 1000);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
    // null
    array = null;
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(null, array);
}

@Test
public void testReverseObjectRange() {
    String[] array = new String[] {"1", "2", "3"};
    // The whole array
    ArrayUtils.reverse(array, 0, 3);
    assertEquals("3", array[0]);
    assertEquals("2", array[1]);
    assertEquals("1", array[2]);
    // a range
    array = new String[] {"1", "2", "3"};
    ArrayUtils.reverse(array, 0, 2);
    assertEquals("2", array[0]);
    assertEquals("1", array[1]);
    assertEquals("3", array[2]);
    // a range with a negative start
    array = new String[] {"1", "2", "3"};
    ArrayUtils.reverse(array, -1, 3);
    assertEquals("3", array[0]);
    assertEquals("2", array[1]);
    assertEquals("1", array[2]);
    // a range with a large stop idnex
    array = new String[] {"1", "2", "3"};
    ArrayUtils.reverse(array, -1, array.length + 1000);
    assertEquals("3", array[0]);
    assertEquals("2", array[1]);
    assertEquals("1", array[2]);
    // null
    array = null;
    ArrayUtils.reverse(array, 0, 3);
    assertEquals(null, array);
}
```