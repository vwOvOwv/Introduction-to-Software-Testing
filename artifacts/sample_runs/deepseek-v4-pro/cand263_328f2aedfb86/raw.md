# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `df4be6cd6e2a8bba13095a4415cfbc80abfbbe5b`
- B: `328f2aedfb8643c3e1e74b5aec9e3628c3cbf2e7`
- test: `src/test/java/org/apache/commons/lang3/time/CalendarUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/CalendarUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `8104`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2390, 'completion_tokens': 3160, 'total_tokens': 5550, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2681}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2006}`

---

- 新增常量 `TIME_ZONE_GET_AVAILABLE_IDS`，用于 `@MethodSource` 提供时区 ID。
- 新增参数化测试方法 `testToLocalDateTime(String id)`，验证 `CalendarUtils#toLocalDateTime()` 实例方法与静态方法。
- 新增 import：`java.time.LocalDateTime`、`java.time.ZoneId`、`java.time.ZonedDateTime`、`java.util.GregorianCalendar`、`java.util.TimeZone`、`org.junit.jupiter.params.ParameterizedTest`、`org.junit.jupiter.params.provider.MethodSource`。
- 原有测试方法无需修改，无需删除。

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

    private static final String TIME_ZONE_GET_AVAILABLE_IDS = "java.util.TimeZone#getAvailableIDs()";

    @ParameterizedTest
    @MethodSource(TIME_ZONE_GET_AVAILABLE_IDS)
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