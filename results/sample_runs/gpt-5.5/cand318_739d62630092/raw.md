# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `b08717ff5fd391ad500a557b8ad8b5c3794a0df5`
- B: `739d62630092ee517129c703cd9433bd7e1184d4`
- test: `src/test/java/org/apache/commons/lang3/builder/DiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/DiffBuilder.java']`
- old_test_mode: `methods`
- user_chars: `9362`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7259, 'completion_tokens': 1883, 'total_tokens': 9142, 'prompt_tokens_details': {'cached_tokens': 3840}, 'completion_tokens_details': {'reasoning_tokens': 516}}`

---

- 修改 `testByteArrayEqualAsObject1`：仅将结尾 formatter 标记从 `@formatter:off` 改为 `@formatter:on`，与测试 diff 保持一致。
- 修改 `testByteArrayEqualAsObjectDeprecated`：仅将结尾 formatter 标记从 `@formatter:off` 改为 `@formatter:on`，与测试 diff 保持一致。
- 新增 `testNestedDiffableNo`：覆盖嵌套 `DiffResult<?>` 无差异时不产生 diff。
- 新增 `testNestedDiffableYesNestedOnly`：覆盖仅嵌套对象有差异时，`append(String, DiffResult<?>)` 能接收并展开 diff。
- 新增 `testNestedDiffableYesNestedNot`：覆盖只有外层字段有差异时结果不受嵌套 diff 影响。
- 新增 `testNestedDiffableYesNestedYes`：覆盖外层字段和嵌套 `DiffResult<?>` 同时有差异时均被保留。
- 需要新增 import：`java.util.List`，用于接收 `DiffResult#getDiffs()` 返回值。

```java
import java.util.List;

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