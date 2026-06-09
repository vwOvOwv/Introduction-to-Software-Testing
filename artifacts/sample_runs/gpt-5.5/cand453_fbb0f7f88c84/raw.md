# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `d99f581745097c9562f1d701a6da66cd81a550f2`
- B: `fbb0f7f88c84001e0a92dae6a71b7e43bda65a56`
- test: `src/test/java/org/apache/commons/lang3/text/WordUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/WordUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `21548`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5666, 'completion_tokens': 515, 'total_tokens': 6181}`

---

- 修改 `testWrap_StringInt`：生产代码调整了 `WordUtils.wrap` 对最后一行和前导空格的处理，因此在该测试中新增覆盖“新行前导空格被移除、尾随空格保留”的断言；无需调整 import。

```java
@Test
public void testWrap_StringInt() {
    assertEquals(null, WordUtils.wrap(null, 20));
    assertEquals(null, WordUtils.wrap(null, -1));
    
    assertEquals("", WordUtils.wrap("", 20));
    assertEquals("", WordUtils.wrap("", -1));
    
    // normal
    final String systemNewLine = System.getProperty("line.separator");
    String input = "Here is one line of text that is going to be wrapped after 20 columns.";
    String expected = "Here is one line of" + systemNewLine + "text that is going" 
        + systemNewLine + "to be wrapped after" + systemNewLine + "20 columns.";
    assertEquals(expected, WordUtils.wrap(input, 20));
    
    // long word at end
    input = "Click here to jump to the commons website - http://commons.apache.org";
    expected = "Click here to jump" + systemNewLine + "to the commons" + systemNewLine 
        + "website -" + systemNewLine + "http://commons.apache.org";
    assertEquals(expected, WordUtils.wrap(input, 20));
    
    // long word in middle
    input = "Click here, http://commons.apache.org, to jump to the commons website";
    expected = "Click here," + systemNewLine + "http://commons.apache.org," + systemNewLine 
        + "to jump to the" + systemNewLine + "commons website";
    assertEquals(expected, WordUtils.wrap(input, 20));

    // leading spaces on a new line are stripped
    // trailing spaces are not stripped
    input = "word1             word2                        word3";
    expected = "word1  " + systemNewLine + "word2  " + systemNewLine + "word3";
    assertEquals(expected, WordUtils.wrap(input, 7));
}
```