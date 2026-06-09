# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `1169aac7a1a7bc056c37369892f638e137bff3e8`
- B: `ec2fa6bd5695b36435cc66ca4cdd8183d077a0cf`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `29907`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7647, 'completion_tokens': 2140, 'total_tokens': 9787}`

---

- 新增 `testRandomAsciiRange`，覆盖新增的 `randomAscii(int minLengthInclusive, int maxLengthExclusive)` 长度范围重载，并校验字符类别。
- 新增 `testRandomAlphabeticRange`，覆盖新增的 `randomAlphabetic(int minLengthInclusive, int maxLengthExclusive)` 长度范围重载，并校验字符类别。
- 新增 `testRandomAlphanumericRange`，覆盖新增的 `randomAlphanumeric(int minLengthInclusive, int maxLengthExclusive)` 长度范围重载，并校验字符类别。
- 新增 `testRandomGraphRange`，覆盖新增的 `randomGraph(int minLengthInclusive, int maxLengthExclusive)` 长度范围重载，并校验字符类别。
- 新增 `testRandomNumericRange`，覆盖新增的 `randomNumeric(int minLengthInclusive, int maxLengthExclusive)` 长度范围重载，并校验字符类别。
- 新增 `testRandomPrintRange`，覆盖新增的 `randomPrint(int minLengthInclusive, int maxLengthExclusive)` 长度范围重载，并校验字符类别。
- 需要调整 import：新增 Hamcrest matcher 静态导入以及 `assertThat` 静态导入。

```java
// IMPORTS_START
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.greaterThanOrEqualTo;
import static org.hamcrest.Matchers.is;
import static org.hamcrest.Matchers.lessThanOrEqualTo;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.nio.charset.Charset;
import java.util.Random;

import org.junit.Test;
// IMPORTS_END

@Test
public void testRandomAsciiRange() {
    final int expectedMinLengthInclusive = 1;
    final int expectedMaxLengthExclusive = 11;
    final String pattern = "^\\p{ASCII}{" + expectedMinLengthInclusive + ',' + expectedMaxLengthExclusive + "}$";

    int maxCreatedLength = expectedMinLengthInclusive;
    int minCreatedLength = expectedMaxLengthExclusive - 1;
    for (int i = 0; i < 1000; i++) {
        final String s = RandomStringUtils.randomAscii(expectedMinLengthInclusive, expectedMaxLengthExclusive);
        assertThat("within range", s.length(), allOf(greaterThanOrEqualTo(expectedMinLengthInclusive), lessThanOrEqualTo(expectedMaxLengthExclusive - 1)));
        assertTrue(s, s.matches(pattern));

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
public void testRandomAlphabeticRange() {
    final int expectedMinLengthInclusive = 1;
    final int expectedMaxLengthExclusive = 11;
    final String pattern = "^\\p{Alpha}{" + expectedMinLengthInclusive + ',' + expectedMaxLengthExclusive + "}$";

    int maxCreatedLength = expectedMinLengthInclusive;
    int minCreatedLength = expectedMaxLengthExclusive - 1;
    for (int i = 0; i < 1000; i++) {
        final String s = RandomStringUtils.randomAlphabetic(expectedMinLengthInclusive, expectedMaxLengthExclusive);
        assertThat("within range", s.length(), allOf(greaterThanOrEqualTo(expectedMinLengthInclusive), lessThanOrEqualTo(expectedMaxLengthExclusive - 1)));
        assertTrue(s, s.matches(pattern));

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
public void testRandomAlphanumericRange() {
    final int expectedMinLengthInclusive = 1;
    final int expectedMaxLengthExclusive = 11;
    final String pattern = "^\\p{Alnum}{" + expectedMinLengthInclusive + ',' + expectedMaxLengthExclusive + "}$";

    int maxCreatedLength = expectedMinLengthInclusive;
    int minCreatedLength = expectedMaxLengthExclusive - 1;
    for (int i = 0; i < 1000; i++) {
        final String s = RandomStringUtils.randomAlphanumeric(expectedMinLengthInclusive, expectedMaxLengthExclusive);
        assertThat("within range", s.length(), allOf(greaterThanOrEqualTo(expectedMinLengthInclusive), lessThanOrEqualTo(expectedMaxLengthExclusive - 1)));
        assertTrue(s, s.matches(pattern));

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
public void testRandomGraphRange() {
    final int expectedMinLengthInclusive = 1;
    final int expectedMaxLengthExclusive = 11;
    final String pattern = "^\\p{Graph}{" + expectedMinLengthInclusive + ',' + expectedMaxLengthExclusive + "}$";

    int maxCreatedLength = expectedMinLengthInclusive;
    int minCreatedLength = expectedMaxLengthExclusive - 1;
    for (int i = 0; i < 1000; i++) {
        final String s = RandomStringUtils.randomGraph(expectedMinLengthInclusive, expectedMaxLengthExclusive);
        assertThat("within range", s.length(), allOf(greaterThanOrEqualTo(expectedMinLengthInclusive), lessThanOrEqualTo(expectedMaxLengthExclusive - 1)));
        assertTrue(s, s.matches(pattern));

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
public void testRandomNumericRange() {
    final int expectedMinLengthInclusive = 1;
    final int expectedMaxLengthExclusive = 11;
    final String pattern = "^\\p{Digit}{" + expectedMinLengthInclusive + ',' + expectedMaxLengthExclusive + "}$";

    int maxCreatedLength = expectedMinLengthInclusive;
    int minCreatedLength = expectedMaxLengthExclusive - 1;
    for (int i = 0; i < 1000; i++) {
        final String s = RandomStringUtils.randomNumeric(expectedMinLengthInclusive, expectedMaxLengthExclusive);
        assertThat("within range", s.length(), allOf(greaterThanOrEqualTo(expectedMinLengthInclusive), lessThanOrEqualTo(expectedMaxLengthExclusive - 1)));
        assertTrue(s, s.matches(pattern));

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
public void testRandomPrintRange() {
    final int expectedMinLengthInclusive = 1;
    final int expectedMaxLengthExclusive = 11;
    final String pattern = "^\\p{Print}{" + expectedMinLengthInclusive + ',' + expectedMaxLengthExclusive + "}$";

    int maxCreatedLength = expectedMinLengthInclusive;
    int minCreatedLength = expectedMaxLengthExclusive - 1;
    for (int i = 0; i < 1000; i++) {
        final String s = RandomStringUtils.randomPrint(expectedMinLengthInclusive, expectedMaxLengthExclusive);
        assertThat("within range", s.length(), allOf(greaterThanOrEqualTo(expectedMinLengthInclusive), lessThanOrEqualTo(expectedMaxLengthExclusive - 1)));
        assertTrue(s, s.matches(pattern));

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
```