# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `f431270c59b6d4558da8dff625a7738591a0d541`
- B: `5b7608d1549989d92dd159392c19d9ba8ce0e62e`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `methods`
- user_chars: `46536`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 15483, 'completion_tokens': 1919, 'total_tokens': 17402}`

---

- 修改 `testSwapCharOutOfRange`：生产代码对越界索引不再抛出 `ArrayIndexOutOfBoundsException`，测试改为断言数组保持不变。
- 修改 `testSwapCharOutOfRangeLen`：生产代码对越界长度会尽可能交换到数组末尾，测试改为断言实际交换后的数组内容。
- 修改 `testSwapDoubleOutOfRange`：生产代码对越界索引不再抛异常，测试改为断言数组保持不变。
- 修改 `testSwapDoubleOutOfRangeLen`：生产代码对越界长度会截断交换范围，测试改为断言实际交换结果。
- 修改 `testSwapFloatOutOfRange`：生产代码对越界索引不再抛异常，测试改为断言数组保持不变。
- 修改 `testSwapFloatOutOfRangeLen`：生产代码对越界长度会截断交换范围，测试改为断言实际交换结果。
- 修改 `testSwapIntOutOfRange`：生产代码对越界索引不再抛异常，测试改为断言数组保持不变。
- 修改 `testSwapIntOutOfRangeLen`：生产代码对越界长度会截断交换范围，测试改为断言实际交换结果。
- 修改 `testSwapLongOutOfRange`：生产代码对越界索引不再抛异常，测试改为断言数组保持不变。
- 修改 `testSwapLongOutOfRangeLen`：生产代码对越界长度会截断交换范围，测试改为断言实际交换结果。
- 修改 `testSwapObjectOutOfRange`：生产代码对越界索引不再抛异常，测试改为断言数组保持不变。
- 修改 `testSwapObjectOutOfRangeLen`：生产代码对越界长度会截断交换范围，测试改为断言实际交换结果。
- 不需要调整 import。

```java
    @Test
    public void testSwapCharOutOfRange() {
        char[] array = new char[] {1, 2, 3};
        ArrayUtils.swap(array, 0, 3);
        assertEquals(1, array[0]);
        assertEquals(2, array[1]);
        assertEquals(3, array[2]);
    }

    @Test
    public void testSwapCharOutOfRangeLen() {
        char[] array = new char[] {1, 2, 3};
        ArrayUtils.swap(array, 0, 2, 2);
        assertEquals(3, array[0]);
        assertEquals(2, array[1]);
        assertEquals(1, array[2]);
    }

    @Test
    public void testSwapDoubleOutOfRange() {
        double[] array = new double[] {1, 2, 3};
        ArrayUtils.swap(array, 0, 3);
        assertEquals(1, array[0], 0);
        assertEquals(2, array[1], 0);
        assertEquals(3, array[2], 0);
    }

    @Test
    public void testSwapDoubleOutOfRangeLen() {
        double[] array = new double[] {1, 2, 3};
        ArrayUtils.swap(array, 0, 2, 2);
        assertEquals(3, array[0], 0);
        assertEquals(2, array[1], 0);
        assertEquals(1, array[2], 0);
    }

    @Test
    public void testSwapFloatOutOfRange() {
        float[] array = new float[] {1, 2, 3};
        ArrayUtils.swap(array, 0, 3);
        assertEquals(1, array[0], 0);
        assertEquals(2, array[1], 0);
        assertEquals(3, array[2], 0);
    }

    @Test
    public void testSwapFloatOutOfRangeLen() {
        float[] array = new float[] {1, 2, 3};
        ArrayUtils.swap(array, 0, 2, 2);
        assertEquals(3, array[0], 0);
        assertEquals(2, array[1], 0);
        assertEquals(1, array[2], 0);
    }

    @Test
    public void testSwapIntOutOfRange() {
        int[] array = new int[] {1, 2, 3};
        ArrayUtils.swap(array, 0, 3);
        assertEquals(1, array[0]);
        assertEquals(2, array[1]);
        assertEquals(3, array[2]);
    }

    @Test
    public void testSwapIntOutOfRangeLen() {
        int[] array = new int[] {1, 2, 3};
        ArrayUtils.swap(array, 0, 2, 2);
        assertEquals(3, array[0]);
        assertEquals(2, array[1]);
        assertEquals(1, array[2]);
    }

    @Test
    public void testSwapLongOutOfRange() {
        long[] array = new long[] {1, 2, 3};
        ArrayUtils.swap(array, 0, 3);
        assertEquals(1, array[0]);
        assertEquals(2, array[1]);
        assertEquals(3, array[2]);
    }

    @Test
    public void testSwapLongOutOfRangeLen() {
        long[] array = new long[] {1, 2, 3};
        ArrayUtils.swap(array, 0, 2, 2);
        assertEquals(3, array[0]);
        assertEquals(2, array[1]);
        assertEquals(1, array[2]);
    }

    @Test
    public void testSwapObjectOutOfRange() {
        String[] array = new String[] {"1", "2", "3"};
        ArrayUtils.swap(array, 0, 3);
        assertEquals("1", array[0]);
        assertEquals("2", array[1]);
        assertEquals("3", array[2]);
    }

    @Test
    public void testSwapObjectOutOfRangeLen() {
        String[] array = new String[] {"1", "2", "3"};
        ArrayUtils.swap(array, 0, 2, 2);
        assertEquals("3", array[0]);
        assertEquals("2", array[1]);
        assertEquals("1", array[2]);
    }
```