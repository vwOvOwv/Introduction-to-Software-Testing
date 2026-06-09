# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `87538ebd4de1d3f81aa8cec8af0ace1da1b23f60`
- B: `26ead6134ad55bf1350e41f05f4d0cbe6d0be4be`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `341968`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 98470, 'completion_tokens': 4666, 'total_tokens': 103136, 'prompt_tokens_details': {'cached_tokens': 92416}, 'completion_tokens_details': {'reasoning_tokens': 3187}, 'prompt_cache_hit_tokens': 92416, 'prompt_cache_miss_tokens': 6054}`

---

- 将在以下测试方法中新增一行断言，以覆盖传入边界值 `start=Integer.MAX_VALUE, end=Integer.MIN_VALUE` 时的逻辑：
    - `testSubarrayBoolean` 新增 `assertSame` 调用。
    - `testSubarrayByte` 新增 `assertSame` 调用。
    - `testSubarrayChar` 新增 `assertSame` 调用。
    - `testSubarrayDouble` 新增 `assertSame` 调用。
    - `testSubarrayFloat` 新增 `assertSame` 调用。
    - `testSubarrayInt` 新增 `assertSame` 调用。
    - `testSubarrayLong` 新增 `assertSame` 调用。
    - `testSubarrayObject` 新增 `assertEquals` 调用。
    - `testSubarrayShort` 新增 `assertSame` 调用。
- 无需新增或修改 import 语句。

```java
@Test
void testSubarrayBoolean() {
    final boolean[] nullArray = null;
    final boolean[] array = {true, true, false, true, false, true};
    final boolean[] leftSubarray = {true, true, false, true};
    final boolean[] midSubarray = {true, false, true, false};
    final boolean[] rightSubarray = {false, true, false, true};

    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, 0, 4)), "0 start, mid end");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, 0, array.length)), "0 start, length end");
    assertTrue(ArrayUtils.isEquals(midSubarray, ArrayUtils.subarray(array, 1, 5)), "mid start, mid end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, array.length)),
            "mid start, length end");

    assertNull(ArrayUtils.subarray(nullArray, 0, 3), "null input");
    assertEquals(ArrayUtils.EMPTY_BOOLEAN_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_BOOLEAN_ARRAY, 1, 2),
            "empty array");
    assertEquals(ArrayUtils.EMPTY_BOOLEAN_ARRAY, ArrayUtils.subarray(array, 4, 2), "start > end");
    assertEquals(ArrayUtils.EMPTY_BOOLEAN_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end");
    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, -2, 4)),
            "start undershoot, normal end");
    assertEquals(ArrayUtils.EMPTY_BOOLEAN_ARRAY, ArrayUtils.subarray(array, 33, 4), "start overshoot, any end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, 33)),
            "normal start, end overshoot");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, -2, 12)), "start undershoot, end overshoot");

    // empty-return tests

    assertSame(ArrayUtils.EMPTY_BOOLEAN_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_BOOLEAN_ARRAY, 1, 2),
            "empty array, object test");
    assertSame(ArrayUtils.EMPTY_BOOLEAN_ARRAY, ArrayUtils.subarray(array, 4, 1), "start > end, object test");
    assertSame(ArrayUtils.EMPTY_BOOLEAN_ARRAY, ArrayUtils.subarray(array, 2147483647, -2147483648), "start > end, object test");
    assertSame(ArrayUtils.EMPTY_BOOLEAN_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end, object test");
    assertSame(ArrayUtils.EMPTY_BOOLEAN_ARRAY, ArrayUtils.subarray(array, 8733, 4),
            "start overshoot, any end, object test");

    // array type tests

    assertSame(boolean.class, ArrayUtils.subarray(array, 2, 4).getClass().getComponentType(), "boolean type");
}

