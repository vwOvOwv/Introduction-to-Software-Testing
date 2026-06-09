# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `a6443e146f825291308319c6a0f2eb82aa34f8c3`
- B: `4bd982d1a1df87724682c17c39bf27b5cbe389be`
- test: `src/test/java/org/apache/commons/lang3/LocaleUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/LocaleUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `28229`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6881, 'completion_tokens': 954, 'total_tokens': 7835, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 812}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 6497}`

---

- 新增 `testLanguageAndUNM49Numeric3AreaCodeLang1312` 测试方法，验证 `toLocale` 可解析三位数字区域代码（UN M.49）的格式，与生产代码中 `case 1` 新增条件保持一致。
- 无需调整现有测试方法或 import。

```java
@Test
public void testLanguageAndUNM49Numeric3AreaCodeLang1312() {
    assertValidToLocale("en_001", "en", "001");
    assertValidToLocale("en_150", "en", "150");
    assertValidToLocale("ar_001", "ar", "001");
}
```