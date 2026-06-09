# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `96e1e3d0c5abd3405719669e06214c1fdc53e85f`
- B: `4c3f1dd00ee7b8800478edb2b50dd687103b5f2a`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `7212`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2421, 'completion_tokens': 1369, 'total_tokens': 3790}`

---

- 修改 `testRepeat_StringStringInt`：对应 `StringUtils.repeat(String, String, int)` 现在会在结果长度整数溢出时抛出 `IllegalArgumentException`，新增 `assertThrows` 断言覆盖该行为；无需调整 import。
- 修改 `testReplace_StringStringArrayStringArray`：仅同步测试 diff 中的注释格式调整，不改变断言行为；无需调整 import。

```java
@Test
void testRepeat_StringStringInt() {
    assertNull(StringUtils.repeat(null, null, 2));
    assertNull(StringUtils.repeat(null, "x", 2));
    assertEquals("", StringUtils.repeat("", null, 2));
    assertEquals("", StringUtils.repeat("ab", "", 0));
    assertEquals("", StringUtils.repeat("", "", 2));
    assertEquals("xx", StringUtils.repeat("", "x", 3));
    assertEquals("?, ?, ?", StringUtils.repeat("?", ", ", 3));
    assertThrows(IllegalArgumentException.class, () -> StringUtils.repeat("?", ", ", 1_073_741_824));
}

@Test
void testReplace_StringStringArrayStringArray() {
    // JAVADOC TESTS START
    assertNull(StringUtils.replaceEach(null, new String[]{"a"}, new String[]{"b"}));
    assertEquals(StringUtils.replaceEach("", new String[]{"a"}, new String[]{"b"}), "");
    assertEquals(StringUtils.replaceEach("aba", null, null), "aba");
    assertEquals(StringUtils.replaceEach("aba", new String[0], null), "aba");
    assertEquals(StringUtils.replaceEach("aba", null, new String[0]), "aba");
    assertEquals(StringUtils.replaceEach("aba", new String[]{"a"}, null), "aba");

    assertEquals(StringUtils.replaceEach("aba", new String[]{"a"}, new String[]{""}), "b");
    assertEquals(StringUtils.replaceEach("aba", new String[]{null}, new String[]{"a"}), "aba");
    assertEquals(StringUtils.replaceEach("abcde", new String[]{"ab", "d"}, new String[]{"w", "t"}), "wcte");
    assertEquals(StringUtils.replaceEach("abcde", new String[]{"ab", "d"}, new String[]{"d", "t"}), "dcte");
    // JAVADOC TESTS END

    assertEquals("bcc", StringUtils.replaceEach("abc", new String[]{"a", "b"}, new String[]{"b", "c"}));
    assertEquals("q651.506bera", StringUtils.replaceEach("d216.102oren",
            new String[]{"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                    "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D",
                    "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                    "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9"},
            new String[]{"n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "a",
                    "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "N", "O", "P", "Q",
                    "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D", "E", "F", "G",
                    "H", "I", "J", "K", "L", "M", "5", "6", "7", "8", "9", "1", "2", "3", "4"}));

    // Test null safety inside arrays - LANG-552
    assertEquals(StringUtils.replaceEach("aba", new String[]{"a"}, new String[]{null}), "aba");
    assertEquals(StringUtils.replaceEach("aba", new String[]{"a", "b"}, new String[]{"c", null}), "cbc");

    assertIllegalArgumentException(() -> StringUtils.replaceEach("abba", new String[] { "a" }, new String[] { "b", "a" }),
            "StringUtils.replaceEach(String, String[], String[]) expecting IllegalArgumentException");
}
```