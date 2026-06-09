# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9ceaaeb6566c78b25da0ae8181964b13f09204a8`
- B: `82cc24437f43d07880d8883229477735431e5d02`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `198418`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 51258, 'completion_tokens': 2652, 'total_tokens': 53910}`

---

- 新增 `testShuffle`，对应生产代码新增 `shuffle(Object[], Random)`，使用固定 `Random` 断言 Fisher-Yates 置换结果，避免无参随机导致测试不稳定；需要新增 `java.util.Random` import。
- 新增 `testShuffleBoolean`，对应生产代码新增 `shuffle(boolean[], Random)`，断言布尔数组按固定随机源完成置换；需要调整 import。
- 新增 `testShuffleByte`，对应生产代码新增 `shuffle(byte[], Random)`，断言 byte 数组按固定随机源完成置换；需要调整 import。
- 新增 `testShuffleChar`，对应生产代码新增 `shuffle(char[], Random)`，断言 char 数组按固定随机源完成置换；需要调整 import。
- 新增 `testShuffleShort`，对应生产代码新增 `shuffle(short[], Random)`，断言 short 数组按固定随机源完成置换；需要调整 import。
- 新增 `testShuffleInt`，对应生产代码新增 `shuffle(int[], Random)`，断言 int 数组按固定随机源完成置换；需要调整 import。
- 新增 `testShuffleLong`，对应生产代码新增 `shuffle(long[], Random)`，断言 long 数组按固定随机源完成置换；需要调整 import。
- 新增 `testShuffleFloat`，对应生产代码新增 `shuffle(float[], Random)`，断言 float 数组按固定随机源完成置换；需要调整 import。
- 新增 `testShuffleDouble`，对应生产代码新增 `shuffle(double[], Random)`，断言 double 数组按固定随机源完成置换；需要调整 import。

```java
// IMPORTS_START
import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNotSame;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertSame;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Date;
import java.util.Map;
import java.util.Random;

import org.junit.Assert;
import org.junit.Test;
// IMPORTS_END

    @Test
    public void testShuffle() {
        final String[] array = new String[] {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10"};

        ArrayUtils.shuffle(array, new Random() {
            @Override
            public int nextInt(final int bound) {
                return 0;
            }
        });

        Assert.assertArrayEquals(new String[] {"2", "3", "4", "5", "6", "7", "8", "9", "10", "1"}, array);
    }

    @Test
    public void testShuffleBoolean() {
        final boolean[] array = new boolean[] {true, false, true, true, false, false, true, false, false, true};

        ArrayUtils.shuffle(array, new Random() {
            @Override
            public int nextInt(final int bound) {
                return 0;
            }
        });

        Assert.assertArrayEquals(new boolean[] {false, true, true, false, false, true, false, false, true, true}, array);
    }

    @Test
    public void testShuffleByte() {
        final byte[] array = new byte[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

        ArrayUtils.shuffle(array, new Random() {
            @Override
            public int nextInt(final int bound) {
                return 0;
            }
        });

        Assert.assertArrayEquals(new byte[] {2, 3, 4, 5, 6, 7, 8, 9, 10, 1}, array);
    }

    @Test
    public void testShuffleChar() {
        final char[] array = new char[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

        ArrayUtils.shuffle(array, new Random() {
            @Override
            public int nextInt(final int bound) {
                return 0;
            }
        });

        Assert.assertArrayEquals(new char[] {2, 3, 4, 5, 6, 7, 8, 9, 10, 1}, array);
    }

    @Test
    public void testShuffleShort() {
        final short[] array = new short[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

        ArrayUtils.shuffle(array, new Random() {
            @Override
            public int nextInt(final int bound) {
                return 0;
            }
        });

        Assert.assertArrayEquals(new short[] {2, 3, 4, 5, 6, 7, 8, 9, 10, 1}, array);
    }

    @Test
    public void testShuffleInt() {
        final int[] array = new int[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

        ArrayUtils.shuffle(array, new Random() {
            @Override
            public int nextInt(final int bound) {
                return 0;
            }
        });

        Assert.assertArrayEquals(new int[] {2, 3, 4, 5, 6, 7, 8, 9, 10, 1}, array);
    }

    @Test
    public void testShuffleLong() {
        final long[] array = new long[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

        ArrayUtils.shuffle(array, new Random() {
            @Override
            public int nextInt(final int bound) {
                return 0;
            }
        });

        Assert.assertArrayEquals(new long[] {2, 3, 4, 5, 6, 7, 8, 9, 10, 1}, array);
    }

    @Test
    public void testShuffleFloat() {
        final float[] array = new float[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

        ArrayUtils.shuffle(array, new Random() {
            @Override
            public int nextInt(final int bound) {
                return 0;
            }
        });

        Assert.assertArrayEquals(new float[] {2, 3, 4, 5, 6, 7, 8, 9, 10, 1}, array, 0.0f);
    }

    @Test
    public void testShuffleDouble() {
        final double[] array = new double[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

        ArrayUtils.shuffle(array, new Random() {
            @Override
            public int nextInt(final int bound) {
                return 0;
            }
        });

        Assert.assertArrayEquals(new double[] {2, 3, 4, 5, 6, 7, 8, 9, 10, 1}, array, 0.0d);
    }
```