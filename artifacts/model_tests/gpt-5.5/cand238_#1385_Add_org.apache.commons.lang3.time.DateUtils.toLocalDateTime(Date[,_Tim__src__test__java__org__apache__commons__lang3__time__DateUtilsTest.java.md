# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `70d5058caa22063049c590bf90ec9585915bf6dc`
- B: `0c6a5c10a7a0f0073b6577e5c4898ceb42428b55`
- test: `src/test/java/org/apache/commons/lang3/time/DateUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DateUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `82882`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 22352, 'completion_tokens': 1177, 'total_tokens': 23529}`

---

- 新增 `testToLocalDateTimeTimeZone` 及其 `MethodSource` 工厂方法 `testToLocalDateTimeTimeZone`，用于覆盖新增的 `DateUtils.toLocalDateTime(Date, TimeZone)`，包括显式时区、默认时区和 DST 场景。
- 新增 `testToLocalDateTime`，用于覆盖新增的 `DateUtils.toLocalDateTime(Date)` 默认时区重载。
- 需要调整 import：新增 `java.time.LocalDateTime`、`java.time.ZoneId`、`java.time.ZoneOffset`、`java.util.stream.Stream` 以及 JUnit 5 参数化测试相关 import。

```java
// IMPORTS_START
import static org.apache.commons.lang3.LangAssertions.assertIllegalArgumentException;
import static org.apache.commons.lang3.LangAssertions.assertNullPointerException;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.Iterator;
import java.util.Locale;
import java.util.NoSuchElementException;
import java.util.TimeZone;
import java.util.stream.Stream;

import org.apache.commons.lang3.AbstractLangTest;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.junitpioneer.jupiter.DefaultLocale;
import org.junitpioneer.jupiter.ReadsDefaultLocale;
import org.junitpioneer.jupiter.WritesDefaultLocale;
// IMPORTS_END

private static Stream<Arguments> testToLocalDateTimeTimeZone() {
    // @formatter:off
    return Stream.of(
            Arguments.of(
                    LocalDateTime.ofInstant(
                            java.sql.Timestamp.valueOf("2000-01-01 12:30:45").toInstant(),
                            TimeZone.getTimeZone("America/New_York").toZoneId()
                    ),
                    java.sql.Timestamp.valueOf("2000-01-01 12:30:45"),
                    TimeZone.getTimeZone("America/New_York")
            ),
            Arguments.of(
                    LocalDateTime.ofInstant(
                            java.sql.Timestamp.valueOf("2023-03-12 02:30:00").toInstant(),
                            TimeZone.getTimeZone("America/New_York").toZoneId()
                    ),
                    java.sql.Timestamp.valueOf("2023-03-12 02:30:00"),
                    TimeZone.getTimeZone("America/New_York")
            ),
            Arguments.of(
                    LocalDateTime.ofInstant(
                            java.sql.Timestamp.valueOf("2023-03-12 02:30:00").toInstant(),
                            TimeZone.getDefault().toZoneId()
                    ),
                    java.sql.Timestamp.valueOf("2023-03-12 02:30:00"),
                    null
            ),
            Arguments.of(
                    LocalDateTime.of(2022, 12, 31, 19, 0),
                    Date.from(LocalDateTime.of(2023, 1, 1, 0, 0)
                            .atOffset(ZoneOffset.UTC)
                            .toInstant()),
                    TimeZone.getTimeZone("America/New_York")
            ),
            Arguments.of(
                    LocalDateTime.of(2023, 3, 12, 3, 0),
                    Date.from(LocalDateTime.of(2023, 3, 12, 7, 0)
                            .atOffset(ZoneOffset.UTC)
                            .toInstant()),
                    TimeZone.getTimeZone("America/New_York")
            ),
            Arguments.of(
                    LocalDateTime.of(2023, 1, 1, 14, 0),
                    Date.from(LocalDateTime.of(2023, 1, 1, 0, 0)
                            .atOffset(ZoneOffset.UTC)
                            .toInstant()),
                    TimeZone.getTimeZone("Pacific/Kiritimati")
            )
    );
    // @formatter:on
}

@ParameterizedTest
@MethodSource
void testToLocalDateTimeTimeZone(final LocalDateTime expected, final Date date, final TimeZone timeZone) {
    assertEquals(expected, DateUtils.toLocalDateTime(date, timeZone));
}

@Test
void testToLocalDateTime() {
    final Date date = new Date();
    assertEquals(LocalDateTime.ofInstant(date.toInstant(), ZoneId.systemDefault()), DateUtils.toLocalDateTime(date));
}
```