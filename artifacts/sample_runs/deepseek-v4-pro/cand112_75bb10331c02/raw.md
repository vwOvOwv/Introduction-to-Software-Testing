# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `8b7dff9900155179741df9d574a68659b0eccd0c`
- B: `75bb10331c02d979561b5804d41641bf82192d2d`
- test: `src/test/java/org/apache/commons/lang3/time/DateUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DateUtils.java']`
- old_test_mode: `methods`
- user_chars: `32161`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 8913, 'completion_tokens': 6373, 'total_tokens': 15286, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2134}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 8529}`

---

- 修改 `testAddDays` 方法：在末尾增加对 `NullPointerException` 的断言，验证 `DateUtils.addDays(null, 0)` 抛出该异常。
- 修改 `testAddHours` 方法：增加对 `NullPointerException` 的断言，验证 `DateUtils.addHours(null, 0)` 抛出该异常。
- 修改 `testAddMilliseconds` 方法：增加对 `NullPointerException` 的断言，验证 `DateUtils.addMilliseconds(null, 0)` 抛出该异常。
- 修改 `testAddMinutes` 方法：增加对 `NullPointerException` 的断言，验证 `DateUtils.addMinutes(null, 0)` 抛出该异常。
- 修改 `testAddMonths` 方法：增加对 `NullPointerException` 的断言，验证 `DateUtils.addMonths(null, 0)` 抛出该异常。
- 修改 `testAddSeconds` 方法：增加对 `NullPointerException` 的断言，验证 `DateUtils.addSeconds(null, 0)` 抛出该异常。
- 修改 `testAddWeeks` 方法：增加对 `NullPointerException` 的断言（此处验证 `DateUtils.addMonths(null, 0)`，与生产代码 diff 一致）。
- 修改 `testAddYears` 方法：增加对 `NullPointerException` 的断言，验证 `DateUtils.addYears(null, 0)` 抛出该异常。
- 修改 `testSetDays` 方法：更新范围外值的断言消息，增加对 `amount=0` 的范围检查断言，并增加对 `NullPointerException` 的断言。
- 修改 `testSetHours` 方法：更新范围外值的断言消息，增加对 `amount=-1` 的范围检查断言，并增加对 `NullPointerException` 的断言。
- 修改 `testSetMilliseconds` 方法：更新范围外值的断言消息，增加对 `amount=-1` 的范围检查断言，并增加对 `NullPointerException` 的断言。
- 修改 `testSetMinutes` 方法：更新范围外值的断言消息，增加对 `amount=-1` 的范围检查断言，并增加对 `NullPointerException` 的断言。
- 修改 `testSetMonths` 方法：增加对 `amount=0` 的合法调用测试，更新范围外值的断言消息，增加对 `amount=-1` 的范围检查断言，并增加对 `NullPointerException` 的断言。
- 修改 `testSetSeconds` 方法：更新范围外值的断言消息，增加对 `amount=-1` 的范围检查断言，并增加对 `NullPointerException` 的断言。
- 修改 `testSetYears` 方法：增加对 `NullPointerException` 的断言，验证 `DateUtils.setYears(null, 0)` 抛出该异常。
- 无需新增或调整 import 语句，现有 `assertThrows` 已可使用。

```java
@Test
public void testAddDays() throws Exception {
    Date result = DateUtils.addDays(BASE_DATE, 1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 6, 4, 3, 2, 1);

    result = DateUtils.addDays(BASE_DATE, -1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 4, 4, 3, 2, 1);

    assertThrows(NullPointerException.class, () -> DateUtils.addDays(null, 0));
}

@Test
public void testAddHours() throws Exception {
    Date result = DateUtils.addHours(BASE_DATE, 1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 5, 3, 2, 1);

    result = DateUtils.addHours(BASE_DATE, -1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 3, 3, 2, 1);

    assertThrows(NullPointerException.class, () -> DateUtils.addHours(null, 0));
}

