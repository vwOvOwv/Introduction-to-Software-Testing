# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `119623760e52ef14cbbf16f57d3ffddc14e4a700`
- B: `f51299ced4fd40b44a3f6eca9ae528e818558205`
- test: `src/test/java/org/apache/commons/lang3/builder/ReflectionDiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/ReflectionDiffBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `13647`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3540, 'completion_tokens': 2388, 'total_tokens': 5928}`

---

- 新增 `test_no_differences_excluded_field`，覆盖 `ReflectionDiffBuilder#setExcludeFieldNames` 排除指定字段后的 diff 行为。
- 新增 `test_no_differences_diff_exclude_annotated_field`，覆盖 `accept` 新增的 `@DiffExclude` 注解排除逻辑。
- 新增 `test_no_differences_diff_exluded_field_and_exclude_annotated_field`，覆盖字段名排除与注解排除同时生效。
- 新增 `testGetExcludeFieldNamesWithNullExcludedFieldNames`，覆盖 `setExcludeFieldNames(null)` 后 `getExcludeFieldNames()` 返回非空空数组。
- 新增 `testGetExcludeFieldNamesWithNullValuesInExcludedFieldNames`，覆盖排除字段名中的 `null` 会被移除且结果可读取。
- 修改测试夹具 `TypeTestClass`，新增 `annotatedField`、`excludedField` 并在 `diff` 中调用 `setExcludeFieldNames("excludedField")`。
- 需要调整 import，新增静态导入 `assertNotNull`。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

import org.apache.commons.lang3.AbstractLangTest;
import org.junit.jupiter.api.Test;
// IMPORTS_END

public class ReflectionDiffBuilderTest extends AbstractLangTest {

    private static final ToStringStyle SHORT_STYLE = ToStringStyle.SHORT_PREFIX_STYLE;

    @SuppressWarnings("unused")
    private static class TypeTestClass implements Diffable<TypeTestClass> {
        private final ToStringStyle style = SHORT_STYLE;
        private final boolean booleanField = true;
        private final boolean[] booleanArrayField = {true};
        private final byte byteField = (byte) 0xFF;
        private final byte[] byteArrayField = {(byte) 0xFF};
        private char charField = 'a';
        private char[] charArrayField = {'a'};
        private final double doubleField = 1.0;
        private final double[] doubleArrayField = {1.0};
        private final float floatField = 1.0f;
        private final float[] floatArrayField = {1.0f};
        int intField = 1;
        private final int[] intArrayField = {1};
        private final long longField = 1L;
        private final long[] longArrayField = {1L};
        private final short shortField = 1;
        private final short[] shortArrayField = {1};
        private final Object objectField = null;
        private final Object[] objectArrayField = {null};
        private static int staticField;
        private transient String transientField;
        @DiffExclude
        private String annotatedField = "a";
        private String excludedField = "a";

        @Override
        public DiffResult diff(final TypeTestClass obj) {
            return new ReflectionDiffBuilder(this, obj, style).setExcludeFieldNames("excludedField").build();
        }

        @Override
        public int hashCode() {
            return HashCodeBuilder.reflectionHashCode(this, false);
        }

        @Override
        public boolean equals(final Object obj) {
            return EqualsBuilder.reflectionEquals(this, obj, false);
        }
    }

    @SuppressWarnings("unused")
    private static class TypeTestChildClass extends TypeTestClass {
        String field = "a";
    }

    @Test
    public void test_no_differences() {
        final TypeTestClass firstObject = new TypeTestClass();
        final TypeTestClass secondObject = new TypeTestClass();

        final DiffResult list = firstObject.diff(secondObject);
        assertEquals(0, list.getNumberOfDiffs());
    }

    @Test
    public void test_primitive_difference() {
        final TypeTestClass firstObject = new TypeTestClass();
        firstObject.charField = 'c';
        final TypeTestClass secondObject = new TypeTestClass();

        final DiffResult list = firstObject.diff(secondObject);
        assertEquals(1, list.getNumberOfDiffs());
    }

