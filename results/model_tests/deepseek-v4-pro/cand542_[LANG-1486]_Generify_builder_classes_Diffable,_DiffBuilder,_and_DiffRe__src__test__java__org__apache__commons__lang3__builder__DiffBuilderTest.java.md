# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `b77014c9536deb38f91eb579c27e2484793eda44`
- B: `0abfa791934a846a563ee6d4e89eb5e3f92f63de`
- test: `src/test/java/org/apache/commons/lang3/builder/DiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/DiffBuilder.java']`
- old_test_mode: `methods`
- user_chars: `45419`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 11654, 'completion_tokens': 6299, 'total_tokens': 17953, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1940}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 11270}`

---

- 修改所有使用 `DiffResult` 和 `DiffBuilder` 的测试方法，为其局部变量/参数添加合适的泛型参数（如 `DiffResult<TypeTestClass>`、`DiffBuilder<TypeTestClass>` 等），并将构造器调用改为钻石语法 `new DiffBuilder<>(...)`，以适配生产代码中 `DiffBuilder<T>` 与 `DiffResult<T>` 的泛型化变更。
- 具体需修改的 @Test 方法：`testBoolean`、`testBooleanArray`、`testByte`、`testByteArray`、`testByteArrayEqualAsObject`、`testChar`、`testCharArray`、`testDiffResult`、`testDouble`、`testDoubleArray`、`testFloat`、`testFloatArray`、`testInt`、`testIntArray`、`testLong`、`testLongArray`、`testNullLhs`、`testNullRhs`、`testObject`、`testObjectArray`、`testObjectArrayEqual`、`testObjectsNotSameButEqual`、`testObjectsNotSameNorEqual`、`testObjectsSameAndEqual`、`testSameObjectIgnoresAppends`、`testShort`、`testShortArray`、`testSimilarObjectIgnoresAppends`、`testStylePassedToDiffResult`、`testTriviallyEqualTestDisabled`、`testTriviallyEqualTestEnabled`。
- 无需新增或删除测试方法；import 无需调整。

```java
@Test
public void testBoolean() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.booleanField = false;
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertEquals(Boolean.class, diff.getType());
    assertEquals(Boolean.TRUE, diff.getLeft());
    assertEquals(Boolean.FALSE, diff.getRight());
}

@Test
public void testBooleanArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.booleanArrayField = new boolean[] {false, false};
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.booleanArrayField),
            (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.booleanArrayField),
            (Object[]) diff.getRight());
}

@Test
public void testByte() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.byteField = 0x01;
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertEquals(Byte.valueOf(class1.byteField), diff.getLeft());
    assertEquals(Byte.valueOf(class2.byteField), diff.getRight());
}

@Test
public void testByteArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.byteArrayField= new byte[] {0x01, 0x02};
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.byteArrayField),
            (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.byteArrayField),
            (Object[]) diff.getRight());
}

@Test
public void testByteArrayEqualAsObject() {
    final DiffResult<String> list = new DiffBuilder<>("String1", "String2", SHORT_STYLE)
        .append("foo", new boolean[] {false}, new boolean[] {false})
        .append("foo", new byte[] {0x01}, new byte[] {0x01})
        .append("foo", new char[] {'a'}, new char[] {'a'})
        .append("foo", new double[] {1.0}, new double[] {1.0})
        .append("foo", new float[] {1.0F}, new float[] {1.0F})
        .append("foo", new int[] {1}, new int[] {1})
        .append("foo", new long[] {1L}, new long[] {1L})
        .append("foo", new short[] {1}, new short[] {1})
        .append("foo", new Object[] {1, "two"}, new Object[] {1, "two"})
        .build();

    assertEquals(0, list.getNumberOfDiffs());
}

@Test
public void testChar() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.charField = 'z';
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertEquals(Character.valueOf(class1.charField), diff.getLeft());
    assertEquals(Character.valueOf(class2.charField), diff.getRight());
}

@Test
public void testCharArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.charArrayField = new char[] {'f', 'o', 'o'};
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.charArrayField),
            (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.charArrayField),
            (Object[]) diff.getRight());
}

