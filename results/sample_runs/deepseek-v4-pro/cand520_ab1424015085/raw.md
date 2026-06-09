# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `408462e80d57be420c153b67f69110e27776d4eb`
- B: `ab1424015085472b2d3865668e370aec8a102331`
- test: `src/test/java/org/apache/commons/lang3/StringEscapeUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringEscapeUtils.java']`
- old_test_mode: `methods`
- user_chars: `10669`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3337, 'completion_tokens': 6659, 'total_tokens': 9996, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 5490}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2953}`

---

- 修改 `testEscapeXmlSupplementaryCharacters`：在原有断言后新增一条混合字符编码的断言。
- 修改 `testUnescapeXmlSupplementaryCharacters`：在原有断言后新增一条混合字符解码的断言。
- 修改 `testEscapeCsvString`：新增一条包含补充字符的转义断言，并调整对齐。
- 修改 `testEscapeCsvWriter`：新增一条包含补充字符的转义 Writer 断言，并调整对齐。
- 修改 `testUnescapeCsvString`：新增一条包含补充字符的反转义断言，删除最后的 `assertEquals("\"foo.bar\"", ...)` 断言，并调整对齐。
- 修改 `testUnescapeCsvWriter`：新增一条包含补充字符的反转义 Writer 断言，删除最后的 `checkCsvUnescapeWriter("\"foo.bar\"", "\"foo.bar\"")` 断言，并调整对齐。
- 无需新增或修改 import。

```java
    @Test
    public void testEscapeXmlSupplementaryCharacters() {
        final CharSequenceTranslator escapeXml = StringEscapeUtils.ESCAPE_XML;
        assertEquals("Supplementary character must be represented using a single escape", "&#144308;",
                escapeXml.translate("\uD84C\uDFB4"));

        assertEquals("Supplementary characters mixed with basic characters should be encoded correctly", "a b c &#144308;",
                        escapeXml.translate("a b c \uD84C\uDFB4"));
    }

    @Test
    public void testUnescapeXmlSupplementaryCharacters() {
        assertEquals("Supplementary character must be represented using a single escape", "\uD84C\uDFB4",
                StringEscapeUtils.unescapeXml("&#144308;") );

        assertEquals("Supplementary characters mixed with basic characters should be decoded correctly", "a b c \uD84C\uDFB4",
                StringEscapeUtils.unescapeXml("a b c &#144308;") );
    }

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
        assertEquals("",   StringEscapeUtils.unescapeCsv(""));
        assertEquals(null, StringEscapeUtils.unescapeCsv(null));
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
    }
```