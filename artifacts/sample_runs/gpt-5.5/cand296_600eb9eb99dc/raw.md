# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `855a5238558d87dd70c6195e12f167b5848808bb`
- B: `600eb9eb99dc5c03b047e3c81b49ee4769787c6a`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `161328`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 39524, 'completion_tokens': 340, 'total_tokens': 39864}`

---

- 新增 `testToCodePoints`，对应生产代码新增 `StringUtils.toCodePoints(CharSequence)`，覆盖普通 BMP 字符、孤立代理项、有效补充字符、`null` 和空串返回值。
- 不需要调整 import，旧测试已静态导入 `assertArrayEquals` 和 `assertNull`，且 `ArrayUtils` 与测试类同包可直接引用。

```java
    @Test
    public void testToCodePoints() throws Exception {
        final int orphanedHighSurrogate = 0xD801;
        final int orphanedLowSurrogate = 0xDC00;
        final int supplementary = 0x2070E;

        final int[] codePoints = {'a', orphanedHighSurrogate, 'b', 'c', supplementary,
                'd', orphanedLowSurrogate, 'e'};
        final String s = new String(codePoints, 0, codePoints.length);
        assertArrayEquals(codePoints, StringUtils.toCodePoints(s));

        assertNull(StringUtils.toCodePoints(null));
        assertArrayEquals(ArrayUtils.EMPTY_INT_ARRAY, StringUtils.toCodePoints(""));
    }
```