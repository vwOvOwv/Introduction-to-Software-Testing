# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `12c71a019faf874e22be3890b5687d757864755f`
- B: `c95ee37dffd44b01d2b816e0d943013bc7bd866c`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `methods`
- user_chars: `97057`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 25028, 'completion_tokens': 4351, 'total_tokens': 29379}`

---

- 修改 `testConstructor`：生产类新增私有构造器和单例实例，测试不再断言仅有一个 public 构造器；需要删除 `Constructor`、`Modifier` import。
- 新增辅助方法 `randomProvider`：生产代码新增 `secure()` / `insecure()` 实例 API，参数化测试需提供两个实例；需要新增 `Stream`、`ParameterizedTest`、`MethodSource` import。
- 修改 `testLANG807`：改为参数化测试并覆盖 `RandomStringUtils.secure()` 与 `RandomStringUtils.insecure()` 的 `next(...)` 实例方法。
- 修改 `testRandomAscii`、`testRandomAsciiRange`、`testRandomGraphRange`、`testRandomNumeric`、`testRandomNumericRange`、`testRandomPrintRange`：静态随机方法委托到实例 API，测试改为参数化调用 `nextXxx(...)`。
- 删除 `testRandomStringUtils` 并新增 `testRandomApis`、`testRandomParameter`：实例 API 覆盖放入参数化测试，显式 `Random` 种子行为保留为独立静态 API 测试。
- 删除 `testRandomStringUtilsHomog` 并新增 `testHomogeneity`：使用实例 `next(...)` 覆盖 secure/insecure 两种随机源。
- 修改 `testRandomWithChars`：改为参数化测试并调用实例 `next(...)` / `nextNumeric(...)`。
- 需要调整 import：移除反射相关 import，新增 `java.util.stream.Stream`、JUnit Params 相关 import，并保留 `assertNotEquals`。

```java
// IMPORTS_START
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.greaterThanOrEqualTo;
import static org.hamcrest.Matchers.is;
import static org.hamcrest.Matchers.lessThan;
import static org.hamcrest.Matchers.lessThanOrEqualTo;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.Random;
import java.util.stream.Stream;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
// IMPORTS_END

// DELETE_TESTS_START
testRandomStringUtils
testRandomStringUtilsHomog
// DELETE_TESTS_END

static Stream<RandomStringUtils> randomProvider() {
    return Stream.of(RandomStringUtils.secure(), RandomStringUtils.insecure());
}

@Test
public void testConstructor() {
    assertNotNull(new RandomStringUtils());
}

@ParameterizedTest
@MethodSource("randomProvider")
public void testLANG807(final RandomStringUtils rsu) {
    final IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> rsu.next(3, 5, 5, false, false));
    final String msg = ex.getMessage();
    assertTrue(msg.contains("start"), "Message (" + msg + ") must contain 'start'");
    assertTrue(msg.contains("end"), "Message (" + msg + ") must contain 'end'");
}

@ParameterizedTest
@MethodSource("randomProvider")
public void testHomogeneity(final RandomStringUtils rsu) {
    final String set = "abc";
    final char[] chars = set.toCharArray();
    final int[] counts = { 0, 0, 0 };
    final int[] expected = { 200, 200, 200 };
    for (int i = 0; i < 100; i++) {
        final String gen = rsu.next(6, chars);
        for (int j = 0; j < 6; j++) {
            switch (gen.charAt(j)) {
            case 'a': {
                counts[0]++;
                break;
            }
            case 'b': {
                counts[1]++;
                break;
            }
            case 'c': {
                counts[2]++;
                break;
            }
            default: {
                fail("generated character not in set");
            }
            }
        }
    }
    assertThat("test homogeneity -- will fail about 1 in 100,000 times", chiSquare(expected, counts), lessThan(23.025850929940457d));
}

