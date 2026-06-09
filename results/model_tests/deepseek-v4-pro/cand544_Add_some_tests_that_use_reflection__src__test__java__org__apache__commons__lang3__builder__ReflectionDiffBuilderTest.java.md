# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `daa63aa595ea39a69e1b44ac23bc50fdcf2afd62`
- B: `b62fc004d1a60757090ba9a177202eed0db57cc0`
- test: `src/test/java/org/apache/commons/lang3/builder/ReflectionDiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/ReflectionDiffBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `15742`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3975, 'completion_tokens': 4071, 'total_tokens': 8046, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 3068}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 3591}`

---

- 新增 `@Test` 方法 `testRetention`，用于验证构建过程不会导致内存泄漏。
- 在以下四个已有 `@Test` 方法末尾新增 `assertNotNull(reflectionDiffBuilder.build())` 断言：  
  `testGetExcludeFieldNamesWithNullExcludedFieldNames`、  
  `testGetExcludeFieldNamesWithNullExcludedFieldNamesCtor`、  
  `testGetExcludeFieldNamesWithNullValuesInExcludedFieldNames`、  
  `testGetExcludeFieldNamesWithNullValuesInExcludedFieldNamesCtor`。
- 新增 `import org.apache.commons.lang3.builder.TestClassBuilder` 以支持 `testRetention` 方法。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

import java.math.BigDecimal;
import java.math.BigInteger;

import org.apache.commons.lang3.AbstractLangTest;
import org.apache.commons.lang3.builder.TestClassBuilder;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    public void testGetExcludeFieldNamesWithNullExcludedFieldNames() {
        // @formatter:off
        final ReflectionDiffBuilder<TypeTestClass> reflectionDiffBuilder = ReflectionDiffBuilder.<TypeTestClass>builder()
                .setDiffBuilder(DiffBuilder.<TypeTestClass>builder()
                        .setLeft(new TypeTestClass())
                        .setRight(new TypeTestChildClass())
                        .setStyle(SHORT_STYLE)
                        .build())
                .build();
        // @formatter:on
        final String[] excludeFieldNames = reflectionDiffBuilder.getExcludeFieldNames();
        assertNotNull(excludeFieldNames);
        assertEquals(0, excludeFieldNames.length);
        assertNotNull(reflectionDiffBuilder.build());
    }

    @Test
    public void testGetExcludeFieldNamesWithNullExcludedFieldNamesCtor() {
        // @formatter:off
        final ReflectionDiffBuilder<TypeTestClass> reflectionDiffBuilder =
                new ReflectionDiffBuilder<>(new TypeTestClass(), new TypeTestChildClass(), SHORT_STYLE);
        // @formatter:on
        reflectionDiffBuilder.setExcludeFieldNames(null);
        final String[] excludeFieldNames = reflectionDiffBuilder.getExcludeFieldNames();
        assertNotNull(excludeFieldNames);
        assertEquals(0, excludeFieldNames.length);
        assertNotNull(reflectionDiffBuilder.build());
    }

    @Test
    public void testGetExcludeFieldNamesWithNullValuesInExcludedFieldNames() {
        // @formatter:off
        final ReflectionDiffBuilder<TypeTestClass> reflectionDiffBuilder = ReflectionDiffBuilder.<TypeTestClass>builder()
                .setDiffBuilder(DiffBuilder.<TypeTestClass>builder()
                        .setLeft(new TypeTestClass())
                        .setRight(new TypeTestChildClass())
                        .setStyle(SHORT_STYLE)
                        .build())
                .setExcludeFieldNames("charField", null)
                .build();
        // @formatter:on
        final String[] excludeFieldNames = reflectionDiffBuilder.getExcludeFieldNames();
        assertNotNull(excludeFieldNames);
        assertEquals(1, excludeFieldNames.length);
        assertEquals("charField", excludeFieldNames[0]);
        assertNotNull(reflectionDiffBuilder.build());
    }

    @Test
    public void testGetExcludeFieldNamesWithNullValuesInExcludedFieldNamesCtor() {
        // @formatter:off
        final ReflectionDiffBuilder<TypeTestClass> reflectionDiffBuilder =
                new ReflectionDiffBuilder<>(new TypeTestClass(), new TypeTestChildClass(), SHORT_STYLE);
        // @formatter:on
        reflectionDiffBuilder.setExcludeFieldNames("charField", null);
        final String[] excludeFieldNames = reflectionDiffBuilder.getExcludeFieldNames();
        assertNotNull(excludeFieldNames);
        assertEquals(1, excludeFieldNames.length);
        assertEquals("charField", excludeFieldNames[0]);
        assertNotNull(reflectionDiffBuilder.build());
    }

    @Test
    public void testRetention() throws Exception {
        // The following should not retain memory.
        for (int i = 0; i < Integer.getInteger("testRecursive", 10_000); i++) {
            final Class<?> clazz = TestClassBuilder.defineSimpleClass(getClass().getPackage().getName(), i);
            final Object firstObject = clazz.newInstance();
            final Object secondObject = clazz.newInstance();
            final ReflectionDiffBuilder<Object> reflectionDiffBuilder = new ReflectionDiffBuilder<>(firstObject, secondObject, SHORT_STYLE);
            assertNotNull(reflectionDiffBuilder.build());
        }
    }
```