@Test
public void testDiffResult() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.intField = 2;

    final DiffResult<TypeTestClass> list = new DiffBuilder<>(class1, class2, SHORT_STYLE)
        .append("prop1", class1.diff(class2))
        .build();
    assertEquals(1, list.getNumberOfDiffs());
    assertEquals("prop1.int", list.getDiffs().get(0).getFieldName());
}

@Test
public void testDouble() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.doubleField = 99.99;
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertEquals(Double.valueOf(class1.doubleField), diff.getLeft());
    assertEquals(Double.valueOf(class2.doubleField), diff.getRight());
}

@Test
public void testDoubleArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.doubleArrayField = new double[] {3.0, 2.9, 2.8};
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.doubleArrayField),
            (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.doubleArrayField),
            (Object[]) diff.getRight());
}

@Test
public void testFloat() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.floatField = 99.99F;
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertEquals(Float.valueOf(class1.floatField), diff.getLeft());
    assertEquals(Float.valueOf(class2.floatField), diff.getRight());
}

@Test
public void testFloatArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.floatArrayField = new float[] {3.0F, 2.9F, 2.8F};
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.floatArrayField),
            (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.floatArrayField),
            (Object[]) diff.getRight());
}

@Test
public void testInt() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.intField = 42;
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertEquals(Integer.valueOf(class1.intField), diff.getLeft());
    assertEquals(Integer.valueOf(class2.intField), diff.getRight());
}

@Test
public void testIntArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.intArrayField = new int[] {3, 2, 1};
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.intArrayField),
            (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.intArrayField),
            (Object[]) diff.getRight());
}

@Test
public void testLong() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.longField = 42L;
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertEquals(Long.valueOf(class1.longField), diff.getLeft());
    assertEquals(Long.valueOf(class2.longField), diff.getRight());
}

@Test
public void testLongArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.longArrayField = new long[] {3L, 2L, 1L};
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.longArrayField),
            (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.longArrayField),
            (Object[]) diff.getRight());
}

@Test
public void testNullLhs() {
    assertThrows(IllegalArgumentException.class, () -> new DiffBuilder<>(null, this, ToStringStyle.DEFAULT_STYLE));
}

@Test
public void testNullRhs() {
    assertThrows(IllegalArgumentException.class, () -> new DiffBuilder<>(this, null, ToStringStyle.DEFAULT_STYLE));
}

@Test
public void testObject() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.objectField = "Some string";
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertEquals(class1.objectField, diff.getLeft());
    assertEquals(class2.objectField, diff.getRight());
}

@Test
public void testObjectArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.objectArrayField = new Object[] {"string", 1, 2};
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
    class1.objectArrayField = new Object[] {"string", 1, 2};
    class2.objectArrayField = new Object[] {"string", 1, 2};
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(0, list.getNumberOfDiffs());
}

@Test
public void testObjectsNotSameButEqual() {
    final TypeTestClass left = new TypeTestClass();
    left.objectField = new Integer(1);
    final TypeTestClass right = new TypeTestClass();
    right.objectField = new Integer(1);
    assertNotSame(left.objectField, right.objectField);
    assertEquals(left.objectField, right.objectField);

    final DiffResult<TypeTestClass> list = left.diff(right);
    assertEquals(0, list.getNumberOfDiffs());
}

@Test
public void testObjectsNotSameNorEqual() {
    final TypeTestClass left = new TypeTestClass();
    left.objectField = 4;
    final TypeTestClass right = new TypeTestClass();
    right.objectField = 100;
    assertNotSame(left.objectField, right.objectField);
    assertNotEquals(left.objectField, right.objectField);

    final DiffResult<TypeTestClass> list = left.diff(right);
    assertEquals(1, list.getNumberOfDiffs());
}

@Test
public void testObjectsSameAndEqual() {
    final Integer sameObject = 1;
    final TypeTestClass left = new TypeTestClass();
    left.objectField = sameObject;
    final TypeTestClass right = new TypeTestClass();
    right.objectField = sameObject;
    assertSame(left.objectField, right.objectField);
    assertEquals(left.objectField, right.objectField);

    final DiffResult<TypeTestClass> list = left.diff(right);
    assertEquals(0, list.getNumberOfDiffs());
}

