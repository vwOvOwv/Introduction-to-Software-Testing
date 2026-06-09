# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `d21a59baa559f57ead53a5bab22d60333dc46041`
- B: `2288b0ff2cce401f510ae9e208fcf1698f4bce79`
- test: `src/test/java/org/apache/commons/lang3/time/DateUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DateUtils.java']`
- old_test_mode: `methods`
- user_chars: `45581`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 17615, 'completion_tokens': 5673, 'total_tokens': 23288, 'prompt_tokens_details': {'cached_tokens': 11520}, 'completion_tokens_details': {'reasoning_tokens': 2417}, 'prompt_cache_hit_tokens': 11520, 'prompt_cache_miss_tokens': 6095}`

---

- 更新 `testCeil` 方法中的注释 `// Fix for http://issues.apache.org/bugzilla/show_bug.cgi?id=25560` 为 `// Fix for https://issues.apache.org/bugzilla/show_bug.cgi?id=25560`，以匹配测试 diff 的 URL 协议变更为 HTTPS。
- 更新 `testRound` 方法中的注释 `// Fix for http://issues.apache.org/bugzilla/show_bug.cgi?id=25560 / LANG-13` 为 `// Fix for https://issues.apache.org/bugzilla/show_bug.cgi?id=25560 / LANG-13`，以匹配测试 diff 的 URL 协议变更为 HTTPS。
- 更新 `testTruncate` 方法中的注释 `// Fix for http://issues.apache.org/bugzilla/show_bug.cgi?id=25560` 为 `// Fix for https://issues.apache.org/bugzilla/show_bug.cgi?id=25560`，以匹配测试 diff 的 URL 协议变更为 HTTPS。
- 更新 `testLang530` 方法中的注释 `// http://issues.apache.org/jira/browse/LANG-530` 为 `// https://issues.apache.org/jira/browse/LANG-530`，以匹配测试 diff 的 URL 协议变更为 HTTPS。
- 无需新增或删除 import，无需删除任何测试方法。

