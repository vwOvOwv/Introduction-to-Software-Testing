# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `49455b78bfc960de70acff552baeafbb705e80a7`
- B: `f8b1f6e7456a92b8aeb3e0aa8ef88936873dae00`
- test: `src/test/java/org/apache/commons/lang3/builder/DiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/DiffBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `24511`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6315, 'completion_tokens': 782, 'total_tokens': 7097, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 622}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 5931}`

---

- 新增 @Test 方法 `testDiffResult`，用于验证新增的 `DiffBuilder.append(String, DiffResult)` 方法能够正确附加子 `DiffResult` 中的差异项。

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