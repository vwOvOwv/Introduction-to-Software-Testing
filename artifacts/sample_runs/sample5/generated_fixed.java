/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.commons.lang3.math;

import static org.apache.commons.lang3.LangAssertions.assertIllegalArgumentException;
import static org.apache.commons.lang3.LangAssertions.assertNullPointerException;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.RoundingMode;
import java.text.NumberFormat;
import java.text.ParseException;
import java.util.function.Function;

import org.apache.commons.lang3.AbstractLangTest;
import org.apache.commons.lang3.JavaVersion;
import org.apache.commons.lang3.SystemProperties;
import org.apache.commons.lang3.SystemUtils;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

/**
 * Tests {@link NumberUtils}.
 */
class NumberUtilsTest extends AbstractLangTest {

    private static void assertCreateNumberZero(final String number, final Object zero, final Object negativeZero) {
        assertEquals(zero, NumberUtils.createNumber(number), () -> "Input: " + number);
        assertEquals(zero, NumberUtils.createNumber("+" + number), () -> "Input: +" + number);
        assertEquals(negativeZero, NumberUtils.createNumber("-" + number), () -> "Input: -" + number);
    }

    private boolean checkCreateNumber(final String val) {
        try {
            return NumberUtils.createNumber(val) != null;
        } catch (final NumberFormatException e) {
            return false;
        }
    }

    @Test
    public void compareByte() {
        assertTrue(NumberUtils.compare((byte) -3, (byte) 0) < 0);
        assertEquals(0, NumberUtils.compare((byte) 113, (byte) 113));
        assertTrue(NumberUtils.compare((byte) 123, (byte) 32) > 0);
    }

    @Test
    public void compareInt() {
        assertTrue(NumberUtils.compare(-3, 0) < 0);
        assertEquals(0, NumberUtils.compare(113, 113));
        assertTrue(NumberUtils.compare(213, 32) > 0);
    }

    private void compareIsCreatableWithCreateNumber(final String val, final boolean expected) {
        final boolean isValid = NumberUtils.isCreatable(val);
        final boolean canCreate = checkCreateNumber(val);
        assertTrue(isValid == expected && canCreate == expected, "Expecting " + expected
            + " for isCreatable/createNumber using \"" + val + "\" but got " + isValid + " and " + canCreate);
    }

    @SuppressWarnings("deprecation")
    private void compareIsNumberWithCreateNumber(final String val, final boolean expected) {
        final boolean isValid = NumberUtils.isNumber(val);
        final boolean canCreate = checkCreateNumber(val);
        assertTrue(isValid == expected && canCreate == expected, "Expecting " + expected
            + " for isNumber/createNumber using \"" + val + "\" but got " + isValid + " and " + canCreate);
    }

    @Test
    public void compareLong() {
        assertTrue(NumberUtils.compare(-3L, 0L) < 0);
        assertEquals(0, NumberUtils.compare(113L, 113L));
        assertTrue(NumberUtils.compare(213L, 32L) > 0);
    }

    @Test
    public void compareShort() {
        assertTrue(NumberUtils.compare((short) -3, (short) 0) < 0);
        assertEquals(0, NumberUtils.compare((short) 113, (short) 113));
        assertTrue(NumberUtils.compare((short) 213, (short) 32) > 0);
    }

    private boolean isApplyNonNull(final String s, final Function<String, ?> function) {
        try {
            assertNotNull(function.apply(s));
            return true;
        } catch (final Exception e) {
            if (!s.matches(".*\\s.*") && SystemProperties.getBoolean(getClass(), "printStackTrace", () -> false)) {
                e.printStackTrace();
            }
            return false;
        }
    }

    private boolean isNumberFormatParsable(final String s) {
        final NumberFormat instance = NumberFormat.getInstance();
        try {
            // Stops parsing when a space is found, then returns an object.
            assertNotNull(instance.parse(s));
            return true;
        } catch (final ParseException e) {
            return false;
        }
    }

    private boolean isNumberIntegerOnlyFormatParsable(final String s) {
        final NumberFormat instance = NumberFormat.getInstance();
        instance.setParseIntegerOnly(true);
        try {
            // Stops parsing when a space is found, then returns an object.
            assertNotNull(instance.parse(s));
            return true;
        } catch (final ParseException e) {
            return false;
        }
    }

    private boolean isParsableByte(final String s) {
        final boolean parsable = NumberUtils.isParsable(s);
        assertTrue(isNumberFormatParsable(s), s);
        assertTrue(isNumberIntegerOnlyFormatParsable(s), s);
        assertEquals(parsable, isApplyNonNull(s, Byte::parseByte), s);
        return parsable;
    }