@ParameterizedTest
@MethodSource("randomProvider")
public void testRandomApis(final RandomStringUtils rsu) {
    String r1 = rsu.next(50);
    assertEquals(50, r1.length(), "random(50) length");
    String r2 = rsu.next(50);
    assertEquals(50, r2.length(), "random(50) length");
    assertFalse(r1.equals(r2), "!r1.equals(r2)");

    r1 = rsu.nextAscii(50);
    assertEquals(50, r1.length(), "randomAscii(50) length");
    for (int i = 0; i < r1.length(); i++) {
        assertThat("char >= 32 && <= 127", (int) r1.charAt(i), allOf(greaterThanOrEqualTo(32), lessThanOrEqualTo(127)));
    }
    r2 = rsu.nextAscii(50);
    assertFalse(r1.equals(r2), "!r1.equals(r2)");

    r1 = rsu.nextAlphabetic(50);
    assertEquals(50, r1.length(), "randomAlphabetic(50)");
    for (int i = 0; i < r1.length(); i++) {
        assertTrue(Character.isLetter(r1.charAt(i)) && !Character.isDigit(r1.charAt(i)), "r1 contains alphabetic");
    }
    r2 = rsu.nextAlphabetic(50);
    assertFalse(r1.equals(r2), "!r1.equals(r2)");

    r1 = rsu.nextAlphanumeric(50);
    assertEquals(50, r1.length(), "randomAlphanumeric(50)");
    for (int i = 0; i < r1.length(); i++) {
        assertTrue(Character.isLetterOrDigit(r1.charAt(i)), "r1 contains alphanumeric");
    }
    r2 = rsu.nextAlphabetic(50);
    assertFalse(r1.equals(r2), "!r1.equals(r2)");

    r1 = rsu.nextGraph(50);
    assertEquals(50, r1.length(), "randomGraph(50) length");
    for (int i = 0; i < r1.length(); i++) {
        assertTrue(r1.charAt(i) >= 33 && r1.charAt(i) <= 126, "char between 33 and 126");
    }
    r2 = rsu.nextGraph(50);
    assertFalse(r1.equals(r2), "!r1.equals(r2)");

    r1 = rsu.nextNumeric(50);
    assertEquals(50, r1.length(), "randomNumeric(50)");
    for (int i = 0; i < r1.length(); i++) {
        assertTrue(Character.isDigit(r1.charAt(i)) && !Character.isLetter(r1.charAt(i)), "r1 contains numeric");
    }
    r2 = rsu.nextNumeric(50);
    assertFalse(r1.equals(r2), "!r1.equals(r2)");

    r1 = rsu.nextPrint(50);
    assertEquals(50, r1.length(), "randomPrint(50) length");
    for (int i = 0; i < r1.length(); i++) {
        assertTrue(r1.charAt(i) >= 32 && r1.charAt(i) <= 126, "char between 32 and 126");
    }
    r2 = rsu.nextPrint(50);
    assertFalse(r1.equals(r2), "!r1.equals(r2)");

    String set = "abcdefg";
    r1 = rsu.next(50, set);
    assertEquals(50, r1.length(), "random(50, \"abcdefg\")");
    for (int i = 0; i < r1.length(); i++) {
        assertTrue(set.indexOf(r1.charAt(i)) > -1, "random char in set");
    }
    r2 = rsu.next(50, set);
    assertFalse(r1.equals(r2), "!r1.equals(r2)");

    r1 = rsu.next(50, (String) null);
    assertEquals(50, r1.length(), "random(50) length");
    r2 = rsu.next(50, (String) null);
    assertEquals(50, r2.length(), "random(50) length");
    assertFalse(r1.equals(r2), "!r1.equals(r2)");

    set = "stuvwxyz";
    r1 = rsu.next(50, set.toCharArray());
    assertEquals(50, r1.length(), "random(50, \"stuvwxyz\")");
    for (int i = 0; i < r1.length(); i++) {
        assertTrue(set.indexOf(r1.charAt(i)) > -1, "random char in set");
    }
    r2 = rsu.next(50, set);
    assertFalse(r1.equals(r2), "!r1.equals(r2)");

    r1 = rsu.next(50, (char[]) null);
    assertEquals(50, r1.length(), "random(50) length");
    r2 = rsu.next(50, (char[]) null);
    assertEquals(50, r2.length(), "random(50) length");
    assertFalse(r1.equals(r2), "!r1.equals(r2)");

    r1 = rsu.next(0);
    assertEquals("", r1, "random(0).equals(\"\")");
}

