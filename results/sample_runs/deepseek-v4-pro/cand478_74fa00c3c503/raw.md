# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ab1424015085472b2d3865668e370aec8a102331`
- B: `74fa00c3c503813da2413b9d5a862bb125ef50e7`
- test: `src/test/java/org/apache/commons/lang3/StringEscapeUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringEscapeUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `39850`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 11038, 'completion_tokens': 3633, 'total_tokens': 14671, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1374}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 10654}`

---

- 新增 `testEscapeXml10` 测试方法，验证 XML 1.0 转义规则（控制字符移除、代理对移除、兼容性转义）。
- 新增 `testEscapeXml11` 测试方法，验证 XML 1.1 转义规则（保留某些控制字符并转义、移除空字符与代理对）。
- 修改 `testEscapeXml` 方法，添加 `@SuppressWarnings("deprecation")` 以抑制对已弃用 `escapeXml`/`ESCAPE_XML` 的警告，方法体不变。
- 修改 `testEscapeXmlSupplementaryCharacters` 方法，添加 `@SuppressWarnings("deprecation")` 注解，方法体不变（使用已弃用的 `ESCAPE_XML`）。
- 修改 `testEscapeXmlAllCharacters` 方法，添加 `@SuppressWarnings("deprecation")` 注解，方法体不变。
- 修改 `testLang720` 方法，添加 `@SuppressWarnings("deprecation")` 注解，方法体不变（使用已弃用的 `escapeXml`）。