@Test
void testSubarrayByte() {
    final byte[] nullArray = null;
    final byte[] array = { 10, 11, 12, 13, 14, 15 };
    final byte[] leftSubarray = { 10, 11, 12, 13 };
    final byte[] midSubarray = { 11, 12, 13, 14 };
    final byte[] rightSubarray = { 12, 13, 14, 15 };
    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, 0, 4)), "0 start, mid end");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, 0, array.length)), "0 start, length end");
    assertTrue(ArrayUtils.isEquals(midSubarray, ArrayUtils.subarray(array, 1, 5)), "mid start, mid end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, array.length)), "mid start, length end");
    assertNull(ArrayUtils.subarray(nullArray, 0, 3), "null input");
    assertEquals(ArrayUtils.EMPTY_BYTE_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_BYTE_ARRAY, 1, 2), "empty array");
    assertEquals(ArrayUtils.EMPTY_BYTE_ARRAY, ArrayUtils.subarray(array, 4, 2), "start > end");
    assertEquals(ArrayUtils.EMPTY_BYTE_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end");
    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, -2, 4)), "start undershoot, normal end");
    assertEquals(ArrayUtils.EMPTY_BYTE_ARRAY, ArrayUtils.subarray(array, 33, 4), "start overshoot, any end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, 33)), "normal start, end overshoot");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, -2, 12)), "start undershoot, end overshoot");
    // empty-return tests
    assertSame(ArrayUtils.EMPTY_BYTE_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_BYTE_ARRAY, 1, 2), "empty array, object test");
    assertSame(ArrayUtils.EMPTY_BYTE_ARRAY, ArrayUtils.subarray(array, 4, 1), "start > end, object test");
    assertSame(ArrayUtils.EMPTY_BYTE_ARRAY, ArrayUtils.subarray(array, 2147483647, -2147483648), "start > end, possible overflow");
    assertSame(ArrayUtils.EMPTY_BYTE_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end, object test");
    assertSame(ArrayUtils.EMPTY_BYTE_ARRAY, ArrayUtils.subarray(array, 8733, 4), "start overshoot, any end, object test");
    // array type tests
    assertSame(byte.class, ArrayUtils.subarray(array, 2, 4).getClass().getComponentType(), "byte type");
}

@Test
void testSubarrayChar() {
    final char[] nullArray = null;
    final char[] array = { 'a', 'b', 'c', 'd', 'e', 'f' };
    final char[] leftSubarray = { 'a', 'b', 'c', 'd' };
    final char[] midSubarray = { 'b', 'c', 'd', 'e' };
    final char[] rightSubarray = { 'c', 'd', 'e', 'f' };

    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, 0, 4)), "0 start, mid end");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, 0, array.length)), "0 start, length end");
    assertTrue(ArrayUtils.isEquals(midSubarray, ArrayUtils.subarray(array, 1, 5)), "mid start, mid end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, array.length)), "mid start, length end");

    assertNull(ArrayUtils.subarray(nullArray, 0, 3), "null input");
    assertEquals(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_CHAR_ARRAY, 1, 2), "empty array");
    assertEquals(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 4, 2), "start > end");
    assertEquals(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end");
    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, -2, 4)), "start undershoot, normal end");
    assertEquals(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 33, 4), "start overshoot, any end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, 33)), "normal start, end overshoot");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, -2, 12)), "start undershoot, end overshoot");

    // empty-return tests

    assertSame(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_CHAR_ARRAY, 1, 2), "empty array, object test");
    assertSame(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 4, 1), "start > end, object test");
    assertSame(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 2147483647, -2147483648), "start > end, possible overflow");
    assertSame(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end, object test");
    assertSame(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 8733, 4), "start overshoot, any end, object test");

    // array type tests

    assertSame(char.class, ArrayUtils.subarray(array, 2, 4).getClass().getComponentType(), "char type");
}