@ParameterizedTest
@MethodSource("randomProvider")
public void testRandomAscii(final RandomStringUtils rsu) {
    final char[] testChars = { (char) 32, (char) 126 };
    final boolean[] found = { false, false };
    for (int i = 0; i < LOOP_COUNT; i++) {
        final String randString = rsu.nextAscii(10);
        for (int j = 0; j < testChars.length; j++) {
            if (randString.indexOf(testChars[j]) > 0) {
                found[j] = true;
            }
        }
    }
    for (int i = 0; i < testChars.length; i++) {
        assertTrue(found[i], "ascii character not generated in 1000 attempts: " + (int) testChars[i] + " -- repeated failures indicate a problem");
    }
}

@ParameterizedTest
@MethodSource("randomProvider")
public void testRandomAsciiRange(final RandomStringUtils rsu) {
    final int expectedMinLengthInclusive = 1;
    final int expectedMaxLengthExclusive = 11;
    final String pattern = "^\\p{ASCII}{" + expectedMinLengthInclusive + ',' + expectedMaxLengthExclusive + "}$";

    int maxCreatedLength = expectedMinLengthInclusive;
    int minCreatedLength = expectedMaxLengthExclusive - 1;
    for (int i = 0; i < LOOP_COUNT; i++) {
        final String s = rsu.nextAscii(expectedMinLengthInclusive, expectedMaxLengthExclusive);
        assertThat("within range", s.length(), allOf(greaterThanOrEqualTo(expectedMinLengthInclusive), lessThanOrEqualTo(expectedMaxLengthExclusive - 1)));
        assertTrue(s.matches(pattern), s);

        if (s.length() < minCreatedLength) {
            minCreatedLength = s.length();
        }

        if (s.length() > maxCreatedLength) {
            maxCreatedLength = s.length();
        }
    }
    assertThat("min generated, may fail randomly rarely", minCreatedLength, is(expectedMinLengthInclusive));
    assertThat("max generated, may fail randomly rarely", maxCreatedLength, is(expectedMaxLengthExclusive - 1));
}

@ParameterizedTest
@MethodSource("randomProvider")
public void testRandomGraphRange(final RandomStringUtils rsu) {
    final int expectedMinLengthInclusive = 1;
    final int expectedMaxLengthExclusive = 11;
    final String pattern = "^\\p{Graph}{" + expectedMinLengthInclusive + ',' + expectedMaxLengthExclusive + "}$";

    int maxCreatedLength = expectedMinLengthInclusive;
    int minCreatedLength = expectedMaxLengthExclusive - 1;
    for (int i = 0; i < LOOP_COUNT; i++) {
        final String s = rsu.nextGraph(expectedMinLengthInclusive, expectedMaxLengthExclusive);
        assertThat("within range", s.length(), allOf(greaterThanOrEqualTo(expectedMinLengthInclusive), lessThanOrEqualTo(expectedMaxLengthExclusive - 1)));
        assertTrue(s.matches(pattern), s);

        if (s.length() < minCreatedLength) {
            minCreatedLength = s.length();
        }

        if (s.length() > maxCreatedLength) {
            maxCreatedLength = s.length();
        }
    }
    assertThat("min generated, may fail randomly rarely", minCreatedLength, is(expectedMinLengthInclusive));
    assertThat("max generated, may fail randomly rarely", maxCreatedLength, is(expectedMaxLengthExclusive - 1));
}

@ParameterizedTest
@MethodSource("randomProvider")
public void testRandomNumeric(final RandomStringUtils rsu) {
    final char[] testChars = { '0', '9' };
    final boolean[] found = { false, false };
    for (int i = 0; i < LOOP_COUNT; i++) {
        final String randString = rsu.nextNumeric(10);
        for (int j = 0; j < testChars.length; j++) {
            if (randString.indexOf(testChars[j]) > 0) {
                found[j] = true;
            }
        }
    }
    for (int i = 0; i < testChars.length; i++) {
        assertTrue(found[i], "digit not generated in 1000 attempts: " + testChars[i] + " -- repeated failures indicate a problem ");
    }
}