@Test
public void testAddMilliseconds() throws Exception {
    Date result = DateUtils.addMilliseconds(BASE_DATE, 1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 4, 3, 2, 2);

    result = DateUtils.addMilliseconds(BASE_DATE, -1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 4, 3, 2, 0);

    assertThrows(NullPointerException.class, () -> DateUtils.addMilliseconds(null, 0));
}

@Test
public void testAddMinutes() throws Exception {
    Date result = DateUtils.addMinutes(BASE_DATE, 1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 4, 4, 2, 1);

    result = DateUtils.addMinutes(BASE_DATE, -1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 4, 2, 2, 1);

    assertThrows(NullPointerException.class, () -> DateUtils.addMinutes(null, 0));
}

@Test
public void testAddMonths() throws Exception {
    Date result = DateUtils.addMonths(BASE_DATE, 1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 7, 5, 4, 3, 2, 1);

    result = DateUtils.addMonths(BASE_DATE, -1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 5, 5, 4, 3, 2, 1);

    assertThrows(NullPointerException.class, () -> DateUtils.addMonths(null, 0));
}

@Test
public void testAddSeconds() throws Exception {
    Date result = DateUtils.addSeconds(BASE_DATE, 1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 4, 3, 3, 1);

    result = DateUtils.addSeconds(BASE_DATE, -1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 4, 3, 1, 1);

    assertThrows(NullPointerException.class, () -> DateUtils.addSeconds(null, 0));
}

@Test
public void testAddWeeks() throws Exception {
    Date result = DateUtils.addWeeks(BASE_DATE, 1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 12, 4, 3, 2, 1);

    result = DateUtils.addWeeks(BASE_DATE, -1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);      // july
    assertDate(result, 2000, 5, 28, 4, 3, 2, 1);   // june

    assertThrows(NullPointerException.class, () -> DateUtils.addMonths(null, 0));
}

@Test
public void testAddYears() throws Exception {
    Date result = DateUtils.addYears(BASE_DATE, 1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2001, 6, 5, 4, 3, 2, 1);

    result = DateUtils.addYears(BASE_DATE, -1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 1999, 6, 5, 4, 3, 2, 1);

    assertThrows(NullPointerException.class, () -> DateUtils.addYears(null, 0));
}

@Test
public void testSetDays() throws Exception {
    Date result = DateUtils.setDays(BASE_DATE, 1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 1, 4, 3, 2, 1);

    result = DateUtils.setDays(BASE_DATE, 29);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 29, 4, 3, 2, 1);

    final String outsideOfRangeAssertionMessage = "DateUtils.setDays did not throw an expected IllegalArgumentException for amount outside of range 1 to 31.";
    assertThrows(
            IllegalArgumentException.class,
            () -> DateUtils.setDays(BASE_DATE, 32),
            outsideOfRangeAssertionMessage);
    assertThrows(
            IllegalArgumentException.class,
            () -> DateUtils.setDays(BASE_DATE, 0),
            outsideOfRangeAssertionMessage);

    assertThrows(NullPointerException.class, () -> DateUtils.setDays(null, 1));
}

@Test
public void testSetHours() throws Exception {
    Date result = DateUtils.setHours(BASE_DATE, 0);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 0, 3, 2, 1);

    result = DateUtils.setHours(BASE_DATE, 23);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 23, 3, 2, 1);

    final String outsideOfRangeAssertionMessage = "DateUtils.setHours did not throw an expected IllegalArgumentException for amount outside of range 0 to 23.";
    assertThrows(
            IllegalArgumentException.class,
            () -> DateUtils.setHours(BASE_DATE, 24),
            outsideOfRangeAssertionMessage);
    assertThrows(
            IllegalArgumentException.class,
            () -> DateUtils.setHours(BASE_DATE, -1),
            outsideOfRangeAssertionMessage);

    assertThrows(NullPointerException.class, () -> DateUtils.setHours(null, 0));
}

