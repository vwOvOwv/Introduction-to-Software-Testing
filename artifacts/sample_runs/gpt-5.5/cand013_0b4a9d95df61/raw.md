# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `b6d284b49de8460381a1752d25f4d4f387db28e2`
- B: `0b4a9d95df610bfcc83c375110ac100d08662ba1`
- test: `src/test/java/org/apache/commons/lang3/LocaleUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/LocaleUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `28189`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6915, 'completion_tokens': 219, 'total_tokens': 7134}`

---

- 新增 `testIllegalLanguageWithNumericCountry`：生产代码将两段 locale 中数字区域码校验收紧为必须同时满足合法 ISO 语言码，需覆盖非法语言加数字国家码应抛异常。
- 新增 `testIllegalSingleCharLanguageWithNumericCountry`：生产代码修复了单字符非法语言码搭配数字区域码被误接受的问题，需新增断言。
- import 无需调整：旧测试类已包含 `@Test` 和 `assertIllegalArgumentException` 所需 import。

```java
@Test
void testIllegalLanguageWithNumericCountry() {
    assertIllegalArgumentException(() -> LocaleUtils.toLocale("../../unexpected_001"));
}

@Test
void testIllegalSingleCharLanguageWithNumericCountry() {
    assertIllegalArgumentException(() -> LocaleUtils.toLocale("x_001"));
}
```