# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `08aa21f9217df0a28d48be5be5db03ddf4867140`
- B: `b31877a46009d5ee52af9b5f737dabe241689931`
- test: `src/test/java/org/apache/commons/lang3/math/NumberUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/math/NumberUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `96504`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 26062, 'completion_tokens': 2990, 'total_tokens': 29052}`

---

- 新增 `testToScaledBigDecimalBigDecimal`，覆盖新增的 `NumberUtils.toScaledBigDecimal(BigDecimal)` 默认 scale=2 与 `HALF_EVEN` 行为及 null 返回 `BigDecimal.ZERO`。
- 新增 `testToScaledBigDecimalBigDecimalIRM`，覆盖新增的 `NumberUtils.toScaledBigDecimal(BigDecimal, int, RoundingMode)` 自定义 scale/roundingMode 与 null 行为。
- 新增 `testToScaledBigDecimalFloat`，覆盖新增的 `NumberUtils.toScaledBigDecimal(Float)` 默认缩放、浮点舍入差异及 null 行为。
- 新增 `testToScaledBigDecimalFloatIRM`，覆盖新增的 `NumberUtils.toScaledBigDecimal(Float, int, RoundingMode)` 自定义缩放、舍入及 null 行为。
- 新增 `testToScaledBigDecimalDouble`，覆盖新增的 `NumberUtils.toScaledBigDecimal(Double)` 默认缩放、`HALF_EVEN` 舍入及 null 行为。
- 新增 `testToScaledBigDecimalDoubleIRM`，覆盖新增的 `NumberUtils.toScaledBigDecimal(Double, int, RoundingMode)` 自定义缩放、舍入及 null 行为。
- 新增 `testToScaledBigDecimalString`，覆盖新增的 `NumberUtils.toScaledBigDecimal(String)` 默认缩放、`HALF_EVEN` 舍入及 null 行为。
- 新增 `testToScaledBigDecimalStringIRM`，覆盖新增的 `NumberUtils.toScaledBigDecimal(String, int, RoundingMode)` 自定义缩放、舍入及 null 行为。
- 需要调整 import：新增 `java.math.RoundingMode` 以编译新增测试方法中对 `RoundingMode` 的引用。

