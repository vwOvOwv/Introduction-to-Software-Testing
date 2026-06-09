# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cdddb82e12ef7b2cc770125e930bde040b032213`
- B: `6e78b38f055516bfef2b7b1e2b83e96a7a67f2ec`
- test: `src/test/java/org/apache/commons/lang3/StringsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Strings.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `5643`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1793, 'completion_tokens': 472, 'total_tokens': 2265}`

---

- 新增 `testEqualsStrings` 参数化测试，以覆盖 `Strings.CS` / `Strings.CI` 的 `equals(String, String)` 对 `null` 的新安全处理。
- 新增 `testEqualsCharSequence` 参数化测试，以覆盖 `equals(CharSequence, CharSequence)` 的空值等价行为。
- 新增 `stringsFactory` 方法作为 `@MethodSource` 数据源。
- 需要调整 import：新增 `java.util.stream.Stream`、`org.junit.jupiter.params.ParameterizedTest` 和 `org.junit.jupiter.params.provider.MethodSource`。

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