```java
@Test
public void testCeil() throws Exception {
    // test javadoc
    assertEquals(dateTimeParser.parse("March 28, 2002 14:00:00.000"),
            DateUtils.ceiling(
                        dateTimeParser.parse("March 28, 2002 13:45:01.231"),
                    Calendar.HOUR),
            "ceiling javadoc-1 failed");
    assertEquals(dateTimeParser.parse("April 1, 2002 00:00:00.000"),
            DateUtils.ceiling(
                        dateTimeParser.parse("March 28, 2002 13:45:01.231"),
                    Calendar.MONTH),
            "ceiling javadoc-2 failed");

    // tests public static Date ceiling(Date date, int field)
    assertEquals(dateParser.parse("January 1, 2003"),
            DateUtils.ceiling(date1, Calendar.YEAR),
            "ceiling year-1 failed");
    assertEquals(dateParser.parse("January 1, 2002"),
            DateUtils.ceiling(date2, Calendar.YEAR),
            "ceiling year-2 failed");
    assertEquals(dateParser.parse("March 1, 2002"),
            DateUtils.ceiling(date1, Calendar.MONTH),
            "ceiling month-1 failed");
    assertEquals(dateParser.parse("December 1, 2001"),
            DateUtils.ceiling(date2, Calendar.MONTH),
            "ceiling month-2 failed");
    assertEquals(dateParser.parse("February 16, 2002"),
            DateUtils.ceiling(date1, DateUtils.SEMI_MONTH),
            "ceiling semimonth-1 failed");
    assertEquals(dateParser.parse("December 1, 2001"),
            DateUtils.ceiling(date2, DateUtils.SEMI_MONTH),
            "ceiling semimonth-2 failed");
    assertEquals(dateParser.parse("February 13, 2002"),
            DateUtils.ceiling(date1, Calendar.DATE),
            "ceiling date-1 failed");
    assertEquals(dateParser.parse("November 19, 2001"),
            DateUtils.ceiling(date2, Calendar.DATE),
            "ceiling date-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 13:00:00.000"),
            DateUtils.ceiling(date1, Calendar.HOUR),
            "ceiling hour-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 2:00:00.000"),
            DateUtils.ceiling(date2, Calendar.HOUR),
            "ceiling hour-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:35:00.000"),
            DateUtils.ceiling(date1, Calendar.MINUTE),
            "ceiling minute-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:24:00.000"),
            DateUtils.ceiling(date2, Calendar.MINUTE),
            "ceiling minute-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:34:57.000"),
            DateUtils.ceiling(date1, Calendar.SECOND),
            "ceiling second-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:23:12.000"),
            DateUtils.ceiling(date2, Calendar.SECOND),
            "ceiling second-2 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.ceiling(dateAmPm1, Calendar.AM_PM),
            "ceiling ampm-1 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.ceiling(dateAmPm2, Calendar.AM_PM),
            "ceiling ampm-2 failed");
    assertEquals(dateTimeParser.parse("February 4, 2002 00:00:00.000"),
            DateUtils.ceiling(dateAmPm3, Calendar.AM_PM),
            "ceiling ampm-3 failed");
    assertEquals(dateTimeParser.parse("February 4, 2002 00:00:00.000"),
            DateUtils.ceiling(dateAmPm4, Calendar.AM_PM),
            "ceiling ampm-4 failed");

 // tests public static Date ceiling(Object date, int field)
    assertEquals(dateParser.parse("January 1, 2003"),
            DateUtils.ceiling((Object) date1, Calendar.YEAR),
            "ceiling year-1 failed");
    assertEquals(dateParser.parse("January 1, 2002"),
            DateUtils.ceiling((Object) date2, Calendar.YEAR),
            "ceiling year-2 failed");
    assertEquals(dateParser.parse("March 1, 2002"),
            DateUtils.ceiling((Object) date1, Calendar.MONTH),
            "ceiling month-1 failed");
    assertEquals(dateParser.parse("December 1, 2001"),
            DateUtils.ceiling((Object) date2, Calendar.MONTH),
            "ceiling month-2 failed");
    assertEquals(dateParser.parse("February 16, 2002"),
            DateUtils.ceiling((Object) date1, DateUtils.SEMI_MONTH),
            "ceiling semimonth-1 failed");
    assertEquals(dateParser.parse("December 1, 2001"),
            DateUtils.ceiling((Object) date2, DateUtils.SEMI_MONTH),
            "ceiling semimonth-2 failed");
    assertEquals(dateParser.parse("February 13, 2002"),
            DateUtils.ceiling((Object) date1, Calendar.DATE),
            "ceiling date-1 failed");
    assertEquals(dateParser.parse("November 19, 2001"),
            DateUtils.ceiling((Object) date2, Calendar.DATE),
            "ceiling date-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 13:00:00.000"),
            DateUtils.ceiling((Object) date1, Calendar.HOUR),
            "ceiling hour-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 2:00:00.000"),
            DateUtils.ceiling((Object) date2, Calendar.HOUR),
            "ceiling hour-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:35:00.000"),
            DateUtils.ceiling((Object) date1, Calendar.MINUTE),
            "ceiling minute-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:24:00.000"),
            DateUtils.ceiling((Object) date2, Calendar.MINUTE),
            "ceiling minute-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:34:57.000"),
            DateUtils.ceiling((Object) date1, Calendar.SECOND),
            "ceiling second-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:23:12.000"),
            DateUtils.ceiling((Object) date2, Calendar.SECOND),
            "ceiling second-2 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.ceiling((Object) dateAmPm1, Calendar.AM_PM),
            "ceiling ampm-1 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.ceiling((Object) dateAmPm2, Calendar.AM_PM),
            "ceiling ampm-2 failed");
    assertEquals(dateTimeParser.parse("February 4, 2002 00:00:00.000"),
            DateUtils.ceiling((Object) dateAmPm3, Calendar.AM_PM),
            "ceiling ampm-3 failed");
    assertEquals(dateTimeParser.parse("February 4, 2002 00:00:00.000"),
            DateUtils.ceiling((Object) dateAmPm4, Calendar.AM_PM),
            "ceiling ampm-4 failed");

    assertEquals(dateTimeParser.parse("February 12, 2002 12:34:57.000"),
            DateUtils.ceiling((Object) cal1, Calendar.SECOND),
            "ceiling calendar second-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:23:12.000"),
            DateUtils.ceiling((Object) cal2, Calendar.SECOND),
            "ceiling calendar second-2 failed");

    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.ceiling((Object) calAmPm1, Calendar.AM_PM),
            "ceiling ampm-1 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.ceiling((Object) calAmPm2, Calendar.AM_PM),
            "ceiling ampm-2 failed");
    assertEquals(dateTimeParser.parse("February 4, 2002 00:00:00.000"),
            DateUtils.ceiling((Object) calAmPm3, Calendar.AM_PM),
            "ceiling ampm-3 failed");
    assertEquals(dateTimeParser.parse("February 4, 2002 00:00:00.000"),
            DateUtils.ceiling((Object) calAmPm4, Calendar.AM_PM),
            "ceiling ampm-4 failed");

    assertThrows(IllegalArgumentException.class, () -> DateUtils.ceiling((Date) null, Calendar.SECOND));
    assertThrows(IllegalArgumentException.class, () -> DateUtils.ceiling((Calendar) null, Calendar.SECOND));
    assertThrows(IllegalArgumentException.class, () -> DateUtils.ceiling((Object) null, Calendar.SECOND));
    assertThrows(ClassCastException.class, () -> DateUtils.ceiling("", Calendar.SECOND));
    assertThrows(IllegalArgumentException.class, () -> DateUtils.ceiling(date1, -9999));

    // Fix for https://issues.apache.org/bugzilla/show_bug.cgi?id=25560
    // Test ceiling across the beginning of daylight saving time
    try {
        TimeZone.setDefault(zone);
        dateTimeParser.setTimeZone(zone);

        assertEquals(dateTimeParser.parse("March 31, 2003 00:00:00.000"),
                DateUtils.ceiling(date4, Calendar.DATE),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 31, 2003 00:00:00.000"),
                DateUtils.ceiling((Object) cal4, Calendar.DATE),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 31, 2003 00:00:00.000"),
                DateUtils.ceiling(date5, Calendar.DATE),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 31, 2003 00:00:00.000"),
                DateUtils.ceiling((Object) cal5, Calendar.DATE),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 31, 2003 00:00:00.000"),
                DateUtils.ceiling(date6, Calendar.DATE),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 31, 2003 00:00:00.000"),
                DateUtils.ceiling((Object) cal6, Calendar.DATE),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 31, 2003 00:00:00.000"),
                DateUtils.ceiling(date7, Calendar.DATE),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 31, 2003 00:00:00.000"),
                DateUtils.ceiling((Object) cal7, Calendar.DATE),
                "ceiling MET date across DST change-over");

        assertEquals(dateTimeParser.parse("March 30, 2003 03:00:00.000"),
                DateUtils.ceiling(date4, Calendar.HOUR_OF_DAY),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 03:00:00.000"),
                DateUtils.ceiling((Object) cal4, Calendar.HOUR_OF_DAY),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 03:00:00.000"),
                DateUtils.ceiling(date5, Calendar.HOUR_OF_DAY),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 03:00:00.000"),
                DateUtils.ceiling((Object) cal5, Calendar.HOUR_OF_DAY),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 04:00:00.000"),
                DateUtils.ceiling(date6, Calendar.HOUR_OF_DAY),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 04:00:00.000"),
                DateUtils.ceiling((Object) cal6, Calendar.HOUR_OF_DAY),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 04:00:00.000"),
                DateUtils.ceiling(date7, Calendar.HOUR_OF_DAY),
                "ceiling MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 04:00:00.000"),
                DateUtils.ceiling((Object) cal7, Calendar.HOUR_OF_DAY),
                "ceiling MET date across DST change-over");

    } finally {
        TimeZone.setDefault(defaultZone);
        dateTimeParser.setTimeZone(defaultZone);
    }

 // Bug 31395, large dates
    final Date endOfTime = new Date(Long.MAX_VALUE); // fyi: Sun Aug 17 07:12:55 CET 292278994 -- 807 millis
    final GregorianCalendar endCal = new GregorianCalendar();
    endCal.setTime(endOfTime);
    assertThrows(ArithmeticException.class, () -> DateUtils.ceiling(endCal, Calendar.DATE));
    endCal.set(Calendar.YEAR, 280000001);
    assertThrows(ArithmeticException.class, () -> DateUtils.ceiling(endCal, Calendar.DATE));
    endCal.set(Calendar.YEAR, 280000000);
    final Calendar cal = DateUtils.ceiling(endCal, Calendar.DATE);
    assertEquals(0, cal.get(Calendar.HOUR));
}

@Test
public void testRound() throws Exception {
    // tests for public static Date round(Date date, int field)
    assertEquals(dateParser.parse("January 1, 2002"),
            DateUtils.round(date1, Calendar.YEAR),
            "round year-1 failed");
    assertEquals(dateParser.parse("January 1, 2002"),
            DateUtils.round(date2, Calendar.YEAR),
            "round year-2 failed");
    assertEquals(dateParser.parse("February 1, 2002"),
            DateUtils.round(date1, Calendar.MONTH),
            "round month-1 failed");
    assertEquals(dateParser.parse("December 1, 2001"),
            DateUtils.round(date2, Calendar.MONTH),
            "round month-2 failed");
    assertEquals(dateParser.parse("February 1, 2002"),
            DateUtils.round(date0, DateUtils.SEMI_MONTH),
            "round semimonth-0 failed");
    assertEquals(dateParser.parse("February 16, 2002"),
            DateUtils.round(date1, DateUtils.SEMI_MONTH),
            "round semimonth-1 failed");
    assertEquals(dateParser.parse("November 16, 2001"),
            DateUtils.round(date2, DateUtils.SEMI_MONTH),
            "round semimonth-2 failed");


    assertEquals(dateParser.parse("February 13, 2002"),
            DateUtils.round(date1, Calendar.DATE),
            "round date-1 failed");
    assertEquals(dateParser.parse("November 18, 2001"),
            DateUtils.round(date2, Calendar.DATE),
            "round date-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 13:00:00.000"),
            DateUtils.round(date1, Calendar.HOUR),
            "round hour-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:00:00.000"),
            DateUtils.round(date2, Calendar.HOUR),
            "round hour-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:35:00.000"),
            DateUtils.round(date1, Calendar.MINUTE),
            "round minute-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:23:00.000"),
            DateUtils.round(date2, Calendar.MINUTE),
            "round minute-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:34:57.000"),
            DateUtils.round(date1, Calendar.SECOND),
            "round second-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:23:11.000"),
            DateUtils.round(date2, Calendar.SECOND),
            "round second-2 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 00:00:00.000"),
            DateUtils.round(dateAmPm1, Calendar.AM_PM),
            "round ampm-1 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.round(dateAmPm2, Calendar.AM_PM),
            "round ampm-2 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.round(dateAmPm3, Calendar.AM_PM),
            "round ampm-3 failed");
    assertEquals(dateTimeParser.parse("February 4, 2002 00:00:00.000"),
            DateUtils.round(dateAmPm4, Calendar.AM_PM),
            "round ampm-4 failed");

    // tests for public static Date round(Object date, int field)
    assertEquals(dateParser.parse("January 1, 2002"),
            DateUtils.round((Object) date1, Calendar.YEAR),
            "round year-1 failed");
    assertEquals(dateParser.parse("January 1, 2002"),
            DateUtils.round((Object) date2, Calendar.YEAR),
            "round year-2 failed");
    assertEquals(dateParser.parse("February 1, 2002"),
            DateUtils.round((Object) date1, Calendar.MONTH),
            "round month-1 failed");
    assertEquals(dateParser.parse("December 1, 2001"),
            DateUtils.round((Object) date2, Calendar.MONTH),
            "round month-2 failed");
    assertEquals(dateParser.parse("February 16, 2002"),
            DateUtils.round((Object) date1, DateUtils.SEMI_MONTH),
            "round semimonth-1 failed");
    assertEquals(dateParser.parse("November 16, 2001"),
            DateUtils.round((Object) date2, DateUtils.SEMI_MONTH),
            "round semimonth-2 failed");
    assertEquals(dateParser.parse("February 13, 2002"),
            DateUtils.round((Object) date1, Calendar.DATE),
            "round date-1 failed");
    assertEquals(dateParser.parse("November 18, 2001"),
            DateUtils.round((Object) date2, Calendar.DATE),
            "round date-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 13:00:00.000"),
            DateUtils.round((Object) date1, Calendar.HOUR),
            "round hour-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:00:00.000"),
            DateUtils.round((Object) date2, Calendar.HOUR),
            "round hour-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:35:00.000"),
            DateUtils.round((Object) date1, Calendar.MINUTE),
            "round minute-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:23:00.000"),
            DateUtils.round((Object) date2, Calendar.MINUTE),
            "round minute-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:34:57.000"),
            DateUtils.round((Object) date1, Calendar.SECOND),
            "round second-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:23:11.000"),
            DateUtils.round((Object) date2, Calendar.SECOND),
            "round second-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:34:57.000"),
            DateUtils.round((Object) cal1, Calendar.SECOND),
            "round calendar second-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:23:11.000"),
            DateUtils.round((Object) cal2, Calendar.SECOND),
            "round calendar second-2 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 00:00:00.000"),
            DateUtils.round((Object) dateAmPm1, Calendar.AM_PM),
            "round ampm-1 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.round((Object) dateAmPm2, Calendar.AM_PM),
            "round ampm-2 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.round((Object) dateAmPm3, Calendar.AM_PM),
            "round ampm-3 failed");
    assertEquals(dateTimeParser.parse("February 4, 2002 00:00:00.000"),
            DateUtils.round((Object) dateAmPm4, Calendar.AM_PM),
            "round ampm-4 failed");

    assertThrows(IllegalArgumentException.class, () -> DateUtils.round((Date) null, Calendar.SECOND));
    assertThrows(IllegalArgumentException.class, () -> DateUtils.round((Calendar) null, Calendar.SECOND));
    assertThrows(IllegalArgumentException.class, () -> DateUtils.round((Object) null, Calendar.SECOND));
    assertThrows(ClassCastException.class, () -> DateUtils.round("", Calendar.SECOND));
    assertThrows(IllegalArgumentException.class, () -> DateUtils.round(date1, -9999));

    assertEquals(dateTimeParser.parse("February 3, 2002 00:00:00.000"),
            DateUtils.round((Object) calAmPm1, Calendar.AM_PM),
            "round ampm-1 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.round((Object) calAmPm2, Calendar.AM_PM),
            "round ampm-2 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.round((Object) calAmPm3, Calendar.AM_PM),
            "round ampm-3 failed");
    assertEquals(dateTimeParser.parse("February 4, 2002 00:00:00.000"),
            DateUtils.round((Object) calAmPm4, Calendar.AM_PM),
            "round ampm-4 failed");

    // Fix for https://issues.apache.org/bugzilla/show_bug.cgi?id=25560 / LANG-13
    // Test rounding across the beginning of daylight saving time
    try {
        TimeZone.setDefault(zone);
        dateTimeParser.setTimeZone(zone);
        assertEquals(dateTimeParser.parse("March 30, 2003 00:00:00.000"),
                DateUtils.round(date4, Calendar.DATE),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 00:00:00.000"),
                DateUtils.round((Object) cal4, Calendar.DATE),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 00:00:00.000"),
                DateUtils.round(date5, Calendar.DATE),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 00:00:00.000"),
                DateUtils.round((Object) cal5, Calendar.DATE),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 00:00:00.000"),
                DateUtils.round(date6, Calendar.DATE),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 00:00:00.000"),
                DateUtils.round((Object) cal6, Calendar.DATE),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March ```java
        assertEquals(dateTimeParser.parse("March 30, 2003 00:00:00.000"),
                DateUtils.round(date7, Calendar.DATE),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 00:00:00.000"),
                DateUtils.round((Object) cal7, Calendar.DATE),
                "round MET date across DST change-over");

        assertEquals(dateTimeParser.parse("March 30, 2003 01:00:00.000"),
                DateUtils.round(date4, Calendar.HOUR_OF_DAY),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 01:00:00.000"),
                DateUtils.round((Object) cal4, Calendar.HOUR_OF_DAY),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 03:00:00.000"),
                DateUtils.round(date5, Calendar.HOUR_OF_DAY),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 03:00:00.000"),
                DateUtils.round((Object) cal5, Calendar.HOUR_OF_DAY),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 03:00:00.000"),
                DateUtils.round(date6, Calendar.HOUR_OF_DAY),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 03:00:00.000"),
                DateUtils.round((Object) cal6, Calendar.HOUR_OF_DAY),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 04:00:00.000"),
                DateUtils.round(date7, Calendar.HOUR_OF_DAY),
                "round MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 04:00:00.000"),
                DateUtils.round((Object) cal7, Calendar.HOUR_OF_DAY),
                "round MET date across DST change-over");
    } finally {
        TimeZone.setDefault(defaultZone);
        dateTimeParser.setTimeZone(defaultZone);
    }
}

