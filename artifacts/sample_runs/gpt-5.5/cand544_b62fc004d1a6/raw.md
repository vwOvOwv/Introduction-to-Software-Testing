# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `daa63aa595ea39a69e1b44ac23bc50fdcf2afd62`
- B: `b62fc004d1a60757090ba9a177202eed0db57cc0`
- test: `src/test/java/org/apache/commons/lang3/builder/ReflectionDiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/ReflectionDiffBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `15742`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3873, 'completion_tokens': 1227, 'total_tokens': 5100}`

---

- 修改 `testGetExcludeFieldNamesWithNullExcludedFieldNames`：生产侧 `build()` 仍应在未设置排除字段时返回非空结果，测试补充 `assertNotNull(reflectionDiffBuilder.build())`。
- 修改 `testGetExcludeFieldNamesWithNullExcludedFieldNamesCtor`：覆盖废弃构造器路径下 `build()` 的非空返回。
- 修改 `testGetExcludeFieldNamesWithNullValuesInExcludedFieldNames`：覆盖排除字段数组含 `null` 时 `build()` 的非空返回。
- 修改 `testGetExcludeFieldNamesWithNullValuesInExcludedFieldNamesCtor`：覆盖废弃构造器路径下排除字段数组含 `null` 时 `build()` 的非空返回。
- 新增 `testRetention`：对动态生成类反复构建 `ReflectionDiffBuilder` 并断言 `build()` 非空，以对应回归覆盖。
- 需要调整 import：新增 `org.apache.commons.lang3.TestClassBuilder`。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

import java.math.BigDecimal;
import java.math.BigInteger;

import org.apache.commons.lang3.AbstractLangTest;
import org.apache.commons.lang3.TestClassBuilder;
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