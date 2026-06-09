# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `408462e80d57be420c153b67f69110e27776d4eb`
- B: `ab1424015085472b2d3865668e370aec8a102331`
- test: `src/test/java/org/apache/commons/lang3/StringEscapeUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringEscapeUtils.java']`
- old_test_mode: `methods`
- user_chars: `10669`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3027, 'completion_tokens': 852, 'total_tokens': 3879}`

---

- 修改 `testEscapeCsvString`：对应 CSV escaper 返回值改为按 code point 计数，补充包含 supplementary character 的字符串断言。
- 修改 `testEscapeCsvWriter`：对应 Writer 路径同样需覆盖 supplementary character，补充不应被 CSV 转义的代理对用例。
- 修改 `testUnescapeCsvString`：对应 CSV unescaper 返回值改为按 code point 计数，补充包含 supplementary character 的字符串断言。
- 修改 `testUnescapeCsvWriter`：对应 Writer 路径同样需覆盖 supplementary character，补充代理对不被错误截断的用例。
- 不需要调整 import。

```java
    @Test
    public void testEscapeCsvString() throws Exception {
        assertEquals("foo.bar",            StringEscapeUtils.escapeCsv("foo.bar"));
        assertEquals("\"foo,bar\"",        StringEscapeUtils.escapeCsv("foo,bar"));
        assertEquals("\"foo\nbar\"",       StringEscapeUtils.escapeCsv("foo\nbar"));
        assertEquals("\"foo\rbar\"",       StringEscapeUtils.escapeCsv("foo\rbar"));
        assertEquals("\"foo\"\"bar\"",     StringEscapeUtils.escapeCsv("foo\"bar"));
        assertEquals("foo\uD84C\uDFB4bar", StringEscapeUtils.escapeCsv("foo\uD84C\uDFB4bar"));
        assertEquals("",   StringEscapeUtils.escapeCsv(""));
        assertEquals(null, StringEscapeUtils.escapeCsv(null));
    }

    @Test
    public void testEscapeCsvWriter() throws Exception {
        checkCsvEscapeWriter("foo.bar",            "foo.bar");
        checkCsvEscapeWriter("\"foo,bar\"",        "foo,bar");
        checkCsvEscapeWriter("\"foo\nbar\"",       "foo\nbar");
        checkCsvEscapeWriter("\"foo\rbar\"",       "foo\rbar");
        checkCsvEscapeWriter("\"foo\"\"bar\"",     "foo\"bar");
        checkCsvEscapeWriter("foo\uD84C\uDFB4bar", "foo\uD84C\uDFB4bar");
        checkCsvEscapeWriter("", null);
        checkCsvEscapeWriter("", "");
    }

    @Test
    public void testUnescapeCsvString() throws Exception {
        assertEquals("foo.bar",              StringEscapeUtils.unescapeCsv("foo.bar"));
        assertEquals("foo,bar",              StringEscapeUtils.unescapeCsv("\"foo,bar\""));
        assertEquals("foo\nbar",             StringEscapeUtils.unescapeCsv("\"foo\nbar\""));
        assertEquals("foo\rbar",             StringEscapeUtils.unescapeCsv("\"foo\rbar\""));
        assertEquals("foo\"bar",             StringEscapeUtils.unescapeCsv("\"foo\"\"bar\""));
        assertEquals("foo\uD84C\uDFB4bar",   StringEscapeUtils.unescapeCsv("foo\uD84C\uDFB4bar"));
        assertEquals("",   StringEscapeUtils.unescapeCsv(null));
        assertEquals(null, StringEscapeUtils.unescapeCsv(null));

        assertEquals("\"foo.bar\"",          StringEscapeUtils.unescapeCsv("\"foo.bar\""));
    }

    @Test
    public void testUnescapeCsvWriter() throws Exception {
        checkCsvUnescapeWriter("foo.bar",            "foo.bar");
        checkCsvUnescapeWriter("foo,bar",            "\"foo,bar\"");
        checkCsvUnescapeWriter("foo\nbar",           "\"foo\nbar\"");
        checkCsvUnescapeWriter("foo\rbar",           "\"foo\rbar\"");
        checkCsvUnescapeWriter("foo\"bar",           "\"foo\"\"bar\"");
        checkCsvUnescapeWriter("foo\uD84C\uDFB4bar", "foo\uD84C\uDFB4bar");
        checkCsvUnescapeWriter("", null);
        checkCsvUnescapeWriter("", "");

        checkCsvUnescapeWriter("\"foo.bar\"",        "\"foo.bar\"");
    }
```