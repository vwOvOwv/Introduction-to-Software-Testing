# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `119623760e52ef14cbbf16f57d3ffddc14e4a700`
- B: `f51299ced4fd40b44a3f6eca9ae528e818558205`
- test: `src/test/java/org/apache/commons/lang3/builder/ReflectionDiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/ReflectionDiffBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `13647`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3658, 'completion_tokens': 3875, 'total_tokens': 7533, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2243}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 3274}`

---

- 新增 import `import static org.junit.jupiter.api.Assertions.assertNotNull;`。
- 修改内部类 `TypeTestClass`：添加字段 `@DiffExclude private String annotatedField = "a";` 和 `private String excludedField = "a";`；在 `diff()` 方法调用中增加 `.setExcludeFieldNames("excludedField")`。
- 新增测试方法：`test_no_differences_excluded_field`、`test_no_differences_diff_exclude_annotated_field`、`test_no_differences_diff_exluded_field_and_exclude_annotated_field`、`testGetExcludeFieldNamesWithNullExcludedFieldNames`、`testGetExcludeFieldNamesWithNullValuesInExcludedFieldNames`。

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