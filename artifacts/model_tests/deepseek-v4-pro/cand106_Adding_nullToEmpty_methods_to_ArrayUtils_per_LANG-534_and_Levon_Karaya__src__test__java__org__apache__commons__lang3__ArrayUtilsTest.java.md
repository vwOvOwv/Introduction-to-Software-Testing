# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `6c53b134b66d9670114247b022b25a60969900e9`
- B: `6b4cb166081e019b87cd2b5a273a1567d3aff545`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `142126`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 35784, 'completion_tokens': 3704, 'total_tokens': 39488, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1002}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 35400}`

---

- 新增测试方法：`testNullToEmptyBoolean`、`testNullToEmptyLong`、`testNullToEmptyInt`、`testNullToEmptyShort`、`testNullToEmptyChar`、`testNullToEmptyByte`、`testNullToEmptyDouble`、`testNullToEmptyFloat`、`testNullToEmptyObject`、`testNullToEmptyString`、`testNullToEmptyBooleanObject`、`testNullToEmptyLongObject`、`testNullToEmptyIntObject`、`testNullToEmptyShortObject`、`testNullToEmptyCharObject`、`testNullToEmptyByteObject`、`testNullToEmptyDoubleObject`、`testNullToEmptyFloatObject`，对应生产代码新增的 `nullToEmpty` 系列重载方法。
- 无需新增 import，现有 import 已覆盖 `TestCase`、`ArrayUtils` 等必需依赖。
- 无需删除或修改任何已有测试方法。

```java
// No import changes needed.

    public void testNullToEmptyBoolean() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_BOOLEAN_ARRAY, ArrayUtils.nullToEmpty((boolean[]) null));
        // Test valid array handling
        boolean[] original = new boolean[] {true, false};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        boolean[] empty = new boolean[]{};
        boolean[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_BOOLEAN_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyLong() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_LONG_ARRAY, ArrayUtils.nullToEmpty((long[]) null));
        // Test valid array handling
        long[] original = new long[] {1L, 2L};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        long[] empty = new long[]{};
        long[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_LONG_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyInt() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_INT_ARRAY, ArrayUtils.nullToEmpty((int[]) null));
        // Test valid array handling
        int[] original = new int[] {1, 2};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        int[] empty = new int[]{};
        int[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_INT_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyShort() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_SHORT_ARRAY, ArrayUtils.nullToEmpty((short[]) null));
        // Test valid array handling
        short[] original = new short[] {1, 2};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        short[] empty = new short[]{};
        short[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_SHORT_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyChar() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_CHAR_ARRAY, ArrayUtils.nullToEmpty((char[]) null));
        // Test valid array handling
        char[] original = new char[] {'a', 'b'};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        char[] empty = new char[]{};
        char[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_CHAR_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyByte() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_BYTE_ARRAY, ArrayUtils.nullToEmpty((byte[]) null));
        // Test valid array handling
        byte[] original = new byte[] {0x0F, 0x0E};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        byte[] empty = new byte[]{};
        byte[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_BYTE_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyDouble() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_DOUBLE_ARRAY, ArrayUtils.nullToEmpty((double[]) null));
        // Test valid array handling
        double[] original = new double[] {1L, 2L};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        double[] empty = new double[]{};
        double[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_DOUBLE_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyFloat() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_FLOAT_ARRAY, ArrayUtils.nullToEmpty((float[]) null));
        // Test valid array handling
        float[] original = new float[] {2.6f, 3.8f};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        float[] empty = new float[]{};
        float[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_FLOAT_ARRAY, result);
        assertTrue(empty != result);
    }

    public void testNullToEmptyObject() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_OBJECT_ARRAY, ArrayUtils.nullToEmpty((Object[]) null));
        // Test valid array handling
        Object[] original = new Object[] {true, false};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        Object[] empty = new Object[]{};
        Object[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_OBJECT_ARRAY, result);
        assertTrue(empty != result);
    }

    public void testNullToEmptyString() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_STRING_ARRAY, ArrayUtils.nullToEmpty((String[]) null));
        // Test valid array handling
        String[] original = new String[] {"abc", "def"};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        String[] empty = new String[]{};
        String[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_STRING_ARRAY, result);
        assertTrue(empty != result);
    }

    public void testNullToEmptyBooleanObject() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_BOOLEAN_OBJECT_ARRAY, ArrayUtils.nullToEmpty((Boolean[]) null));
        // Test valid array handling
        Boolean[] original = new Boolean[] {Boolean.TRUE, Boolean.FALSE};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        Boolean[] empty = new Boolean[]{};
        Boolean[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_BOOLEAN_OBJECT_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyLongObject() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_LONG_OBJECT_ARRAY, ArrayUtils.nullToEmpty((Long[]) null));
        // Test valid array handling
        Long[] original = new Long[] {1L, 2L};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        Long[] empty = new Long[]{};
        Long[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_LONG_OBJECT_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyIntObject() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_INTEGER_OBJECT_ARRAY, ArrayUtils.nullToEmpty((Integer[]) null));
        // Test valid array handling
        Integer[] original = new Integer[] {1, 2};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        Integer[] empty = new Integer[]{};
        Integer[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_INTEGER_OBJECT_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyShortObject() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_SHORT_OBJECT_ARRAY, ArrayUtils.nullToEmpty((Short[]) null));
        // Test valid array handling
        Short[] original = new Short[] {1, 2};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        Short[] empty = new Short[]{};
        Short[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_SHORT_OBJECT_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyCharObject() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_CHARACTER_OBJECT_ARRAY, ArrayUtils.nullToEmpty((Character[]) null));
        // Test valid array handling
        Character[] original = new Character[] {'a', 'b'};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        Character[] empty = new Character[]{};
        Character[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_CHARACTER_OBJECT_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyByteObject() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_BYTE_OBJECT_ARRAY, ArrayUtils.nullToEmpty((Byte[]) null));
        // Test valid array handling
        Byte[] original = new Byte[] {0x0F, 0x0E};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        Byte[] empty = new Byte[]{};
        Byte[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_BYTE_OBJECT_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyDoubleObject() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_DOUBLE_OBJECT_ARRAY, ArrayUtils.nullToEmpty((Double[]) null));
        // Test valid array handling
        Double[] original = new Double[] {1D, 2D};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        Double[] empty = new Double[]{};
        Double[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_DOUBLE_OBJECT_ARRAY, result);
        assertTrue(empty != result);
    }
    
    public void testNullToEmptyFloatObject() {
        // Test null handling
        assertEquals(ArrayUtils.EMPTY_FLOAT_OBJECT_ARRAY, ArrayUtils.nullToEmpty((Float[]) null));
        // Test valid array handling
        Float[] original = new Float[] {2.6f, 3.8f};
        assertEquals(original, ArrayUtils.nullToEmpty(original));
        // Test empty array handling
        Float[] empty = new Float[]{};
        Float[] result = ArrayUtils.nullToEmpty(empty);
        assertEquals(ArrayUtils.EMPTY_FLOAT_OBJECT_ARRAY, result);
        assertTrue(empty != result);
    }
```