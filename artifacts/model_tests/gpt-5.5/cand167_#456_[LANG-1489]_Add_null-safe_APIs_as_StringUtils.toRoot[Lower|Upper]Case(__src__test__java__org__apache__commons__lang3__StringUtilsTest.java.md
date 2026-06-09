# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `7c32e527651a8a235d1b78b2f5d3f53d5e9bb6cb`
- B: `ba1c22ce8378d389a0ee267e2f75a17a4860c7ba`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `165572`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 40406, 'completion_tokens': 829, 'total_tokens': 41235}`

---

- 新增 `testToRootLowerCase`，覆盖新增的 `StringUtils.toRootLowerCase(String)` 对 `null`、普通大小写转换以及土耳其默认 Locale 下仍使用 `Locale.ROOT` 的行为。
- 新增 `testToRootUpperCase`，覆盖新增的 `StringUtils.toRootUpperCase(String)` 对 `null`、普通大小写转换以及土耳其默认 Locale 下仍使用 `Locale.ROOT` 的行为。
- 需要调整 import：新增 `assertNotEquals` 的静态导入以支持 Locale 差异的 sanity check。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.UnsupportedEncodingException;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.nio.CharBuffer;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;
import java.util.Objects;
import java.util.regex.PatternSyntaxException;

import org.apache.commons.lang3.text.WordUtils;
import org.junit.jupiter.api.Test;
// IMPORTS_END

@Test
public void testToRootLowerCase() {
    assertEquals(null, StringUtils.toRootLowerCase(null));
    assertEquals("a", StringUtils.toRootLowerCase("A"));
    assertEquals("a", StringUtils.toRootLowerCase("a"));
    final Locale TURKISH = Locale.forLanguageTag("tr");
    // Sanity checks:
    assertNotEquals("title", "TITLE".toLowerCase(TURKISH));
    assertEquals("title", "TITLE".toLowerCase(Locale.ROOT));
    assertEquals("title", StringUtils.toRootLowerCase("TITLE"));
    // Make sure we are not using the default Locale:
    Locale defaultLocales = Locale.getDefault();
    try {
        Locale.setDefault(TURKISH);
        assertEquals("title", StringUtils.toRootLowerCase("TITLE"));
    } finally {
        Locale.setDefault(defaultLocales);
    }
}

@Test
public void testToRootUpperCase() {
    assertEquals(null, StringUtils.toRootUpperCase(null));
    assertEquals("A", StringUtils.toRootUpperCase("a"));
    assertEquals("A", StringUtils.toRootUpperCase("A"));
    final Locale TURKISH = Locale.forLanguageTag("tr");
    // Sanity checks:
    assertNotEquals("TITLE", "title".toUpperCase(TURKISH));
    assertEquals("TITLE", "title".toUpperCase(Locale.ROOT));
    assertEquals("TITLE", StringUtils.toRootUpperCase("title"));
    // Make sure we are not using the default Locale:
    Locale defaultLocales = Locale.getDefault();
    try {
        Locale.setDefault(TURKISH);
        assertEquals("TITLE", StringUtils.toRootUpperCase("title"));
    } finally {
        Locale.setDefault(defaultLocales);
    }
}
```