    private boolean isParsableDouble(final String s) {
        final boolean parsable = NumberUtils.isParsable(s);
        assertTrue(isNumberFormatParsable(s), s);
        assertTrue(isNumberIntegerOnlyFormatParsable(s), s);
        assertEquals(parsable, isApplyNonNull(s, Double::parseDouble), s);
        return parsable;
    }

    private boolean isParsableFloat(final String s) {
        final boolean parsable = NumberUtils.isParsable(s);
        assertTrue(isNumberFormatParsable(s), s);
        assertTrue(isNumberIntegerOnlyFormatParsable(s), s);
        assertEquals(parsable, isApplyNonNull(s, Float::parseFloat), s);
        return parsable;
    }

    private boolean isParsableInteger(final String s) {
        final boolean parsable = NumberUtils.isParsable(s);
        assertTrue(isNumberFormatParsable(s), s);
        assertTrue(isNumberIntegerOnlyFormatParsable(s), s);
        assertEquals(parsable, isApplyNonNull(s, Integer::parseInt), s);
        return parsable;
    }

    private boolean isParsableLong(final String s) {
        final boolean parsable = NumberUtils.isParsable(s);
        assertTrue(isNumberFormatParsable(s), s);
        assertTrue(isNumberIntegerOnlyFormatParsable(s), s);
        assertEquals(parsable, isApplyNonNull(s, Long::parseLong), s);
        return parsable;
    }

    private boolean isParsableShort(final String s) {
        final boolean parsable = NumberUtils.isParsable(s);
        assertTrue(isNumberFormatParsable(s), s);
        assertTrue(isNumberIntegerOnlyFormatParsable(s), s);
        assertEquals(parsable, isApplyNonNull(s, Short::parseShort), s);
        return parsable;
    }

    /**
     * Test for {@link NumberUtils#toDouble(BigDecimal)}
     */
    @Test
    void testBigIntegerToDoubleBigInteger() {
        assertEquals(0.0d, NumberUtils.toDouble((BigDecimal) null), "toDouble(BigInteger) 1 failed");
        assertEquals(8.5d, NumberUtils.toDouble(BigDecimal.valueOf(8.5d)), "toDouble(BigInteger) 2 failed");
    }

    /**
     * Test for {@link NumberUtils#toDouble(BigDecimal, double)}
     */
    @Test
    void testBigIntegerToDoubleBigIntegerD() {
        assertEquals(1.1d, NumberUtils.toDouble((BigDecimal) null, 1.1d), "toDouble(BigInteger) 1 failed");
        assertEquals(8.5d, NumberUtils.toDouble(BigDecimal.valueOf(8.5d), 1.1d), "toDouble(BigInteger) 2 failed");
    }

