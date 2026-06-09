# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `bd25bdcf802194e39ab101c47a8b16f996d47b9e`
- B: `972aa7b29a7cb7306b9e0737bac86fa42d6218ac`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `9627`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3123, 'completion_tokens': 1811, 'total_tokens': 4934}`

---

- 修改 `testReplace_StringStringArrayStringArrayBoolean`：生产代码将 `replaceEachRepeatedly` 的递归 TTL 改为 `max(searchList.length, DEFAULT_TTL)`，测试需补充默认 TTL、较大替换列表 TTL、递归收敛与循环引用场景断言。
- 不需要调整 import：新增断言仍只使用既有的 `assertEquals`、`assertNull`、`assertThrows`。

```java
@Test
public void testReplace_StringStringArrayStringArrayBoolean() {
    //JAVADOC TESTS START
    assertNull(StringUtils.replaceEachRepeatedly(null, new String[]{"a"}, new String[]{"b"}));
    assertEquals("", StringUtils.replaceEachRepeatedly("", new String[]{"a"}, new String[]{"b"}));
    assertEquals("aba", StringUtils.replaceEachRepeatedly("aba", null, null));
    assertEquals("aba", StringUtils.replaceEachRepeatedly("aba", new String[0], null));
    assertEquals("aba", StringUtils.replaceEachRepeatedly("aba", null, new String[0]));
    assertEquals("aba", StringUtils.replaceEachRepeatedly("aba", new String[0], null));

    assertEquals("b", StringUtils.replaceEachRepeatedly("aba", new String[]{"a"}, new String[]{""}));
    assertEquals("aba", StringUtils.replaceEachRepeatedly("aba", new String[]{null}, new String[]{"a"}));
    assertEquals("wcte", StringUtils.replaceEachRepeatedly("abcde", new String[]{"ab", "d"}, new String[]{"w", "t"}));
    assertEquals("tcte", StringUtils.replaceEachRepeatedly("abcde", new String[]{"ab", "d"}, new String[]{"d", "t"}));

    // Test recursive replacement - LANG-1528 & LANG-1753
    assertEquals("blaan", StringUtils.replaceEachRepeatedly("blllaan", new String[]{"llaan"}, new String[]{"laan"}));
    assertEquals("blaan", StringUtils.replaceEachRepeatedly("bllllaan", new String[]{"llaan"}, new String[]{"laan"}));

    // Test default TTL for smaller search lists. 32 characters reduced to 16, then 8, 4, 2, 1.
    assertEquals("a", StringUtils.replaceEachRepeatedly("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            new String[]{"aa"}, new String[]{"a"}));

    // Test default TTL exceeded. 33 characters reduced to 17, then 9, 5, 3, 2 (still found).
    assertThrows(
            IllegalStateException.class,
            () -> StringUtils.replaceEachRepeatedly("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                    new String[]{"aa"}, new String[]{"a"}),
            "Cannot be resolved within the default time-to-live limit");

    // Test larger TTL for larger search lists. Replace repeatedly until there are no more possible replacements.
    assertEquals("000000000", StringUtils.replaceEachRepeatedly("aA0aA0aA0",
            new String[]{"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                    "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D",
                    "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                    "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9"},
            new String[]{"b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
                    "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E",
                    "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
                    "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"}));

    // Test long infinite cycle: a -> b -> ... -> 9 -> 0 -> a -> b -> ...
    assertThrows(
            IllegalStateException.class,
            () -> StringUtils.replaceEachRepeatedly("a",
                    new String[]{"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                            "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D",
                            "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                            "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"},
                    new String[]{"b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
                            "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E",
                            "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
                            "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a"}),
            "Should be a circular reference");

    assertThrows(
            IllegalStateException.class,
            () -> StringUtils.replaceEachRepeatedly("%{key1}",
                    new String[] {"%{key1}", "%{key2}", "%{key3}"},
                    new String[] {"Key1 %{key2}", "Key2 %{key3}", "Key3 %{key1}"}),
            "Should be a circular reference");

    assertThrows(
            IllegalStateException.class,
            () -> StringUtils.replaceEachRepeatedly("abcde", new String[]{"ab", "d"}, new String[]{"d", "ab"}),
            "Should be a circular reference");

    //JAVADOC TESTS END
}
```