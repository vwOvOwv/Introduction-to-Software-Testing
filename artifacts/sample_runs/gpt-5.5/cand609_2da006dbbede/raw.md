# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `593ccc17b8aae20f73d7059a3c34184c8a5a0eda`
- B: `2da006dbbede3f18d0898819edae9a5c71eac947`
- test: `src/test/java/org/apache/commons/lang3/StringEscapeUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringEscapeUtils.java']`
- old_test_mode: `methods`
- user_chars: `3283`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1269, 'completion_tokens': 302, 'total_tokens': 1571}`

---

- 修改 `testEscapeHtmlHighUnicode`：仅同步测试 diff 中注释文本，将 `codepoint` 改为 `code point`；不需要调整 import。

```java
@Test
public void testEscapeHtmlHighUnicode() {
    // this is the utf8 representation of the character:
    // COUNTING ROD UNIT DIGIT THREE
    // in Unicode
    // code point: U+1D362
    final byte[] data = { (byte) 0xF0, (byte) 0x9D, (byte) 0x8D, (byte) 0xA2 };

    final String original = new String(data, StandardCharsets.UTF_8);

    final String escaped = StringEscapeUtils.escapeHtml4( original );
    assertEquals(original, escaped, "High Unicode should not have been escaped");

    final String unescaped = StringEscapeUtils.unescapeHtml4( escaped );
    assertEquals(original, unescaped, "High Unicode should have been unchanged");

// TODO: I think this should hold, needs further investigation
//        String unescapedFromEntity = StringEscapeUtils.unescapeHtml4( "&#119650;" );
//        assertEquals( "High Unicode should have been unescaped", original, unescapedFromEntity);
}
```