@Test
public void testTruncate() throws Exception {
    // tests public static Date truncate(Date date, int field)
    assertEquals(dateParser.parse("January 1, 2002"),
            DateUtils.truncate(date1, Calendar.YEAR),
            "truncate year-1 failed");
    assertEquals(dateParser.parse("January 1, 2001"),
            DateUtils.truncate(date2, Calendar.YEAR),
            "truncate year-2 failed");
    assertEquals(dateParser.parse("February 1, 2002"),
            DateUtils.truncate(date1, Calendar.MONTH),
            "truncate month-1 failed");
    assertEquals(dateParser.parse("November 1, 2001"),
            DateUtils.truncate(date2, Calendar.MONTH),
            "truncate month-2 failed");
    assertEquals(dateParser.parse("February 1, 2002"),
            DateUtils.truncate(date1, DateUtils.SEMI_MONTH),
            "truncate semimonth-1 failed");
    assertEquals(dateParser.parse("November 16, 2001"),
            DateUtils.truncate(date2, DateUtils.SEMI_MONTH),
            "truncate semimonth-2 failed");
    assertEquals(dateParser.parse("February 12, 2002"),
            DateUtils.truncate(date1, Calendar.DATE),
            "truncate date-1 failed");
    assertEquals(dateParser.parse("November 18, 2001"),
            DateUtils.truncate(date2, Calendar.DATE),
            "truncate date-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:00:00.000"),
            DateUtils.truncate(date1, Calendar.HOUR),
            "truncate hour-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:00:00.000"),
            DateUtils.truncate(date2, Calendar.HOUR),
            "truncate hour-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:34:00.000"),
            DateUtils.truncate(date1, Calendar.MINUTE),
            "truncate minute-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:23:00.000"),
            DateUtils.truncate(date2, Calendar.MINUTE),
            "truncate minute-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:34:56.000"),
            DateUtils.truncate(date1, Calendar.SECOND),
            "truncate second-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:23:11.000"),
            DateUtils.truncate(date2, Calendar.SECOND),
            "truncate second-2 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 00:00:00.000"),
            DateUtils.truncate(dateAmPm1, Calendar.AM_PM),
            "truncate ampm-1 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 00:00:00.000"),
            DateUtils.truncate(dateAmPm2, Calendar.AM_PM),
            "truncate ampm-2 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.truncate(dateAmPm3, Calendar.AM_PM),
            "truncate ampm-3 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.truncate(dateAmPm4, Calendar.AM_PM),
            "truncate ampm-4 failed");

    // tests public static Date truncate(Object date, int field)
    assertEquals(dateParser.parse("January 1, 2002"),
            DateUtils.truncate((Object) date1, Calendar.YEAR),
            "truncate year-1 failed");
    assertEquals(dateParser.parse("January 1, 2001"),
            DateUtils.truncate((Object) date2, Calendar.YEAR),
            "truncate year-2 failed");
    assertEquals(dateParser.parse("February 1, 2002"),
            DateUtils.truncate((Object) date1, Calendar.MONTH),
            "truncate month-1 failed");
    assertEquals(dateParser.parse("November 1, 2001"),
            DateUtils.truncate((Object) date2, Calendar.MONTH),
            "truncate month-2 failed");
    assertEquals(dateParser.parse("February 1, 2002"),
            DateUtils.truncate((Object) date1, DateUtils.SEMI_MONTH),
            "truncate semimonth-1 failed");
    assertEquals(dateParser.parse("November 16, 2001"),
            DateUtils.truncate((Object) date2, DateUtils.SEMI_MONTH),
            "truncate semimonth-2 failed");
    assertEquals(dateParser.parse("February 12, 2002"),
            DateUtils.truncate((Object) date1, Calendar.DATE),
            "truncate date-1 failed");
    assertEquals(dateParser.parse("November 18, 2001"),
            DateUtils.truncate((Object) date2, Calendar.DATE),
            "truncate date-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:00:00.000"),
            DateUtils.truncate((Object) date1, Calendar.HOUR),
            "truncate hour-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:00:00.000"),
            DateUtils.truncate((Object) date2, Calendar.HOUR),
            "truncate hour-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:34:00.000"),
            DateUtils.truncate((Object) date1, Calendar.MINUTE),
            "truncate minute-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:23:00.000"),
            DateUtils.truncate((Object) date2, Calendar.MINUTE),
            "truncate minute-2 failed");
    assertEquals(dateTimeParser.parse("February 12, 2002 12:34:56.000"),
            DateUtils.truncate((Object) date1, Calendar.SECOND),
            "truncate second-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:23:11.000"),
            DateUtils.truncate((Object) date2, Calendar.SECOND),
            "truncate second-2 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 00:00:00.000"),
            DateUtils.truncate((Object) dateAmPm1, Calendar.AM_PM),
            "truncate ampm-1 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 00:00:00.000"),
            DateUtils.truncate((Object) dateAmPm2, Calendar.AM_PM),
            "truncate ampm-2 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.truncate((Object) dateAmPm3, Calendar.AM_PM),
            "truncate ampm-3 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.truncate((Object) dateAmPm4, Calendar.AM_PM),
            "truncate ampm-4 failed");

    assertEquals(dateTimeParser.parse("February 12, 2002 12:34:56.000"),
            DateUtils.truncate((Object) cal1, Calendar.SECOND),
            "truncate calendar second-1 failed");
    assertEquals(dateTimeParser.parse("November 18, 2001 1:23:11.000"),
            DateUtils.truncate((Object) cal2, Calendar.SECOND),
            "truncate calendar second-2 failed");

    assertEquals(dateTimeParser.parse("February 3, 2002 00:00:00.000"),
            DateUtils.truncate((Object) calAmPm1, Calendar.AM_PM),
            "truncate ampm-1 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 00:00:00.000"),
            DateUtils.truncate((Object) calAmPm2, Calendar.AM_PM),
            "truncate ampm-2 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.truncate((Object) calAmPm3, Calendar.AM_PM),
            "truncate ampm-3 failed");
    assertEquals(dateTimeParser.parse("February 3, 2002 12:00:00.000"),
            DateUtils.truncate((Object) calAmPm4, Calendar.AM_PM),
            "truncate ampm-4 failed");

    assertThrows(IllegalArgumentException.class, () -> DateUtils.truncate((Date) null, Calendar.SECOND));
    assertThrows(IllegalArgumentException.class, () -> DateUtils.truncate((Calendar) null, Calendar.SECOND));
    assertThrows(IllegalArgumentException.class, () -> DateUtils.truncate((Object) null, Calendar.SECOND));
    assertThrows(ClassCastException.class, () -> DateUtils.truncate("", Calendar.SECOND));

    // Fix for https://issues.apache.org/bugzilla/show_bug.cgi?id=25560
    // Test truncate across beginning of daylight saving time
    try {
        TimeZone.setDefault(zone);
        dateTimeParser.setTimeZone(zone);
        assertEquals(dateTimeParser.parse("March 30, 2003 00:00:00.000"),
                DateUtils.truncate(date3, Calendar.DATE),
                "truncate MET date across DST change-over");
        assertEquals(dateTimeParser.parse("March 30, 2003 00:00:00.000"),
                DateUtils.truncate((Object) cal3, Calendar.DATE),
                "truncate MET date across DST change-over");
        // Test truncate across end of daylight saving time
        assertEquals(dateTimeParser.parse("October 26, 2003 00:00:00.000"),
                DateUtils.truncate(date8, Calendar.DATE),
                "truncate MET date across DST change-over");
        assertEquals(dateTimeParser.parse("October 26, 2003 00:00:00.000"),
                DateUtils.truncate((Object) cal8, Calendar.DATE),
                "truncate MET date across DST change-over");
    } finally {
        TimeZone.setDefault(defaultZone);
        dateTimeParser.setTimeZone(defaultZone);
    }

    // Bug 31395, large dates
    final Date endOfTime = new Date(Long.MAX_VALUE); // fyi: Sun Aug 17 07:12:55 CET 292278994 -- 807 millis
    final GregorianCalendar endCal = new GregorianCalendar();
    endCal.setTime(endOfTime);
    assertThrows(ArithmeticException.class, () -> DateUtils.truncate(endCal, Calendar.DATE));
    endCal.set(Calendar.YEAR, 280000001);
    assertThrows(ArithmeticException.class, () -> DateUtils.truncate(endCal, Calendar.DATE));
    endCal.set(Calendar.YEAR, 280000000);
    final Calendar cal = DateUtils.truncate(endCal, Calendar.DATE);
    assertEquals(0, cal.get(Calendar.HOUR));
}

// https://issues.apache.org/jira/browse/LANG-530
@SuppressWarnings("deprecation")
@Test
public void testLang530() throws ParseException {
    final Date d = new Date();
    final String isoDateStr = DateFormatUtils.ISO_DATETIME_TIME_ZONE_FORMAT.format(d);
    final Date d2 = DateUtils.parseDate(isoDateStr, DateFormatUtils.ISO_DATETIME_TIME_ZONE_FORMAT.getPattern());
    // the format loses milliseconds so have to reintroduce them
    assertEquals(d.getTime(), d2.getTime() + d.getTime() % 1000, "Date not equal to itself ISO formatted and parsed");
}
```