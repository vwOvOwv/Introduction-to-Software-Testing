# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ea47f03c4d6fba945be43d5c676075ba98b28138`
- B: `8a82d7b79b9de7edf2a7a22a7a32026d2b961662`
- test: `src/test/java/org/apache/commons/lang3/builder/DiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/DiffBuilder.java']`
- old_test_mode: `methods`
- user_chars: `28369`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7638, 'completion_tokens': 4187, 'total_tokens': 11825}`

---

- 修改辅助方法 `TypeTestClass.diff`：生产代码 `DiffBuilder.build()` 返回类型由 `DiffList` 改为 `DiffResult`，因此实现 `Diffable` 的测试辅助类也需返回 `DiffResult`。
- 修改 `testBoolean`、`testBooleanArray`、`testByte`、`testByteArray`、`testChar`、`testCharArray`、`testDouble`、`testDoubleArray`、`testFloat`、`testFloatArray`、`testInt`、`testIntArray`、`testLong`、`testLongArray`、`testShort`、`testShortArray`、`testObject`、`testObjectsEqual`、`testObjectArray`、`testObjectArrayEqual`、`testByteArrayEqualAsObject`、`testSameObjectIgnoresAppends`、`testSimilarObjectIgnoresAppends`：局部变量类型由 `DiffList` 改为 `DiffResult`。
- 删除旧测试方法 `testStylePassedToDiffList`，并新增等价的 `testStylePassedToDiffResult`：测试名与新返回类型 `DiffResult` 保持一致。
- 不需要调整 import：`DiffResult` 与测试类位于同一 package。

```java
// DELETE_TESTS_START
testStylePassedToDiffList
// DELETE_TESTS_END

        @Override
        public DiffResult diff(TypeTestClass obj) {
            return new DiffBuilder(this, obj, style)
                .append("boolean", booleanField, obj.booleanField)
                .append("booleanArray", booleanArrayField, obj.booleanArrayField)
                .append("byte", byteField, obj.byteField)
                .append("byteArray", byteArrayField, obj.byteArrayField)
                .append("char", charField, obj.charField)
                .append("charArray", charArrayField, obj.charArrayField)
                .append("double", doubleField, obj.doubleField)
                .append("doubleArray", doubleArrayField, obj.doubleArrayField)
                .append("float", floatField, obj.floatField)
                .append("floatArray", floatArrayField, obj.floatArrayField)
                .append("int", intField, obj.intField)
                .append("intArray", intArrayField, obj.intArrayField)
                .append("long", longField, obj.longField)
                .append("longArray", longArrayField, obj.longArrayField)
                .append("short", shortField, obj.shortField)
                .append("shortArray", shortArrayField, obj.shortArrayField)
                .append("object", objectField, obj.objectField)
                .append("objectArray", objectArrayField, obj.objectArrayField)
                .build();
        }

    @Test
    public void testBoolean() {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.booleanField = false;
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertEquals(Boolean.class, diff.getType());
        assertEquals(Boolean.TRUE, diff.getLeft());
        assertEquals(Boolean.FALSE, diff.getRight());        
    }

    @Test
    public void testBooleanArray() throws Exception {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.booleanArrayField = new boolean[] {false, false};
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertArrayEquals(ArrayUtils.toObject(class1.booleanArrayField), 
                (Object[]) diff.getLeft());
        assertArrayEquals(ArrayUtils.toObject(class2.booleanArrayField), 
                (Object[]) diff.getRight());
    }

    @Test
    public void testByte() {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.byteField = 0x01;
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertEquals(Byte.valueOf(class1.byteField), diff.getLeft());
        assertEquals(Byte.valueOf(class2.byteField), diff.getRight());        
    }

    @Test
    public void testByteArray() throws Exception {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.byteArrayField= new byte[] {0x01, 0x02};
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertArrayEquals(ArrayUtils.toObject(class1.byteArrayField), 
                (Object[]) diff.getLeft());
        assertArrayEquals(ArrayUtils.toObject(class2.byteArrayField), 
                (Object[]) diff.getRight());
    }

    @Test
    public void testByteArrayEqualAsObject() throws Exception {
        DiffResult list = new DiffBuilder("String1", "String2", SHORT_STYLE)
            .append("foo", (Object) new boolean[] {false}, (Object) new boolean[] {false})
            .append("foo", (Object) new byte[] {0x01}, (Object) new byte[] {0x01})
            .append("foo", (Object) new char[] {'a'}, (Object) new char[] {'a'})
            .append("foo", (Object) new double[] {1.0}, (Object) new double[] {1.0})
            .append("foo", (Object) new float[] {1.0F}, (Object) new float[] {1.0F})
            .append("foo", (Object) new int[] {1}, (Object) new int[] {1})
            .append("foo", (Object) new long[] {1L}, (Object) new long[] {1L})
            .append("foo", (Object) new short[] {1}, (Object) new short[] {1})
            .append("foo", (Object) new Object[] {1, "two"}, (Object) new Object[] {1, "two"})
            .build();

        assertEquals(0, list.getNumberOfDiffs());
    }

    @Test
    public void testChar() {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.charField = 'z';
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertEquals(Character.valueOf(class1.charField), diff.getLeft());
        assertEquals(Character.valueOf(class2.charField), diff.getRight());
    }

    @Test
    public void testCharArray() throws Exception {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.charArrayField = new char[] {'f', 'o', 'o'};
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertArrayEquals(ArrayUtils.toObject(class1.charArrayField), 
                (Object[]) diff.getLeft());
        assertArrayEquals(ArrayUtils.toObject(class2.charArrayField), 
                (Object[]) diff.getRight());
    }

    @Test
    public void testDouble() {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.doubleField = 99.99;
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertEquals(Double.valueOf(class1.doubleField), diff.getLeft());
        assertEquals(Double.valueOf(class2.doubleField), diff.getRight());
    }    

    @Test
    public void testDoubleArray() throws Exception {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.doubleArrayField = new double[] {3.0, 2.9, 2.8};
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertArrayEquals(ArrayUtils.toObject(class1.doubleArrayField), 
                (Object[]) diff.getLeft());
        assertArrayEquals(ArrayUtils.toObject(class2.doubleArrayField), 
                (Object[]) diff.getRight());
    }

    @Test
    public void testFloat() {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.floatField = 99.99F;
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertEquals(Float.valueOf(class1.floatField), diff.getLeft());
        assertEquals(Float.valueOf(class2.floatField), diff.getRight());
    }    

    @Test
    public void testFloatArray() throws Exception {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.floatArrayField = new float[] {3.0F, 2.9F, 2.8F};
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertArrayEquals(ArrayUtils.toObject(class1.floatArrayField), 
                (Object[]) diff.getLeft());
        assertArrayEquals(ArrayUtils.toObject(class2.floatArrayField), 
                (Object[]) diff.getRight());
    }    

    @Test
    public void testInt() {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.intField = 42;
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertEquals(Integer.valueOf(class1.intField), diff.getLeft());
        assertEquals(Integer.valueOf(class2.intField), diff.getRight());
    }    

    @Test
    public void testIntArray() throws Exception {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.intArrayField = new int[] {3, 2, 1};
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertArrayEquals(ArrayUtils.toObject(class1.intArrayField), 
                (Object[]) diff.getLeft());
        assertArrayEquals(ArrayUtils.toObject(class2.intArrayField), 
                (Object[]) diff.getRight());
    }

    @Test
    public void testLong() {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.longField = 42L;
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertEquals(Long.valueOf(class1.longField), diff.getLeft());
        assertEquals(Long.valueOf(class2.longField), diff.getRight());
    }    

    @Test
    public void testLongArray() throws Exception {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.longArrayField = new long[] {3L, 2L, 1L};
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertArrayEquals(ArrayUtils.toObject(class1.longArrayField), 
                (Object[]) diff.getLeft());
        assertArrayEquals(ArrayUtils.toObject(class2.longArrayField), 
                (Object[]) diff.getRight());
    }

    @Test
    public void testObject() throws Exception {        
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.objectField = "Some string";
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertEquals(class1.objectField, diff.getLeft());
        assertEquals(class2.objectField, diff.getRight());                
    }

    @Test
    public void testObjectArray() throws Exception {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.objectArrayField = new Object[] {"string", 1, 2};
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertArrayEquals(class1.objectArrayField, (Object[]) diff.getLeft());
        assertArrayEquals(class2.objectArrayField, (Object[]) diff.getRight());
    }   

    @Test
    public void testObjectArrayEqual() throws Exception {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class1.objectArrayField = new Object[] {"string", 1, 2};
        class2.objectArrayField = new Object[] {"string", 1, 2};
        DiffResult list = class1.diff(class2);
        assertEquals(0, list.getNumberOfDiffs());
    }  

    @Test
    public void testObjectsEqual() throws Exception {        
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class1.objectField = "Some string";
        class2.objectField = "Some string";
        DiffResult list = class1.diff(class2);
        assertEquals(0, list.getNumberOfDiffs());
    }

    @Test
    public void testSameObjectIgnoresAppends() {
        TypeTestClass testClass = new TypeTestClass();        
        DiffResult list = new DiffBuilder(testClass, testClass, SHORT_STYLE)
            .append("ignored", false, true)
            .build();
        assertEquals(0, list.getNumberOfDiffs());
    }

    @Test
    public void testShort() {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.shortField = 42;
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertEquals(Short.valueOf(class1.shortField), diff.getLeft());
        assertEquals(Short.valueOf(class2.shortField), diff.getRight());
    }    

    @Test
    public void testShortArray() throws Exception {
        TypeTestClass class1 = new TypeTestClass();
        TypeTestClass class2 = new TypeTestClass();
        class2.shortArrayField = new short[] {3, 2, 1};
        DiffResult list = class1.diff(class2);
        assertEquals(1, list.getNumberOfDiffs());
        Diff<?> diff = list.getDiffs().get(0);
        assertArrayEquals(ArrayUtils.toObject(class1.shortArrayField), 
                (Object[]) diff.getLeft());
        assertArrayEquals(ArrayUtils.toObject(class2.shortArrayField), 
                (Object[]) diff.getRight());
    }

    @Test
    public void testSimilarObjectIgnoresAppends() {
        TypeTestClass testClass1 = new TypeTestClass();
        TypeTestClass testClass2 = new TypeTestClass();
        DiffResult list = new DiffBuilder(testClass1, testClass2, SHORT_STYLE)
            .append("ignored", false, true)
            .build();
        assertEquals(0, list.getNumberOfDiffs());
    }

    @Test
    public void testStylePassedToDiffResult() {
        TypeTestClass class1 = new TypeTestClass();
        DiffResult list = class1.diff(class1);
        assertEquals(SHORT_STYLE, list.getToStringStyle());
        
        class1.style = ToStringStyle.MULTI_LINE_STYLE;
        list = class1.diff(class1);
        assertEquals(ToStringStyle.MULTI_LINE_STYLE, list.getToStringStyle());
    }
```