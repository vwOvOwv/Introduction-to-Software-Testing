# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `d962b3c924f132b83d6db99ca126ac75a1469d90`
- B: `b11591895eed00e9f6e0bcb19178dedbaab4a971`
- test: `src/test/java/org/apache/commons/lang3/text/FormattableUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/FormattableUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `10605`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3396, 'completion_tokens': 1450, 'total_tokens': 4846, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1290}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 3012}`

---

- 新增 `testPercentLiteral` 测试方法，验证含一个百分号的字符串能原样输出。
- 新增 `testPercentLiteralX2` 测试方法，验证含两个百分号的字符串能原样输出。
- 无需修改任何已有测试方法。
- 无需调整 import。

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