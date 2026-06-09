# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e42dad3901e2fd6dcb0388bab79719cb0071187f`
- B: `8ea0c0284810bd6ec00f608be31abd20dbd4b72b`
- test: `src/test/java/org/apache/commons/lang3/LocaleUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/LocaleUtils.java']`
- old_test_mode: `methods`
- user_chars: `10314`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2924, 'completion_tokens': 786, 'total_tokens': 3710}`

---

- 修改 `testToLocale_1Part`：生产代码 `toLocale` 现在允许 2 或 3 位全小写语言码，因此删除 `"uuu"` 应抛异常的旧断言。
- 新增 `testThreeCharsLocale`：覆盖 LANG-915，验证 `"udm"`、`"tet"` 这类 3 位语言码可转换为 `Locale`。
- 需要新增 import：`testThreeCharsLocale` 使用 `Arrays.asList`，需添加 `java.util.Arrays`。

```java
import java.util.Arrays;

    @Test
    public void testToLocale_1Part() {
        assertNull(LocaleUtils.toLocale((String) null));
        
        assertValidToLocale("us");
        assertValidToLocale("fr");
        assertValidToLocale("de");
        assertValidToLocale("zh");
        // Valid format but lang doesnt exist, should make instance anyway
        assertValidToLocale("qq");
        // LANG-941: JDK 8 introduced the empty locale as one of the default locales
        assertValidToLocale("");

        try {
            LocaleUtils.toLocale("Us");
            fail("Should fail if not lowercase");
        } catch (final IllegalArgumentException iae) {}
        try {
            LocaleUtils.toLocale("US");
            fail("Should fail if not lowercase");
        } catch (final IllegalArgumentException iae) {}
        try {
            LocaleUtils.toLocale("uS");
            fail("Should fail if not lowercase");
        } catch (final IllegalArgumentException iae) {}
        try {
            LocaleUtils.toLocale("u#");
            fail("Should fail if not lowercase");
        } catch (final IllegalArgumentException iae) {}
        
        try {
            LocaleUtils.toLocale("u");
            fail("Must be 2 chars if less than 5");
        } catch (final IllegalArgumentException iae) {}

        try {
            LocaleUtils.toLocale("uu_U");
            fail("Must be 2 chars if less than 5");
        } catch (final IllegalArgumentException iae) {}
    }

    /**
     * Test for 3-chars locale, further details at LANG-915
     */
    @Test
    public void testThreeCharsLocale() {
        for (final String str : Arrays.asList("udm", "tet")) {
            final Locale locale = LocaleUtils.toLocale(str);
            assertNotNull(locale);
            assertEquals(str, locale.getLanguage());
            assertTrue(StringUtils.isBlank(locale.getCountry()));
            assertEquals(new Locale(str), locale);
        }
    }
```