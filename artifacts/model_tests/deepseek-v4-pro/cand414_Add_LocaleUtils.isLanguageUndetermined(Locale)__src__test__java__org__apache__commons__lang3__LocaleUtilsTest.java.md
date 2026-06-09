# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `43d375178761672b62971309af25b72e980aec50`
- B: `d26170a97698da141d616942f2673874e043a13c`
- test: `src/test/java/org/apache/commons/lang3/LocaleUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/LocaleUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `26020`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6566, 'completion_tokens': 1150, 'total_tokens': 7716, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 838}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 6182}`

---

- 新增 `import static org.junit.jupiter.api.Assertions.assertNotEquals;` 以支持 `testIsLanguageUndetermined` 中的断言。
- 新增 `@Test void testIsLanguageUndetermined()` 方法，验证 `isLanguageUndetermined(Locale)` 的正确行为。

```java
import static org.junit.jupiter.api.Assertions.assertNotEquals;

@Test
public void testIsLanguageUndetermined() {
    final Set<Locale> set = LocaleUtils.availableLocaleSet();
    // Determined
    assertNotEquals(set.contains(LOCALE_EN), LocaleUtils.isLanguageUndetermined(LOCALE_EN));
    assertNotEquals(set.contains(LOCALE_EN_US), LocaleUtils.isLanguageUndetermined(LOCALE_EN_US));
    assertNotEquals(set.contains(LOCALE_FR), LocaleUtils.isLanguageUndetermined(LOCALE_FR));
    assertNotEquals(set.contains(LOCALE_FR_CA), LocaleUtils.isLanguageUndetermined(LOCALE_FR_CA));
    // Undetermined
    assertEquals(set.contains(LOCALE_EN_US_ZZZZ), LocaleUtils.isLanguageUndetermined(LOCALE_EN_US_ZZZZ));
    assertEquals(set.contains(LOCALE_QQ), LocaleUtils.isLanguageUndetermined(LOCALE_QQ));
    assertEquals(set.contains(LOCALE_QQ_ZZ), LocaleUtils.isLanguageUndetermined(LOCALE_QQ_ZZ));
    //
    assertTrue(LocaleUtils.isLanguageUndetermined(null));
}
```