@Test
public void testSetMilliseconds() throws Exception {
    Date result = DateUtils.setMilliseconds(BASE_DATE, 0);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 4, 3, 2, 0);

    result = DateUtils.setMilliseconds(BASE_DATE, 999);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 4, 3, 2, 999);

    final String outsideOfRangeAssertionMessage = "DateUtils.setMilliseconds did not throw an expected IllegalArgumentException for range outside of 0 to 999.";
    assertThrows(
            IllegalArgumentException.class,
            () -> DateUtils.setMilliseconds(BASE_DATE, 1000),
            outsideOfRangeAssertionMessage);
    assertThrows(
            IllegalArgumentException.class,
            () -> DateUtils.setMilliseconds(BASE_DATE, -1),
            outsideOfRangeAssertionMessage);

    assertThrows(NullPointerException.class, () -> DateUtils.setMilliseconds(null, 0));
}

@Test
public void testSetMinutes() throws Exception {
    Date result = DateUtils.setMinutes(BASE_DATE, 0);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 4, 0, 2, 1);

    result = DateUtils.setMinutes(BASE_DATE, 59);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 4, 59, 2, 1);

    final String outsideOfRangeAssertionMessage = "DateUtils.setMinutes did not throw an expected IllegalArgumentException for amount outside of range 0 to 59.";
    assertThrows(
            IllegalArgumentException.class,
            () -> DateUtils.setMinutes(BASE_DATE, 60),
            outsideOfRangeAssertionMessage);
    assertThrows(
            IllegalArgumentException.class,
            () -> DateUtils.setMinutes(BASE_DATE, -1),
            outsideOfRangeAssertionMessage);

    assertThrows(NullPointerException.class, () -> DateUtils.setMinutes(null, 0));
}

@Test
public void testSetMonths() throws Exception {
    Date result = DateUtils.setMonths(BASE_DATE, 5);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 5, 5, 4, 3, 2, 1);

    result = DateUtils.setMonths(BASE_DATE, 1);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 1, 5, 4, 3, 2, 1);

    result = DateUtils.setMonths(BASE_DATE, 0);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 0, 5, 4, 3, 2, 1);

    final String outsideOfRangeAssertionMessage = "DateUtils.setMonths did not throw an expected IllegalArgumentException for amount outside of range 0 to 11.";
    assertThrows(
            IllegalArgumentException.class,
            () -> DateUtils.setMonths(BASE_DATE, 12),
            outsideOfRangeAssertionMessage);
    assertThrows(
            IllegalArgumentException.class,
            () -> DateUtils.setMonths(BASE_DATE, -1),
            outsideOfRangeAssertionMessage);

    assertThrows(NullPointerException.class, () -> DateUtils.setMonths(null, 0));
}

@Test
public void testSetSeconds() throws Exception {
    Date result = DateUtils.setSeconds(BASE_DATE, 0);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 4, 3, 0, 1);

    result = DateUtils.setSeconds(BASE_DATE, 59);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2000, 6, 5, 4, 3, 59, 1);

    final String outsideOfRangeAssertionMessage = "DateUtils.setSeconds did not throw an expected IllegalArgumentException for amount outside of range 0 to 59.";
    assertThrows(
            IllegalArgumentException.class,
            () -> DateUtils.setSeconds(BASE_DATE, 60),
            outsideOfRangeAssertionMessage);
    assertThrows(
            IllegalArgumentException.class,
            () -> DateUtils.setSeconds(BASE_DATE, -1),
            outsideOfRangeAssertionMessage);

    assertThrows(NullPointerException.class, () -> DateUtils.setSeconds(null, 0));
}

@Test
public void testSetYears() throws Exception {
    Date result = DateUtils.setYears(BASE_DATE, 2005);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 2005, 6, 5, 4, 3, 2, 1);

    result = DateUtils.setYears(BASE_DATE, 1999);
    assertNotSame(BASE_DATE, result);
    assertDate(BASE_DATE, 2000, 6, 5, 4, 3, 2, 1);
    assertDate(result, 1999, 6, 5, 4, 3, 2, 1);

    assertThrows(NullPointerException.class, () -> DateUtils.setYears(null, 0));
}
```