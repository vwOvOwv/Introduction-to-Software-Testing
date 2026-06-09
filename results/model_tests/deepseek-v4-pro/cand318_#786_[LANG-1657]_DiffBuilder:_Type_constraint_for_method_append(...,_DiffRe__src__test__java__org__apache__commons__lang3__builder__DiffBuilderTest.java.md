# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `b08717ff5fd391ad500a557b8ad8b5c3794a0df5`
- B: `739d62630092ee517129c703cd9433bd7e1184d4`
- test: `src/test/java/org/apache/commons/lang3/builder/DiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/DiffBuilder.java']`
- old_test_mode: `methods`
- user_chars: `9362`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2879, 'completion_tokens': 6133, 'total_tokens': 9012, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 3891}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2495}`

---

- 新增内部类 `NestedTypeTestClass`，用于构造具有 `Diffable` 行为的嵌套对象，以支持嵌套 diff 场景的测试。
- 修改内部类 `TypeTestClass`，添加字段 `nestedDiffableField` 并在 `diff()` 方法中调用 `append` 传入其 diff 结果，以验证 `DiffBuilder.append(String, DiffResult<?>)` 的泛型修正。
- 修改测试方法 `testByteArrayEqualAsObject1`，将末尾的格式化注释 `// @formatter:off` 改为 `// @formatter:on`，与生产代码保持一致的格式修正。
- 修改测试方法 `testByteArrayEqualAsObjectDeprecated`，同上修改末尾格式化注释。
- 新增测试方法 `testNestedDiffableNo`，验证两个对象无差异时嵌套 diff 结果为空。
- 新增测试方法 `testNestedDiffableYesNestedOnly`，验证仅嵌套字段存在差异时的 diff 结果。
- 新增测试方法 `testNestedDiffableYesNestedNot`，验证仅非嵌套字段存在差异时的 diff 结果。
- 新增测试方法 `testNestedDiffableYesNestedYes`，验证嵌套字段和非嵌套字段同时存在差异时的 diff 结果。
- 新增 import `java.util.List`，因为新增测试使用了 `List<Diff<?>>`。