    // Testing JDK against old Lang functionality
    @Test
    void testCompareDouble() {
        assertEquals(0, Double.compare(Double.NaN, Double.NaN));
        assertEquals(Double.compare(Double.NaN, Double.POSITIVE_INFINITY), +1);
        assertEquals(Double.compare(Double.NaN, Double.MAX_VALUE), +1);
        assertEquals(Double.compare(Double.NaN, 1.2d), +1);
        assertEquals(Double.compare(Double.NaN, 0.0d), +1);
        assertEquals(Double.compare(Double.NaN, -0.0d), +1);
        assertEquals(Double.compare(Double.NaN, -1.2d), +1);
        assertEquals(Double.compare(Double.NaN, -Double.MAX_VALUE), +1);
        assertEquals(Double.compare(Double.NaN, Double.NEGATIVE_INFINITY), +1);

        assertEquals(Double.compare(Double.POSITIVE_INFINITY, Double.NaN), -1);
        assertEquals(0, Double.compare(Double.POSITIVE_INFINITY, Double.POSITIVE_INFINITY));
        assertEquals(Double.compare(Double.POSITIVE_INFINITY, Double.MAX_VALUE), +1);
        assertEquals(Double.compare(Double.POSITIVE_INFINITY, 1.2d), +1);
        assertEquals(Double.compare(Double.POSITIVE_INFINITY, 0.0d), +1);
        assertEquals(Double.compare(Double.POSITIVE_INFINITY, -0.0d), +1);
        assertEquals(Double.compare(Double.POSITIVE_INFINITY, -1.2d), +1);
        assertEquals(Double.compare(Double.POSITIVE_INFINITY, -Double.MAX_VALUE), +1);
        assertEquals(Double.compare(Double.POSITIVE_INFINITY, Double.NEGATIVE_INFINITY), +1);

        assertEquals(Double.compare(Double.MAX_VALUE, Double.NaN), -1);
        assertEquals(Double.compare(Double.MAX_VALUE, Double.POSITIVE_INFINITY), -1);
        assertEquals(0, Double.compare(Double.MAX_VALUE, Double.MAX_VALUE));
        assertEquals(Double.compare(Double.MAX_VALUE, 1.2d), +1);
        assertEquals(Double.compare(Double.MAX_VALUE, 0.0d), +1);
        assertEquals(Double.compare(Double.MAX_VALUE, -0.0d), +1);
        assertEquals(Double.compare(Double.MAX_VALUE, -1.2d), +1);
        assertEquals(Double.compare(Double.MAX_VALUE, -Double.MAX_VALUE), +1);
        assertEquals(Double.compare(Double.MAX_VALUE, Double.NEGATIVE_INFINITY), +1);

        assertEquals(Double.compare(1.2d, Double.NaN), -1);
        assertEquals(Double.compare(1.2d, Double.POSITIVE_INFINITY), -1);
        assertEquals(Double.compare(1.2d, Double.MAX_VALUE), -1);
        assertEquals(0, Double.compare(1.2d, 1.2d));
        assertEquals(Double.compare(1.2d, 0.0d), +1);
        assertEquals(Double.compare(1.2d, -0.0d), +1);
        assertEquals(Double.compare(1.2d, -1.2d), +1);
        assertEquals(Double.compare(1.2d, -Double.MAX_VALUE), +1);
        assertEquals(Double.compare(1.2d, Double.NEGATIVE_INFINITY), +1);

        assertEquals(Double.compare(0.0d, Double.NaN), -1);
        assertEquals(Double.compare(0.0d, Double.POSITIVE_INFINITY), -1);
        assertEquals(Double.compare(0.0d, Double.MAX_VALUE), -1);
        assertEquals(Double.compare(0.0d, 1.2d), -1);
        assertEquals(0, Double.compare(0.0d, 0.0d));
        assertEquals(Double.compare(0.0d, -0.0d), +1);
        assertEquals(Double.compare(0.0d, -1.2d), +1);
        assertEquals(Double.compare(0.0d, -Double.MAX_VALUE), +1);
        assertEquals(Double.compare(0.0d, Double.NEGATIVE_INFINITY), +1);

        assertEquals(Double.compare(-0.0d, Double.NaN), -1);
        assertEquals(Double.compare(-0.0d, Double.POSITIVE_INFINITY), -1);
        assertEquals(Double.compare(-0.0d, Double.MAX_VALUE), -1);
        assertEquals(Double.compare(-0.0d, 1.2d), -1);
        assertEquals(Double.compare(-0.0d, 0.0d), -1);
        assertEquals(0, Double.compare(-0.0d, -0.0d));
        assertEquals(Double.compare(-0.0d, -1.2d), +1);
        assertEquals(Double.compare(-0.0d, -Double.MAX_VALUE), +1);
        assertEquals(Double.compare(-0.0d, Double.NEGATIVE_INFINITY), +1);

        assertEquals(Double.compare(-1.2d, Double.NaN), -1);
        assertEquals(Double.compare(-1.2d, Double.POSITIVE_INFINITY), -1);
        assertEquals(Double.compare(-1.2d, Double.MAX_VALUE), -1);
        assertEquals(Double.compare(-1.2d, 1.2d), -1);
        assertEquals(Double.compare(-1.2d, 0.0d), -1);
        assertEquals(Double.compare(-1.2d, -0.0d), -1);
        assertEquals(0, Double.compare(-1.2d, -1.2d));
        assertEquals(Double.compare(-1.2d, -Double.MAX_VALUE), +1);
        assertEquals(Double.compare(-1.2d, Double.NEGATIVE_INFINITY), +1);

        assertEquals(Double.compare(-Double.MAX_VALUE, Double.NaN), -1);
        assertEquals(Double.compare(-Double.MAX_VALUE, Double.POSITIVE_INFINITY), -1);
        assertEquals(Double.compare(-Double.MAX_VALUE, Double.MAX_VALUE), -1);
        assertEquals(Double.compare(-Double.MAX_VALUE, 1.2d), -1);
        assertEquals(Double.compare(-Double.MAX_VALUE, 0.0d), -1);
        assertEquals(Double.compare(-Double.MAX_VALUE, -0.0d), -1);
        assertEquals(Double.compare(-Double.MAX_VALUE, -1.2d), -1);
        assertEquals(0, Double.compare(-Double.MAX_VALUE, -Double.MAX_VALUE));
        assertEquals(Double.compare(-Double.MAX_VALUE, Double.NEGATIVE_INFINITY), +1);

        assertEquals(Double.compare(Double.NEGATIVE_INFINITY, Double.NaN), -1);
        assertEquals(Double.compare(Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY), -1);
        assertEquals(Double.compare(Double.NEGATIVE_INFINITY, Double.MAX_VALUE), -1);
        assertEquals(Double.compare(Double.NEGATIVE_INFINITY, 1.2d), -1);
        assertEquals(Double.compare(Double.NEGATIVE_INFINITY, 0.0d), -1);
        assertEquals(Double.compare(Double.NEGATIVE_INFINITY, -0.0d), -1);
        assertEquals(Double.compare(Double.NEGATIVE_INFINITY, -1.2d), -1);
        assertEquals(Double.compare(Double.NEGATIVE_INFINITY, -Double.MAX_VALUE), -1);
        assertEquals(0, Double.compare(Double.NEGATIVE_INFINITY, Double.NEGATIVE_INFINITY));
    }

