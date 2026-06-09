# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `0745c26dac9ac76086f10c302d252a71bf4a68c5`
- B: `3df7f4440e7447bc55e95400ec511323e708c652`
- test: `src/test/java/org/apache/commons/lang3/LocaleUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/LocaleUtils.java']`
- old_test_mode: `methods`
- user_chars: `8916`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2543, 'completion_tokens': 721, 'total_tokens': 3264}`

---

- 新增 `testLang1823`：覆盖生产代码现在允许带 `#` 的 locale variant（如 `th_TH_#Thai`）解析。
- 修改 `testParseAllLocales`：生产代码不再对包含 `#` 的 locale 字符串统一抛出异常，而是支持可由标准构造器重建的特殊/扩展 locale。
- 新增 `testSpecialCases`：覆盖 `th_TH_TH_#u-nu-thai` 与 `ja_JP_JP_#u-ca-japanese` 等 `Locale` 构造器特殊案例。
- import 无需调整。

```java
    /**
     * Tests #LANG-1823
     */
    @Test
    void testLang1823() {
        assertValidToLocale("th_TH_#Thai", "th", "TH", "#Thai");
    }

    @ParameterizedTest
    @MethodSource("java.util.Locale#getAvailableLocales")
    void testParseAllLocales(final Locale actualLocale) {
        // Check if it's possible to recreate the Locale using just the standard constructor
        final Locale locale = new Locale(actualLocale.getLanguage(), actualLocale.getCountry(), actualLocale.getVariant());
        if (actualLocale.equals(locale)) { // it is possible for LocaleUtils.toLocale to handle these Locales
            assertEquals(actualLocale, LocaleUtils.toLocale(actualLocale.toString()));
            final String str = actualLocale.toString();
            // Look for the script/extension suffix
            int suff = str.indexOf("_#");
            if (suff == -1) {
                suff = str.indexOf("#");
            }
            String localeStr = str;
            if (suff >= 0) { // we have a suffix
                localeStr = str.substring(0, suff);
            }
            assertEquals(actualLocale, LocaleUtils.toLocale(localeStr));
        }
    }

    /**
     * Special cases from https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Locale.html#special_cases_constructor
     */
    @Test
    void testSpecialCases() {
        assertValidToLocale("th_TH_TH", "th", "TH", "TH");
        assertValidToLocale("ja_JP_JP", "ja", "JP", "JP");
        // "th_TH_TH_#u-nu-thai" and friends
        LocaleUtils.localeLookupList(new Locale("th", "TH", "TH")).forEach(locale -> assertEquals(locale, LocaleUtils.toLocale(locale.toString())));
        // "ja_JP_JP_#u-ca-japanese" and friends
        LocaleUtils.localeLookupList(new Locale("ja", "JP", "JP")).forEach(locale -> assertEquals(locale, LocaleUtils.toLocale(locale.toString())));
    }
```