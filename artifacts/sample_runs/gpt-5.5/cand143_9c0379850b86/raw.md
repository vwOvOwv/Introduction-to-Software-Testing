# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e1077c023de72a2935c144f3533d4d4a69924699`
- B: `9c0379850b869e3a02320f9a5149eaad2c4cb76b`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `90595`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 22278, 'completion_tokens': 561, 'total_tokens': 22839}`

---

- 新增测试方法 `testDefaultIfEmpty_StringBuilders`，覆盖 `defaultIfEmpty(CharSequence, CharSequence)` 对 `StringBuilder` 空值与非空值的行为。
- 新增测试方法 `testDefaultIfEmpty_StringBuffers`，覆盖 `defaultIfEmpty(CharSequence, CharSequence)` 对 `StringBuffer` 空值与非空值的行为。
- 新增测试方法 `testDefaultIfEmpty_CharBuffers`，覆盖 `defaultIfEmpty(CharSequence, CharSequence)` 对 `CharBuffer` 空值与非空值的行为。
- 需要调整 import，新增 `java.nio.CharBuffer` 以支持新增 `CharBuffer.wrap(...)` 测试用例。

```java
// IMPORTS_START
import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.nio.CharBuffer;
import java.util.Arrays;
import java.util.Collections;
import java.util.Iterator;
import java.util.Locale;

import junit.framework.TestCase;

import org.apache.commons.lang3.text.WordUtils;
// IMPORTS_END

    public void testDefaultIfEmpty_StringBuilders() {
        assertEquals("NULL", StringUtils.defaultIfEmpty(new StringBuilder(""), new StringBuilder("NULL")).toString());
        assertEquals("abc", StringUtils.defaultIfEmpty(new StringBuilder("abc"), new StringBuilder("NULL")).toString());
        assertNull(StringUtils.defaultIfEmpty(new StringBuilder(""), null));
    }

    public void testDefaultIfEmpty_StringBuffers() {
        assertEquals("NULL", StringUtils.defaultIfEmpty(new StringBuffer(""), new StringBuffer("NULL")).toString());
        assertEquals("abc", StringUtils.defaultIfEmpty(new StringBuffer("abc"), new StringBuffer("NULL")).toString());
        assertNull(StringUtils.defaultIfEmpty(new StringBuffer(""), null));
    }

    public void testDefaultIfEmpty_CharBuffers() {
        assertEquals("NULL", StringUtils.defaultIfEmpty(CharBuffer.wrap(""), CharBuffer.wrap("NULL")).toString());
        assertEquals("abc", StringUtils.defaultIfEmpty(CharBuffer.wrap("abc"), CharBuffer.wrap("NULL")).toString());
        assertNull(StringUtils.defaultIfEmpty(CharBuffer.wrap(""), null));
    }
```