    @Test
    void testCompareFloat() {
        assertEquals(0, Float.compare(Float.NaN, Float.NaN));
        assertEquals(Float.compare(Float.NaN, Float.POSITIVE_INFINITY), +1);
        assertEquals(Float.compare(Float.NaN, Float.MAX_VALUE), +1);
        assertEquals(Float.compare(Float.NaN, 1.2f), +1);
        assertEquals(Float.compare(Float.NaN, 0.0f), +1);
        assertEquals(Float.compare(Float.NaN, -0.0f), +1);
        assertEquals(Float.compare(Float.NaN, -1.2f), +1);
        assertEquals(Float.compare(Float.NaN, -Float.MAX_VALUE), +1);
        assertEquals(Float.compare(Float.NaN, Float.NEGATIVE_INFINITY), +1);

        assertEquals(Float.compare(Float.POSITIVE_INFINITY, Float.NaN), -1);
        assertEquals(0, Float.compare(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY));
        assertEquals(Float.compare(Float.POSITIVE_INFINITY, Float.MAX_VALUE), +1);
        assertEquals(Float.compare(Float.POSITIVE_INFINITY, 1.2f), +1);
        assertEquals(Float.compare(Float.POSITIVE_INFINITY, 0.0f), +1);
        assertEquals(Float.compare(Float.POSITIVE_INFINITY, -0.0f), +1);
        assertEquals(Float.compare(Float.POSITIVE_INFINITY, -1.2f), +1);
        assertEquals(Float.compare(Float.POSITIVE_INFINITY, -Float.MAX_VALUE), +1);
        assertEquals(Float.compare(Float.POSITIVE_INFINITY, Float.NEGATIVE_INFINITY), +1);

        assertEquals(Float.compare(Float.MAX_VALUE, Float.NaN), -1);
        assertEquals(Float.compare(Float.MAX_VALUE, Float.POSITIVE_INFINITY), -1);
        assertEquals(0, Float.compare(Float.MAX_VALUE, Float.MAX_VALUE));
        assertEquals(Float.compare(Float.MAX_VALUE, 1.2f), +1);
        assertEquals(Float.compare(Float.MAX_VALUE, 0.0f), +1);
        assertEquals(Float.compare(Float.MAX_VALUE, -0.0f), +1);
        assertEquals(Float.compare(Float.MAX_VALUE, -1.2f), +1);
        assertEquals(Float.compare(Float.MAX_VALUE, -Float.MAX_VALUE), +1);
        assertEquals(Float.compare(Float.MAX_VALUE, Float.NEGATIVE_INFINITY), +1);

        assertEquals(Float.compare(1.2f, Float.NaN), -1);
        assertEquals(Float.compare(1.2f, Float.POSITIVE_INFINITY), -1);
        assertEquals(Float.compare(1.2f, Float.MAX_VALUE), -1);
        assertEquals(0, Float.compare(1.2f, 1.2f));
        assertEquals(Float.compare(1.2f, 0.0f), +1);
        assertEquals(Float.compare(1.2f, -0.0f), +1);
        assertEquals(Float.compare(1.2f, -1.2f), +1);
        assertEquals(Float.compare(1.2f, -Float.MAX_VALUE), +1);
        assertEquals(Float.compare(1.2f, Float.NEGATIVE_INFINITY), +1);

        assertEquals(Float.compare(0.0f, Float.NaN), -1);
        assertEquals(Float.compare(0.0f, Float.POSITIVE_INFINITY), -1);
        assertEquals(Float.compare(0.0f, Float.MAX_VALUE), -1);
        assertEquals(Float.compare(0.0f, 1.2f), -1);
        assertEquals(0, Float.compare(0.0f, 0.0f));
        assertEquals(Float.compare(0.0f, -0.0f), +1);
        assertEquals(Float.compare(0.0f, -1.2f), +1);
        assertEquals(Float.compare(0.0f, -Float.MAX_VALUE), +1);
        assertEquals(Float.compare(0.0f, Float.NEGATIVE_INFINITY), +1);

        assertEquals(Float.compare(-0.0f, Float.NaN), -1);
        assertEquals(Float.compare(-0.0f, Float.POSITIVE_INFINITY), -1);
        assertEquals(Float.compare(-0.0f, Float.MAX_VALUE), -1);
        assertEquals(Float.compare(-0.0f, 1.2f), -1);
        assertEquals(Float.compare(-0.0f, 0.0f), -1);
        assertEquals(0, Float.compare(-0.0f, -0.0f));
        assertEquals(Float.compare(-0.0f, -1.2f), +1);
        assertEquals(Float.compare(-0.0f, -Float.MAX_VALUE), +1);
        assertEquals(Float.compare(-0.0f, Float.NEGATIVE_INFINITY), +1);

        assertEquals(Float.compare(-1.2f, Float.NaN), -1);
        assertEquals(Float.compare(-1.2f, Float.POSITIVE_INFINITY), -1);
        assertEquals(Float.compare(-1.2f, Float.MAX_VALUE), -1);
        assertEquals(Float.compare(-1.2f, 1.2f), -1);
        assertEquals(Float.compare(-1.2f, 0.0f), -1);
        assertEquals(Float.compare(-1.2f, -0.0f), -1);
        assertEquals(0, Float.compare(-1.2f, -1.2f));
        assertEquals(Float.compare(-1.2f, -Float.MAX_VALUE), +1);
        assertEquals(Float.compare(-1.2f, Float.NEGATIVE_INFINITY), +1);

        assertEquals(Float.compare(-Float.MAX_VALUE, Float.NaN), -1);
        assertEquals(Float.compare(-Float.MAX_VALUE, Float.POSITIVE_INFINITY), -1);
        assertEquals(Float.compare(-Float.MAX_VALUE, Float.MAX_VALUE), -1);
        assertEquals(Float.compare(-Float.MAX_VALUE, 1.2f), -1);
        assertEquals(Float.compare(-Float.MAX_VALUE, 0.0f), -1);
        assertEquals(Float.compare(-Float.MAX_VALUE, -0.0f), -1);
        assertEquals(Float.compare(-Float.MAX_VALUE, -1.2f), -1);
        assertEquals(0, Float.compare(-Float.MAX_VALUE, -Float.MAX_VALUE));
        assertEquals(Float.compare(-Float.MAX_VALUE, Float.NEGATIVE_INFINITY), +1);

        assertEquals(Float.compare(Float.NEGATIVE_INFINITY, Float.NaN), -1);
        assertEquals(Float.compare(Float.NEGATIVE_INFINITY, Float.POSITIVE_INFINITY), -1);
        assertEquals(Float.compare(Float.NEGATIVE_INFINITY, Float.MAX_VALUE), -1);
        assertEquals(Float.compare(Float.NEGATIVE_INFINITY, 1.2f), -1);
        assertEquals(Float.compare(Float.NEGATIVE_INFINITY, 0.0f), -1);
        assertEquals(Float.compare(Float.NEGATIVE_INFINITY, -0.0f), -1);
        assertEquals(Float.compare(Float.NEGATIVE_INFINITY, -1.2f), -1);
        assertEquals(Float.compare(Float.NEGATIVE_INFINITY, -Float.MAX_VALUE), -1);
        assertEquals(0, Float.compare(Float.NEGATIVE_INFINITY, Float.NEGATIVE_INFINITY));
    }