@Test
void testSubarrayDouble() {
    final double[] nullArray = null;
    final double[] array = { 10.123, 11.234, 12.345, 13.456, 14.567, 15.678 };
    final double[] leftSubarray = { 10.123, 11.234, 12.345, 13.456 };
    final double[] midSubarray = { 11.234, 12.345, 13.456, 14.567 };
    final double[] rightSubarray = { 12.345, 13.456, 14.567, 15.678 };
    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, 0, 4)), "0 start, mid end");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, 0, array.length)), "0 start, length end");
    assertTrue(ArrayUtils.isEquals(midSubarray, ArrayUtils.subarray(array, 1, 5)), "mid start, mid end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, array.length)), "mid start, length end");
    assertNull(ArrayUtils.subarray(nullArray, 0, 3), "null input");
    assertEquals(ArrayUtils.EMPTY_DOUBLE_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_DOUBLE_ARRAY, 1, 2), "empty array");
    assertEquals(ArrayUtils.EMPTY_DOUBLE_ARRAY, ArrayUtils.subarray(array, 4, 2), "start > end");
    assertEquals(ArrayUtils.EMPTY_DOUBLE_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end");
    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, -2, 4)), "start undershoot, normal end");
    assertEquals(ArrayUtils.EMPTY_DOUBLE_ARRAY, ArrayUtils.subarray(array, 33, 4), "start overshoot, any end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, 33)), "normal start, end overshoot");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, -2, 12)), "start undershoot, end overshoot");
    // empty-return tests
    assertSame(ArrayUtils.EMPTY_DOUBLE_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_DOUBLE_ARRAY, 1, 2), "empty array, object test");
    assertSame(ArrayUtils.EMPTY_DOUBLE_ARRAY, ArrayUtils.subarray(array, 4, 1), "start > end, object test");
    assertSame(ArrayUtils.EMPTY_DOUBLE_ARRAY, ArrayUtils.subarray(array, 2147483647, -2147483648), "start > end, possible overflow");
    assertSame(ArrayUtils.EMPTY_DOUBLE_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end, object test");
    assertSame(ArrayUtils.EMPTY_DOUBLE_ARRAY, ArrayUtils.subarray(array, 8733, 4), "start overshoot, any end, object test");
    // array type tests
    assertSame(double.class, ArrayUtils.subarray(array, 2, 4).getClass().getComponentType(), "double type");
}

@Test
void testSubarrayFloat() {
    final float[] nullArray = null;
    final float[] array = { 10, 11, 12, 13, 14, 15 };
    final float[] leftSubarray = { 10, 11, 12, 13 };
    final float[] midSubarray = { 11, 12, 13, 14 };
    final float[] rightSubarray = { 12, 13, 14, 15 };
    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, 0, 4)), "0 start, mid end");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, 0, array.length)), "0 start, length end");
    assertTrue(ArrayUtils.isEquals(midSubarray, ArrayUtils.subarray(array, 1, 5)), "mid start, mid end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, array.length)), "mid start, length end");
    assertNull(ArrayUtils.subarray(nullArray, 0, 3), "null input");
    assertEquals(ArrayUtils.EMPTY_FLOAT_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_FLOAT_ARRAY, 1, 2), "empty array");
    assertEquals(ArrayUtils.EMPTY_FLOAT_ARRAY, ArrayUtils.subarray(array, 4, 2), "start > end");
    assertEquals(ArrayUtils.EMPTY_FLOAT_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end");
    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, -2, 4)), "start undershoot, normal end");
    assertEquals(ArrayUtils.EMPTY_FLOAT_ARRAY, ArrayUtils.subarray(array, 33, 4), "start overshoot, any end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, 33)), "normal start, end overshoot");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, -2, 12)), "start undershoot, end overshoot");
    // empty-return tests
    assertSame(ArrayUtils.EMPTY_FLOAT_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_FLOAT_ARRAY, 1, 2), "empty array, object test");
    assertSame(ArrayUtils.EMPTY_FLOAT_ARRAY, ArrayUtils.subarray(array, 4, 1), "start > end, object test");
    assertSame(ArrayUtils.EMPTY_FLOAT_ARRAY, ArrayUtils.subarray(array, 2147483647, -2147483648), "start > end, possible overflow");
    assertSame(ArrayUtils.EMPTY_FLOAT_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end, object test");
    assertSame(ArrayUtils.EMPTY_FLOAT_ARRAY, ArrayUtils.subarray(array, 8733, 4), "start overshoot, any end, object test");
    // array type tests
    assertSame(float.class, ArrayUtils.subarray(array, 2, 4).getClass().getComponentType(), "float type");
}

