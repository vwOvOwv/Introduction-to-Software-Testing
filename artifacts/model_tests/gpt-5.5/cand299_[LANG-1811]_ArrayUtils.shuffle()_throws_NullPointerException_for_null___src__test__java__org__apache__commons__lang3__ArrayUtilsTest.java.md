# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `48d6e758f79255da5a1e307a2bbcfa60726ad8a0`
- B: `623235ebca46bea1a6e8cc02b7d7084c1698ab80`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `350692`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 94774, 'completion_tokens': 1690, 'total_tokens': 96464}`

---

- 新增 `testShuffleNullAndEmptyNoOp`，覆盖生产代码中各 `shuffle(array, random)` 重载对 `null` 数组、`null` 随机源和空数组改为 no-op 的行为，并顺带覆盖无随机源重载的 null/empty no-op。
- 新增 `testShuffleNullRandomDoesNotModify`，对照生产 diff 中 `random == null` 时不进入 Fisher-Yates 循环，断言非空数组内容保持不变。
- 不需要调整 import，现有 `assertArrayEquals`、`seededRandom()` 和 `ArrayUtils` 均已可用。

```java
    @Test
    void testShuffleNullAndEmptyNoOp() {
        ArrayUtils.shuffle((boolean[]) null);
        ArrayUtils.shuffle((byte[]) null);
        ArrayUtils.shuffle((char[]) null);
        ArrayUtils.shuffle((double[]) null);
        ArrayUtils.shuffle((float[]) null);
        ArrayUtils.shuffle((int[]) null);
        ArrayUtils.shuffle((long[]) null);
        ArrayUtils.shuffle((short[]) null);
        ArrayUtils.shuffle((String[]) null);

        ArrayUtils.shuffle(ArrayUtils.EMPTY_BOOLEAN_ARRAY);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_BYTE_ARRAY);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_CHAR_ARRAY);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_DOUBLE_ARRAY);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_FLOAT_ARRAY);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_INT_ARRAY);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_LONG_ARRAY);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_SHORT_ARRAY);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_STRING_ARRAY);

        ArrayUtils.shuffle((boolean[]) null, null);
        ArrayUtils.shuffle((boolean[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_BOOLEAN_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_BOOLEAN_ARRAY, seededRandom());

        ArrayUtils.shuffle((byte[]) null, null);
        ArrayUtils.shuffle((byte[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_BYTE_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_BYTE_ARRAY, seededRandom());

        ArrayUtils.shuffle((char[]) null, null);
        ArrayUtils.shuffle((char[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_CHAR_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_CHAR_ARRAY, seededRandom());

        ArrayUtils.shuffle((double[]) null, null);
        ArrayUtils.shuffle((double[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_DOUBLE_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_DOUBLE_ARRAY, seededRandom());

        ArrayUtils.shuffle((float[]) null, null);
        ArrayUtils.shuffle((float[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_FLOAT_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_FLOAT_ARRAY, seededRandom());

        ArrayUtils.shuffle((int[]) null, null);
        ArrayUtils.shuffle((int[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_INT_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_INT_ARRAY, seededRandom());

        ArrayUtils.shuffle((long[]) null, null);
        ArrayUtils.shuffle((long[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_LONG_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_LONG_ARRAY, seededRandom());

        ArrayUtils.shuffle((short[]) null, null);
        ArrayUtils.shuffle((short[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_SHORT_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_SHORT_ARRAY, seededRandom());

        ArrayUtils.shuffle((String[]) null, null);
        ArrayUtils.shuffle((String[]) null, seededRandom());
        ArrayUtils.shuffle(ArrayUtils.EMPTY_STRING_ARRAY, null);
        ArrayUtils.shuffle(ArrayUtils.EMPTY_STRING_ARRAY, seededRandom());
    }

    @Test
    void testShuffleNullRandomDoesNotModify() {
        final boolean[] booleans = { true, false, true };
        final byte[] bytes = { 1, 2, 3 };
        final char[] chars = { 'a', 'b', 'c' };
        final double[] doubles = { 1, 2, 3 };
        final float[] floats = { 1, 2, 3 };
        final int[] ints = { 1, 2, 3 };
        final long[] longs = { 1, 2, 3 };
        final short[] shorts = { 1, 2, 3 };
        final String[] strings = { "1", "2", "3" };

        ArrayUtils.shuffle(booleans, null);
        ArrayUtils.shuffle(bytes, null);
        ArrayUtils.shuffle(chars, null);
        ArrayUtils.shuffle(doubles, null);
        ArrayUtils.shuffle(floats, null);
        ArrayUtils.shuffle(ints, null);
        ArrayUtils.shuffle(longs, null);
        ArrayUtils.shuffle(shorts, null);
        ArrayUtils.shuffle(strings, null);

        assertArrayEquals(new boolean[] { true, false, true }, booleans);
        assertArrayEquals(new byte[] { 1, 2, 3 }, bytes);
        assertArrayEquals(new char[] { 'a', 'b', 'c' }, chars);
        assertArrayEquals(new double[] { 1, 2, 3 }, doubles);
        assertArrayEquals(new float[] { 1, 2, 3 }, floats);
        assertArrayEquals(new int[] { 1, 2, 3 }, ints);
        assertArrayEquals(new long[] { 1, 2, 3 }, longs);
        assertArrayEquals(new short[] { 1, 2, 3 }, shorts);
        assertArrayEquals(new String[] { "1", "2", "3" }, strings);
    }
```