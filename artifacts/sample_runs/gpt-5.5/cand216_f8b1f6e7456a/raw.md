# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `49455b78bfc960de70acff552baeafbb705e80a7`
- B: `f8b1f6e7456a92b8aeb3e0aa8ef88936873dae00`
- test: `src/test/java/org/apache/commons/lang3/builder/DiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/DiffBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `24511`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6279, 'completion_tokens': 256, 'total_tokens': 6535}`

---

- 新增 `testDiffResult`：覆盖生产代码新增的 `DiffBuilder.append(String, DiffResult)`，断言嵌套 `DiffResult` 的字段名前缀会拼接为 `prop1.int`。
- import 无需调整：新增测试仅使用当前测试类已有的 `@Test`、`assertEquals` 及同包类型。

```java
    @Test
    public void testDiffResult() {
        final TypeTestClass class1 = new TypeTestClass();
        final TypeTestClass class2 = new TypeTestClass();
        class2.intField = 2;

        final DiffResult list = new DiffBuilder(class1, class2, SHORT_STYLE)
            .append("prop1", class1.diff(class2))
            .build();
        assertEquals(1, list.getNumberOfDiffs());
        assertEquals("prop1.int", list.getDiffs().get(0).getFieldName());
    }
```