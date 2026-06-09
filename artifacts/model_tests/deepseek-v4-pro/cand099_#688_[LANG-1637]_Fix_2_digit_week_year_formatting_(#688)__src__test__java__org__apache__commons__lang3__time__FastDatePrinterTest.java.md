# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `2a8356cd433ccbe3338c823ad7c61b6f895cccf2`
- B: `63f644daa847e193d9f70791ef2337816f6409a6`
- test: `src/test/java/org/apache/commons/lang3/time/FastDatePrinterTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/FastDatePrinter.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `18986`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5276, 'completion_tokens': 3217, 'total_tokens': 8493, 'prompt_tokens_details': {'cached_tokens': 5120}, 'completion_tokens_details': {'reasoning_tokens': 3023}, 'prompt_cache_hit_tokens': 5120, 'prompt_cache_miss_tokens': 156}`

---

```java
    @DefaultLocale(language = "en", country = "US")
    @DefaultTimeZone("America/New_York")
    @Test
    public void testWeekYear() {
        final GregorianCalendar cal = new GregorianCalendar(2020, 12, 31, 0, 0, 0);
        final DatePrinter printer4Digits = getInstance("YYYY");
        final DatePrinter printer4DigitsFallback = getInstance("YYY");
        final DatePrinter printer2Digits = getInstance("YY");
        final DatePrinter printer4DigitAnotherFallback = getInstance("Y");
        assertEquals("2021", printer4Digits.format(cal));
        assertEquals("2021", printer4DigitsFallback.format(cal));
        assertEquals("2021", printer4DigitAnotherFallback.format(cal));
        assertEquals("21", printer2Digits.format(cal));
    }
```