# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ba6cf8e2390f18db484da766db19285255ac3e82`
- B: `8089a0c2d3207ed26531f877352336baf1c6c5bb`
- test: `src/test/java/org/apache/commons/lang3/math/NumberUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/math/NumberUtils.java']`
- old_test_mode: `methods`
- user_chars: `14683`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 4466, 'completion_tokens': 2272, 'total_tokens': 6738}`

---

- 新增 `testIsParsableDoubleTrue`、`testIsParsableFalse`、`testIsParsableFloatTrue`、`testIsParsableNull`、`testIsParsableTrue`，以覆盖 `isParsable` 现在委托 `Double/Float/Long` 解析后支持的科学计数法、类型后缀和十六进制浮点等行为。
- 删除旧的 `testIsParsable`，因为其中对 `isParsable` 的旧语义断言已被拆分为参数化测试。
- 修改 `testLang1729IsParsableDouble`，将 `"1.f"` 和 `"1.d"` 从 TODO 改为应返回 `true` 的断言。
- 修改 `testLang1729IsParsableFloat`，将 `"1.f"` 和 `"1.d"` 从 TODO 改为应返回 `true` 的断言。
- 需要新增 `ParameterizedTest` 和 `ValueSource` 的 import，以支持新增的参数化测试。

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

// DELETE_TESTS_START
testIsParsable
// DELETE_TESTS_END

@ParameterizedTest
// @formatter:off
@ValueSource(strings = {
        // Decimal floating-point literals (no suffix or 'd'/'D' suffix)
        "3.14",
        "3.14d",
        "3.14D",
        ".5",
        ".5d",
        "5.",
        "5.d",
        "5d",
        "0.0",
        "0.0d",
        // Exponential (scientific) notation
        "1.23e10",
        "1.23e10d",
        "1.23E10",
        "1.23e-10",
        "1.23e-10d",
        "1e5",
        "1e5d",
        ".5e3",
        ".5e3d",
        // Hexadecimal floating-point literals
        "0x1.8p3",
        "0x1.8p3d",
        "0x.8p0",
        "0x1p-3",
        "0x1.fffffffffffffp1023",
        "0x1.fffffffffffffp1023d",
        // With leading zeros
        "01.5",
        "01.5d" })
// @formatter:on
void testIsParsableDoubleTrue(final String input) {
    Double.parseDouble(input);
    assertTrue(NumberUtils.isParsable(input));
}

@ParameterizedTest
@ValueSource(strings = { "", "0xC1AB", "65CBA2", "pendro", "64, 2", "64.2.2", "64..", "64L", "-", "--2",
        // Invalid scientific notation.
        "e5", "1e", "1e+", "1e-", "1ee5", "1e5e5",
        // Invalid type suffixes.
        "f", "d", "-f", "-d", })
void testIsParsableFalse(final String input) {
    assertFalse(NumberUtils.isParsable(input));
}

@ParameterizedTest
// @formatter:off
@ValueSource(strings = {
        // Decimal floating-point literals
        "3.14f",
        "3.14F",
        ".5f",
        "5.f",
        "5f",
        "0.0f",
        // Exponential (scientific) notation
        "1.23e10f",
        "1.23E10f",
        "1.23e-10f",
        "1e5f",
        ".5e3f",
        // Hexadecimal floating-point literals
        "0x1.8p3f",
        "0x.8p0f",
        "0x1p-3f",
        "0x1.fffffep127f",
        // With leading zeros
        "01.5f"})
// @formatter:on
void testIsParsableFloatTrue(final String input) {
    Float.parseFloat(input);
    assertTrue(NumberUtils.isParsable(input));
}

@Test
void testIsParsableNull() {
    // Can't use null in @ValueSource(strings)
    assertFalse(NumberUtils.isParsable(null));
}

@ParameterizedTest
// @formatter:off
@ValueSource(strings = {
        "64.",
        "-64.",
        "64.2",
        "64",
        "018",
        ".18",
        "-65",
        "-018",
        "-018.2",
        "-.236",
        "2.",
        "2.f",
        "2.d",
        "1.2e-5f",
        "1.2e-5d",
        // Additional tests for scientific notation.
        "1e5", "1E5", "1.2e5", "1.2E5", "1.2e+5", "1.2e-5", "-1.2e-5", "1e5f", "1e5F", "1e5d", "1e5D",
        // Additional tests for type suffixes.
        "2f", "2F", "2d", "2D", "2.0f", "2.0F", "2.0d", "2.0D", "-2.0f", "-2.0d" })
// @formatter:on
void testIsParsableTrue(final String input) {
    assertTrue(NumberUtils.isParsable(input));
}

@Test
void testLang1729IsParsableDouble() {
    assertTrue(isParsableDouble("1"));
    assertTrue(isParsableDouble("1."));
    assertTrue(isParsableDouble("1.f"));
    assertTrue(isParsableDouble("1.d"));
    assertTrue(isParsableDouble("1.0"));
    assertFalse(isParsableDouble("1.0."));
    assertFalse(isParsableDouble("1 2 3"));
    assertFalse(isParsableDouble("１ ２ ３"));
}

@Test
void testLang1729IsParsableFloat() {
    assertTrue(isParsableFloat("1"));
    assertTrue(isParsableFloat("1."));
    assertTrue(isParsableFloat("1.f"));
    assertTrue(isParsableFloat("1.d"));
    assertTrue(isParsableFloat("1.0"));
    assertFalse(isParsableFloat("1.0."));
    assertFalse(isParsableFloat("1 2 3"));
    assertFalse(isParsableFloat("１ ２ ３"));
}
```