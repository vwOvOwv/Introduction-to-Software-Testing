# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9bebec9cf9e6f4f1f0ae0673ab3fc672f87d18b1`
- B: `71f6746f81bb9650f6f228ea204d85ba2c5b7392`
- test: `src/test/java/org/apache/commons/lang3/CharSetTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/CharSet.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `22346`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5644, 'completion_tokens': 328, 'total_tokens': 5972, 'prompt_tokens_details': {'cached_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 130}}`

---

- 新增 `testJavadocExamples`，覆盖 `CharSet.getInstance` Javadoc 中关于 `^` 否定字符和字面量字符的示例行为。
- 不需要调整 import；旧测试中已有 `assertTrue` 和 `assertFalse` 的静态导入。

```java
@Test
public void testJavadocExamples() throws Exception {
    assertFalse(CharSet.getInstance("^a-c").contains('a'));
    assertTrue(CharSet.getInstance("^a-c").contains('d'));
    assertTrue(CharSet.getInstance("^^a-c").contains('a'));
    assertFalse(CharSet.getInstance("^^a-c").contains('^'));
    assertTrue(CharSet.getInstance("^a-cd-f").contains('d'));
    assertTrue(CharSet.getInstance("a-c^").contains('^'));
    assertTrue(CharSet.getInstance("^", "a-c").contains('^'));
}
```