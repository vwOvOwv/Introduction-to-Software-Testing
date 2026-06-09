# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `619a7024c4a808fbd3cde9d8545959d77a94717b`
- B: `55a2a03aa30836c814b9c2d50d5081a52f01d83c`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `232233`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 60838, 'completion_tokens': 5860, 'total_tokens': 66698}`

---

- 新增 `testIndexesOf` 和 `testIndexesOfWithStartIndex`，对应生产代码新增 `Object[]` 的 `indexesOf(...)` 返回所有匹配下标的 `BitSet`。
- 新增 `testIndexesOfLong` 和 `testIndexesOfLongWithStartIndex`，对应生产代码新增 `long[]` 的 `indexesOf(...)` 重载。
- 新增 `textIndexesOfInt` 和 `testIndexesOfIntWithStartIndex`，对应生产代码新增 `int[]` 的 `indexesOf(...)` 重载。
- 新增 `testIndexesOfShort` 和 `testIndexesOfShortWithStartIndex`，对应生产代码新增 `short[]` 的 `indexesOf(...)` 重载。
- 新增 `testIndexesOfChar` 和 `testIndexesOfCharWithStartIndex`，对应生产代码新增 `char[]` 的 `indexesOf(...)` 重载。
- 新增 `testIndexesOfByte` 和 `testIndexesOfByteWithStartIndex`，对应生产代码新增 `byte[]` 的 `indexesOf(...)` 重载。
- 新增 `testIndexesOfDouble`、`testIndexesOfDoubleWithStartIndex`、`testIndexesOfDoubleTolerance` 和 `testIndexesOfDoubleWithStartIndexTolerance`，对应生产代码新增 `double[]` 含 tolerance 的 `indexesOf(...)` 重载。
- 新增 `testIndexesOfFloat` 和 `testIndexesOfFloatWithStartIndex`，对应生产代码新增 `float[]` 的 `indexesOf(...)` 重载。
- 新增 `testIndexesOfBoolean` 和 `testIndexesOfBooleanWithStartIndex`，对应生产代码新增 `boolean[]` 的 `indexesOf(...)` 重载。
- 需要调整 import：新增 `java.util.BitSet` 以编译新增 `BitSet` 断言。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.util.Arrays;
import java.util.Collections;
import java.util.BitSet;
import java.util.Comparator;
import java.util.Date;
import java.util.Map;
import java.util.Random;

import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    public void testIndexesOf() {
        final Object[] array = new Object[]{"0", "1", "2", "3", null, "0"};
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf((Object[]) null, null));
        assertEquals(emptySet, ArrayUtils.indexesOf(new Object[0], "0"));
        testSet.set(5);
        testSet.set(0);
        assertEquals(testSet, ArrayUtils.indexesOf(array, "0"));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, "2"));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, "3"));
        testSet.clear();
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, null));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, "notInArray"));
    }

    @Test
    public void testIndexesOfWithStartIndex() {
        final Object[] array = new Object[]{"0", "1", "2", "3", "2", "3", "1", null, "0"};
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(null, null, 2));
        assertEquals(emptySet, ArrayUtils.indexesOf(new Object[0], "0", 0));
        assertEquals(emptySet, ArrayUtils.indexesOf(null, "0", 2));
        testSet.set(8);
        assertEquals(testSet, ArrayUtils.indexesOf(array, "0", 8));
        testSet.set(0);
        assertEquals(testSet, ArrayUtils.indexesOf(array, "0", 0));
        testSet.clear();
        testSet.set(6);
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, "1", 0));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, "1", 9));
        testSet.clear();
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, "2", 3));
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, "2", 0));
        testSet.clear();
        testSet.set(3);
        testSet.set(5);
        assertEquals(testSet, ArrayUtils.indexesOf(array, "3", 0));
        testSet.clear();
        testSet.set(7);
        assertEquals(testSet, ArrayUtils.indexesOf(array, null, 0));
    }

    @Test
    public void testIndexesOfLong() {
        final long[] array = new long[]{0, 1, 2, 3};
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf((long[]) null, 0));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 4));
        testSet.set(0);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 1));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 2));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 3));
    }

    @Test
    public void testIndexesOfLongWithStartIndex() {
        final long[] array = new long[]{0, 1, 2, 3, 2, 1, 0, 1};
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf((long[]) null, 0, 0));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 4, 0));
        testSet.set(6);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 0, 1));
        testSet.set(0);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 0, 0));
        testSet.clear();
        testSet.set(1);
        testSet.set(5);
        testSet.set(7);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 1, 0));
        testSet.clear();
        testSet.set(2);
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 2, 0));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 3, 0));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 3, 8));
    }

    @Test
    public void textIndexesOfInt() {
        int[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 0));
        array = new int[]{0, 1, 2, 3, 0};
        testSet.set(0);
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 1));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 2));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 3));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 99));
    }

    @Test
    public void testIndexesOfIntWithStartIndex() {
        int[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 0, 2));
        array = new int[]{0, 1, 2, 3, 0};
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 0, 2));
        testSet.set(0);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 0, 0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 1, 1));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 2, 0));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 3, 0));
        assertEquals(testSet, ArrayUtils.indexesOf(array, 3, -1));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 99, 0));
    }

    @Test
    public void testIndexesOfShort() {
        short[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, (short) 0));
        array = new short[]{0, 1, 2, 3, 0};
        testSet.set(0);
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (short) 0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (short) 1));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (short) 2));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (short) 3));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, (short) 99));
    }

    @Test
    public void testIndexesOfShortWithStartIndex() {
        short[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, (short) 0, 2));
        array = new short[]{0, 1, 2, 3, 0};
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (short) 0, 2));
        testSet.set(0);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (short) 0, 0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (short) 1, 1));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (short) 2, 0));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (short) 3, 0));
        assertEquals(testSet, ArrayUtils.indexesOf(array, (short) 3, -1));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, (short) 99, 0));
    }

    @Test
    public void testIndexesOfChar() {
        char[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 'a'));
        array = new char[]{'a', 'b', 'c', 'd', 'a'};
        testSet.set(0);
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 'a'));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 'b'));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 'c'));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 'd'));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 'e'));
    }

    @Test
    public void testIndexesOfCharWithStartIndex() {
        char[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 'a', 0));
        array = new char[]{'a', 'b', 'c', 'd', 'a'};
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 'a', 2));
        testSet.set(0);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 'a', 0));
        assertEquals(testSet, ArrayUtils.indexesOf(array, 'a', -1));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 'b', 1));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 'c', 0));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 'd', 0));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 'd', 5));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 'e', 0));
    }

    @Test
    public void testIndexesOfByte() {
        byte[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, (byte) 0));
        array = new byte[]{0, 1, 2, 3, 0};
        testSet.set(0);
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (byte) 0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (byte) 1));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (byte) 2));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (byte) 3));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, (byte) 99));
    }

    @Test
    public void testIndexesOfByteWithStartIndex() {
        byte[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, (byte) 0, 2));
        array = new byte[]{0, 1, 2, 3, 0};
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (byte) 0, 2));
        testSet.set(0);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (byte) 0, 0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (byte) 1, 1));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (byte) 2, 0));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (byte) 3, 0));
        assertEquals(testSet, ArrayUtils.indexesOf(array, (byte) 3, -1));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, (byte) 99, 0));
    }

    @SuppressWarnings("cast")
    @Test
    public void testIndexesOfDouble() {
        double[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 0));
        array = new double[]{0, 1, 2, 3, 0};
        testSet.set(0);
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 1));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 2));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 3));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 99));
    }

    @SuppressWarnings("cast")
    @Test
    public void testIndexesOfDoubleWithStartIndex() {
        double[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 0, 2));
        array = new double[]{0, 1, 2, 3, 0};
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 0, 2));
        testSet.set(0);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 0, 0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 1, 1));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 2, 0));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 3, 0));
        assertEquals(testSet, ArrayUtils.indexesOf(array, 3, -1));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 99, 0));
    }

    @SuppressWarnings("cast")
    @Test
    public void testIndexesOfDoubleTolerance() {
        double[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, (double) 0, (double) 0));
        array = new double[0];
        assertEquals(emptySet, ArrayUtils.indexesOf(array, (double) 0, (double) 0));
        array = new double[]{0, 1, 2, 3, 0};
        testSet.set(0);
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (double) 0, 0.3));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 4.15, 2.0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 1.00001324, 0.0001));
    }

    @SuppressWarnings("cast")
    @Test
    public void testIndexesOfDoubleWithStartIndexTolerance() {
        double[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, (double) 0, 0, (double) 0));
        array = new double[0];
        assertEquals(emptySet, ArrayUtils.indexesOf(array, (double) 0, 0, (double) 0));
        array = new double[]{0, 1, 2, 3, 0};
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (double) 0, 1, 0.3));
        testSet.set(0);
        assertEquals(testSet, ArrayUtils.indexesOf(array, (double) 0, 0, 0.3));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 2, 0, 0.35));
        assertEquals(testSet, ArrayUtils.indexesOf(array, 2, 2, 0.35));
        assertEquals(testSet, ArrayUtils.indexesOf(array, 2, -1, 0.35));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 2, 3, 0.35));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 4.15, 0, 2.0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 1.00001324, 0, 0.0001));
    }

    @SuppressWarnings("cast")
    @Test
    public void testIndexesOfFloat() {
        float[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 0));
        array = new float[]{0, 1, 2, 3, 0};
        testSet.set(0);
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 1));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 2));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 3));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 99));
    }

    @SuppressWarnings("cast")
    @Test
    public void testIndexesOfFloatWithStartIndex() {
        float[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 0, 2));
        array = new float[]{0, 1, 2, 3, 0};
        testSet.set(4);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 0, 2));
        testSet.set(0);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 0, 0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 1, 1));
        testSet.clear();
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 2, 0));
        testSet.clear();
        testSet.set(3);
        assertEquals(testSet, ArrayUtils.indexesOf(array, 3, 0));
        assertEquals(testSet, ArrayUtils.indexesOf(array, 3, -1));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, 99, 0));
    }

    @Test
    public void testIndexesOfBoolean() {
        boolean[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, true));
        array = new boolean[0];
        assertEquals(emptySet, ArrayUtils.indexesOf(array, true));
        array = new boolean[]{true, false, true};
        testSet.set(0);
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, true));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, false));
        array = new boolean[]{true, true};
        assertEquals(emptySet, ArrayUtils.indexesOf(array, false));
    }

    @Test
    public void testIndexesOfBooleanWithStartIndex() {
        boolean[] array = null;
        BitSet emptySet = new BitSet();
        BitSet testSet = new BitSet();
        assertEquals(emptySet, ArrayUtils.indexesOf(array, true, 0));
        array = new boolean[0];
        assertEquals(emptySet, ArrayUtils.indexesOf(array, true, 0));
        array = new boolean[]{true, false, true};
        testSet.set(2);
        assertEquals(testSet, ArrayUtils.indexesOf(array, true, 1));
        testSet.set(0);
        assertEquals(testSet, ArrayUtils.indexesOf(array, true, 0));
        testSet.clear();
        testSet.set(1);
        assertEquals(testSet, ArrayUtils.indexesOf(array, false, 1));
        array = new boolean[]{true, true};
        assertEquals(emptySet, ArrayUtils.indexesOf(array, false, 0));
        assertEquals(emptySet, ArrayUtils.indexesOf(array, false, -1));
    }
```