    @SuppressWarnings("cast") // suppress instanceof warning check
    @Test
    void testConstants() {
        assertInstanceOf(Long.class, NumberUtils.LONG_ZERO);
        assertInstanceOf(Long.class, NumberUtils.LONG_ONE);
        assertInstanceOf(Long.class, NumberUtils.LONG_MINUS_ONE);
        assertInstanceOf(Integer.class, NumberUtils.INTEGER_ZERO);
        assertInstanceOf(Integer.class, NumberUtils.INTEGER_ONE);
        assertInstanceOf(Integer.class, NumberUtils.INTEGER_MINUS_ONE);
        assertInstanceOf(Short.class, NumberUtils.SHORT_ZERO);
        assertInstanceOf(Short.class, NumberUtils.SHORT_ONE);
        assertInstanceOf(Short.class, NumberUtils.SHORT_MINUS_ONE);
        assertInstanceOf(Byte.class, NumberUtils.BYTE_ZERO);
        assertInstanceOf(Byte.class, NumberUtils.BYTE_ONE);
        assertInstanceOf(Byte.class, NumberUtils.BYTE_MINUS_ONE);
        assertInstanceOf(Double.class, NumberUtils.DOUBLE_ZERO);
        assertInstanceOf(Double.class, NumberUtils.DOUBLE_ONE);
        assertInstanceOf(Double.class, NumberUtils.DOUBLE_MINUS_ONE);
        assertInstanceOf(Float.class, NumberUtils.FLOAT_ZERO);
        assertInstanceOf(Float.class, NumberUtils.FLOAT_ONE);
        assertInstanceOf(Float.class, NumberUtils.FLOAT_MINUS_ONE);

        assertEquals(0, NumberUtils.LONG_ZERO.longValue());
        assertEquals(1, NumberUtils.LONG_ONE.longValue());
        assertEquals(NumberUtils.LONG_MINUS_ONE.longValue(), -1);
        assertEquals(0, NumberUtils.INTEGER_ZERO.intValue());
        assertEquals(1, NumberUtils.INTEGER_ONE.intValue());
        assertEquals(NumberUtils.INTEGER_MINUS_ONE.intValue(), -1);
        assertEquals(0, NumberUtils.SHORT_ZERO.shortValue());
        assertEquals(1, NumberUtils.SHORT_ONE.shortValue());
        assertEquals(NumberUtils.SHORT_MINUS_ONE.shortValue(), -1);
        assertEquals(0, NumberUtils.BYTE_ZERO.byteValue());
        assertEquals(1, NumberUtils.BYTE_ONE.byteValue());
        assertEquals(NumberUtils.BYTE_MINUS_ONE.byteValue(), -1);
        assertEquals(0.0d, NumberUtils.DOUBLE_ZERO.doubleValue());
        assertEquals(1.0d, NumberUtils.DOUBLE_ONE.doubleValue());
        assertEquals(NumberUtils.DOUBLE_MINUS_ONE.doubleValue(), -1.0d);
        assertEquals(0.0f, NumberUtils.FLOAT_ZERO.floatValue());
        assertEquals(1.0f, NumberUtils.FLOAT_ONE.floatValue());
        assertEquals(NumberUtils.FLOAT_MINUS_ONE.floatValue(), -1.0f);
    }