@Test
void testSubarrayInt() {
    final int[] nullArray = null;
    final int[] array = { 10, 11, 12, 13, 14, 15 };
    final int[] leftSubarray = { 10, 11, 12, 13 };
    final int[] midSubarray = { 11, 12, 13, 14 };
    final int[] rightSubarray = { 12, 13, 14, 15 };
    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, 0, 4)), "0 start, mid end");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, 0, array.length)), "0 start, length end");
    assertTrue(ArrayUtils.isEquals(midSubarray, ArrayUtils.subarray(array, 1, 5)), "mid start, mid end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, array.length)), "mid start, length end");
    assertNull(ArrayUtils.subarray(nullArray, 0, 3), "null input");
    assertEquals(ArrayUtils.EMPTY_INT_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_INT_ARRAY, 1, 2), "empty array");
    assertEquals(ArrayUtils.EMPTY_INT_ARRAY, ArrayUtils.subarray(array, 4, 2), "start > end");
    assertEquals(ArrayUtils.EMPTY_INT_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end");
    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, -2, 4)), "start undershoot, normal end");
    assertEquals(ArrayUtils.EMPTY_INT_ARRAY, ArrayUtils.subarray(array, 33, 4), "start overshoot, any end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, 33)), "normal start, end overshoot");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, -2, 12)), "start undershoot, end overshoot");
    // empty-return tests
    assertSame(ArrayUtils.EMPTY_INT_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_INT_ARRAY, 1, 2), "empty array, object test");
    assertSame(ArrayUtils.EMPTY_INT_ARRAY, ArrayUtils.subarray(array, 4, 1), "start > end, object test");
    assertSame(ArrayUtils.EMPTY_INT_ARRAY, ArrayUtils.subarray(array, 2147483647, -2147483648), "start > end, possible overflow");
    assertSame(ArrayUtils.EMPTY_INT_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end, object test");
    assertSame(ArrayUtils.EMPTY_INT_ARRAY, ArrayUtils.subarray(array, 8733, 4), "start overshoot, any end, object test");
    // array type tests
    assertSame(int.class, ArrayUtils.subarray(array, 2, 4).getClass().getComponentType(), "int type");
}

@Test
void testSubarrayLong() {
    final long[] nullArray = null;
    final long[] array = { 999910, 999911, 999912, 999913, 999914, 999915 };
    final long[] leftSubarray = { 999910, 999911, 999912, 999913 };
    final long[] midSubarray = { 999911, 999912, 999913, 999914 };
    final long[] rightSubarray = { 999912, 999913, 999914, 999915 };

    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, 0, 4)), "0 start, mid end");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, 0, array.length)), "0 start, length end");
    assertTrue(ArrayUtils.isEquals(midSubarray, ArrayUtils.subarray(array, 1, 5)), "mid start, mid end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, array.length)),
            "mid start, length end");

    assertNull(ArrayUtils.subarray(nullArray, 0, 3), "null input");
    assertEquals(ArrayUtils.EMPTY_LONG_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_LONG_ARRAY, 1, 2),
            "empty array");
    assertEquals(ArrayUtils.EMPTY_LONG_ARRAY, ArrayUtils.subarray(array, 4, 2), "start > end");
    assertEquals(ArrayUtils.EMPTY_LONG_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end");
    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, -2, 4)),
            "start undershoot, normal end");
    assertEquals(ArrayUtils.EMPTY_LONG_ARRAY, ArrayUtils.subarray(array, 33, 4), "start overshoot, any end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, 33)),
            "normal start, end overshoot");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, -2, 12)), "start undershoot, end overshoot");

    // empty-return tests

    assertSame(ArrayUtils.EMPTY_LONG_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_LONG_ARRAY, 1, 2),
            "empty array, object test");
    assertSame(ArrayUtils.EMPTY_LONG_ARRAY, ArrayUtils.subarray(array, 4, 1), "start > end, object test");
    assertSame(ArrayUtils.EMPTY_LONG_ARRAY, ArrayUtils.subarray(array, 2147483647, -2147483648), "start > end, possible overflow");
    assertSame(ArrayUtils.EMPTY_LONG_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end, object test");
    assertSame(ArrayUtils.EMPTY_LONG_ARRAY, ArrayUtils.subarray(array, 8733, 4),
            "start overshoot, any end, object test");

    // array type tests

    assertSame(long.class, ArrayUtils.subarray(array, 2, 4).getClass().getComponentType(), "long type");
}

