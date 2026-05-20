# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `48d6e758f79255da5a1e307a2bbcfa60726ad8a0`
- B: `623235ebca46bea1a6e8cc02b7d7084c1698ab80`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `350964`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 106563, 'completion_tokens': 2528, 'total_tokens': 109091, 'prompt_tokens_details': {'cached_tokens': 106496}, 'prompt_cache_hit_tokens': 106496, 'prompt_cache_miss_tokens': 67}`

---

- 新增 `testShuffleBoolean` 方法：增加对 `null` 和空数组的调用，与生产代码中 `shuffle(boolean[])` 的 null-safe 变更对应。
- 修改 `testShuffleBooleanRandom` 方法：增加对 `null` 数组、`null` Random、空数组的调用，以及 `shuffle(array1, null)` 后数组不变的断言，与生产代码中 `shuffle(boolean[], Random)` 的 null-safe 变更对应。
- 新增 `testShuffleByte` 方法：增加对 `null` 和空数组的调用，与生产代码中 `shuffle(byte[])` 的 null-safe 变更对应。
- 修改 `testShuffleByteRandom` 方法：增加对 `null` 数组、`null` Random、空数组的调用，以及 `shuffle(array1, null)` 后数组不变的断言，与生产代码中 `shuffle(byte[], Random)` 的 null-safe 变更对应。
- 新增 `testShuffleChar` 方法：增加对 `null` 和空数组的调用，与生产代码中 `shuffle(char[])` 的 null-safe 变更对应。
- 修改 `testShuffleCharRandom` 方法：增加对 `null` 数组、`null` Random、空数组的调用，以及 `shuffle(array1, null)` 后数组不变的断言，与生产代码中 `shuffle(char[], Random)` 的 null-safe 变更对应。
- 新增 `testShuffleDouble` 方法：增加对 `null` 和空数组的调用，与生产代码中 `shuffle(double[])` 的 null-safe 变更对应。
- 修改 `testShuffleDoubleRandom` 方法：增加对 `null` 数组、`null` Random、空数组的调用，以及 `shuffle(array1, null)` 后数组不变的断言，与生产代码中 `shuffle(double[], Random)` 的 null-safe 变更对应。
- 新增 `testShuffleFloat` 方法：增加对 `null` 和空数组的调用，与生产代码中 `shuffle(float[])` 的 null-safe 变更对应。
- 修改 `testShuffleFloatRandom` 方法：增加对 `null` 数组、`null` Random、空数组的调用，以及 `shuffle(array1, null)` 后数组不变的断言，与生产代码中 `shuffle(float[], Random)` 的 null-safe 变更对应。
- 新增 `testShuffleInt` 方法：增加对 `null` 和空数组的调用，与生产代码中 `shuffle(int[])` 的 null-safe 变更对应。
- 修改 `testShuffleIntRandom` 方法：增加对 `null` 数组、`null` Random、空数组的调用，以及 `shuffle(array1, null)` 后数组不变的断言，与生产代码中 `shuffle(int[], Random)` 的 null-safe 变更对应。
- 新增 `testShuffleLong` 方法：增加对 `null` 和空数组的调用，与生产代码中 `shuffle(long[])` 的 null-safe 变更对应。
- 修改 `testShuffleLongRandom` 方法：增加对 `null` 数组、`null` Random、空数组的调用，以及 `shuffle(array1, null)` 后数组不变的断言，与生产代码中 `shuffle(long[], Random)` 的 null-safe 变更对应。
- 新增 `testShuffleShort` 方法：增加对 `null` 和空数组的调用，与生产代码中 `shuffle(short[])` 的 null-safe 变更对应。
- 修改 `testShuffleShortRandom` 方法：增加对 `null` 数组、`null` Random、空数组的调用，以及 `shuffle(array1, null)` 后数组不变的断言，与生产代码中 `shuffle(short[], Random)` 的 null-safe 变更对应。
- 新增 `testShuffleString` 方法：增加对 `null` 和空数组的调用，与生产代码中 `shuffle(Object[])` 的 null-safe 变更对应。
- 修改 `testShuffleStringRandom` 方法：增加对 `null` 数组、`null` Random、空数组的调用，以及 `shuffle(array1, null)` 后数组不变的断言，与生产代码中 `shuffle(Object[], Random)` 的 null-safe 变更对应。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Arrays;
import java.util.BitSet;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;
import java.util.Map;
import java.util.Random;
import java.util.function.Function;
import java.util.function.Supplier;

import org.apache.commons.lang3.function.Suppliers;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    void testShuffleBoolean() {
        ArrayUtils.shuffle((boolean[]) null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_BOOLEAN_ARRAY);
        // Don't use a "small" array to reduce spurious failures.
        final boolean[] array1 = { true, false, true, true, false, false, true, false, false, true, true, false, true, true, false, false, true, false, false,
                true, true, false, true, true, false, false, true, false, false, true, false, true, true, false, true, true, false, false, true, false, false,
                false, true, true, false, false, true, false, false, true, false, true, true, false, true, true, false, false, true, false };
        final boolean[] array2 = ArrayUtils.clone(array1);
        ArrayUtils.shuffle(array1);
        assertFalse(Arrays.equals(array1, array2));
    }

    @Test
    void testShuffleBooleanRandom() {
        ArrayUtils.shuffle((boolean[]) null, null);
        ArrayUtils.shuffle((boolean[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_BOOLEAN_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_BOOLEAN_ARRAY, seededRandom());
        // Don't use a "small" array to reduce spurious failures.
        final boolean[] array1 = { true, false, true, true, false, false, true, false, false, true, true, false, true, true, false, false, true, false, false,
                true, true, false, true, true, false, false, true, false, false, true, false, true, true, false, true, true, false, false, true, false, false,
                false, true, true, false, false, true, false, false, true, false, true, true, false, true, true, false, false, true, false };
        final boolean[] array2 = ArrayUtils.clone(array1);
        // no shuffle
        ArrayUtils.shuffle(array1, null);
        assertTrue(Arrays.equals(array1, array2));
        // actual shuffle
        ArrayUtils.shuffle(array1, seededRandom());
        assertFalse(Arrays.equals(array1, array2));
    }

    @Test
    void testShuffleByte() {
        ArrayUtils.shuffle((byte[]) null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_BYTE_ARRAY);
        // Don't use a "small" array, reduce spurious failures.
        final byte[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2,
                3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final byte[] array2 = ArrayUtils.clone(array1);
        ArrayUtils.shuffle(array1);
        assertFalse(Arrays.equals(array1, array2));
        for (final byte element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleByteRandom() {
        ArrayUtils.shuffle((byte[]) null, null);
        ArrayUtils.shuffle((byte[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_BYTE_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_BYTE_ARRAY, seededRandom());
        // Don't use a "small" array, reduce spurious failures.
        final byte[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2,
                3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final byte[] array2 = ArrayUtils.clone(array1);
        // no shuffle
        ArrayUtils.shuffle(array1, null);
        assertTrue(Arrays.equals(array1, array2));
        // actual shuffle
        ArrayUtils.shuffle(array1, seededRandom());
        assertFalse(Arrays.equals(array1, array2));
        for (final byte element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleChar() {
        ArrayUtils.shuffle((char[]) null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_CHAR_ARRAY);
        // Don't use a "small" array, reduce spurious failures.
        final char[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2,
                3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final char[] array2 = ArrayUtils.clone(array1);
        ArrayUtils.shuffle(array1);
        assertFalse(Arrays.equals(array1, array2));
        for (final char element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleCharRandom() {
        ArrayUtils.shuffle((char[]) null, null);
        ArrayUtils.shuffle((char[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_CHAR_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_CHAR_ARRAY, seededRandom());
        // Don't use a "small" array, reduce spurious failures.
        final char[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2,
                3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final char[] array2 = ArrayUtils.clone(array1);
        // no shuffle
        ArrayUtils.shuffle(array1, null);
        assertTrue(Arrays.equals(array1, array2));
        // actual shuffle
        ArrayUtils.shuffle(array1, seededRandom());
        assertFalse(Arrays.equals(array1, array2));
        for (final char element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleDouble() {
        ArrayUtils.shuffle((double[]) null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_DOUBLE_ARRAY);
        // Don't use a "small" array, reduce spurious failures.
        final double[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1,
                2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final double[] array2 = ArrayUtils.clone(array1);
        ArrayUtils.shuffle(array1);
        assertFalse(Arrays.equals(array1, array2));
        for (final double element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleDoubleRandom() {
        ArrayUtils.shuffle((double[]) null, null);
        ArrayUtils.shuffle((double[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_DOUBLE_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_DOUBLE_ARRAY, seededRandom());
        // Don't use a "small" array, reduce spurious failures.
        final double[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1,
                2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final double[] array2 = ArrayUtils.clone(array1);
        // no shuffle
        ArrayUtils.shuffle(array1, null);
        assertTrue(Arrays.equals(array1, array2));
        // actual shuffle
        ArrayUtils.shuffle(array1, seededRandom());
        assertFalse(Arrays.equals(array1, array2));
        for (final double element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleFloat() {
        ArrayUtils.shuffle((float[]) null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_FLOAT_ARRAY);
        // Don't use a "small" array, reduce spurious failures.
        final float[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1,
                2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final float[] array2 = ArrayUtils.clone(array1);
        ArrayUtils.shuffle(array1);
        assertFalse(Arrays.equals(array1, array2));
        for (final float element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleFloatRandom() {
        ArrayUtils.shuffle((float[]) null, null);
        ArrayUtils.shuffle((float[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_FLOAT_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_FLOAT_ARRAY, seededRandom());
        // Don't use a "small" array, reduce spurious failures.
        final float[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1,
                2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final float[] array2 = ArrayUtils.clone(array1);
        // no shuffle
        ArrayUtils.shuffle(array1, null);
        assertTrue(Arrays.equals(array1, array2));
        // actual shuffle
        ArrayUtils.shuffle(array1, seededRandom());
        assertFalse(Arrays.equals(array1, array2));
        for (final float element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleInt() {
        ArrayUtils.shuffle((int[]) null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_INT_ARRAY);
        // Don't use a "small" array, reduce spurious failures.
        final int[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2,
                3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final int[] array2 = ArrayUtils.clone(array1);
        ArrayUtils.shuffle(array1);
        assertFalse(Arrays.equals(array1, array2));
        for (final int element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleIntRandom() {
        ArrayUtils.shuffle((int[]) null, null);
        ArrayUtils.shuffle((int[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_INT_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_INT_ARRAY, seededRandom());
        // Don't use a "small" array, reduce spurious failures.
        final int[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2,
                3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final int[] array2 = ArrayUtils.clone(array1);
        // no shuffle
        ArrayUtils.shuffle(array1, null);
        assertTrue(Arrays.equals(array1, array2));
        // actual shuffle
        ArrayUtils.shuffle(array1);
        assertFalse(Arrays.equals(array1, array2));
        for (final int element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleLong() {
        ArrayUtils.shuffle((long[]) null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_LONG_ARRAY);
        // Don't use a "small" array, reduce spurious failures.
        final long[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2,
                3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final long[] array2 = ArrayUtils.clone(array1);
        ArrayUtils.shuffle(array1);
        assertFalse(Arrays.equals(array1, array2));
        for (final long element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleLongRandom() {
        ArrayUtils.shuffle((long[]) null, null);
        ArrayUtils.shuffle((long[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_LONG_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_LONG_ARRAY, seededRandom());
        // Don't use a "small" array, reduce spurious failures.
        final long[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2,
                3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9```java
    @Test
    void testShuffleLongRandom() {
        ArrayUtils.shuffle((long[]) null, null);
        ArrayUtils.shuffle((long[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_LONG_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_LONG_ARRAY, seededRandom());
        // Don't use a "small" array, reduce spurious failures.
        final long[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2,
                3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
                1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final long[] array2 = ArrayUtils.clone(array1);
        // no shuffle
        ArrayUtils.shuffle(array1, null);
        assertTrue(Arrays.equals(array1, array2));
        // actual shuffle
        ArrayUtils.shuffle(array1, seededRandom());
        assertFalse(Arrays.equals(array1, array2));
        for (final long element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleShort() {
        ArrayUtils.shuffle((short[]) null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_SHORT_ARRAY);
        // Don't use a "small" array, reduce spurious failures.
        final short[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1,
                2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final short[] array2 = ArrayUtils.clone(array1);
        ArrayUtils.shuffle(array1);
        assertFalse(Arrays.equals(array1, array2));
        for (final short element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleShortRandom() {
        ArrayUtils.shuffle((short[]) null, null);
        ArrayUtils.shuffle((short[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_SHORT_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_SHORT_ARRAY, seededRandom());
        // Don't use a "small" array, reduce spurious failures.
        final short[] array1 = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1,
                2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        final short[] array2 = ArrayUtils.clone(array1);
        // no shuffle
        ArrayUtils.shuffle(array1, null);
        assertTrue(Arrays.equals(array1, array2));
        // actual shuffle
        ArrayUtils.shuffle(array1, seededRandom());
        assertFalse(Arrays.equals(array1, array2));
        for (final short element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleString() {
        ArrayUtils.shuffle((String[]) null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_STRING_ARRAY);
        // Don't use a "small" array, reduce spurious failures.
        final String[] array1 = { "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "0", "1", "2",
                "3", "4", "5", "6", "7", "8", "9", "10", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "0", "1", "2", "3", "4", "5", "6", "7", "8",
                "9", "10", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10" };
        final String[] array2 = ArrayUtils.clone(array1);
        ArrayUtils.shuffle(array1);
        assertFalse(Arrays.equals(array1, array2));
        for (final String element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }

    @Test
    void testShuffleStringRandom() {
        ArrayUtils.shuffle((String[]) null, null);
        ArrayUtils.shuffle((String[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_STRING_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_STRING_ARRAY, seededRandom());
        // Don't use a "small" array, reduce spurious failures.
        final String[] array1 = { "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "0", "1", "2",
                "3", "4", "5", "6", "7", "8", "9", "10", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "0", "1", "2", "3", "4", "5", "6", "7", "8",
                "9", "10", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10" };
        final String[] array2 = ArrayUtils.clone(array1);
        // no shuffle
        ArrayUtils.shuffle(array1, null);
        assertTrue(Arrays.equals(array1, array2));
        // actual shuffle
        ArrayUtils.shuffle(array1, seededRandom());
        assertFalse(Arrays.equals(array1, array2));
        for (final String element : array2) {
            assertTrue(ArrayUtils.contains(array1, element), () -> "Element " + element + " not found");
        }
    }
```