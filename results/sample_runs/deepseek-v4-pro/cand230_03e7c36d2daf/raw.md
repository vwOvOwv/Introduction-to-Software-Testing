# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `323a41a913c291f24ff4dd2c0c5a9660864a6717`
- B: `03e7c36d2dafca70e1f0e2c27a77ed4816cecf3f`
- test: `src/test/java/org/apache/commons/lang3/LocaleUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/LocaleUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `26064`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6676, 'completion_tokens': 1280, 'total_tokens': 7956, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 902}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 6292}`

---

- 新增测试方法 `testToLocaleGetIso3Country`，用于验证纯国家代码字符串（如 "US"）通过 `toLocale` 转换为 `Locale` 后能正确返回 ISO 3 位国家代码，对应生产代码 `parseLocale` 新增的纯国家代码处理逻辑。
- 新增测试方法 `testToLocaleGetIso3Language`，用于验证纯国家代码的 `Locale` 在默认英语区域设置下能返回正确的显示国家名，对应生产代码变更。
- 需要在测试文件头部新增 `import org.junitpioneer.jupiter.DefaultLocale;`，以支持 `@DefaultLocale` 注解。

```java
import org.junitpioneer.jupiter.DefaultLocale;

@Test
void testToLocaleGetIso3Country() {
    assertEquals("USA", LocaleUtils.toLocale("US").getISO3Country());
    assertEquals("GBR", LocaleUtils.toLocale("GB").getISO3Country());
    assertEquals("PAK", LocaleUtils.toLocale("PK").getISO3Country());
    assertEquals("IND", LocaleUtils.toLocale("IN").getISO3Country());
    assertEquals("FRA", LocaleUtils.toLocale("FR").getISO3Country());
}

@Test
@DefaultLocale(country = "US", language = "en")
void testToLocaleGetIso3Language() {
    assertEquals("United States", LocaleUtils.toLocale("US").getDisplayCountry());
    assertEquals("United Kingdom", LocaleUtils.toLocale("GB").getDisplayCountry());
    assertEquals("Pakistan", LocaleUtils.toLocale("PK").getDisplayCountry());
    assertEquals("India", LocaleUtils.toLocale("IN").getDisplayCountry());
    assertEquals("France", LocaleUtils.toLocale("FR").getDisplayCountry());
}
```