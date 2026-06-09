# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `d962b3c924f132b83d6db99ca126ac75a1469d90`
- B: `b11591895eed00e9f6e0bcb19178dedbaab4a971`
- test: `src/test/java/org/apache/commons/lang3/text/FormattableUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/FormattableUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `10605`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3388, 'completion_tokens': 245, 'total_tokens': 3633}`

---

- 新增 `testPercentLiteral`：覆盖生产代码改为 `formatter.format(SIMPLEST_FORMAT, buf.toString())` 后，包含单个 `%` 的文本应按字面量输出而不触发格式化异常。
- 新增 `testPercentLiteralX2`：覆盖同一变更下多个 `%` 字面量的输出行为。
- import 无需调整：现有 `assertEquals`、`Formatter` 和 `@Test` import 已满足新增测试。

```java
@Test
void testPercentLiteral() {
    assertEquals("100% done", FormattableUtils.append("100% done", new Formatter(), 0, -1, -1).toString());
}

@Test
void testPercentLiteralX2() {
    assertEquals("50% off 100% items", FormattableUtils.append("50% off 100% items", new Formatter(), 0, -1, -1).toString());
}
```