# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `df4be6cd6e2a8bba13095a4415cfbc80abfbbe5b`
- B: `328f2aedfb8643c3e1e74b5aec9e3628c3cbf2e7`
- test: `src/test/java/org/apache/commons/lang3/time/CalendarUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/CalendarUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `8104`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2376, 'completion_tokens': 639, 'total_tokens': 3015}`

---

- 新增 `@ParameterizedTest` 方法 `testToLocalDateTime`，覆盖新增的 `CalendarUtils.toLocalDateTime()` 实例转换行为并按所有可用时区验证。
- 需要调整 import：新增 `java.time.*`、`GregorianCalendar`、`TimeZone` 以及 JUnit 5 参数化测试相关 import。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Calendar;
import java.util.GregorianCalendar;
import java.util.Locale;
import java.util.TimeZone;

import org.apache.commons.lang3.AbstractLangTest;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
// IMPORTS_END

    @ParameterizedTest
    @MethodSource("java.util.TimeZone#getAvailableIDs()")
    public void testToLocalDateTime(final String id) {
        final TimeZone timeZone = TimeZone.getTimeZone(id);
        final ZoneId zoneId = timeZone.toZoneId();
        final Calendar calendar = new GregorianCalendar(timeZone);
        calendar.setTimeInMillis(0);
        assertEquals(LocalDateTime.ofInstant(calendar.toInstant(), calendar.getTimeZone().toZoneId()), new CalendarUtils(calendar).toLocalDateTime());
        final ZonedDateTime zdt1 = ZonedDateTime.of(1, 2, 3, 4, 5, 6, 0, zoneId);
        calendar.setTimeInMillis(zdt1.toInstant().toEpochMilli());
        assertEquals(LocalDateTime.ofInstant(zdt1.toInstant(), calendar.getTimeZone().toZoneId()), new CalendarUtils(calendar).toLocalDateTime());
    }
```