# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `63d8a025e6f38ddfc966c4104ac783bcb59031e0`
- B: `a3995141bf1b8a478e86fdbecc95f2b98f892647`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `204726`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 53453, 'completion_tokens': 3244, 'total_tokens': 56697}`

---

- 新增 `testSwapPrimitiveAndObjectArrays`，对应生产代码新增的各基本类型及 `Object[]` 的 `swap(array, offset1, offset2)` 与 `swap(array, offset1, offset2, len)` 重载；无需调整 import。
- 新增 `testSwapOutOfRange`，对应新增 `swap` 在索引越界时应抛出 `ArrayIndexOutOfBoundsException` 的行为；无需调整 import。
- 新增 `testSwapRangeOutOfRange`，对应新增带 `len` 的 `swap` 在交换区间越界时应抛出 `ArrayIndexOutOfBoundsException` 的行为；无需调整 import。
- 新增 `testShiftPrimitiveAndObjectArrays`，对应生产代码新增的各基本类型及 `Object[]` 的整数组 `shift(array, offset)` 重载；无需调整 import。
- 新增 `testShiftPrimitiveAndObjectArrayRanges`，对应生产代码新增的各基本类型及 `Object[]` 的区间 `shift(array, start, end, offset)` 重载；无需调整 import。

```java
@Test
public void testSwapPrimitiveAndObjectArrays() {
    char[] chars = new char[] {1, 2, 3, 4};
    ArrayUtils.swap(chars, 0, 2);
    assertArrayEquals(new char[] {3, 2, 1, 4}, chars);
    ArrayUtils.swap(chars, 0, 2, 2);
    assertArrayEquals(new char[] {1, 4, 3, 2}, chars);

    byte[] bytes = new byte[] {1, 2, 3, 4};
    ArrayUtils.swap(bytes, 0, 2);
    assertArrayEquals(new byte[] {3, 2, 1, 4}, bytes);
    ArrayUtils.swap(bytes, 0, 2, 2);
    assertArrayEquals(new byte[] {1, 4, 3, 2}, bytes);

    short[] shorts = new short[] {1, 2, 3, 4};
    ArrayUtils.swap(shorts, 0, 2);
    assertArrayEquals(new short[] {3, 2, 1, 4}, shorts);
    ArrayUtils.swap(shorts, 0, 2, 2);
    assertArrayEquals(new short[] {1, 4, 3, 2}, shorts);

    int[] ints = new int[] {1, 2, 3, 4};
    ArrayUtils.swap(ints, 0, 2);
    assertArrayEquals(new int[] {3, 2, 1, 4}, ints);
    ArrayUtils.swap(ints, 0, 2, 2);
    assertArrayEquals(new int[] {1, 4, 3, 2}, ints);

    long[] longs = new long[] {1, 2, 3, 4};
    ArrayUtils.swap(longs, 0, 2);
    assertArrayEquals(new long[] {3, 2, 1, 4}, longs);
    ArrayUtils.swap(longs, 0, 2, 2);
    assertArrayEquals(new long[] {1, 4, 3, 2}, longs);

    float[] floats = new float[] {1, 2, 3, 4};
    ArrayUtils.swap(floats, 0, 2);
    assertArrayEquals(new float[] {3, 2, 1, 4}, floats, 0);
    ArrayUtils.swap(floats, 0, 2, 2);
    assertArrayEquals(new float[] {1, 4, 3, 2}, floats, 0);

    double[] doubles = new double[] {1, 2, 3, 4};
    ArrayUtils.swap(doubles, 0, 2);
    assertArrayEquals(new double[] {3, 2, 1, 4}, doubles, 0);
    ArrayUtils.swap(doubles, 0, 2, 2);
    assertArrayEquals(new double[] {1, 4, 3, 2}, doubles, 0);

    boolean[] booleans = new boolean[] {true, false, false, true};
    ArrayUtils.swap(booleans, 0, 2);
    assertArrayEquals(new boolean[] {false, false, true, true}, booleans);
    ArrayUtils.swap(booleans, 0, 2, 2);
    assertArrayEquals(new boolean[] {true, true, false, false}, booleans);

    String[] objects = new String[] {"1", "2", "3", "4"};
    ArrayUtils.swap(objects, 0, 2);
    assertArrayEquals(new String[] {"3", "2", "1", "4"}, objects);
    ArrayUtils.swap(objects, 0, 2, 2);
    assertArrayEquals(new String[] {"1", "4", "3", "2"}, objects);

    ArrayUtils.swap((Object[]) null, 0, 1);
    ArrayUtils.swap((int[]) null, 0, 1);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapOutOfRange() {
    ArrayUtils.swap(new int[] {1, 2, 3}, 0, 3);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapRangeOutOfRange() {
    ArrayUtils.swap(new String[] {"1", "2", "3"}, 0, 2, 2);
}

@Test
public void testShiftPrimitiveAndObjectArrays() {
    int[] ints = new int[] {1, 2, 3, 4};
    ArrayUtils.shift(ints, 1);
    assertArrayEquals(new int[] {4, 1, 2, 3}, ints);
    ArrayUtils.shift(ints, -1);
    assertArrayEquals(new int[] {1, 2, 3, 4}, ints);
    ArrayUtils.shift(ints, 5);
    assertArrayEquals(new int[] {4, 1, 2, 3}, ints);
    ArrayUtils.shift(ints, -3);
    assertArrayEquals(new int[] {3, 4, 1, 2}, ints);

    long[] longs = new long[] {1, 2, 3, 4};
    ArrayUtils.shift(longs, 1);
    assertArrayEquals(new long[] {4, 1, 2, 3}, longs);

    short[] shorts = new short[] {1, 2, 3, 4};
    ArrayUtils.shift(shorts, 1);
    assertArrayEquals(new short[] {4, 1, 2, 3}, shorts);

    byte[] bytes = new byte[] {1, 2, 3, 4};
    ArrayUtils.shift(bytes, 1);
    assertArrayEquals(new byte[] {4, 1, 2, 3}, bytes);

    char[] chars = new char[] {1, 2, 3, 4};
    ArrayUtils.shift(chars, 1);
    assertArrayEquals(new char[] {4, 1, 2, 3}, chars);

    float[] floats = new float[] {1, 2, 3, 4};
    ArrayUtils.shift(floats, 1);
    assertArrayEquals(new float[] {4, 1, 2, 3}, floats, 0);

    double[] doubles = new double[] {1, 2, 3, 4};
    ArrayUtils.shift(doubles, 1);
    assertArrayEquals(new double[] {4, 1, 2, 3}, doubles, 0);

    boolean[] booleans = new boolean[] {true, false, false, true};
    ArrayUtils.shift(booleans, 1);
    assertArrayEquals(new boolean[] {true, true, false, false}, booleans);

    String[] objects = new String[] {"1", "2", "3", "4"};
    ArrayUtils.shift(objects, 1);
    assertArrayEquals(new String[] {"4", "1", "2", "3"}, objects);
    ArrayUtils.shift(objects, 4);
    assertArrayEquals(new String[] {"4", "1", "2", "3"}, objects);

    ArrayUtils.shift((Object[]) null, 1);
    ArrayUtils.shift((int[]) null, 1);
}

@Test
public void testShiftPrimitiveAndObjectArrayRanges() {
    int[] ints = new int[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(ints, 1, 3, 1);
    assertArrayEquals(new int[] {1, 3, 2, 4, 5}, ints);
    ArrayUtils.shift(ints, 1, 4, 2);
    assertArrayEquals(new int[] {1, 2, 4, 3, 5}, ints);

    long[] longs = new long[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(longs, 1, 3, 1);
    assertArrayEquals(new long[] {1, 3, 2, 4, 5}, longs);

    short[] shorts = new short[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(shorts, 1, 3, 1);
    assertArrayEquals(new short[] {1, 3, 2, 4, 5}, shorts);

    byte[] bytes = new byte[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(bytes, 1, 3, 1);
    assertArrayEquals(new byte[] {1, 3, 2, 4, 5}, bytes);

    char[] chars = new char[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(chars, 1, 3, 1);
    assertArrayEquals(new char[] {1, 3, 2, 4, 5}, chars);

    float[] floats = new float[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(floats, 1, 3, 1);
    assertArrayEquals(new float[] {1, 3, 2, 4, 5}, floats, 0);

    double[] doubles = new double[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(doubles, 1, 3, 1);
    assertArrayEquals(new double[] {1, 3, 2, 4, 5}, doubles, 0);

    boolean[] booleans = new boolean[] {false, true, false, true, false};
    ArrayUtils.shift(booleans, 1, 3, 1);
    assertArrayEquals(new boolean[] {false, false, true, true, false}, booleans);

    String[] objects = new String[] {"1", "2", "3", "4", "5"};
    ArrayUtils.shift(objects, 1, 3, 1);
    assertArrayEquals(new String[] {"1", "3", "2", "4", "5"}, objects);
    ArrayUtils.shift(objects, 1, 4, 2);
    assertArrayEquals(new String[] {"1", "2", "4", "3", "5"}, objects);

    int[] noElements = new int[] {1, 2, 3, 4};
    ArrayUtils.shift(noElements, 1, 1, 1);
    assertArrayEquals(new int[] {1, 2, 3, 4}, noElements);
}
```