```java
// IMPORTS_START
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.RoundingMode;

import org.junit.Test;
// IMPORTS_END

/**
 * Test for {@link NumberUtils#toScaledBigDecimal(BigDecimal)}.
 */
@Test
public void testToScaledBigDecimalBigDecimal() {
    assertTrue("toScaledBigDecimal(BigDecimal) 1 failed",
        NumberUtils.toScaledBigDecimal(BigDecimal.valueOf(123.456)).equals(BigDecimal.valueOf(123.46)));
    // Test RoudingMode.HALF_EVEN default rounding.
    assertTrue("toScaledBigDecimal(BigDecimal) 2 failed",
        NumberUtils.toScaledBigDecimal(BigDecimal.valueOf(23.515)).equals(BigDecimal.valueOf(23.52)));
    assertTrue("toScaledBigDecimal(BigDecimal) 3 failed",
        NumberUtils.toScaledBigDecimal(BigDecimal.valueOf(23.525)).equals(BigDecimal.valueOf(23.52)));
    assertTrue("toScaledBigDecimal(BigDecimal) 4 failed",
        NumberUtils.toScaledBigDecimal(BigDecimal.valueOf(23.525))
            .multiply(BigDecimal.valueOf(100)).toString()
            .equals("2352.00"));
    assertTrue("toScaledBigDecimal(BigDecimal) 5 failed",
        NumberUtils.toScaledBigDecimal((BigDecimal) null).equals(BigDecimal.ZERO));
}

/**
 * Test for {@link NumberUtils#toScaledBigDecimal(BigDecimal, int, RoundingMode)}.
 */
@Test
public void testToScaledBigDecimalBigDecimalIRM() {
    assertTrue("toScaledBigDecimal(BigDecimal, int, RoudingMode) 1 failed",
        NumberUtils.toScaledBigDecimal(BigDecimal.valueOf(123.456), 1, RoundingMode.CEILING).equals(BigDecimal.valueOf(123.5)));
    assertTrue("toScaledBigDecimal(BigDecimal, int, RoudingMode) 2 failed",
        NumberUtils.toScaledBigDecimal(BigDecimal.valueOf(23.5159), 3, RoundingMode.FLOOR).equals(BigDecimal.valueOf(23.515)));
    assertTrue("toScaledBigDecimal(BigDecimal, int, RoudingMode) 3 failed",
        NumberUtils.toScaledBigDecimal(BigDecimal.valueOf(23.525), 2, RoundingMode.HALF_UP).equals(BigDecimal.valueOf(23.53)));
    assertTrue("toScaledBigDecimal(BigDecimal, int, RoudingMode) 4 failed",
        NumberUtils.toScaledBigDecimal(BigDecimal.valueOf(23.521), 4, RoundingMode.HALF_EVEN)
            .multiply(BigDecimal.valueOf(1000))
            .toString()
            .equals("23521.0000"));
    assertTrue("toScaledBigDecimal(BigDecimal, int, RoudingMode) 5 failed",
        NumberUtils.toScaledBigDecimal((BigDecimal) null, 2, RoundingMode.HALF_UP).equals(BigDecimal.ZERO));
}

/**
 * Test for {@link NumberUtils#toScaledBigDecimal(Float)}.
 */
@Test
public void testToScaledBigDecimalFloat() {
    assertTrue("toScaledBigDecimal(Float) 1 failed",
        NumberUtils.toScaledBigDecimal(Float.valueOf(123.456f)).equals(BigDecimal.valueOf(123.46)));
    // Test RoudingMode.HALF_EVEN default rounding.
    assertTrue("toScaledBigDecimal(Float) 2 failed",
        NumberUtils.toScaledBigDecimal(Float.valueOf(23.515f)).equals(BigDecimal.valueOf(23.51)));
    // Note. NumberUtils.toScaledBigDecimal(Float.valueOf(23.515f)).equals(BigDecimal.valueOf(23.51))
    // because of roundoff error. It is ok.
    assertTrue("toScaledBigDecimal(Float) 3 failed",
        NumberUtils.toScaledBigDecimal(Float.valueOf(23.525f)).equals(BigDecimal.valueOf(23.52)));
    assertTrue("toScaledBigDecimal(Float) 4 failed",
        NumberUtils.toScaledBigDecimal(Float.valueOf(23.525f))
            .multiply(BigDecimal.valueOf(100)).toString()
            .equals("2352.00"));
    assertTrue("toScaledBigDecimal(Float) 5 failed",
        NumberUtils.toScaledBigDecimal((Float) null).equals(BigDecimal.ZERO));
}

/**
 * Test for {@link NumberUtils#toScaledBigDecimal(Float, int, RoundingMode)}.
 */
@Test
public void testToScaledBigDecimalFloatIRM() {
    assertTrue("toScaledBigDecimal(Float, int, RoudingMode) 1 failed",
        NumberUtils.toScaledBigDecimal(Float.valueOf(123.456f), 1, RoundingMode.CEILING).equals(BigDecimal.valueOf(123.5)));
    assertTrue("toScaledBigDecimal(Float, int, RoudingMode) 2 failed",
        NumberUtils.toScaledBigDecimal(Float.valueOf(23.5159f), 3, RoundingMode.FLOOR).equals(BigDecimal.valueOf(23.515)));
    // The following happens due to roundoff error. We're ok with this.
    assertTrue("toScaledBigDecimal(Float, int, RoudingMode) 3 failed",
        NumberUtils.toScaledBigDecimal(Float.valueOf(23.525f), 2, RoundingMode.HALF_UP).equals(BigDecimal.valueOf(23.52)));
    assertTrue("toScaledBigDecimal(Float, int, RoudingMode) 4 failed",
        NumberUtils.toScaledBigDecimal(Float.valueOf(23.521f), 4, RoundingMode.HALF_EVEN)
            .multiply(BigDecimal.valueOf(1000))
            .toString()
            .equals("23521.0000"));
    assertTrue("toScaledBigDecimal(Float, int, RoudingMode) 5 failed",
        NumberUtils.toScaledBigDecimal((Float) null, 2, RoundingMode.HALF_UP).equals(BigDecimal.ZERO));
}

/**
 * Test for {@link NumberUtils#toScaledBigDecimal(Double)}.
 */
@Test
public void testToScaledBigDecimalDouble() {
    assertTrue("toScaledBigDecimal(Double) 1 failed",
        NumberUtils.toScaledBigDecimal(Double.valueOf(123.456d)).equals(BigDecimal.valueOf(123.46)));
    // Test RoudingMode.HALF_EVEN default rounding.
    assertTrue("toScaledBigDecimal(Double) 2 failed",
        NumberUtils.toScaledBigDecimal(Double.valueOf(23.515d)).equals(BigDecimal.valueOf(23.52)));
    assertTrue("toScaledBigDecimal(Double) 3 failed",
        NumberUtils.toScaledBigDecimal(Double.valueOf(23.525d)).equals(BigDecimal.valueOf(23.52)));
    assertTrue("toScaledBigDecimal(Double) 4 failed",
        NumberUtils.toScaledBigDecimal(Double.valueOf(23.525d))
            .multiply(BigDecimal.valueOf(100)).toString()
            .equals("2352.00"));
    assertTrue("toScaledBigDecimal(Double) 5 failed",
        NumberUtils.toScaledBigDecimal((Double) null).equals(BigDecimal.ZERO));
}

/**
 * Test for {@link NumberUtils#toScaledBigDecimal(Double, int, RoundingMode)}.
 */
@Test
public void testToScaledBigDecimalDoubleIRM() {
    assertTrue("toScaledBigDecimal(Double, int, RoudingMode) 1 failed",
        NumberUtils.toScaledBigDecimal(Double.valueOf(123.456d), 1, RoundingMode.CEILING).equals(BigDecimal.valueOf(123.5)));
    assertTrue("toScaledBigDecimal(Double, int, RoudingMode) 2 failed",
        NumberUtils.toScaledBigDecimal(Double.valueOf(23.5159d), 3, RoundingMode.FLOOR).equals(BigDecimal.valueOf(23.515)));
    assertTrue("toScaledBigDecimal(Double, int, RoudingMode) 3 failed",
        NumberUtils.toScaledBigDecimal(Double.valueOf(23.525d), 2, RoundingMode.HALF_UP).equals(BigDecimal.valueOf(23.53)));
    assertTrue("toScaledBigDecimal(Double, int, RoudingMode) 4 failed",
        NumberUtils.toScaledBigDecimal(Double.valueOf(23.521d), 4, RoundingMode.HALF_EVEN)
            .multiply(BigDecimal.valueOf(1000))
            .toString()
            .equals("23521.0000"));
    assertTrue("toScaledBigDecimal(Double, int, RoudingMode) 5 failed",
        NumberUtils.toScaledBigDecimal((Double) null, 2, RoundingMode.HALF_UP).equals(BigDecimal.ZERO));
}

/**
 * Test for {@link NumberUtils#toScaledBigDecimal(String)}.
 */
@Test
public void testToScaledBigDecimalString() {
    assertTrue("toScaledBigDecimal(String) 1 failed",
        NumberUtils.toScaledBigDecimal("123.456").equals(BigDecimal.valueOf(123.46)));
    // Test RoudingMode.HALF_EVEN default rounding.
    assertTrue("toScaledBigDecimal(String) 2 failed",
        NumberUtils.toScaledBigDecimal("23.515").equals(BigDecimal.valueOf(23.52)));
    assertTrue("toScaledBigDecimal(String) 3 failed",
        NumberUtils.toScaledBigDecimal("23.525").equals(BigDecimal.valueOf(23.52)));
    assertTrue("toScaledBigDecimal(String) 4 failed",
        NumberUtils.toScaledBigDecimal("23.525")
            .multiply(BigDecimal.valueOf(100)).toString()
            .equals("2352.00"));
    assertTrue("toScaledBigDecimal(String) 5 failed",
        NumberUtils.toScaledBigDecimal((String) null).equals(BigDecimal.ZERO));
}

/**
 * Test for {@link NumberUtils#toScaledBigDecimal(String, int, RoundingMode)}.
 */
@Test
public void testToScaledBigDecimalStringIRM() {
    assertTrue("toScaledBigDecimal(String, int, RoudingMode) 1 failed",
        NumberUtils.toScaledBigDecimal("123.456", 1, RoundingMode.CEILING).equals(BigDecimal.valueOf(123.5)));
    assertTrue("toScaledBigDecimal(String, int, RoudingMode) 2 failed",
        NumberUtils.toScaledBigDecimal("23.5159", 3, RoundingMode.FLOOR).equals(BigDecimal.valueOf(23.515)));
    assertTrue("toScaledBigDecimal(String, int, RoudingMode) 3 failed",
        NumberUtils.toScaledBigDecimal("23.525", 2, RoundingMode.HALF_UP).equals(BigDecimal.valueOf(23.53)));
    assertTrue("toScaledBigDecimal(String, int, RoudingMode) 4 failed",
        NumberUtils.toScaledBigDecimal("23.521", 4, RoundingMode.HALF_EVEN)
            .multiply(BigDecimal.valueOf(1000))
            .toString()
            .equals("23521.0000"));
    assertTrue("toScaledBigDecimal(String, int, RoudingMode) 5 failed",
        NumberUtils.toScaledBigDecimal((String) null, 2, RoundingMode.HALF_UP).equals(BigDecimal.ZERO));
}
```