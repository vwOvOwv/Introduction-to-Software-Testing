# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `09cee6a4ada4c7bb69fb32be33001290b744e0fa`
- B: `ef26a667633275fa656b74b841f9e74a3a6879ab`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `154536`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 38228, 'completion_tokens': 1557, 'total_tokens': 39785}`

---

- 新增 `testIsSorted`，覆盖新增的对象数组自然顺序 `ArrayUtils.isSorted(T[])`。
- 新增 `testIsSortedComparator`，覆盖新增的带 `Comparator` 的对象数组排序判断。
- 新增 `testIsSortedNullComparator`，覆盖新增的空比较器非法参数分支。
- 新增 `testIsSortedInt`、`testIsSortedFloat`、`testIsSortedLong`、`testIsSortedDouble`、`testIsSortedChar`、`testIsSortedByte`、`testIsSortedShort`、`testIsSortedBool`，覆盖新增的各 primitive 数组 `isSorted` 重载。
- 需要调整 import：新增 `java.util.Comparator`，并可将 JUnit 断言静态导入合并为 `org.junit.Assert.*`。

```java
// IMPORTS_START
import static org.junit.Assert.*;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Date;
import java.util.Map;

import org.junit.Test;
// IMPORTS_END

@Test
public void testIsSorted() {
    Integer[] array = null;
    assertTrue(ArrayUtils.isSorted(array));

    array = new Integer[]{1};
    assertTrue(ArrayUtils.isSorted(array));

    array = new Integer[]{1,2,3};
    assertTrue(ArrayUtils.isSorted(array));

    array = new Integer[]{1,3,2};
    assertFalse(ArrayUtils.isSorted(array));
}

@Test
public void testIsSortedComparator() {
    Comparator<Integer> c = new Comparator<Integer>() {
            public int compare(Integer o1, Integer o2) {
                    return o2.compareTo(o1);
                }
        };

    Integer[] array = null;
    assertTrue(ArrayUtils.isSorted(array, c));

    array = new Integer[]{1};
    assertTrue(ArrayUtils.isSorted(array, c));

    array = new Integer[]{3,2,1};
    assertTrue(ArrayUtils.isSorted(array, c));

    array = new Integer[]{1,3,2};
    assertFalse(ArrayUtils.isSorted(array, c));
}

@Test(expected = IllegalArgumentException.class)
public void testIsSortedNullComparator() throws Exception {
    ArrayUtils.isSorted(null, null);
}

@Test
public void testIsSortedInt() {
    int[] array = null;
    assertTrue(ArrayUtils.isSorted(array));

    array = new int[]{1};
    assertTrue(ArrayUtils.isSorted(array));

    array = new int[]{1,2,3};
    assertTrue(ArrayUtils.isSorted(array));

    array = new int[]{1,3,2};
    assertFalse(ArrayUtils.isSorted(array));
}

@Test
public void testIsSortedFloat() {
    float[] array = null;
    assertTrue(ArrayUtils.isSorted(array));

    array = new float[]{0f};
    assertTrue(ArrayUtils.isSorted(array));

    array = new float[]{-1f, 0f, 0.1f, 0.2f};
    assertTrue(ArrayUtils.isSorted(array));

    array = new float[]{-1f, 0.2f, 0.1f, 0f};
    assertFalse(ArrayUtils.isSorted(array));
}

@Test
public void testIsSortedLong() {
    long[] array = null;
    assertTrue(ArrayUtils.isSorted(array));

    array = new long[]{0L};
    assertTrue(ArrayUtils.isSorted(array));

    array = new long[]{-1L, 0L, 1L};
    assertTrue(ArrayUtils.isSorted(array));

    array = new long[]{-1L, 1L, 0L};
    assertFalse(ArrayUtils.isSorted(array));
}

@Test
public void testIsSortedDouble() {
    double[] array = null;
    assertTrue(ArrayUtils.isSorted(array));

    array = new double[]{0.0};
    assertTrue(ArrayUtils.isSorted(array));

    array = new double[]{-1.0, 0.0, 0.1, 0.2};
    assertTrue(ArrayUtils.isSorted(array));

    array = new double[]{-1.0, 0.2, 0.1, 0.0};
    assertFalse(ArrayUtils.isSorted(array));
}

@Test
public void testIsSortedChar() {
    char[] array = null;
    assertTrue(ArrayUtils.isSorted(array));

    array = new char[]{'a'};
    assertTrue(ArrayUtils.isSorted(array));

    array = new char[]{'a', 'b', 'c'};
    assertTrue(ArrayUtils.isSorted(array));

    array = new char[]{'a', 'c', 'b'};
    assertFalse(ArrayUtils.isSorted(array));
}

@Test
public void testIsSortedByte() {
    byte[] array = null;
    assertTrue(ArrayUtils.isSorted(array));

    array = new byte[]{0x10};
    assertTrue(ArrayUtils.isSorted(array));

    array = new byte[]{0x10, 0x20, 0x30};
    assertTrue(ArrayUtils.isSorted(array));

    array = new byte[]{0x10, 0x30, 0x20};
    assertFalse(ArrayUtils.isSorted(array));
}

@Test
public void testIsSortedShort() {
    short[] array = null;
    assertTrue(ArrayUtils.isSorted(array));

    array = new short[]{0};
    assertTrue(ArrayUtils.isSorted(array));

    array = new short[]{-1, 0, 1};
    assertTrue(ArrayUtils.isSorted(array));

    array = new short[]{-1, 1, 0};
    assertFalse(ArrayUtils.isSorted(array));
}

@Test
public void testIsSortedBool() {
    boolean[] array = null;
    assertTrue(ArrayUtils.isSorted(array));

    array = new boolean[]{true};
    assertTrue(ArrayUtils.isSorted(array));

    array = new boolean[]{false, true};
    assertTrue(ArrayUtils.isSorted(array));

    array = new boolean[]{true, false};
    assertFalse(ArrayUtils.isSorted(array));
}
```