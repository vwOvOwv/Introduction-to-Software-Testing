# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `63d8a025e6f38ddfc966c4104ac783bcb59031e0`
- B: `a3995141bf1b8a478e86fdbecc95f2b98f892647`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `204726`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 61215, 'completion_tokens': 1813, 'total_tokens': 63028, 'prompt_tokens_details': {'cached_tokens': 54400}, 'completion_tokens_details': {'reasoning_tokens': 1529}, 'prompt_cache_hit_tokens': 54400, 'prompt_cache_miss_tokens': 6815}`

---

- 新增 @Test 方法：testSwapChar、testSwapCharRange、testSwapCharOutOfRange、testSwapCharOutOfRangeLen
- 新增 @Test 方法：testSwapFloat、testSwapFloatRange、testSwapFloatOutOfRange、testSwapFloatOutOfRangeLen
- 新增 @Test 方法：testSwapDouble、testSwapDoubleRange、testSwapDoubleOutOfRange、testSwapDoubleOutOfRangeLen
- 新增 @Test 方法：testSwapInt、testSwapIntRange、testSwapIntOutOfRange、testSwapIntOutOfRangeLen
- 新增 @Test 方法：testSwapLong、testSwapLongRange、testSwapLongOutOfRange、testSwapLongOutOfRangeLen
- 新增 @Test 方法：testSwapObject、testSwapObjectRange、testSwapObjectOutOfRange、testSwapObjectOutOfRangeLen
- 新增 @Test 方法：testShiftDouble、testShiftRangeDouble、testShiftRangeNoElemDouble、testShiftAllDouble
- 新增 @Test 方法：testShiftFloat、testShiftRangeFloat、testShiftRangeNoElemFloat、testShiftAllFloat
- 新增 @Test 方法：testShiftShort、testShiftRangeShort、testShiftRangeNoElemShort、testShiftAllShort
- 新增 @Test 方法：testShiftByte、testShiftRangeByte、testShiftRangeNoElemByte、testShiftAllByte
- 新增 @Test 方法：testShiftChar、testShiftRangeChar、testShiftRangeNoElemChar、testShiftAllChar
- 新增 @Test 方法：testShiftLong、testShiftRangeLong、testShiftRangeNoElemLong、testShiftAllLong
- 新增 @Test 方法：testShiftInt、testShiftRangeInt、testShiftRangeNoElemInt、testShiftAllInt
- 新增 @Test 方法：testShiftObject、testShiftRangeObject、testShiftRangeNoElemObject、testShiftAllObject
- 无需调整 import，旧测试文件现有 import 已覆盖所有新测试所需的类。

```java
// IMPORTS_START
// IMPORTS_END
//-----------------------------------------------------------------------
@Test
public void testSwapChar() {
    char[] array = new char[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
}

@Test
public void testSwapCharRange() {
    char[] array = new char[] {1, 2, 3, 4};
    ArrayUtils.swap(array, 0, 2, 2);
    assertEquals(3, array[0]);
    assertEquals(4, array[1]);
    assertEquals(1, array[2]);
    assertEquals(2, array[3]);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapCharOutOfRange() {
    char[] array = new char[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 3);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapCharOutOfRangeLen() {
    char[] array = new char[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2, 2);
}

@Test
public void testSwapFloat() {
    float[] array = new float[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2);
    assertEquals(3, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(1, array[2], 0);
}

@Test
public void testSwapFloatRange() {
    float[] array = new float[] {1, 2, 3, 4};
    ArrayUtils.swap(array, 0, 2, 2);
    assertEquals(3, array[0], 0);
    assertEquals(4, array[1], 0);
    assertEquals(1, array[2], 0);
    assertEquals(2, array[3], 0);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapFloatOutOfRange() {
    float[] array = new float[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 3);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapFloatOutOfRangeLen() {
    float[] array = new float[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2, 2);
}

@Test
public void testSwapDouble() {
    double[] array = new double[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2);
    assertEquals(3, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(1, array[2], 0);
}

@Test
public void testSwapDoubleRange() {
    double[] array = new double[] {1, 2, 3, 4};
    ArrayUtils.swap(array, 0, 2, 2);
    assertEquals(3, array[0], 0);
    assertEquals(4, array[1], 0);
    assertEquals(1, array[2], 0);
    assertEquals(2, array[3], 0);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapDoubleOutOfRange() {
    double[] array = new double[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 3);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapDoubleOutOfRangeLen() {
    double[] array = new double[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2, 2);
}

@Test
public void testSwapInt() {
    int[] array = new int[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
}

@Test
public void testSwapIntRange() {
    int[] array = new int[] {1, 2, 3, 4};
    ArrayUtils.swap(array, 0, 2, 2);
    assertEquals(3, array[0]);
    assertEquals(4, array[1]);
    assertEquals(1, array[2]);
    assertEquals(2, array[3]);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapIntOutOfRange() {
    int[] array = new int[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 3);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapIntOutOfRangeLen() {
    int[] array = new int[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2, 2);
}

@Test
public void testSwapLong() {
    long[] array = new long[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2);
    assertEquals(3, array[0]);
    assertEquals(2, array[1]);
    assertEquals(1, array[2]);
}

@Test
public void testSwapLongRange() {
    long[] array = new long[] {1, 2, 3, 4};
    ArrayUtils.swap(array, 0, 2, 2);
    assertEquals(3, array[0]);
    assertEquals(4, array[1]);
    assertEquals(1, array[2]);
    assertEquals(2, array[3]);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapLongOutOfRange() {
    long[] array = new long[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 3);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapLongOutOfRangeLen() {
    long[] array = new long[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2, 2);
}

@Test
public void testSwapObject() {
    String[] array = new String[] {"1", "2", "3"};
    ArrayUtils.swap(array, 0, 2);
    assertEquals("3", array[0]);
    assertEquals("2", array[1]);
    assertEquals("1", array[2]);
}

@Test
public void testSwapObjectRange() {
    String[] array = new String[] {"1", "2", "3", "4"};
    ArrayUtils.swap(array, 0, 2, 2);
    assertEquals("3", array[0]);
    assertEquals("4", array[1]);
    assertEquals("1", array[2]);
    assertEquals("2", array[3]);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapObjectOutOfRange() {
    String[] array = new String[] {"1", "2", "3"};
    ArrayUtils.swap(array, 0, 3);
}

@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapObjectOutOfRangeLen() {
    String[] array = new String[] {"1", "2", "3"};
    ArrayUtils.swap(array, 0, 2, 2);
}

//-----------------------------------------------------------------------
@Test
public void testShiftDouble() {
    double[] array = new double[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1);
    assertEquals(4, array[0], 0);
    assertEquals(1, array[1], 0);
    assertEquals(2, array[2], 0);
    assertEquals(3, array[3], 0);
    ArrayUtils.shift(array, -1);
    assertEquals(1, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(3, array[2], 0);
    assertEquals(4, array[3], 0);
    ArrayUtils.shift(array, 5);
    assertEquals(4, array[0], 0);
    assertEquals(1, array[1], 0);
    assertEquals(2, array[2], 0);
    assertEquals(3, array[3], 0);
    ArrayUtils.shift(array, -3);
    assertEquals(3, array[0], 0);
    assertEquals(4, array[1], 0);
    assertEquals(1, array[2], 0);
    assertEquals(2, array[3], 0);
}

@Test
public void testShiftRangeDouble() {
    double[] array = new double[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(array, 1, 3, 1);
    assertEquals(1, array[0], 0);
    assertEquals(3, array[1], 0);
    assertEquals(2, array[2], 0);
    assertEquals(4, array[3], 0);
    assertEquals(5, array[4], 0);
    ArrayUtils.shift(array, 1, 4, 2);
    assertEquals(1, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(4, array[2], 0);
    assertEquals(3, array[3], 0);
    assertEquals(5, array[4], 0);
}

@Test
public void testShiftRangeNoElemDouble() {
    double[] array = new double[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1, 1, 1);
    assertEquals(1, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(3, array[2], 0);
    assertEquals(4, array[3], 0);
}

@Test
public void testShiftAllDouble() {
    double[] array = new double[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 4);
    assertEquals(1, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(3, array[2], 0);
    assertEquals(4, array[3], 0);
    ArrayUtils.shift(array, -4);
    assertEquals(1, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(3, array[2], 0);
    assertEquals(4, array[3], 0);
}

@Test
public void testShiftFloat() {
    float[] array = new float[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1);
    assertEquals(4, array[0], 0);
    assertEquals(1, array[1], 0);
    assertEquals(2, array[2], 0);
    assertEquals(3, array[3], 0);
    ArrayUtils.shift(array, -1);
    assertEquals(1, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(3, array[2], 0);
    assertEquals(4, array[3], 0);
    ArrayUtils.shift(array, 5);
    assertEquals(4, array[0], 0);
    assertEquals(1, array[1], 0);
    assertEquals(2, array[2], 0);
    assertEquals(3, array[3], 0);
    ArrayUtils.shift(array, -3);
    assertEquals(3, array[0], 0);
    assertEquals(4, array[1], 0);
    assertEquals(1, array[2], 0);
    assertEquals(2, array[3], 0);
}

@Test
public void testShiftRangeFloat() {
    float[] array = new float[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(array, 1, 3, 1);
    assertEquals(1, array[0], 0);
    assertEquals(3, array[1], 0);
    assertEquals(2, array[2], 0);
    assertEquals(4, array[3], 0);
    assertEquals(5, array[4], 0);
    ArrayUtils.shift(array, 1, 4, 2);
    assertEquals(1, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(4, array[2], 0);
    assertEquals(3, array[3], 0);
    assertEquals(5, array[4], 0);
}

@Test
public void testShiftRangeNoElemFloat() {
    float[] array = new float[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1, 1, 1);
    assertEquals(1, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(3, array[2], 0);
    assertEquals(4, array[3], 0);
}

@Test
public void testShiftAllFloat() {
    float[] array = new float[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 4);
    assertEquals(1, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(3, array[2], 0);
    assertEquals(4, array[3], 0);
    ArrayUtils.shift(array, -4);
    assertEquals(1, array[0], 0);
    assertEquals(2, array[1], 0);
    assertEquals(3, array[2], 0);
    assertEquals(4, array[3], 0);
}

@Test
public void testShiftShort() {
    short[] array = new short[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1);
    assertEquals(4, array[0]);
    assertEquals(1, array[1]);
    assertEquals(2, array[2]);
    assertEquals(3, array[3]);
    ArrayUtils.shift(array, -1);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
    ArrayUtils.shift(array, 5);
    assertEquals(4, array[0]);
    assertEquals(1, array[1]);
    assertEquals(2, array[2]);
    assertEquals(3, array[3]);
    ArrayUtils.shift(array, -3);
    assertEquals(3, array[0]);
    assertEquals(4, array[1]);
    assertEquals(1, array[2]);
    assertEquals(2, array[3]);
}

@Test
public void testShiftRangeShort() {
    short[] array = new short[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(array, 1, 3, 1);
    assertEquals(1, array[0]);
    assertEquals(3, array[1]);
    assertEquals(2, array[2]);
    assertEquals(4, array[3]);
    assertEquals(5, array[4]);
    ArrayUtils.shift(array, 1, 4, 2);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(4, array[2]);
    assertEquals(3, array[3]);
    assertEquals(5, array[4]);
}

@Test
public void testShiftRangeNoElemShort() {
    short[] array = new short[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1, 1, 1);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
}

@Test
public void testShiftAllShort() {
    short[] array = new short[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 4);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
    ArrayUtils.shift(array, -4);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
}

@Test
public void testShiftByte() {
    byte[] array = new byte[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1);
    assertEquals(4, array[0]);
    assertEquals(1, array[1]);
    assertEquals(2, array[2]);
    assertEquals(3, array[3]);
    ArrayUtils.shift(array, -1);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
    ArrayUtils.shift(array, 5);
    assertEquals(4, array[0]);
    assertEquals(1, array[1]);
    assertEquals(2, array[2]);
    assertEquals(3, array[3]);
    ArrayUtils.shift(array, -3);
    assertEquals(3, array[0]);
    assertEquals(4, array[1]);
    assertEquals(1, array[2]);
    assertEquals(2, array[3]);
}

@Test
public void testShiftRangeByte() {
    byte[] array = new byte[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(array, 1, 3, 1);
    assertEquals(1, array[0]);
    assertEquals(3, array[1]);
    assertEquals(2, array[2]);
    assertEquals(4, array[3]);
    assertEquals(5, array[4]);
    ArrayUtils.shift(array, 1, 4, 2);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(4, array[2]);
    assertEquals(3, array[3]);
    assertEquals(5, array[4]);
}

@Test
public void testShiftRangeNoElemByte() {
    byte[] array = new byte[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1, 1, 1);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
}

@Test
public void testShiftAllByte() {
    byte[] array = new byte[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 4);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
    ArrayUtils.shift(array, -4);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
}

@Test
public void testShiftChar() {
    char[] array = new char[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1);
    assertEquals(4, array[0]);
    assertEquals(1, array[1]);
    assertEquals(2, array[2]);
    assertEquals(3, array[3]);
    ArrayUtils.shift(array, -1);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
    ArrayUtils.shift(array, 5);
    assertEquals(4, array[0]);
    assertEquals(1, array[1]);
    assertEquals(2, array[2]);
    assertEquals(3, array[3]);
    ArrayUtils.shift(array, -3);
    assertEquals(3, array[0]);
    assertEquals(4, array[1]);
    assertEquals(1, array[2]);
    assertEquals(2, array[3]);
}

@Test
public void testShiftRangeChar() {
    char[] array = new char[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(array, 1, 3, 1);
    assertEquals(1, array[0]);
    assertEquals(3, array[1]);
    assertEquals(2, array[2]);
    assertEquals(4, array[3]);
    assertEquals(5, array[4]);
    ArrayUtils.shift(array, 1, 4, 2);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(4, array[2]);
    assertEquals(3, array[3]);
    assertEquals(5, array[4]);
}

@Test
public void testShiftRangeNoElemChar() {
    char[] array = new char[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1, 1, 1);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
}

@Test
public void testShiftAllChar() {
    char[] array = new char[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 4);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
    ArrayUtils.shift(array, -4);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
}

@Test
public void testShiftLong() {
    long[] array = new long[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1);
    assertEquals(4, array[0]);
    assertEquals(1, array[1]);
    assertEquals(2, array[2]);
    assertEquals(3, array[3]);
    ArrayUtils.shift(array, -1);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
    ArrayUtils.shift(array, 5);
    assertEquals(4, array[0]);
    assertEquals(1, array[1]);
    assertEquals(2, array[2]);
    assertEquals(3, array[3]);
    ArrayUtils.shift(array, -3);
    assertEquals(3, array[0]);
    assertEquals(4, array[1]);
    assertEquals(1, array[2]);
    assertEquals(2, array[3]);
}

@Test
public void testShiftRangeLong() {
    long[] array = new long[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(array, 1, 3, 1);
    assertEquals(1, array[0]);
    assertEquals(3, array[1]);
    assertEquals(2, array[2]);
    assertEquals(4, array[3]);
    assertEquals(5, array[4]);
    ArrayUtils.shift(array, 1, 4, 2);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(4, array[2]);
    assertEquals(3, array[3]);
    assertEquals(5, array[4]);
}

@Test
public void testShiftRangeNoElemLong() {
    long[] array = new long[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1, 1, 1);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
}

@Test
public void testShiftAllLong() {
    long[] array = new long[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 4);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
    ArrayUtils.shift(array, -4);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
}

@Test
public void testShiftInt() {
    int[] array = new int[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1);
    assertEquals(4, array[0]);
    assertEquals(1, array[1]);
    assertEquals(2, array[2]);
    assertEquals(3, array[3]);
    ArrayUtils.shift(array, -1);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
    ArrayUtils.shift(array, 5);
    assertEquals(4, array[0]);
    assertEquals(1, array[1]);
    assertEquals(2, array[2]);
    assertEquals(3, array[3]);
    ArrayUtils.shift(array, -3);
    assertEquals(3, array[0]);
    assertEquals(4, array[1]);
    assertEquals(1, array[2]);
    assertEquals(2, array[3]);
}

@Test
public void testShiftRangeInt() {
    int[] array = new int[] {1, 2, 3, 4, 5};
    ArrayUtils.shift(array, 1, 3, 1);
    assertEquals(1, array[0]);
    assertEquals(3, array[1]);
    assertEquals(2, array[2]);
    assertEquals(4, array[3]);
    assertEquals(5, array[4]);
    ArrayUtils.shift(array, 1, 4, 2);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(4, array[2]);
    assertEquals(3, array[3]);
    assertEquals(5, array[4]);
}

@Test
public void testShiftRangeNoElemInt() {
    int[] array = new int[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 1, 1, 1);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
}

@Test
public void testShiftAllInt() {
    int[] array = new int[] {1, 2, 3, 4};
    ArrayUtils.shift(array, 4);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
    ArrayUtils.shift(array, -4);
    assertEquals(1, array[0]);
    assertEquals(2, array[1]);
    assertEquals(3, array[2]);
    assertEquals(4, array[3]);
}

@Test
public void testShiftObject() {
    String[] array = new String[] {"1", "2", "3", "4"};
    ArrayUtils.shift(array, 1);
    assertEquals("4", array[0]);
    assertEquals("1", array[1]);
    assertEquals("2", array[2]);
    assertEquals("3", array[3]);
    ArrayUtils.shift(array, -1);
    assertEquals("1", array[0]);
    assertEquals("2", array[1]);
    assertEquals("3", array[2]);
    assertEquals("4", array[3]);
    ArrayUtils.shift(array, 5);
    assertEquals("4", array[0]);
    assertEquals("1", array[1]);
    assertEquals("2", array[2]);
    assertEquals("3", array[3]);
    ArrayUtils.shift(array, -3);
    assertEquals("3", array[0]);
    assertEquals("4", array[1]);
    assertEquals("1", array[2]);
    assertEquals("2", array[3]);
}

@Test
public void testShiftRangeObject() {
    String[] array = new String[] {"1", "2", "3", "4", "5"};
    ArrayUtils.shift(array, 1, 3, 1);
    assertEquals("1", array[0]);
    assertEquals("3", array[1]);
    assertEquals("2", array[2]);
    assertEquals("4", array[3]);
    assertEquals("5", array[4]);
    ArrayUtils.shift(array, 1, 4, 2);
    assertEquals```java
    assertEquals("5", array[4]);
    ArrayUtils.shift(array, 1, 4, 2);
    assertEquals("1", array[0]);
    assertEquals("2", array[1]);
    assertEquals("4", array[2]);
    assertEquals("3", array[3]);
    assertEquals("5", array[4]);
}

@Test
public void testShiftRangeNoElemObject() {
    String[] array = new String[] {"1", "2", "3", "4"};
    ArrayUtils.shift(array, 1, 1, 1);
    assertEquals("1", array[0]);
    assertEquals("2", array[1]);
    assertEquals("3", array[2]);
    assertEquals("4", array[3]);
}

@Test
public void testShiftAllObject() {
    String[] array = new String[] {"1", "2", "3", "4"};
    ArrayUtils.shift(array, 4);
    assertEquals("1", array[0]);
    assertEquals("2", array[1]);
    assertEquals("3", array[2]);
    assertEquals("4", array[3]);
    ArrayUtils.shift(array, -4);
    assertEquals("1", array[0]);
    assertEquals("2", array[1]);
    assertEquals("3", array[2]);
    assertEquals("4", array[3]);
}
```