    @Test
    void testConstructor() {
        assertNotNull(new NumberUtils());
        final Constructor<?>[] cons = NumberUtils.class.getDeclaredConstructors();
        assertEquals(1, cons.length);
        assertTrue(Modifier.isPublic(cons[0].getModifiers()));
        assertTrue(Modifier.isPublic(NumberUtils.class.getModifiers()));
        assertFalse(Modifier.isFinal(NumberUtils.class.getModifiers()));
    }

    @Test
    void testCreateBigDecimal() {
        assertEquals(new BigDecimal("1234.5"), NumberUtils.createBigDecimal("1234.5"),
            "createBigDecimal(String) failed");
        assertNull(NumberUtils.createBigDecimal(null), "createBigDecimal(null) failed");
        testCreateBigDecimalFailure("");
        testCreateBigDecimalFailure(" ");
        testCreateBigDecimalFailure("\b\t\n\f\r");
        // Funky whitespaces
        testCreateBigDecimalFailure("\u00A0\uFEFF\u000B\u000C\u001C\u001D\u001E\u001F");
        // sign alone not valid
        testCreateBigDecimalFailure("-");
        // comment in NumberUtils suggests some implementations may incorrectly allow this
        testCreateBigDecimalFailure("--");
        testCreateBigDecimalFailure("--0");
        // sign alone not valid
        testCreateBigDecimalFailure("+");
        // in case this was also allowed by some JVMs
        testCreateBigDecimalFailure("++");
        testCreateBigDecimalFailure("++0");
    }

    protected void testCreateBigDecimalFailure(final String str) {
        assertThrows(NumberFormatException.class, () -> NumberUtils.createBigDecimal(str),
            "createBigDecimal(\"" + str + "\") should have failed.");
    }

