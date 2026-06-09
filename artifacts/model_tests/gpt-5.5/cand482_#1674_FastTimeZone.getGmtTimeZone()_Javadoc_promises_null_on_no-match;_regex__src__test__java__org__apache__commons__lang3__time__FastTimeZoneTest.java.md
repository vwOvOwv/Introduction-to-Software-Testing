# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `5a62dd00b16179fcba4566728c8b39d8461af4fa`
- B: `2c0b8483606efbfbaccf600e3bc31fe10533e004`
- test: `src/test/java/org/apache/commons/lang3/time/FastTimeZoneTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/FastTimeZone.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `12956`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3906, 'completion_tokens': 827, 'total_tokens': 4733}`

---

- 新增 `testEmptyStringReturnsNonNullDespiteJavadoc`，覆盖生产代码文档说明的 lenient regex 行为：空字符串匹配并返回 GMT 而非 `null`。
- 新增 `testGmtOnlyReturnsNonNull`，覆盖 `"GMT"` 单独输入时小时/分钟缺失但仍默认 0 偏移的行为。
- 新增 `testInvalidStringReturnsNull`，覆盖真正不匹配 regex 的输入仍返回 `null`。
- 新增 `testJavadocReflectsLenientBehavior`，对照生产 diff 中 Javadoc 新增说明，断言源码包含更新后的描述。
- 新增 `testPlusOnlyReturnsNonNull`，覆盖 `"+"` 这种 sign-only 输入匹配并返回 GMT 的行为。
- 需要调整 import：新增 `assertNotNull`、`assertNull`、`assertTrue` 以及 `StandardCharsets`、`Files`、`Path`、`Paths`、`TimeZone`。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.TimeZone;

import org.apache.commons.lang3.AbstractLangTest;
import org.junit.jupiter.api.Test;
// IMPORTS_END

@Test
void testEmptyStringReturnsNonNullDespiteJavadoc() {
    // Javadoc claims null when pattern does not match. Empty string matches
    // the over-permissive regex and returns the GMT zone instead.
    final TimeZone tz = FastTimeZone.getGmtTimeZone("");
    assertNotNull(tz);
    assertEquals(0, tz.getRawOffset());
}

@Test
void testGmtOnlyReturnsNonNull() {
    // The literal "GMT" prefix on its own matches; both digit groups absent.
    final TimeZone tz = FastTimeZone.getGmtTimeZone("GMT");
    assertNotNull(tz);
    assertEquals(0, tz.getRawOffset());
}

@Test
void testInvalidStringReturnsNull() {
    // Negative control: a string that genuinely cannot match the regex returns null.
    assertNull(FastTimeZone.getGmtTimeZone("XYZ"), "non-matching input returns null");
}

/**
 * Patched-source check. After the doc-only patch lands, the Javadoc on {@code getGmtTimeZone(String)} no longer promises "null if pattern does not match"
 * for the empty / sign-only / GMT-only inputs. We string-search the source file for the corrected wording so reverting the Javadoc (mutation control) flips
 * this assertion to FAIL.
 */
@Test
void testJavadocReflectsLenientBehavior() throws Exception {
    final Path src = Paths.get("src/main/java/org/apache/commons/lang3/time/FastTimeZone.java");
    final String body = new String(Files.readAllBytes(src), StandardCharsets.UTF_8);
    assertTrue(body.contains("defaulting to GMT for an unrecognized but parseable input"));
}

@Test
void testPlusOnlyReturnsNonNull() {
    // Sign-only input still matches the regex; hours and minutes default to 0.
    final TimeZone tz = FastTimeZone.getGmtTimeZone("+");
    assertNotNull(tz);
    assertEquals(0, tz.getRawOffset());
}
```