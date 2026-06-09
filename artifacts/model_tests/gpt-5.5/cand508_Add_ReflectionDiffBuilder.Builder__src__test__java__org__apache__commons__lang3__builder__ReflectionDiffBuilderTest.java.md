# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `aa4eef85cfd88e55677df238b44c6cc463d0af91`
- B: `4949adec480ddccdee4f7d09231e85e84fec00a1`
- test: `src/test/java/org/apache/commons/lang3/builder/ReflectionDiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/ReflectionDiffBuilder.java']`
- old_test_mode: `methods`
- user_chars: `20308`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5148, 'completion_tokens': 902, 'total_tokens': 6050}`

---

- 修改 `testGetExcludeFieldNamesWithNullExcludedFieldNames`：改用新的 `ReflectionDiffBuilder.builder()` 与 `DiffBuilder.builder()` 配置路径，覆盖 Builder 默认 `excludeFieldNames` 为非 null 空数组的行为。
- 新增 `testGetExcludeFieldNamesWithNullExcludedFieldNamesCtor`：保留已废弃构造器加 `setExcludeFieldNames(null)` 的兼容性断言。
- 修改 `testGetExcludeFieldNamesWithNullValuesInExcludedFieldNames`：改用新 Builder API 的 `setExcludeFieldNames("charField", null)`，验证 null 被过滤且字段名排序/保留正确。
- 新增 `testGetExcludeFieldNamesWithNullValuesInExcludedFieldNamesCtor`：保留已废弃构造器加 `setExcludeFieldNames("charField", null)` 的兼容性断言。
- 不需要调整 import：`DiffBuilder` 与测试类位于同一 package，JUnit 断言 import 不变。

```java
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
    }
```