    @Test
    void testCreateBigInteger() {
        assertEquals(new BigInteger("12345"), NumberUtils.createBigInteger("12345"), "createBigInteger(String) failed");
        assertNull(NumberUtils.createBigInteger(null), "createBigInteger(null) failed");
        testCreateBigIntegerFailure("");
        testCreateBigIntegerFailure(" ");
        testCreateBigIntegerFailure("\b\t\n\f\r");
        // Funky whitespaces
        testCreateBigIntegerFailure("\u00A0\uFEFF\u000B\u000C\u001C\u001D\u001E\u001F");
        assertEquals(new BigInteger("255"), NumberUtils.createBigInteger("0xff"), "createBigInteger(String) failed");
        assertEquals(new BigInteger("255"), NumberUtils.createBigInteger("0Xff"), "createBigInteger(String) failed");
        assertEquals(new BigInteger("255"), NumberUtils.createBigInteger("#ff"), "createBigInteger(String) failed");
        assertEquals(new BigInteger("-255"), NumberUtils.createBigInteger("-0xff"), "createBigInteger(String) failed");
        assertEquals(new BigInteger("255"), NumberUtils.createBigInteger("0377"), "createBigInteger(String) failed");
        assertEquals(new BigInteger("-255"), NumberUtils.createBigInteger("-0377"), "createBigInteger(String) failed");
        assertEquals(new BigInteger("-255"), NumberUtils.createBigInteger("-0377"), "createBigInteger(String) failed");
        assertEquals(new BigInteger("-0"), NumberUtils.createBigInteger("-0"), "createBigInteger(String) failed");
        assertEquals(new BigInteger("0"), NumberUtils.createBigInteger("0"), "createBigInteger(String) failed");
        testCreateBigIntegerFailure("#");
        testCreateBigIntegerFailure("-#");
        testCreateBigIntegerFailure("0x");
        testCreateBigIntegerFailure("-0x");
        // LANG-1645
        assertEquals(new BigInteger("+FFFFFFFFFFFFFFFF", 16), NumberUtils.createBigInteger("+0xFFFFFFFFFFFFFFFF"));
        assertEquals(new BigInteger("+FFFFFFFFFFFFFFFF", 16), NumberUtils.createBigInteger("+#FFFFFFFFFFFFFFFF"));
        assertEquals(new BigInteger("+1234567", 8), NumberUtils.createBigInteger("+01234567"));
    }

    protected void testCreateBigIntegerFailure(final String str) {
        assertThrows(NumberFormatException.class, () -> NumberUtils.createBigInteger(str),
            "createBigInteger(\"" + str + "\") should have failed.");
    }

    @Test
    void testCreateDouble() {
        assertEquals(Double.valueOf("1234.5"), NumberUtils.createDouble("1234.5"), "createDouble(String) failed");
        assertNull(NumberUtils.createDouble(null), "createDouble(null) failed");
        testCreateDoubleFailure("");
        testCreateDoubleFailure(" ");
        testCreateDoubleFailure("\b\t\n\f\r");
        // Funky whitespaces
        testCreateDoubleFailure("\u00A0\uFEFF\u000B\u000C\u001C\u001D\u001E\u001F");
    }

    protected void testCreateDoubleFailure(final String str) {
        assertThrows(NumberFormatException.class, () -> NumberUtils.createDouble(str),
            "createDouble(\"" + str + "\") should have failed.");
    }

    @Test
    void testCreateFloat() {
        assertEquals(Float.valueOf("1234.5"), NumberUtils.createFloat("1234.5"), "createFloat(String) failed");
        assertNull(NumberUtils.createFloat(null), "createFloat(null) failed");
        testCreateFloatFailure("");
        testCreateFloatFailure(" ");
        testCreateFloatFailure("\b\t\n\f\r");
        // Funky whitespaces
        testCreateFloatFailure("\u00A0\uFEFF\u000B\u000C\u001C\u001D\u001E\u001F");
    }

    protected void testCreateFloatFailure(final String str) {
        assertThrows(NumberFormatException.class, () -> NumberUtils.createFloat(str),
            "createFloat(\"" + str + "\") should have failed.");
    }

