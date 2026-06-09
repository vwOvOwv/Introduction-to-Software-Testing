# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `a40b2a907a69e51675d7d0502b2608833c4da343`
- B: `c37a911d3a1541adc25c8d76f717015b2266d123`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `19733`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5771, 'completion_tokens': 2490, 'total_tokens': 8261}`

---

- 修改 `testAbbreviate_StringInt`：生产代码将默认省略标记委托到新重载，并新增对过小 `maxWidth` 的异常路径，测试中保留原断言并清理异常断言写法。
- 新增 `testAbbreviate_StringStringInt`：覆盖新增的 `abbreviate(String, String, int)` 重载，包括空标记、不同省略标记和宽度过小异常。
- 修改 `testAbbreviate_StringIntInt`：生产代码异常逻辑改为经由新标记长度计算，测试中仅调整异常断言写法以适配新实现。
- 新增 `testAbbreviate_StringStringIntInt` 和辅助方法 `assertAbbreviateWithAbbrevMarkerAndOffset`：覆盖新增的 `abbreviate(String, String, int, int)` 重载及不同 offset/marker 组合。
- 不需要调整 import。

```java
@Test
public void testAbbreviate_StringInt() {
    assertNull(StringUtils.abbreviate(null, 10));
    assertEquals("", StringUtils.abbreviate("", 10));
    assertEquals("short", StringUtils.abbreviate("short", 10));
    assertEquals("Now is ...", StringUtils.abbreviate("Now is the time for all good men to come to the aid of their party.", 10));

    final String raspberry = "raspberry peach";
    assertEquals("raspberry p...", StringUtils.abbreviate(raspberry, 14));
    assertEquals("raspberry peach", StringUtils.abbreviate("raspberry peach", 15));
    assertEquals("raspberry peach", StringUtils.abbreviate("raspberry peach", 16));
    assertEquals("abc...", StringUtils.abbreviate("abcdefg", 6));
    assertEquals("abcdefg", StringUtils.abbreviate("abcdefg", 7));
    assertEquals("abcdefg", StringUtils.abbreviate("abcdefg", 8));
    assertEquals("a...", StringUtils.abbreviate("abcdefg", 4));
    assertEquals("", StringUtils.abbreviate("", 4));

    try {
        StringUtils.abbreviate("abc", 3);
        fail("StringUtils.abbreviate expecting IllegalArgumentException");
    } catch (final IllegalArgumentException expected) {
        // empty
    }
}