    @Test
    public void test_array_difference() {
        final TypeTestClass firstObject = new TypeTestClass();
        firstObject.charArrayField = new char[] { 'c' };
        final TypeTestClass secondObject = new TypeTestClass();

        final DiffResult list = firstObject.diff(secondObject);
        assertEquals(1, list.getNumberOfDiffs());
    }

    @Test
    public void test_transient_field_difference() {
        final TypeTestClass firstObject = new TypeTestClass();
        firstObject.transientField = "a";
        final TypeTestClass secondObject = new TypeTestClass();
        firstObject.transientField = "b";

        final DiffResult list = firstObject.diff(secondObject);
        assertEquals(0, list.getNumberOfDiffs());
    }

    @Test
    public void test_no_differences_inheritance() {
        final TypeTestChildClass firstObject = new TypeTestChildClass();
        final TypeTestChildClass secondObject = new TypeTestChildClass();

        final DiffResult list = firstObject.diff(secondObject);
        assertEquals(0, list.getNumberOfDiffs());
    }

    @Test
    public void test_difference_in_inherited_field() {
        final TypeTestChildClass firstObject = new TypeTestChildClass();
        firstObject.intField = 99;
        final TypeTestChildClass secondObject = new TypeTestChildClass();

        final DiffResult list = firstObject.diff(secondObject);
        assertEquals(1, list.getNumberOfDiffs());
    }

    @Test
    public void test_no_differences_excluded_field() {
        final TypeTestClass firstObject = new TypeTestClass();
        firstObject.excludedField = "b";
        final TypeTestClass secondObject = new TypeTestClass();

        final DiffResult list = firstObject.diff(secondObject);
        assertEquals(0, list.getNumberOfDiffs());
    }

    @Test
    public void test_no_differences_diff_exclude_annotated_field() {
        final TypeTestClass firstObject = new TypeTestClass();
        firstObject.annotatedField = "b";
        final TypeTestClass secondObject = new TypeTestClass();

        final DiffResult list = firstObject.diff(secondObject);
        assertEquals(0, list.getNumberOfDiffs());
    }

    @Test
    public void test_no_differences_diff_exluded_field_and_exclude_annotated_field() {
        final TypeTestClass firstObject = new TypeTestClass();
        firstObject.excludedField = "b";
        firstObject.annotatedField = "b";
        final TypeTestClass secondObject = new TypeTestClass();

        final DiffResult list = firstObject.diff(secondObject);
        assertEquals(0, list.getNumberOfDiffs());
    }

    @Test
    public void testGetExcludeFieldNamesWithNullExcludedFieldNames() {
        final ReflectionDiffBuilder<TypeTestClass> reflectionDiffBuilder = new ReflectionDiffBuilder<>(new TypeTestClass(), new TypeTestChildClass(), SHORT_STYLE);
        reflectionDiffBuilder.setExcludeFieldNames(null);
        final String[] excludeFieldNames = reflectionDiffBuilder.getExcludeFieldNames();
        assertNotNull(excludeFieldNames);
        assertEquals(0, excludeFieldNames.length);
    }

    @Test
    public void testGetExcludeFieldNamesWithNullValuesInExcludedFieldNames() {
        final ReflectionDiffBuilder<TypeTestClass> reflectionDiffBuilder = new ReflectionDiffBuilder<>(new TypeTestClass(), new TypeTestChildClass(), SHORT_STYLE);
        reflectionDiffBuilder.setExcludeFieldNames("charField", null);
        final String[] excludeFieldNames = reflectionDiffBuilder.getExcludeFieldNames();
        assertNotNull(excludeFieldNames);
        assertEquals(1, excludeFieldNames.length);
        assertEquals("charField", excludeFieldNames[0]);
    }
}
```