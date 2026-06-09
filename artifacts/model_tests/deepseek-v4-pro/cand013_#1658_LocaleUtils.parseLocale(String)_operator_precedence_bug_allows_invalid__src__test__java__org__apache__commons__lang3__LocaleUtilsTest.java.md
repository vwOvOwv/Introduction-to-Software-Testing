# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `b6d284b49de8460381a1752d25f4d4f387db28e2`
- B: `0b4a9d95df610bfcc83c375110ac100d08662ba1`
- test: `src/test/java/org/apache/commons/lang3/LocaleUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/LocaleUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `28189`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7264, 'completion_tokens': 2587, 'total_tokens': 9851, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2432}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 6880}`

---

- 新增 `testIllegalLanguageWithNumericCountry` 测试方法，验证非法语言搭配数字国家码时抛出异常。
- 新增 `testIllegalSingleCharLanguageWithNumericCountry` 测试方法，验证单字符语言搭配数字国家码时抛出异常。  
  两者均对应生产代码修复优先级导致需要语言码校验通过后才接受数字区域码。无需调整 import。

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