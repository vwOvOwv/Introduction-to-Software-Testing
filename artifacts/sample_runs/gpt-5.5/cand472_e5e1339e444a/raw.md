# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `1dd511132f104e15d370c468f8afc267d9ae827e`
- B: `e5e1339e444a2e0c0835b318a20b38c170de15d5`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `11936`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3225, 'completion_tokens': 1370, 'total_tokens': 4595}`

---

- 新增 `testGetBytes_Charset`，覆盖新增的 `StringUtils.getBytes(String, Charset)` 对 `null`、默认字符集和指定字符集的行为；需要新增 `StandardCharsets` import。
- 新增 `testGetBytes_String`，覆盖新增的 `StringUtils.getBytes(String, String)` 对 `null`、默认字符集名称和指定字符集名称的行为。
- 修改 `testStringUtilsCharSequenceContract`，将新增的两个以 `String` 为首参且返回 `byte[]` 的 `getBytes` 方法加入排除列表，匹配生产代码新增 API。
- 不删除 `testUnescapeSurrogatePairs` 和 `testWrapIfMissing_StringChar`，它们与本次生产行为变更无关。

```java
import java.nio.charset.StandardCharsets;

@Test
public void testGetBytes_Charset() {
    assertArrayEquals(ArrayUtils.EMPTY_BYTE_ARRAY, StringUtils.getBytes(null, (Charset) null));
    assertArrayEquals(StringUtils.EMPTY.getBytes(), StringUtils.getBytes(StringUtils.EMPTY, (Charset) null));
    assertArrayEquals(StringUtils.EMPTY.getBytes(StandardCharsets.US_ASCII),
        StringUtils.getBytes(StringUtils.EMPTY, StandardCharsets.US_ASCII));
}

@Test
public void testGetBytes_String() throws UnsupportedEncodingException {
    assertArrayEquals(ArrayUtils.EMPTY_BYTE_ARRAY, StringUtils.getBytes(null, (String) null));
    assertArrayEquals(StringUtils.EMPTY.getBytes(), StringUtils.getBytes(StringUtils.EMPTY, (String) null));
    assertArrayEquals(StringUtils.EMPTY.getBytes(StandardCharsets.US_ASCII.name()),
        StringUtils.getBytes(StringUtils.EMPTY, StandardCharsets.US_ASCII.name()));
}

@Test
public void testStringUtilsCharSequenceContract() {
    final Class<StringUtils> c = StringUtils.class;
    // Methods that are expressly excluded from testStringUtilsCharSequenceContract()
    final String[] excludeMethods = {
        "public static int org.apache.commons.lang3.StringUtils.compare(java.lang.String,java.lang.String)",
        "public static int org.apache.commons.lang3.StringUtils.compare(java.lang.String,java.lang.String,boolean)",
        "public static int org.apache.commons.lang3.StringUtils.compareIgnoreCase(java.lang.String,java.lang.String)",
        "public static int org.apache.commons.lang3.StringUtils.compareIgnoreCase(java.lang.String,java.lang.String,boolean)",
        "public static byte[] org.apache.commons.lang3.StringUtils.getBytes(java.lang.String,java.nio.charset.Charset)",
        "public static byte[] org.apache.commons.lang3.StringUtils.getBytes(java.lang.String,java.lang.String) throws java.io.UnsupportedEncodingException"
    };
    final Method[] methods = c.getMethods();

    for (final Method m : methods) {
        final String methodStr = m.toString();
        if (m.getReturnType() == String.class || m.getReturnType() == String[].class) {
            // Assume this is mutable and ensure the first parameter is not CharSequence.
            // It may be String or it may be something else (String[], Object, Object[]) so
            // don't actively test for that.
            final Class<?>[] params = m.getParameterTypes();
            if (params.length > 0 && (params[0] == CharSequence.class || params[0] == CharSequence[].class)) {
                assertTrue(!ArrayUtils.contains(excludeMethods, methodStr),
                        "The method \"" + methodStr + "\" appears to be mutable in spirit and therefore must not accept a CharSequence");
            }
        } else {
            // Assume this is immutable in spirit and ensure the first parameter is not String.
            // As above, it may be something other than CharSequence.
            final Class<?>[] params = m.getParameterTypes();
            if (params.length > 0 && (params[0] == String.class || params[0] == String[].class)) {
                assertTrue(ArrayUtils.contains(excludeMethods, methodStr),
                        "The method \"" + methodStr + "\" appears to be immutable in spirit and therefore must not accept a String");
            }
        }
    }
}
```