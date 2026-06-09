# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cb3cbd356feb56c002a8f7fa173a4e0b3cb9f919`
- B: `faa1a1eea544dbdf5c2fa88c622e6e3eedd09837`
- test: `src/test/java/org/apache/commons/lang3/builder/DiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/DiffBuilder.java']`
- old_test_mode: `methods`
- user_chars: `49885`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 12795, 'completion_tokens': 7437, 'total_tokens': 20232, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 4731}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 12411}`

---

根据生产代码重构（`objectsEquals`重命名为`equals`、引入延迟求值的`SDiff`，移除`validateFieldNameNotNull`），测试代码需同步调整断言的消息格式化以及方法链样式，以保证在B版本上编译通过且断言成功。

- 将修改 `testBoolean` 方法，为 `getType()` 断言增加 `Supplier` 消息以匹配新 `SDiff` 产生的类型。
- 将修改 `testBooleanArray` 方法，将多行 `assertArrayEquals` 合并为单行，与B端格式一致。
- 将修改 `testByte` 方法，新增 `getType()` 断言及 `Supplier` 消息；该方法在A端未展示，需按 diff 整体提供。
- 将修改 `testByteArray` 方法，格式化 `assertArrayEquals` 为单行。
- 将修改 `testByteArrayEqualAsObject` 方法，将链式构建改为单行链式调用。
- 将修改 `testCharArray` 方法，格式化 `assertArrayEquals` 为单行。
- 将修改 `testDiffResult` 方法，将链式构建改为单行链式调用。
- 将修改 `testDoubleArray` 方法，格式化 `assertArrayEquals` 为单行。
- 将修改 `testFloatArray` 方法，格式化 `assertArrayEquals` 为单行。
- 将修改 `testIntArray` 方法，格式化 `assertArrayEquals` 为单行。
- 将修改 `testLongArray` 方法，格式化 `assertArrayEquals` 为单行。
- 将修改 `testObjectArray` 方法，使用空格分隔数组字面量。
- 将修改 `testObjectArrayEqual` 方法，使用空格分隔数组字面量。
- 将修改 `testSameObjectIgnoresAppends` 方法，将链式构建改为单行链式调用。
- 将修改 `testShortArray` 方法，格式化 `assertArrayEquals` 为单行。
- 将修改 `testSimilarObjectIgnoresAppends` 方法，将链式构建改为单行链式调用。

无需调整 import 区。

```java
@Test
public void testBoolean() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.booleanField = false;
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertEquals(Boolean.class, diff.getType(), () -> diff.getType().getClass().toString());
    assertEquals(Boolean.TRUE, diff.getLeft());
    assertEquals(Boolean.FALSE, diff.getRight());
}

@Test
public void testBooleanArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.booleanArrayField = new boolean[] { false, false };
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.booleanArrayField), (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.booleanArrayField), (Object[]) diff.getRight());
}

@Test
public void testByte() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.byteField = 0x01;
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertEquals(Byte.class, diff.getType(), () -> diff.getType().getClass().toString());
    assertEquals(Byte.valueOf(class1.byteField), diff.getLeft());
    assertEquals(Byte.valueOf(class2.byteField), diff.getRight());
}

@Test
public void testByteArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.byteArrayField = new byte[] { 0x01, 0x02 };
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.byteArrayField), (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.byteArrayField), (Object[]) diff.getRight());
}

@Test
public void testByteArrayEqualAsObject() {
    final DiffResult<String> list = new DiffBuilder<>("String1", "String2", SHORT_STYLE).append("foo", new boolean[] { false }, new boolean[] { false })
            .append("foo", new byte[] { 0x01 }, new byte[] { 0x01 }).append("foo", new char[] { 'a' }, new char[] { 'a' })
            .append("foo", new double[] { 1.0 }, new double[] { 1.0 }).append("foo", new float[] { 1.0F }, new float[] { 1.0F })
            .append("foo", new int[] { 1 }, new int[] { 1 }).append("foo", new long[] { 1L }, new long[] { 1L })
            .append("foo", new short[] { 1 }, new short[] { 1 }).append("foo", new Object[] { 1, "two" }, new Object[] { 1, "two" }).build();

    assertEquals(0, list.getNumberOfDiffs());
}

@Test
public void testCharArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.charArrayField = new char[] { 'f', 'o', 'o' };
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.charArrayField), (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.charArrayField), (Object[]) diff.getRight());
}

@Test
public void testDiffResult() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.intField = 2;

    final DiffResult<TypeTestClass> list = new DiffBuilder<>(class1, class2, SHORT_STYLE).append("prop1", class1.diff(class2)).build();
    assertEquals(1, list.getNumberOfDiffs());
    assertEquals("prop1.int", list.getDiffs().get(0).getFieldName());
}

@Test
public void testDoubleArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.doubleArrayField = new double[] { 3.0, 2.9, 2.8 };
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.doubleArrayField), (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.doubleArrayField), (Object[]) diff.getRight());
}

@Test
public void testFloatArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.floatArrayField = new float[] { 3.0F, 2.9F, 2.8F };
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.floatArrayField), (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.floatArrayField), (Object[]) diff.getRight());
}

@Test
public void testIntArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.intArrayField = new int[] { 3, 2, 1 };
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.intArrayField), (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.intArrayField), (Object[]) diff.getRight());
}

@Test
public void testLongArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.longArrayField = new long[] { 3L, 2L, 1L };
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.longArrayField), (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.longArrayField), (Object[]) diff.getRight());
}

@Test
public void testObjectArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.objectArrayField = new Object[] { "string", 1, 2 };
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(class1.objectArrayField, (Object[]) diff.getLeft());
    assertArrayEquals(class2.objectArrayField, (Object[]) diff.getRight());
}

@Test
public void testObjectArrayEqual() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class1.objectArrayField = new Object[] { "string", 1, 2 };
    class2.objectArrayField = new Object[] { "string", 1, 2 };
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(0, list.getNumberOfDiffs());
}

@Test
public void testSameObjectIgnoresAppends() {
    final TypeTestClass testClass = new TypeTestClass();
    final DiffResult<TypeTestClass> list = new DiffBuilder<>(testClass, testClass, SHORT_STYLE).append("ignored", false, true).build();
    assertEquals(0, list.getNumberOfDiffs());
}

@Test
public void testShortArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.shortArrayField = new short[] { 3, 2, 1 };
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.shortArrayField), (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.shortArrayField), (Object[]) diff.getRight());
}

@Test
public void testSimilarObjectIgnoresAppends() {
    final TypeTestClass testClass1 = new TypeTestClass();
    final TypeTestClass testClass2 = new TypeTestClass();
    final DiffResult<TypeTestClass> list = new DiffBuilder<>(testClass1, testClass2, SHORT_STYLE).append("ignored", false, true).build();
    assertEquals(0, list.getNumberOfDiffs());
}
```