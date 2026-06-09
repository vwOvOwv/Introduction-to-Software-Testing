# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `a93703d002bc4850e7adcdfc9b51664fca7b8836`
- B: `be370cd0ef134bb44fde733e4ee91661a012dae5`
- test: `src/test/java/org/apache/commons/lang3/text/ExtendedMessageFormatTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/ExtendedMessageFormat.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `24360`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5781, 'completion_tokens': 304, 'total_tokens': 6085}`

---

- 新增 `testEmbeddedPatternInChoice`：对应 `insertFormats` 现在在嵌套 choice pattern 中不再查找自定义格式，需覆盖 LANG-917 的嵌入 `{1,number}` 场景。
- import 无需调整：新增测试仅使用已有的 `@Test`、`assertEquals`、`ExtendedMessageFormat` 和 `registry`。

```java
/**
 * Test Bug LANG-917 - IndexOutOfBoundsException and/or infinite loop when using a choice pattern
 */
@Test
public void testEmbeddedPatternInChoice() {
    final String pattern = "Hi {0,lower}, got {1,choice,0#none|1#one|1<{1,number}}, {2,upper}!";
    final ExtendedMessageFormat emf = new ExtendedMessageFormat(pattern, registry);
    assertEquals("Hi there, got 3, GREAT!", emf.format(new Object[] {"there", 3, "great"}));
}
```