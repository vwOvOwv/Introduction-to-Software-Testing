# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `323a41a913c291f24ff4dd2c0c5a9660864a6717`
- B: `03e7c36d2dafca70e1f0e2c27a77ed4816cecf3f`
- test: `src/test/java/org/apache/commons/lang3/LocaleUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/LocaleUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `26337`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6737, 'completion_tokens': 581, 'total_tokens': 7318, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 6481}`

---

- 新增 `testToLocaleGetIso3Country` 测试方法，验证 `LocaleUtils.toLocale("US")` 等返回的 ISO3 国家代码。
- 新增 `testToLocaleGetIso3Language` 测试方法，使用 `@DefaultLocale` 注解设置默认区域，验证 `LocaleUtils.toLocale("US")` 等返回的显示国家名称。
- 新增 import `org.junitpioneer.jupiter.DefaultLocale`，以支持 `@DefaultLocale` 注解。

```java
// IMPORTS_START
import static org.apache.commons.lang3.JavaVersion.JAVA_1_4;
import static org.apache.commons.lang3.LangAssertions.assertIllegalArgumentException;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.util.Arrays;
import java.util.Collection;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.junitpioneer.jupiter.DefaultLocale;
// IMPORTS_END

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