@Test
public void testAbbreviate_StringStringInt() {
    assertNull(StringUtils.abbreviate(null, null, 10));
    assertNull(StringUtils.abbreviate(null, "...", 10));
    assertEquals("paranaguacu", StringUtils.abbreviate("paranaguacu", null, 10));
    assertEquals("", StringUtils.abbreviate("", "...", 2));
    assertEquals("wai**", StringUtils.abbreviate("waiheke", "**", 5));
    assertEquals("And af,,,,", StringUtils.abbreviate("And after a long time, he finally met his son.", ",,,,", 10));

    final String raspberry = "raspberry peach";
    assertEquals("raspberry pe..", StringUtils.abbreviate(raspberry, "..", 14));
    assertEquals("raspberry peach", StringUtils.abbreviate("raspberry peach", "---*---", 15));
    assertEquals("raspberry peach", StringUtils.abbreviate("raspberry peach", ".", 16));
    assertEquals("abc()(", StringUtils.abbreviate("abcdefg", "()(", 6));
    assertEquals("abcdefg", StringUtils.abbreviate("abcdefg", ";", 7));
    assertEquals("abcdefg", StringUtils.abbreviate("abcdefg", "_-", 8));
    assertEquals("abc.", StringUtils.abbreviate("abcdefg", ".", 4));
    assertEquals("", StringUtils.abbreviate("", 4));

    try {
        @SuppressWarnings("unused")
        final
        String res = StringUtils.abbreviate("abcdefghij", "...", 3);
        fail("StringUtils.abbreviate expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        // empty
    }
}

@Test
public void testAbbreviate_StringIntInt() {
    assertNull(StringUtils.abbreviate(null, 10, 12));
    assertEquals("", StringUtils.abbreviate("", 0, 10));
    assertEquals("", StringUtils.abbreviate("", 2, 10));

    try {
        StringUtils.abbreviate("abcdefghij", 0, 3);
        fail("StringUtils.abbreviate expecting IllegalArgumentException");
    } catch (final IllegalArgumentException expected) {
        // empty
    }
    try {
        StringUtils.abbreviate("abcdefghij", 5, 6);
        fail("StringUtils.abbreviate expecting IllegalArgumentException");
    } catch (final IllegalArgumentException expected) {
        // empty
    }

    final String raspberry = "raspberry peach";
    assertEquals("raspberry peach", StringUtils.abbreviate(raspberry, 11, 15));

    assertNull(StringUtils.abbreviate(null, 7, 14));
    assertAbbreviateWithOffset("abcdefg...", -1, 10);
    assertAbbreviateWithOffset("abcdefg...", 0, 10);
    assertAbbreviateWithOffset("abcdefg...", 1, 10);
    assertAbbreviateWithOffset("abcdefg...", 2, 10);
    assertAbbreviateWithOffset("abcdefg...", 3, 10);
    assertAbbreviateWithOffset("abcdefg...", 4, 10);
    assertAbbreviateWithOffset("...fghi...", 5, 10);
    assertAbbreviateWithOffset("...ghij...", 6, 10);
    assertAbbreviateWithOffset("...hijk...", 7, 10);
    assertAbbreviateWithOffset("...ijklmno", 8, 10);
    assertAbbreviateWithOffset("...ijklmno", 9, 10);
    assertAbbreviateWithOffset("...ijklmno", 10, 10);
    assertAbbreviateWithOffset("...ijklmno", 10, 10);
    assertAbbreviateWithOffset("...ijklmno", 11, 10);
    assertAbbreviateWithOffset("...ijklmno", 12, 10);
    assertAbbreviateWithOffset("...ijklmno", 13, 10);
    assertAbbreviateWithOffset("...ijklmno", 14, 10);
    assertAbbreviateWithOffset("...ijklmno", 15, 10);
    assertAbbreviateWithOffset("...ijklmno", 16, 10);
    assertAbbreviateWithOffset("...ijklmno", Integer.MAX_VALUE, 10);
}

@Test
public void testAbbreviate_StringStringIntInt() {
    assertNull(StringUtils.abbreviate(null, null, 10, 12));
    assertNull(StringUtils.abbreviate(null, "...", 10, 12));
    assertEquals("", StringUtils.abbreviate("", null, 0, 10));
    assertEquals("", StringUtils.abbreviate("", "...", 2, 10));

    try {
        StringUtils.abbreviate("abcdefghij", "::", 0, 2);
        fail("StringUtils.abbreviate expecting IllegalArgumentException");
    } catch (final IllegalArgumentException expected) {
        // empty
    }
    try {
        StringUtils.abbreviate("abcdefghij", "!!!", 5, 6);
        fail("StringUtils.abbreviate expecting IllegalArgumentException");
    } catch (final IllegalArgumentException expected) {
        // empty
    }

    final String raspberry = "raspberry peach";
    assertEquals("raspberry peach", StringUtils.abbreviate(raspberry, "--", 12, 15));

    assertNull(StringUtils.abbreviate(null, ";", 7, 14));
    assertAbbreviateWithAbbrevMarkerAndOffset("abcdefgh;;", ";;", -1, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("abcdefghi.", ".", 0, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("abcdefgh++", "++", 1, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("abcdefghi*", "*", 2, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("abcdef{{{{", "{{{{", 4, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("abcdef____", "____", 5, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("==fghijk==", "==", 5, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("___ghij___", "___", 6, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("/ghijklmno", "/", 7, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("/ghijklmno", "/", 8, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("/ghijklmno", "/", 9, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("///ijklmno", "///", 10, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("//hijklmno", "//", 10, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("//hijklmno", "//", 11, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("...ijklmno", "...", 12, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("/ghijklmno", "/", 13, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("/ghijklmno", "/", 14, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("999ijklmno", "999", 15, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("_ghijklmno", "_", 16, 10);
    assertAbbreviateWithAbbrevMarkerAndOffset("+ghijklmno", "+", Integer.MAX_VALUE, 10);
}

private void assertAbbreviateWithAbbrevMarkerAndOffset(final String expected, final String abbrevMarker, final int offset, final int maxWidth) {
    final String abcdefghijklmno = "abcdefghijklmno";
    final String message = "abbreviate(String,String,int,int) failed";
    final String actual = StringUtils.abbreviate(abcdefghijklmno, abbrevMarker, offset, maxWidth);
    if (offset >= 0 && offset < abcdefghijklmno.length()) {
        assertTrue(message + " -- should contain offset character",
                actual.indexOf((char) ('a' + offset)) != -1);
    }
    assertTrue(message + " -- should not be greater than maxWidth",
            actual.length() <= maxWidth);
    assertEquals(message, expected, actual);
}
```