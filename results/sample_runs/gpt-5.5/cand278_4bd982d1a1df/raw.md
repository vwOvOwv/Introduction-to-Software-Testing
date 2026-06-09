# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `a6443e146f825291308319c6a0f2eb82aa34f8c3`
- B: `4bd982d1a1df87724682c17c39bf27b5cbe389be`
- test: `src/test/java/org/apache/commons/lang3/LocaleUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/LocaleUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `28229`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6643, 'completion_tokens': 195, 'total_tokens': 6838}`

---

- 新增 `testLanguageAndUNM49Numeric3AreaCodeLang1312`：对应 `LocaleUtils.toLocale` 现在允许语言加 3 位 UN M49 数字地区码（如 `en_001`）解析为 `Locale(language, numericCountry)`；无需调整 import。

```java
    @Test
    public void testLanguageAndUNM49Numeric3AreaCodeLang1312() {
        assertValidToLocale("en_001", "en", "001");
        assertValidToLocale("en_150", "en", "150");
        assertValidToLocale("ar_001", "ar", "001");
    }
```