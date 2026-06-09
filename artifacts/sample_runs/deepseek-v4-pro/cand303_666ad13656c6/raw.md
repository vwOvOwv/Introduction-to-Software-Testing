# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `328f2aedfb8643c3e1e74b5aec9e3628c3cbf2e7`
- B: `666ad13656c690b310fc2c6487dd60b6ed72a5ed`
- test: `src/test/java/org/apache/commons/lang3/time/CalendarUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/CalendarUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `8858`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2598, 'completion_tokens': 1114, 'total_tokens': 3712, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 857}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2214}`

---

- 新增 `@ParameterizedTest` 方法 `testToZonedDateTime`，对应生产代码新增的 `toZonedDateTime` 静态方法与实例方法。
- 无需调整 import，旧的测试类已包含所需的所有类型。

```java
@ParameterizedTest
@MethodSource(TIME_ZONE_GET_AVAILABLE_IDS)
public void testToZonedDateTime(final String id) {
    final TimeZone timeZone = TimeZone.getTimeZone(id);
    final ZoneId zoneId = timeZone.toZoneId();
    final Calendar calendar = new GregorianCalendar(timeZone);
    calendar.setTimeInMillis(0);
    assertEquals(ZonedDateTime.ofInstant(calendar.toInstant(), calendar.getTimeZone().toZoneId()), new CalendarUtils(calendar).toZonedDateTime());
    final ZonedDateTime zdt1 = ZonedDateTime.of(1, 2, 3, 4, 5, 6, 0, zoneId);
    calendar.setTimeInMillis(zdt1.toInstant().toEpochMilli());
    assertEquals(ZonedDateTime.ofInstant(zdt1.toInstant(), calendar.getTimeZone().toZoneId()), new CalendarUtils(calendar).toZonedDateTime());
}
```