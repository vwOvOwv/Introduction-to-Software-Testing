# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `cdddb82e12ef7b2cc770125e930bde040b032213`
- B: `6e78b38f055516bfef2b7b1e2b83e96a7a67f2ec`
- test: `src/test/java/org/apache/commons/lang3/StringsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Strings.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `5912`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1862, 'completion_tokens': 461, 'total_tokens': 2323, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 1606}`

---

- 新增 `import java.util.stream.Stream;`、`import org.junit.jupiter.params.ParameterizedTest;` 和 `import org.junit.jupiter.params.provider.MethodSource;`，以支持参数化测试。
- 新增 `public static Stream<Strings> stringsFactory()` 方法，提供 `Strings.CS` 和 `Strings.CI` 实例作为参数化测试的数据源。
- 新增 `@ParameterizedTest` 方法 `testEqualsStrings`，测试 `Strings.equals(String, String)` 方法对 null 参数的处理，对应生产代码中 `equals(String, String)` 方法改为 null-safe 的 `eq(s1, s2)`。
- 新增 `@ParameterizedTest` 方法 `testEqualsCharSequence`，测试 `Strings.equals(CharSequence, CharSequence)` 方法对 null 参数的处理，对应生产代码中 `equals(CharSequence, CharSequence)` 方法改为 null-safe 的 `eq(cs1, cs2)`。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.stream.Stream;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
// IMPORTS_END

    public static Stream<Strings> stringsFactory() {
        return Stream.of(Strings.CS, Strings.CI);
    }

    @ParameterizedTest
    @MethodSource("stringsFactory")
    public void testEqualsStrings(final Strings strings) {
        final String nullStr = null;
        assertTrue(strings.equals(nullStr, nullStr));
        assertFalse(strings.equals(nullStr, ""));
        assertFalse(strings.equals("", nullStr));
    }

    @ParameterizedTest
    @MethodSource("stringsFactory")
    public void testEqualsCharSequence(final Strings strings) {
        final CharSequence nullCharSequence = null;
        assertTrue(strings.equals(nullCharSequence, nullCharSequence));
        assertFalse(strings.equals(nullCharSequence, ""));
        assertFalse(strings.equals("", nullCharSequence));
    }
```