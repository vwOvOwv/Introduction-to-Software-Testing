# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `d13a40266f9b357d96b71b2ef6bc420443b61dd1`
- B: `612595106054d0ff2320cc15f88cfef8959e1531`
- test: `src/test/java/org/apache/commons/lang3/text/StrBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/StrBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `77916`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 19135, 'completion_tokens': 1354, 'total_tokens': 20489}`

---

- 新增 `testReadFromReader`，覆盖生产代码新增的 `StrBuilder.readFrom(Readable)` 在 `Reader` 分支读取并返回长度的行为。
- 新增 `testReadFromReaderAppendsToEnd`，覆盖 `readFrom` 从 `Reader` 读取时追加到现有内容末尾的行为。
- 新增 `testReadFromCharBuffer`，覆盖 `readFrom` 在 `CharBuffer` 分支读取并返回长度的行为。
- 新增 `testReadFromCharBufferAppendsToEnd`，覆盖 `readFrom` 从 `CharBuffer` 读取时追加到现有内容末尾的行为。
- 新增 `testReadFromReadable`，覆盖 `readFrom` 在普通 `Readable` 分支读取并返回长度的行为，并新增测试辅助类 `MockReadable`。
- 新增 `testReadFromReadableAppendsToEnd`，覆盖 `readFrom` 从普通 `Readable` 读取时追加到现有内容末尾的行为。
- 新增 `testAppendToWriter`，覆盖生产代码新增的 `StrBuilder.appendTo(Appendable)` 在 `Writer` 分支的写入行为。
- 新增 `testAppendToStringBuilder`，覆盖 `appendTo` 在 `StringBuilder` 分支的追加行为。
- 新增 `testAppendToStringBuffer`，覆盖 `appendTo` 在 `StringBuffer` 分支的追加行为。
- 新增 `testAppendToCharBuffer`，覆盖 `appendTo` 在 `CharBuffer` 分支的写入行为。
- 需要调整 import，新增 `java.io.IOException`、`java.io.StringReader`、`java.io.StringWriter` 和 `java.nio.CharBuffer`。

```java
// IMPORTS_START
import org.junit.Test;
import static org.junit.Assert.*;

import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.io.StringWriter;
import java.io.Writer;
import java.nio.CharBuffer;
import java.util.Arrays;

import org.apache.commons.lang3.ArrayUtils;
// IMPORTS_END

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