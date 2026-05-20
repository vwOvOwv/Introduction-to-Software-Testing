# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `70d5058caa22063049c590bf90ec9585915bf6dc`
- B: `0c6a5c10a7a0f0073b6577e5c4898ceb42428b55`
- test: `src/test/java/org/apache/commons/lang3/time/DateUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DateUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `83153`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 23424, 'completion_tokens': 807, 'total_tokens': 24231, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 23168}`

---

- 新增 `testToLocalDateTime()` 和 `testToLocalDateTimeTimeZone()` 两个测试方法，对应生产代码新增的 `toLocalDateTime` 方法。
- 新增 `import java.time.LocalDateTime;`、`import java.time.ZoneId;`、`import java.time.ZoneOffset;`、`import java.util.stream.Stream;`、`import org.junit.jupiter.params.ParameterizedTest;`、`import org.junit.jupiter.params.provider.Arguments;`、`import org.junit.jupiter.params.provider.MethodSource;` 以支持新测试。

```java
// IMPORTS_START
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.util.stream.Stream;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
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