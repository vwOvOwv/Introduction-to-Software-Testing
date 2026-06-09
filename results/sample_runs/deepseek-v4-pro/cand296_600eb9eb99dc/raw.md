# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `855a5238558d87dd70c6195e12f167b5848808bb`
- B: `600eb9eb99dc5c03b047e3c81b49ee4769787c6a`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `161328`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 40567, 'completion_tokens': 2554, 'total_tokens': 43121, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2167}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 40183}`

---

- 将新增 `testToCodePoints` 测试方法，验证新增的 `StringUtils.toCodePoints(CharSequence)` 方法的 null、空字符串、代理对及普通字符的正确性。
- 由于新测试方法内使用 `assertArrayEquals` 与 `assertNull`，而旧的逐个静态断言导入已改为星号导入 `import static org.junit.Assert.*;`，因此需更新 import 区块以匹配提交 B 的变更。

```java
// IMPORTS_START
import static org.junit.Assert.*;

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
import java.util.Objects;
import java.util.regex.PatternSyntaxException;

import org.apache.commons.lang3.text.WordUtils;
import org.junit.Test;
// IMPORTS_END

    @Test
    public void testToCodePoints() throws Exception {
        final int orphanedHighSurrogate = 0xD801;
        final int orphanedLowSurrogate = 0xDC00;
        final int supplementary = 0x2070E;
        
        final int[] codePoints = {'a', orphanedHighSurrogate, 'b','c', supplementary, 
                'd', orphanedLowSurrogate, 'e'};
        final String s = new String(codePoints, 0, codePoints.length);
        assertArrayEquals(codePoints, StringUtils.toCodePoints(s));
        
        assertNull(StringUtils.toCodePoints(null));
        assertArrayEquals(ArrayUtils.EMPTY_INT_ARRAY, StringUtils.toCodePoints(""));
    }
```