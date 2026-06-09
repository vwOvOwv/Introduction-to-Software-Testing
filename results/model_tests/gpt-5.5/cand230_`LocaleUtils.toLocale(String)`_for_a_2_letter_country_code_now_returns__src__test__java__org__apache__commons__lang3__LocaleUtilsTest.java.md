# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `323a41a913c291f24ff4dd2c0c5a9660864a6717`
- B: `03e7c36d2dafca70e1f0e2c27a77ed4816cecf3f`
- test: `src/test/java/org/apache/commons/lang3/LocaleUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/LocaleUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `26064`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6328, 'completion_tokens': 614, 'total_tokens': 6942}`

---

- 新增 `testToLocaleGetIso3Country`：覆盖生产代码新增的仅国家码字符串（如 `"US"`）可解析为 `new Locale("", country)` 的行为。
- 新增 `testToLocaleGetIso3Language`：覆盖仅国家码 Locale 在固定默认 Locale 下的显示国家名称，需使用 `@DefaultLocale` 固定测试环境。
- 需要调整 import：新增 `org.junitpioneer.jupiter.DefaultLocale` 导入以支持新增测试注解。

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