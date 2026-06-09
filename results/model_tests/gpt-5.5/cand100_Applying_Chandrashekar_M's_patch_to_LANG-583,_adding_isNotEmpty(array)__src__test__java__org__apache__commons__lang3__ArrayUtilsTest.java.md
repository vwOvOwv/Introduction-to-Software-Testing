# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `23f3b9084354089b1a6b58629877ccc58292687c`
- B: `643302af8c0e10ed7ee1d9ca3c60fa0f61eaaf08`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `119182`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 29469, 'completion_tokens': 914, 'total_tokens': 30383}`

---

- 新增测试方法 `testIsNotEmptyObject`，对应生产代码新增的 `ArrayUtils.isNotEmpty(Object[])` 泛型对象数组重载，断言 `null`、空数组和非空数组行为。
- 新增测试方法 `testIsNotEmptyPrimitives`，对应生产代码新增的所有 primitive 数组 `isNotEmpty` 重载，覆盖 `null`、空数组和非空数组。
- 不需要调整 import，当前测试类继承 `junit.framework.TestCase`，已有 `assertFalse` / `assertTrue` 可用。

```java
/**
 * Test for {@link ArrayUtils#isNotEmpty(java.lang.Object[])}.
 */
public void testIsNotEmptyObject() {
    Object[] emptyArray = new Object[] {};
    Object[] notEmptyArray = new Object[] { new String("Value") };
    assertFalse(ArrayUtils.isNotEmpty((Object[]) null));
    assertFalse(ArrayUtils.isNotEmpty(emptyArray));
    assertTrue(ArrayUtils.isNotEmpty(notEmptyArray));
}

/**
 * Tests for {@link ArrayUtils#isNotEmpty(long[])},
 * {@link ArrayUtils#isNotEmpty(int[])},
 * {@link ArrayUtils#isNotEmpty(short[])},
 * {@link ArrayUtils#isNotEmpty(char[])},
 * {@link ArrayUtils#isNotEmpty(byte[])},
 * {@link ArrayUtils#isNotEmpty(double[])},
 * {@link ArrayUtils#isNotEmpty(float[])} and
 * {@link ArrayUtils#isNotEmpty(boolean[])}.
 */
public void testIsNotEmptyPrimitives() {
    long[] emptyLongArray = new long[] {};
    long[] notEmptyLongArray = new long[] { 1L };
    assertFalse(ArrayUtils.isNotEmpty((long[]) null));
    assertFalse(ArrayUtils.isNotEmpty(emptyLongArray));
    assertTrue(ArrayUtils.isNotEmpty(notEmptyLongArray));

    int[] emptyIntArray = new int[] {};
    int[] notEmptyIntArray = new int[] { 1 };
    assertFalse(ArrayUtils.isNotEmpty((int[]) null));
    assertFalse(ArrayUtils.isNotEmpty(emptyIntArray));
    assertTrue(ArrayUtils.isNotEmpty(notEmptyIntArray));

    short[] emptyShortArray = new short[] {};
    short[] notEmptyShortArray = new short[] { 1 };
    assertFalse(ArrayUtils.isNotEmpty((short[]) null));
    assertFalse(ArrayUtils.isNotEmpty(emptyShortArray));
    assertTrue(ArrayUtils.isNotEmpty(notEmptyShortArray));

    char[] emptyCharArray = new char[] {};
    char[] notEmptyCharArray = new char[] { 1 };
    assertFalse(ArrayUtils.isNotEmpty((char[]) null));
    assertFalse(ArrayUtils.isNotEmpty(emptyCharArray));
    assertTrue(ArrayUtils.isNotEmpty(notEmptyCharArray));

    byte[] emptyByteArray = new byte[] {};
    byte[] notEmptyByteArray = new byte[] { 1 };
    assertFalse(ArrayUtils.isNotEmpty((byte[]) null));
    assertFalse(ArrayUtils.isNotEmpty(emptyByteArray));
    assertTrue(ArrayUtils.isNotEmpty(notEmptyByteArray));

    double[] emptyDoubleArray = new double[] {};
    double[] notEmptyDoubleArray = new double[] { 1.0 };
    assertFalse(ArrayUtils.isNotEmpty((double[]) null));
    assertFalse(ArrayUtils.isNotEmpty(emptyDoubleArray));
    assertTrue(ArrayUtils.isNotEmpty(notEmptyDoubleArray));

    float[] emptyFloatArray = new float[] {};
    float[] notEmptyFloatArray = new float[] { 1.0F };
    assertFalse(ArrayUtils.isNotEmpty((float[]) null));
    assertFalse(ArrayUtils.isNotEmpty(emptyFloatArray));
    assertTrue(ArrayUtils.isNotEmpty(notEmptyFloatArray));

    boolean[] emptyBooleanArray = new boolean[] {};
    boolean[] notEmptyBooleanArray = new boolean[] { true };
    assertFalse(ArrayUtils.isNotEmpty((boolean[]) null));
    assertFalse(ArrayUtils.isNotEmpty(emptyBooleanArray));
    assertTrue(ArrayUtils.isNotEmpty(notEmptyBooleanArray));
}
```