```java
// IMPORTS_START
import java.util.List;
// IMPORTS_END

/**
 * Test fixture.
 */
private static class NestedTypeTestClass implements Diffable<NestedTypeTestClass> {

    private final ToStringStyle style = SHORT_STYLE;
    private boolean booleanField = true;

    @Override
    public DiffResult<NestedTypeTestClass> diff(final NestedTypeTestClass obj) {
        // @formatter:off
        return new DiffBuilder<>(this, obj, style)
                .append("boolean", booleanField, obj.booleanField)
                .build();
        // @formatter:on
    }

    @Override
    public boolean equals(final Object obj) {
        return EqualsBuilder.reflectionEquals(this, obj, false);
    }

    @Override
    public int hashCode() {
        return HashCodeBuilder.reflectionHashCode(this, false);
    }
}

/**
 * Test fixture.
 */
private static final class TypeTestClass implements Diffable<TypeTestClass> {
    private ToStringStyle style = SHORT_STYLE;
    private boolean booleanField = true;
    private boolean[] booleanArrayField = { true };
    private byte byteField = 1;
    private byte[] byteArrayField = { 1 };
    private char charField = 'a';
    private char[] charArrayField = { 'a' };
    private double doubleField = 1.0;
    private double[] doubleArrayField = { 1.0 };
    private float floatField = 1.0F;
    private float[] floatArrayField = { 1.0F };
    private int intField = 1;
    private int[] intArrayField = { 1 };
    private long longField = 1L;
    private long[] longArrayField = { 1L };
    private short shortField = 1;
    private short[] shortArrayField = { 1 };
    private Object objectField;
    private Object[] objectArrayField = { null };
    private final NestedTypeTestClass nestedDiffableField = new NestedTypeTestClass();

    @Override
    public DiffResult<TypeTestClass> diff(final TypeTestClass obj) {
        // @formatter:off
        return new DiffBuilder<>(this, obj, style)
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
                .append("objectField", objectField, obj.objectField)
                .append("objectArrayField", objectArrayField, obj.objectArrayField)
                .append("nestedDiffableField", nestedDiffableField.diff(obj.nestedDiffableField))
                .build();
        // @formatter:on
    }

    @Override
    public boolean equals(final Object obj) {
        return EqualsBuilder.reflectionEquals(this, obj, false);
    }

    @Override
    public int hashCode() {
        return HashCodeBuilder.reflectionHashCode(this, false);
    }
}

@Test
public void testByteArrayEqualAsObject1() {
    // @formatter:off
    final DiffResult<String> list = DiffBuilder.<String>builder().setLeft("String1").setRight("String2").setStyle(SHORT_STYLE).build()
            .append("foo", new boolean[] { false }, new boolean[] { false })
            .append("foo", new byte[] { 0x01 }, new byte[] { 0x01 })
            .append("foo", new char[] { 'a' }, new char[] { 'a' })
            .append("foo", new double[] { 1.0 }, new double[] { 1.0 })
            .append("foo", new float[] { 1.0F }, new float[] { 1.0F })
            .append("foo", new int[] { 1 }, new int[] { 1 })
            .append("foo", new long[] { 1L }, new long[] { 1L })
            .append("foo", new short[] { 1 }, new short[] { 1 })
            .append("foo", new Object[] { 1, "two" }, new Object[] { 1, "two" })
            .build();
    // @formatter:on
    assertEquals(0, list.getNumberOfDiffs());
}

@Test
public void testByteArrayEqualAsObjectDeprecated() {
    // @formatter:off
    final DiffResult<String> list = new DiffBuilder<>("String1", "String2", SHORT_STYLE)
            .append("foo", new boolean[] { false }, new boolean[] { false })
            .append("foo", new byte[] { 0x01 }, new byte[] { 0x01 })
            .append("foo", new char[] { 'a' }, new char[] { 'a' })
            .append("foo", new double[] { 1.0 }, new double[] { 1.0 })
            .append("foo", new float[] { 1.0F }, new float[] { 1.0F })
            .append("foo", new int[] { 1 }, new int[] { 1 })
            .append("foo", new long[] { 1L }, new long[] { 1L })
            .append("foo", new short[] { 1 }, new short[] { 1 })
            .append("foo", new Object[] { 1, "two" }, new Object[] { 1, "two" })
            .build();
    // @formatter:on
    assertEquals(0, list.getNumberOfDiffs());
}

@Test
public void testNestedDiffableNo() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(0, list.getNumberOfDiffs());
    final List<Diff<?>> diff = list.getDiffs();
    assertTrue(diff.isEmpty());
}

@Test
public void testNestedDiffableYesNestedOnly() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.nestedDiffableField.booleanField = false;
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertEquals(Object.class, diff.getType());
    assertEquals(Boolean.TRUE, diff.getLeft());
    assertEquals(Boolean.FALSE, diff.getRight());
}

@Test
public void testNestedDiffableYesNestedNot() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.intField = 9;
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(1, list.getNumberOfDiffs());
    final Diff<?> diff = list.getDiffs().get(0);
    assertEquals(Integer.class, diff.getType());
    assertEquals(1, diff.getLeft());
    assertEquals(9, diff.getRight());
}

@Test
public void testNestedDiffableYesNestedYes() {
    final TypeTestClass class1 = new TypeTestClass();
    final TypeTestClass class2 = new TypeTestClass();
    class2.intField = 9;
    class2.nestedDiffableField.booleanField = false;
    final DiffResult<TypeTestClass> list = class1.diff(class2);
    assertEquals(2, list.getNumberOfDiffs());
    final Diff<?> diff0 = list.getDiffs().get(0);
    assertEquals(Integer.class, diff0.getType());
    assertEquals(1, diff0.getLeft());
    assertEquals(9, diff0.getRight());
    final Diff<?> diff1 = list.getDiffs().get(1);
    assertEquals(Object.class, diff1.getType());
    assertEquals(Boolean.TRUE, diff1.getLeft());
    assertEquals(Boolean.FALSE, diff1.getRight());
}
```