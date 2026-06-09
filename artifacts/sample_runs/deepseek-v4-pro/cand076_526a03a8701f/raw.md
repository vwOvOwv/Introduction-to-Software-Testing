# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cc54667ce1ee7d4cbddd836d14467d1569b4057f`
- B: `526a03a8701f85e422786f0a4d1fadd3f0c249c1`
- test: `src/test/java/org/apache/commons/lang3/time/DateUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DateUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `93081`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 25848, 'completion_tokens': 1525, 'total_tokens': 27373, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 548}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 25464}`

---

- 新增 `@Test` 方法 `testFailedTimeZonePatternDoesNotPoisonNextPatternInstant`，用于验证修复时区泄漏的生产代码变更；该方法与人类金标准测试一致，无需调整已有方法或 import。

```java
    /**
     * Failed date parse can poison the calendar's time zone for the next pattern.
     *
     * <p>
     * {@link DateUtils#parseDateWithLeniency} reuses a single {@link Calendar} across pattern attempts. The reset between iterations is
     * {@link Calendar#clear()}, which does NOT reset the calendar's time zone. A TZ-aware pattern (e.g. starts with {@code "X"}, {@code "Z"}, {@code "z"}) that
     * successfully consumes its TZ token (mutating the calendar via {@link Calendar#setTimeZone}) before failing on later tokens leaves the calendar carrying
     * the parsed (foreign) zone. The next pattern in the list then interprets its date fields against that zone, producing a wrong instant.
     * </p>
     *
     * <p>
     * <b>Construction:</b> input {@code "+0500 01/01/2024"} is parsed against two patterns:
     * </p>
     * <ol>
     * <li>{@code "Z 'X' MM/dd/yyyy"}: the {@code Z} strategy consumes {@code "+0500"} and calls {@code calendar.setTimeZone(GMT+05:00)}; the next literal
     * {@code 'X'} fails to match {@code " 01"}, so the overall parse returns false. The leaked TZ remains on the shared calendar.</li>
     * <li>{@code "'+0500 'MM/dd/yyyy"}: a TZ-less pattern that absorbs the literal prefix and parses the date. With the bug, the calendar still carries
     * GMT+05:00, so the date is interpreted as midnight in GMT+05:00 (5 hours earlier as an instant) than the same date interpreted in the system default
     * zone.</li>
     * </ol>
     *
     * <p>
     * The assertion compares {@link Date#getTime()} against a baseline parse using only the second pattern. A naive PoC that only checked calendar fields
     * (year/month/day) would not detect the bug because those equal in both runs.
     * </p>
     *
     * <p>
     * Pre-patch: the bug shifts the resulting instant by 5 hours.<br>
     * Post-patch: {@code parseDateWithLeniency} restores {@code calendar.setTimeZone(TimeZone.getDefault())} before each iteration, so the leaked zone never
     * reaches the second attempt and both instants match.
     * </p>
     */
    @Test
    public void testFailedTimeZonePatternDoesNotPoisonNextPatternInstant() throws Exception {
        final String input = "+0500 01/01/2024";
        // Baseline: a single TZ-less pattern; no leak source. The calendar uses
        // TimeZone.getDefault(), so the result is midnight 2024-01-01 in the default zone.
        final Date baseline = DateUtils.parseDate(input, "'+0500 'MM/dd/yyyy");
        assertNotNull(baseline, "baseline parse must succeed");
        // Poisoning sequence:
        //   pattern 1 = "Z 'X' MM/dd/yyyy"  -> Z consumes "+0500" then setTimeZone(GMT+05:00),
        //                                       'X' literal mismatches " 01", returns false.
        //   pattern 2 = "'+0500 'MM/dd/yyyy"-> matches the whole input via literal prefix +
        //                                       MM/dd/yyyy. With the bug, calendar still has
        //                                       GMT+05:00 leaked from pattern 1, so the date
        //                                       is interpreted in GMT+05:00 instead of default.
        final Date poisoned = DateUtils.parseDate(input, "Z 'X' MM/dd/yyyy", "'+0500 'MM/dd/yyyy");
        assertNotNull(poisoned, "poisoning sequence parse must succeed via the second pattern");
        // Compare INSTANTS, not Y/M/D. Calendar fields equal in both runs by coincidence
        // even when the bug shifts the underlying instant.
        assertEquals(baseline.getTime(), poisoned.getTime(),
                "Calendar TZ leaked from a failed prior pattern must not affect the instant produced by a subsequent TZ-less pattern");
    }
```