@Test
void testSubarrayObject() {
    final Object[] nullArray = null;
    final Object[] objectArray = { "a", "b", "c", "d", "e", "f" };

    assertEquals("abcd", StringUtils.join(ArrayUtils.subarray(objectArray, 0, 4)), "0 start, mid end");
    assertEquals("abcdef", StringUtils.join(ArrayUtils.subarray(objectArray, 0, objectArray.length)),
            "0 start, length end");
    assertEquals("bcd", StringUtils.join(ArrayUtils.subarray(objectArray, 1, 4)), "mid start, mid end");
    assertEquals("bcdef", StringUtils.join(ArrayUtils.subarray(objectArray, 1, objectArray.length)),
            "mid start, length end");

    assertNull(ArrayUtils.subarray(nullArray, 0, 3), "null input");
    assertEquals("", StringUtils.join(ArrayUtils.subarray(ArrayUtils.EMPTY_OBJECT_ARRAY, 1, 2)), "empty array");
    assertEquals("", StringUtils.join(ArrayUtils.subarray(objectArray, 4, 2)), "start > end");
    assertEquals("", StringUtils.join(ArrayUtils.subarray(objectArray, 2147483647, -2147483648)), "start > end");
    assertEquals("", StringUtils.join(ArrayUtils.subarray(objectArray, 3, 3)), "start == end");
    assertEquals("abcd", StringUtils.join(ArrayUtils.subarray(objectArray, -2, 4)), "start undershoot, normal end");
    assertEquals("", StringUtils.join(ArrayUtils.subarray(objectArray, 33, 4)), "start overshoot, any end");
    assertEquals("cdef", StringUtils.join(ArrayUtils.subarray(objectArray, 2, 33)), "normal start, end overshoot");
    assertEquals("abcdef", StringUtils.join(ArrayUtils.subarray(objectArray, -2, 12)),
            "start undershoot, end overshoot");

    // array type tests
    final Date[] dateArray = { new java.sql.Date(new Date().getTime()),
            new Date(), new Date(), new Date(), new Date() };

    assertSame(Object.class, ArrayUtils.subarray(objectArray, 2, 4).getClass().getComponentType(), "Object type");
    assertSame(Date.class, ArrayUtils.subarray(dateArray, 1, 4).getClass().getComponentType(),
            "java.util.Date type");
    assertNotSame(java.sql.Date.class, ArrayUtils.subarray(dateArray, 1, 4).getClass().getComponentType(),
            "java.sql.Date type");
    assertThrows(ClassCastException.class,
            () -> java.sql.Date[].class.cast(ArrayUtils.subarray(dateArray, 1, 3)),
            "Invalid downcast");
}

