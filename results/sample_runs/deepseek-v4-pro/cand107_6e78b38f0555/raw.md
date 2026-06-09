# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cdddb82e12ef7b2cc770125e930bde040b032213`
- B: `6e78b38f055516bfef2b7b1e2b83e96a7a67f2ec`
- test: `src/test/java/org/apache/commons/lang3/StringsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Strings.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `5643`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1803, 'completion_tokens': 1153, 'total_tokens': 2956, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 806}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1419}`

---

- 新增测试工厂方法 `stringsFactory`，提供 `Strings.CS` 和 `Strings.CI` 两个参数源。
- 新增参数化测试方法 `testEqualsStrings`，验证空安全字符串相等行为。
- 新增参数化测试方法 `testEqualsCharSequence`，验证空安全字符序列相等行为。
- 新增导入 `java.util.stream.Stream`、`org.junit.jupiter.params.ParameterizedTest`、`org.junit.jupiter.params.provider.MethodSource`。

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