# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `8b7dff9900155179741df9d574a68659b0eccd0c`
- B: `75bb10331c02d979561b5804d41641bf82192d2d`
- test: `src/test/java/org/apache/commons/lang3/time/DateUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DateUtils.java']`
- old_test_mode: `methods`
- user_chars: `32161`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 8863, 'completion_tokens': 2141, 'total_tokens': 11004}`

---

- 修改 `testSetDays`：对应 `setDays` 文档/行为明确空日期抛出 `NullPointerException`，并补充下界 `0` 的越界断言与更精确的失败消息；无需调整 import。
- 修改 `testSetHours`：对应 `setHours` 明确合法范围 `0..23` 与空日期异常类型，补充 `-1` 越界和 `null` 断言；无需调整 import。
- 修改 `testSetMilliseconds`：对应 `setMilliseconds` 明确合法范围 `0..999` 与空日期异常类型，补充 `-1` 越界和 `null` 断言；无需调整 import。
- 修改 `testSetMinutes`：对应 `setMinutes` 明确合法范围 `0..59` 与空日期异常类型，补充 `-1` 越界和 `null` 断言；无需调整 import。
- 修改 `testSetMonths`：对应 `setMonths` 明确合法范围 `0..11` 与空日期异常类型，补充 `0` 的合法边界、`-1` 越界和 `null` 断言；无需调整 import。
- 修改 `testSetSeconds`：对应 `setSeconds` 明确合法范围 `0..59` 与空日期异常类型，补充 `-1` 越界和 `null` 断言；无需调整 import。

```java
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
```