@Test
void testSubarrayShort() {
    final short[] nullArray = null;
    final short[] array = { 10, 11, 12, 13, 14, 15 };
    final short[] leftSubarray = { 10, 11, 12, ```java
// 注意：前文输出的 testSubarrayChar 方法应替换为下面的 testSubarrChar 方法，以匹配原有测试方法名
@Test
void testSubarrChar() {
    final char[] nullArray = null;
    final char[] array = { 'a', 'b', 'c', 'd', 'e', 'f' };
    final char[] leftSubarray = { 'a', 'b', 'c', 'd' };
    final char[] midSubarray = { 'b', 'c', 'd', 'e' };
    final char[] rightSubarray = { 'c', 'd', 'e', 'f' };

    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, 0, 4)), "0 start, mid end");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, 0, array.length)), "0 start, length end");
    assertTrue(ArrayUtils.isEquals(midSubarray, ArrayUtils.subarray(array, 1, 5)), "mid start, mid end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, array.length)), "mid start, length end");

    assertNull(ArrayUtils.subarray(nullArray, 0, 3), "null input");
    assertEquals(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_CHAR_ARRAY, 1, 2), "empty array");
    assertEquals(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 4, 2), "start > end");
    assertEquals(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end");
    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, -2, 4)), "start undershoot, normal end");
    assertEquals(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 33, 4), "start overshoot, any end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, 33)), "normal start, end overshoot");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, -2, 12)), "start undershoot, end overshoot");

    // empty-return tests

    assertSame(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_CHAR_ARRAY, 1, 2), "empty array, object test");
    assertSame(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 4, 1), "start > end, object test");
    assertSame(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 2147483647, -2147483648), "start > end, possible overflow");
    assertSame(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end, object test");
    assertSame(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.subarray(array, 8733, 4), "start overshoot, any end, object test");

    // array type tests

    assertSame(char.class, ArrayUtils.subarray(array, 2, 4).getClass().getComponentType(), "char type");
}

@Test
void testSubarrayShort() {
    final short[] nullArray = null;
    final short[] array = {10, 11, 12, 13, 14, 15};
    final short[] leftSubarray = {10, 11, 12, 13};
    final short[] midSubarray = {11, 12, 13, 14};
    final short[] rightSubarray = {12, 13, 14, 15};

    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, 0, 4)), "0 start, mid end");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, 0, array.length)), "0 start, length end");
    assertTrue(ArrayUtils.isEquals(midSubarray, ArrayUtils.subarray(array, 1, 5)), "mid start, mid end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, array.length)),
            "mid start, length end");

    assertNull(ArrayUtils.subarray(nullArray, 0, 3), "null input");
    assertEquals(ArrayUtils.EMPTY_SHORT_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_SHORT_ARRAY, 1, 2),
            "empty array");
    assertEquals(ArrayUtils.EMPTY_SHORT_ARRAY, ArrayUtils.subarray(array, 4, 2), "start > end");
    assertEquals(ArrayUtils.EMPTY_SHORT_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end");
    assertTrue(ArrayUtils.isEquals(leftSubarray, ArrayUtils.subarray(array, -2, 4)),
            "start undershoot, normal end");
    assertEquals(ArrayUtils.EMPTY_SHORT_ARRAY, ArrayUtils.subarray(array, 33, 4), "start overshoot, any end");
    assertTrue(ArrayUtils.isEquals(rightSubarray, ArrayUtils.subarray(array, 2, 33)),
            "normal start, end overshoot");
    assertTrue(ArrayUtils.isEquals(array, ArrayUtils.subarray(array, -2, 12)), "start undershoot, end overshoot");

    // empty-return tests

    assertSame(ArrayUtils.EMPTY_SHORT_ARRAY, ArrayUtils.subarray(ArrayUtils.EMPTY_SHORT_ARRAY, 1, 2),
            "empty array, object test");
    assertSame(ArrayUtils.EMPTY_SHORT_ARRAY, ArrayUtils.subarray(array, 4, 1), "start > end, object test");
    assertSame(ArrayUtils.EMPTY_SHORT_ARRAY, ArrayUtils.subarray(array, 2147483647, -2147483648), "start > end, possible overflow");
    assertSame(ArrayUtils.EMPTY_SHORT_ARRAY, ArrayUtils.subarray(array, 3, 3), "start == end, object test");
    assertSame(ArrayUtils.EMPTY_SHORT_ARRAY, ArrayUtils.subarray(array, 8733, 4),
            "start overshoot, any end, object test");

    // array type tests

    assertSame(short.class, ArrayUtils.subarray(array, 2, 4).getClass().getComponentType(), "short type");
}
```