@Test
public void testSameObjectIgnoresAppends() {
    final TypeTestClass testClass = new TypeTestClass();
    final DiffResult<TypeTestClass> list = new DiffBuilder<>(testClass, testClass, SHORT_STYLE)
        .append("ignored", false, true)
        .build();
    assertEquals(0, list.getNumberOfDiffs());
}

@Test
public void testShort() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.shortField = 42;
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertEquals(Short.valueOf(class1.shortField), diff.getLeft());
    assertEquals(Short.valueOf(class2.shortField), diff.getRight());
}

@Test
public void testShortArray() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.shortArrayField = new short[] {3, 2, 1};
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertArrayEquals(ArrayUtils.toObject(class1.shortArrayField),
            (Object[]) diff.getLeft());
    assertArrayEquals(ArrayUtils.toObject(class2.shortArrayField),
            (Object[]) diff.getRight());
}

@Test
public void testSimilarObjectIgnoresAppends() {
    final TypeTestClass testClass1 = new TypeTestClass();
    final TypeTestClass testClass2 = new TypeTestClass();
    final DiffResult<TypeTestClass> list = new DiffBuilder<>(testClass1, testClass2, SHORT_STYLE)
        .append("ignored", false, true)
        .build();
    assertEquals(0, list.getNumberOfDiffs());
}

@Test
public void testStylePassedToDiffResult() {
    final TypeTestClass class1 = new TypeTestClass();
    DiffResult<TypeTestClass> list = class1.diff(class1);
    assertEquals(SHORT_STYLE, list.getToStringStyle());

    class1.style = ToStringStyle.MULTI_LINE_STYLE;
    list = class1.diff(class1);
    assertEquals(ToStringStyle.MULTI_LINE_STYLE, list.getToStringStyle());
}

@Test
public void testTriviallyEqualTestDisabled() {
    final Matcher<Integer> equalToOne = equalTo(1);

    // Constructor's arguments are not trivially equal, but not testing for that.
    final DiffBuilder<Integer> explicitTestAndNotEqual1 = new DiffBuilder<>(1, 2, null, false);
    explicitTestAndNotEqual1.append("letter", "X", "Y");
    assertThat(explicitTestAndNotEqual1.build().getNumberOfDiffs(), equalToOne);

    // Constructor's arguments are trivially equal, but not testing for that.
    final DiffBuilder<Integer> explicitTestAndNotEqual2 = new DiffBuilder<>(1, 1, null, false);
    // This append(f, l, r) will not abort early.
    explicitTestAndNotEqual2.append("letter", "X", "Y");
    assertThat(explicitTestAndNotEqual2.build().getNumberOfDiffs(), equalToOne);
}

@Test
public void testTriviallyEqualTestEnabled() {
    final Matcher<Integer> equalToZero = equalTo(0);
    final Matcher<Integer> equalToOne = equalTo(1);

    // The option to test if trivially equal is enabled by default.
    final DiffBuilder<Integer> implicitTestAndEqual = new DiffBuilder<>(1, 1, null);
    // This append(f, l, r) will abort without creating a Diff for letter.
    implicitTestAndEqual.append("letter", "X", "Y");
    assertThat(implicitTestAndEqual.build().getNumberOfDiffs(), equalToZero);

    final DiffBuilder<Integer> implicitTestAndNotEqual = new DiffBuilder<>(1, 2, null);
    // This append(f, l, r) will not abort early
    // because the constructor's arguments were not trivially equal.
    implicitTestAndNotEqual.append("letter", "X", "Y");
    assertThat(implicitTestAndNotEqual.build().getNumberOfDiffs(), equalToOne);

    // This is explicitly enabling the trivially equal test.
    final DiffBuilder<Integer> explicitTestAndEqual = new DiffBuilder<>(1, 1, null, true);
    explicitTestAndEqual.append("letter", "X", "Y");
    assertThat(explicitTestAndEqual.build().getNumberOfDiffs(), equalToZero);
}
```