    @Test
    void testCreateInteger() {
        assertEquals(Integer.valueOf("12345"), NumberUtils.createInteger("12345"), "createInteger(String) failed");
        assertNull(NumberUtils.createInteger(null), "createInteger(null) failed");
        testCreateIntegerFailure("");
        testCreateIntegerFailure(" ");
        testCreateIntegerFailure("\b\t\n\f\r");
        // Funky whitespaces
        testCreateIntegerFailure("\u00A0\uFEFF\u000B\u000C\u001C\u001D\u001E\u001F");
        // LANG-1645
        assertEquals(Integer.decode("+0xF"), NumberUtils.createInteger("+0xF"));
    }

    protected void testCreateIntegerFailure(final String str) {
        assertThrows(NumberFormatException.class, () -> NumberUtils.createInteger(str),
            "createInteger(\"" + str + "\") should have failed.");
    }

    @Test
    void testCreateLong() {
        assertEquals(Long.valueOf("12345"), NumberUtils.createLong("12345"), "createLong(String) failed");
        assertNull(NumberUtils.createLong(null), "createLong(null) failed");
        testCreateLongFailure("");
        testCreateLongFailure(" ");
        testCreateLongFailure("\b\t\n\f\r");
        // Funky whitespaces
        testCreateLongFailure("\u00A0\uFEFF\u000B\u000C\u001C\u001D\u001E\u001F");
        // LANG-1645
        assertEquals(Long.decode("+0xFFFFFFFF"), NumberUtils.createLong("+0xFFFFFFFF"));
    }

    protected void testCreateLongFailure(final String str) {
        assertThrows(NumberFormatException.class, () -> NumberUtils.createLong(str),
            "createLong(\"" + str + "\") should have failed.");
    }

    @Test
    void testCreateNumber() {
        // a lot of things can go wrong
        assertEquals(Float.valueOf("1234.5"), NumberUtils.createNumber("1234.5"), "createNumber(String) 1 failed");
        assertEquals(Integer.valueOf("12345"), NumberUtils.createNumber("12345"), "createNumber(String) 2 failed");
        assertEquals(Double.valueOf("1234.5"), NumberUtils.createNumber("1234.5D"), "createNumber(String) 3 failed");
        assertEquals(Double.valueOf("1234.5"), NumberUtils.createNumber("1234.5d"), "createNumber(String) 3 failed");
        assertEquals(Float.valueOf("1234.5"), NumberUtils.createNumber("1234.5F"), "createNumber(String) 4 failed");
        assertEquals(Float.valueOf("1234.5"), NumberUtils.createNumber("1234.5f"), "createNumber(String) 4 failed");
        assertEquals(Long.valueOf(Integer.MAX_VALUE + 1L), NumberUtils.createNumber("" + (Integer.MAX_VALUE + 1L)),
            "createNumber(String) 5 failed");
        assertEquals(Long.valueOf(12345), NumberUtils.createNumber("12345L"), "createNumber(String) 6 failed");
        assertEquals(Long.valueOf(12345), NumberUtils.createNumber("12345l"), "createNumber(String) 6 failed");
        assertEquals(Float.valueOf("-1234.5"), NumberUtils.createNumber("-1234.5"), "createNumber(String) 7 failed");
        assertEquals(Integer.valueOf("-12345"), NumberUtils.createNumber("-12345"), "createNumber(String) 8 failed");
        assertEquals(0xFADE, NumberUtils.createNumber("0xFADE").intValue(), "createNumber(String) 9a failed");
        assertEquals(0xFADE, NumberUtils.createNumber("0Xfade").intValue(), "createNumber(String) 9b failed");
        assertEquals(-0xFADE, NumberUtils.createNumber("-0xFADE").intValue(), "createNumber(String) 10a failed");
        assertEquals(-0xFADE, NumberUtils.createNumber("-0Xfade").intValue(), "createNumber(String) 10b failed");
        assertEquals(Double.valueOf("1.1E200"), NumberUtils.createNumber("1.1E200"), "createNumber(String) 11 failed");
        assertEquals(Float.valueOf("1.1E20"), NumberUtils.createNumber("1.1E20"), "createNumber(String) 12 failed");
        assertEquals(Double.valueOf("-1.1E200"), NumberUtils.createNumber("-1.1E200"),
            "createNumber(String) 13 failed");
        assertEquals(Double.valueOf("1.1E-200"), NumberUtils.createNumber("1.1E-200"),
            "createNumber(String) 14 failed");
        assertNull(NumberUtils.createNumber(null), "createNumber(null) failed");
        assertEquals(new BigInteger("12345678901234567890"), NumberUtils.createNumber("12345678901234567890L"),
            "createNumber(String) failed");

        assertEquals(new BigDecimal("1.1E-700"), NumberUtils.createNumber("1.1E