@ParameterizedTest
@MethodSource("randomProvider")
public void testRandomNumericRange(final RandomStringUtils rsu) {
    final int expectedMinLengthInclusive = 1;
    final int expectedMaxLengthExclusive = 11;
    final String pattern = "^\\p{Digit}{" + expectedMinLengthInclusive + ',' + expectedMaxLengthExclusive + "}$";

    int maxCreatedLength = expectedMinLengthInclusive;
    int minCreatedLength = expectedMaxLengthExclusive - 1;
    for (int i = 0; i < LOOP_COUNT; i++) {
        final String s = rsu.nextNumeric(expectedMinLengthInclusive, expectedMaxLengthExclusive);
        assertThat("within range", s.length(), allOf(greaterThanOrEqualTo(expectedMinLengthInclusive), lessThanOrEqualTo(expectedMaxLengthExclusive - 1)));
        assertTrue(s.matches(pattern), s);

        if (s.length() < minCreatedLength) {
            minCreatedLength = s.length();
        }

        if (s.length() > maxCreatedLength) {
            maxCreatedLength = s.length();
        }
    }
    assertThat("min generated, may fail randomly rarely", minCreatedLength, is(expectedMinLengthInclusive));
    assertThat("max generated, may fail randomly rarely", maxCreatedLength, is(expectedMaxLengthExclusive - 1));
}

@Test
public void testRandomParameter() {
    final long seedMillis = System.currentTimeMillis();
    final String r1 = RandomStringUtils.random(50, 0, 0, true, true, null, new Random(seedMillis));
    final String r2 = RandomStringUtils.random(50, 0, 0, true, true, null, new Random(seedMillis));
    assertEquals(r1, r2, "r1.equals(r2)");
}

@ParameterizedTest
@MethodSource("randomProvider")
public void testRandomPrintRange(final RandomStringUtils rsu) {
    final int expectedMinLengthInclusive = 1;
    final int expectedMaxLengthExclusive = 11;
    final String pattern = "^\\p{Print}{" + expectedMinLengthInclusive + ',' + expectedMaxLengthExclusive + "}$";

    int maxCreatedLength = expectedMinLengthInclusive;
    int minCreatedLength = expectedMaxLengthExclusive - 1;
    for (int i = 0; i < LOOP_COUNT; i++) {
        final String s = rsu.nextPrint(expectedMinLengthInclusive, expectedMaxLengthExclusive);
        assertThat("within range", s.length(), allOf(greaterThanOrEqualTo(expectedMinLengthInclusive), lessThanOrEqualTo(expectedMaxLengthExclusive - 1)));
        assertTrue(s.matches(pattern), s);

        if (s.length() < minCreatedLength) {
            minCreatedLength = s.length();
        }

        if (s.length() > maxCreatedLength) {
            maxCreatedLength = s.length();
        }
    }
    assertThat("min generated, may fail randomly rarely", minCreatedLength, is(expectedMinLengthInclusive));
    assertThat("max generated, may fail randomly rarely", maxCreatedLength, is(expectedMaxLengthExclusive - 1));
}

@ParameterizedTest
@MethodSource("randomProvider")
public void testRandomWithChars(final RandomStringUtils rsu) {
    final char[] digitChars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};

    String r1, r2, r3;

    r1 = rsu.next(50, 0, 0, true, true, digitChars);
    assertEquals(50, r1.length(), "randomNumeric(50)");
    for (int i = 0; i < r1.length(); i++) {
        assertTrue(
                Character.isDigit(r1.charAt(i)) && !Character.isLetter(r1.charAt(i)),
                "r1 contains numeric");
    }
    r2 = rsu.nextNumeric(50);
    assertNotEquals(r1, r2);

    r3 = rsu.next(50, 0, 0, true, true, digitChars);
    assertNotEquals(r1, r3);
    assertNotEquals(r2, r3);
}
```