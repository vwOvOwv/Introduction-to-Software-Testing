# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e01f2a4a19d1d249204177020a3824cce06251f4`
- B: `cc6a92b1a5bb1a9a1d38d4bce67644dbb1b2b349`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `118666`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 29164, 'completion_tokens': 533, 'total_tokens': 29697}`

---

- 新增 `testToEncodedString`：生产代码新增 `StringUtils.toEncodedString(byte[], Charset)`，测试需覆盖默认字符集、显式文件编码和 UTF-16 编码路径。
- 调整 import：新增 `java.nio.charset.Charset`，用于调用新增的 `toEncodedString` 方法。

```java
// IMPORTS_START
import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertSame;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.UnsupportedEncodingException;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.nio.CharBuffer;
import java.nio.charset.Charset;
import java.util.Arrays;
import java.util.Collections;
import java.util.Iterator;
import java.util.Locale;

import org.apache.commons.lang3.text.WordUtils;
import org.junit.Test;
// IMPORTS_END

/**
 * Tests {@link StringUtils#toEncodedString(byte[], Charset)}
 * 
 * @throws UnsupportedEncodingException
 * @see StringUtils#toEncodedString(byte[], Charset)
 */
@Test
public void testToEncodedString() throws UnsupportedEncodingException {
    final String expectedString = "The quick brown fox jumped over the lazy dog.";
    String encoding = SystemUtils.FILE_ENCODING;
    byte[] expectedBytes = expectedString.getBytes(encoding);
    // sanity check start
    assertArrayEquals(expectedBytes, expectedString.getBytes());
    // sanity check end
    assertEquals(expectedString, StringUtils.toEncodedString(expectedBytes, Charset.defaultCharset()));
    assertEquals(expectedString, StringUtils.toEncodedString(expectedBytes, Charset.forName(encoding)));
    encoding = "UTF-16";
    expectedBytes = expectedString.getBytes(encoding);
    assertEquals(expectedString, StringUtils.toEncodedString(expectedBytes, Charset.forName(encoding)));
}
```