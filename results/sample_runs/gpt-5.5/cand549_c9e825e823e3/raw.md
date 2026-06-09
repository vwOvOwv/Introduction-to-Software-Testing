# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `b5de0ef28017583a451dbec86928f7682b2f8a94`
- B: `c9e825e823e30c5b1e3ddc9de5e8fd0094d52ee5`
- test: `src/test/java/org/apache/commons/lang3/LocaleUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/LocaleUtils.java']`
- old_test_mode: `methods`
- user_chars: `6440`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1954, 'completion_tokens': 927, 'total_tokens': 2881}`

---

- 新增 `testToLocale_Locale_defaults`：覆盖新增的 `LocaleUtils.toLocale(Locale)` 对 `null` 和默认 Locale 的行为。
- 新增 `testToLocales`：使用所有可用 Locale 验证 `toLocale(Locale)` 返回入参本身。
- 修改 `testToLocale_1Part`：将 `LocaleUtils.toLocale(null)` 改为 `LocaleUtils.toLocale((String) null)`，避免新增重载后调用歧义。
- 修改 `testParseAllLocales`：仅同步参数命名为 `actualLocale`，断言逻辑保持不变。
- import 无需调整：`Locale`、`@Test`、`@ParameterizedTest`、`@MethodSource` 等已被现有测试使用。

```java
    /**
     * Test toLocale(Locale) method.
     */
    @Test
    public void testToLocale_Locale_defaults() {
        assertNull(LocaleUtils.toLocale((String) null));
        assertEquals(Locale.getDefault(), LocaleUtils.toLocale((Locale) null));
        assertEquals(Locale.getDefault(), LocaleUtils.toLocale(Locale.getDefault()));
    }

    /**
     * Test toLocale(Locale) method.
     */
    @ParameterizedTest
    @MethodSource("java.util.Locale#getAvailableLocales")
    public void testToLocales(final Locale actualLocale) {
        assertEquals(actualLocale, LocaleUtils.toLocale(actualLocale));
    }

    /**
     * Test toLocale(String) method.
     */
    @Test
    public void testToLocale_1Part() {
        assertNull(LocaleUtils.toLocale((String) null));

        assertValidToLocale("us");
        assertValidToLocale("fr");
        assertValidToLocale("de");
        assertValidToLocale("zh");
        // Valid format but lang doesn't exist, should make instance anyway
        assertValidToLocale("qq");
        // LANG-941: JDK 8 introduced the empty locale as one of the default locales
        assertValidToLocale("");

        assertThrows(IllegalArgumentException.class, () -> LocaleUtils.toLocale("Us"), "Should fail if not lowercase");
        assertThrows(IllegalArgumentException.class, () -> LocaleUtils.toLocale("uS"), "Should fail if not lowercase");
        assertThrows(IllegalArgumentException.class, () -> LocaleUtils.toLocale("u#"), "Should fail if not lowercase");
        assertThrows(
                IllegalArgumentException.class, () -> LocaleUtils.toLocale("u"), "Must be 2 chars if less than 5");
        assertThrows(
                IllegalArgumentException.class, () -> LocaleUtils.toLocale("uu_U"), "Must be 2 chars if less than 5");
    }

    @ParameterizedTest
    @MethodSource("java.util.Locale#getAvailableLocales")
    public void testParseAllLocales(final Locale actualLocale) {
        // Check if it's possible to recreate the Locale using just the standard constructor
        final Locale locale = new Locale(actualLocale.getLanguage(), actualLocale.getCountry(), actualLocale.getVariant());
        if (actualLocale.equals(locale)) { // it is possible for LocaleUtils.toLocale to handle these Locales
            final String str = actualLocale.toString();
            // Look for the script/extension suffix
            int suff = str.indexOf("_#");
            if (suff == - 1) {
                suff = str.indexOf("#");
            }
            String localeStr = str;
            if (suff >= 0) { // we have a suffix
                assertThrows(IllegalArgumentException.class, () -> LocaleUtils.toLocale(str));
                // try without suffix
                localeStr = str.substring(0, suff);
            }
            final Locale loc = LocaleUtils.toLocale(localeStr);
            assertEquals(actualLocale, loc);
        }
    }
```