# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `d13a40266f9b357d96b71b2ef6bc420443b61dd1`
- B: `612595106054d0ff2320cc15f88cfef8959e1531`
- test: `src/test/java/org/apache/commons/lang3/text/StrBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/StrBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `77916`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 19201, 'completion_tokens': 1940, 'total_tokens': 21141, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 978}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 18817}`

---

- 新增 `testReadFromReader`、`testReadFromReaderAppendsToEnd`、`testReadFromCharBuffer`、`testReadFromCharBufferAppendsToEnd`、`testReadFromReadable`、`testReadFromReadableAppendsToEnd`、`MockReadable`（辅助类）、`testAppendToWriter`、`testAppendToStringBuilder`、`testAppendToStringBuffer`、`testAppendToCharBuffer` 测试方法；需要添加 `import java.io.IOException; import java.io.StringReader; import java.io.StringWriter; import java.nio.CharBuffer;`。

```java
// IMPORTS_START
import java.io.IOException;
import java.io.StringReader;
import java.io.StringWriter;
import java.nio.CharBuffer;
// IMPORTS_END

    //-----------------------------------------------------------------------
    @Test
    public void testReadFromReader() throws Exception {
        String s = "";
        for (int i = 0; i < 100; ++i) {
            StrBuilder sb = new StrBuilder();
            int len = sb.readFrom(new StringReader(s));

            assertEquals(s.length(), len);
            assertEquals(s, sb.toString());

            s += Integer.toString(i);
        }
    }

    @Test
    public void testReadFromReaderAppendsToEnd() throws Exception {
        StrBuilder sb = new StrBuilder("Test");
        sb.readFrom(new StringReader(" 123"));
        assertEquals("Test 123", sb.toString());
    }

    @Test
    public void testReadFromCharBuffer() throws Exception {
        String s = "";
        for (int i = 0; i < 100; ++i) {
            StrBuilder sb = new StrBuilder();
            int len = sb.readFrom(CharBuffer.wrap(s));

            assertEquals(s.length(), len);
            assertEquals(s, sb.toString());

            s += Integer.toString(i);
        }
    }

    @Test
    public void testReadFromCharBufferAppendsToEnd() throws Exception {
        StrBuilder sb = new StrBuilder("Test");
        sb.readFrom(CharBuffer.wrap(" 123"));
        assertEquals("Test 123", sb.toString());
    }

    @Test
    public void testReadFromReadable() throws Exception {
        String s = "";
        for (int i = 0; i < 100; ++i) {
            StrBuilder sb = new StrBuilder();
            int len = sb.readFrom(new MockReadable(s));

            assertEquals(s.length(), len);
            assertEquals(s, sb.toString());

            s += Integer.toString(i);
        }
    }

    @Test
    public void testReadFromReadableAppendsToEnd() throws Exception {
        StrBuilder sb = new StrBuilder("Test");
        sb.readFrom(new MockReadable(" 123"));
        assertEquals("Test 123", sb.toString());
    }

    private static class MockReadable implements Readable {

        private final CharBuffer src;

        public MockReadable(final String src) {
            this.src = CharBuffer.wrap(src);
        }

        @Override
        public int read(final CharBuffer cb) throws IOException {
            return src.read(cb);
        }
    }

    //-----------------------------------------------------------------------
    @Test
    public void testAppendToWriter() throws Exception {
        final StrBuilder sb = new StrBuilder("1234567890");
        final StringWriter writer = new StringWriter();
        writer.append("Test ");

        sb.appendTo(writer);

        assertEquals("Test 1234567890", writer.toString());
    }

    @Test
    public void testAppendToStringBuilder() throws Exception {
        final StrBuilder sb = new StrBuilder("1234567890");
        final StringBuilder builder = new StringBuilder("Test ");

        sb.appendTo(builder);

        assertEquals("Test 1234567890", builder.toString());
    }

    @Test
    public void testAppendToStringBuffer() throws Exception {
        final StrBuilder sb = new StrBuilder("1234567890");
        final StringBuffer buffer = new StringBuffer("Test ");

        sb.appendTo(buffer);

        assertEquals("Test 1234567890", buffer.toString());
    }

    @Test
    public void testAppendToCharBuffer() throws Exception {
        final StrBuilder sb = new StrBuilder("1234567890");
        final String text = "Test ";
        final CharBuffer buffer = CharBuffer.allocate(sb.size() + text.length());
        buffer.put(text);

        sb.appendTo(buffer);

        buffer.flip();
        assertEquals("Test 1234567890", buffer.toString());
    }
```