```java
    @Test
    @SuppressWarnings( "deprecation" ) // ESCAPE_XML has been replaced by ESCAPE_XML10 and ESCAPE_XML11 in 3.3
    public void testEscapeXml() throws Exception {
        assertEquals("&lt;abc&gt;", StringEscapeUtils.escapeXml("<abc>"));
        assertEquals("<abc>", StringEscapeUtils.unescapeXml("&lt;abc&gt;"));

        assertEquals("XML should not escape >0x7f values",
                "\u00A1", StringEscapeUtils.escapeXml("\u00A1"));
        assertEquals("XML should be able to unescape >0x7f values",
                "\u00A0", StringEscapeUtils.unescapeXml("&#160;"));
        assertEquals("XML should be able to unescape >0x7f values with one leading 0",
                "\u00A0", StringEscapeUtils.unescapeXml("&#0160;"));
        assertEquals("XML should be able to unescape >0x7f values with two leading 0s",
                "\u00A0", StringEscapeUtils.unescapeXml("&#00160;"));
        assertEquals("XML should be able to unescape >0x7f values with three leading 0s",
                "\u00A0", StringEscapeUtils.unescapeXml("&#000160;"));

        assertEquals("ain't", StringEscapeUtils.unescapeXml("ain&apos;t"));
        assertEquals("ain&apos;t", StringEscapeUtils.escapeXml("ain't"));
        assertEquals("", StringEscapeUtils.escapeXml(""));
        assertEquals(null, StringEscapeUtils.escapeXml(null));
        assertEquals(null, StringEscapeUtils.unescapeXml(null));

        StringWriter sw = new StringWriter();
        try {
            StringEscapeUtils.ESCAPE_XML.translate("<abc>", sw);
        } catch (final IOException e) {
        }
        assertEquals("XML was escaped incorrectly", "&lt;abc&gt;", sw.toString() );

        sw = new StringWriter();
        try {
            StringEscapeUtils.UNESCAPE_XML.translate("&lt;abc&gt;", sw);
        } catch (final IOException e) {
        }
        assertEquals("XML was unescaped incorrectly", "<abc>", sw.toString() );
    }

    @Test
    public void testEscapeXml10() throws Exception {
        assertEquals("a&lt;b&gt;c&quot;d&apos;e&amp;f", StringEscapeUtils.escapeXml10("a<b>c\"d'e&f"));
        assertEquals("XML 1.0 should not escape \t \n \r",
                "a\tb\rc\nd", StringEscapeUtils.escapeXml10("a\tb\rc\nd"));
        assertEquals("XML 1.0 should omit most #x0-x8 | #xb | #xc | #xe-#x19",
                "ab", StringEscapeUtils.escapeXml10("a\u0000\u0001\u0008\u000b\u000c\u000e\u001fb"));
        assertEquals("XML 1.0 should omit #xd800-#xdfff",
                "a\ud7ff  \ue000b", StringEscapeUtils.escapeXml10("a\ud7ff\ud800 \udfff \ue000b"));
        assertEquals("XML 1.0 should omit #xfffe | #xffff",
                "a\ufffdb", StringEscapeUtils.escapeXml10("a\ufffd\ufffe\uffffb"));
        assertEquals("XML 1.0 should escape #x7f-#x84 | #x86 - #x9f, for XML 1.1 compatibility",
                "a\u007e&#127;&#132;\u0085&#134;&#159;\u00a0b", StringEscapeUtils.escapeXml10("a\u007e\u007f\u0084\u0085\u0086\u009f\u00a0b"));
    }

    @Test
    public void testEscapeXml11() throws Exception {
        assertEquals("a&lt;b&gt;c&quot;d&apos;e&amp;f", StringEscapeUtils.escapeXml11("a<b>c\"d'e&f"));
        assertEquals("XML 1.1 should not escape \t \n \r",
                "a\tb\rc\nd", StringEscapeUtils.escapeXml11("a\tb\rc\nd"));
        assertEquals("XML 1.1 should omit #x0",
                "ab", StringEscapeUtils.escapeXml11("a\u0000b"));
        assertEquals("XML 1.1 should escape #x1-x8 | #xb | #xc | #xe-#x19",
                "a&#1;&#8;&#11;&#12;&#14;&#31;b", StringEscapeUtils.escapeXml11("a\u0001\u0008\u000b\u000c\u000e\u001fb"));
        assertEquals("XML 1.1 should escape #x7F-#x84 | #x86-#x9F",
                "a\u007e&#127;&#132;\u0085&#134;&#159;\u00a0b", StringEscapeUtils.escapeXml11("a\u007e\u007f\u0084\u0085\u0086\u009f\u00a0b"));
        assertEquals("XML 1.1 should omit #xd800-#xdfff",
                "a\ud7ff  \ue000b", StringEscapeUtils.escapeXml11("a\ud7ff\ud800 \udfff \ue000b"));
        assertEquals("XML 1.1 should omit #xfffe | #xffff",
                "a\ufffdb", StringEscapeUtils.escapeXml11("a\ufffd\ufffe\uffffb"));
    }

    @Test
    @SuppressWarnings( "deprecation" ) // ESCAPE_XML has been replaced by ESCAPE_XML10 and ESCAPE_XML11 in 3.3
    public void testEscapeXmlSupplementaryCharacters() {
        final CharSequenceTranslator escapeXml = 
            StringEscapeUtils.ESCAPE_XML.with( NumericEntityEscaper.between(0x7f, Integer.MAX_VALUE) );

        assertEquals("Supplementary character must be represented using a single escape", "&#144308;",
                escapeXml.translate("\uD84C\uDFB4"));

        assertEquals("Supplementary characters mixed with basic characters should be encoded correctly", "a b c &#144308;",
                        escapeXml.translate("a b c \uD84C\uDFB4"));
    }
    
    @Test
    @SuppressWarnings( "deprecation" ) // ESCAPE_XML has been replaced by ESCAPE_XML10 and ESCAPE_XML11 in 3.3
    public void testEscapeXmlAllCharacters() {
        // http://www.w3.org/TR/xml/#charsets says:
        // Char ::= #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF] /* any Unicode character,
        // excluding the surrogate blocks, FFFE, and FFFF. */
        final CharSequenceTranslator escapeXml = StringEscapeUtils.ESCAPE_XML
                .with(NumericEntityEscaper.below(9), NumericEntityEscaper.between(0xB, 0xC), NumericEntityEscaper.between(0xE, 0x19),
                        NumericEntityEscaper.between(0xD800, 0xDFFF), NumericEntityEscaper.between(0xFFFE, 0xFFFF), NumericEntityEscaper.above(0x110000));

        assertEquals("&#0;&#1;&#2;&#3;&#4;&#5;&#6;&#7;&#8;", escapeXml.translate("\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\u0008"));
        assertEquals("\t", escapeXml.translate("\t")); // 0x9
        assertEquals("\n", escapeXml.translate("\n")); // 0xA
        assertEquals("&#11;&#12;", escapeXml.translate("\u000B\u000C"));
        assertEquals("\r", escapeXml.translate("\r")); // 0xD
        assertEquals("Hello World! Ain&apos;t this great?", escapeXml.translate("Hello World! Ain't this great?"));
        assertEquals("&#14;&#15;&#24;&#25;", escapeXml.translate("\u000E\u000F\u0018\u0019"));
    }

    @Test
    @SuppressWarnings( "deprecation" ) // escapeXml(String) has been replaced by escapeXml10(String) and escapeXml11(String) in 3.3
    public void testLang720() {
        final String input = new StringBuilder("\ud842\udfb7").append("A").toString();
        final String escaped = StringEscapeUtils.escapeXml(input);
        assertEquals(input, escaped);
    }
```