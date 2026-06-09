# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ea47d47ea8ab89a8ab84488cac0d0ce030c28efd`
- B: `f43534ec04d4c4bae666033e2041ecde21c19a56`
- test: `src/test/java/org/apache/commons/lang3/RegExUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RegExUtils.java']`
- old_test_mode: `methods`
- user_chars: `12924`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3761, 'completion_tokens': 1447, 'total_tokens': 5208}`

---

- 新增 `testReplaceAll`：覆盖生产代码新增/主推的 `replaceAll(CharSequence, Pattern, String)` 重载，并通过 `(CharSequence)` 强制选择新签名。
- 修改 `testReplaceAll_StringPatternString` 为 `testReplaceAllDeprecated`：保留对已废弃 `replaceAll(String, Pattern, String)` 的兼容性断言，对应生产代码新增 deprecated 委托方法。
- 删除旧测试方法名 `testReplaceAll_StringPatternString`：该方法被拆分为新重载测试和 deprecated 旧重载测试。
- import 无需调整：现有 `Pattern`、`Test`、断言静态导入仍可满足编译。

```java
// DELETE_TESTS_START
testReplaceAll_StringPatternString
// DELETE_TESTS_END

@Test
public void testReplaceAll() {
    assertNull(RegExUtils.replaceAll((CharSequence) null, Pattern.compile(""), ""));

    assertEquals("any", RegExUtils.replaceAll((CharSequence) "any", (Pattern) null, ""));
    assertEquals("any", RegExUtils.replaceAll((CharSequence) "any", Pattern.compile(""), null));

    assertEquals("zzz", RegExUtils.replaceAll((CharSequence) "", Pattern.compile(""), "zzz"));
    assertEquals("zzz", RegExUtils.replaceAll((CharSequence) "", Pattern.compile(".*"), "zzz"));
    assertEquals("", RegExUtils.replaceAll((CharSequence) "", Pattern.compile(".+"), "zzz"));
    assertEquals("ZZaZZbZZcZZ", RegExUtils.replaceAll((CharSequence) "abc", Pattern.compile(""), "ZZ"));

    assertEquals("z\nz", RegExUtils.replaceAll((CharSequence) "<__>\n<__>", Pattern.compile("<.*>"), "z"));
    assertEquals("z", RegExUtils.replaceAll((CharSequence) "<__>\n<__>", Pattern.compile("(?s)<.*>"), "z"));

    assertEquals("z", RegExUtils.replaceAll((CharSequence) "<__>\n<__>", Pattern.compile("<.*>", Pattern.DOTALL), "z"));
    assertEquals("z", RegExUtils.replaceAll((CharSequence) "<__>\\n<__>", Pattern.compile("<.*>"), "z"));
    assertEquals("X", RegExUtils.replaceAll((CharSequence) "<A>\nxy\n</A>", Pattern.compile("<A>.*</A>", Pattern.DOTALL), "X"));

    assertEquals("ABC___123", RegExUtils.replaceAll((CharSequence) "ABCabc123", Pattern.compile("[a-z]"), "_"));
    assertEquals("ABC_123", RegExUtils.replaceAll((CharSequence) "ABCabc123", Pattern.compile("[^A-Z0-9]+"), "_"));
    assertEquals("ABC123", RegExUtils.replaceAll((CharSequence) "ABCabc123", Pattern.compile("[^A-Z0-9]+"), ""));
    assertEquals("Lorem_ipsum_dolor_sit", RegExUtils.replaceAll((CharSequence) "Lorem ipsum  dolor   sit", Pattern.compile("( +)([a-z]+)"), "_$2"));
}

@Test
public void testReplaceAllDeprecated() {
    assertNull(RegExUtils.replaceAll(null, Pattern.compile(""), ""));

    assertEquals("any", RegExUtils.replaceAll("any", (Pattern) null, ""));
    assertEquals("any", RegExUtils.replaceAll("any", Pattern.compile(""), null));

    assertEquals("zzz", RegExUtils.replaceAll("", Pattern.compile(""), "zzz"));
    assertEquals("zzz", RegExUtils.replaceAll("", Pattern.compile(".*"), "zzz"));
    assertEquals("", RegExUtils.replaceAll("", Pattern.compile(".+"), "zzz"));
    assertEquals("ZZaZZbZZcZZ", RegExUtils.replaceAll("abc", Pattern.compile(""), "ZZ"));

    assertEquals("z\nz", RegExUtils.replaceAll("<__>\n<__>", Pattern.compile("<.*>"), "z"));
    assertEquals("z", RegExUtils.replaceAll("<__>\n<__>", Pattern.compile("(?s)<.*>"), "z"));

    assertEquals("z", RegExUtils.replaceAll("<__>\n<__>", Pattern.compile("<.*>", Pattern.DOTALL), "z"));
    assertEquals("z", RegExUtils.replaceAll("<__>\\n<__>", Pattern.compile("<.*>"), "z"));
    assertEquals("X", RegExUtils.replaceAll("<A>\nxy\n</A>", Pattern.compile("<A>.*</A>", Pattern.DOTALL), "X"));

    assertEquals("ABC___123", RegExUtils.replaceAll("ABCabc123", Pattern.compile("[a-z]"), "_"));
    assertEquals("ABC_123", RegExUtils.replaceAll("ABCabc123", Pattern.compile("[^A-Z0-9]+"), "_"));
    assertEquals("ABC123", RegExUtils.replaceAll("ABCabc123", Pattern.compile("[^A-Z0-9]+"), ""));
    assertEquals("Lorem_ipsum_dolor_sit", RegExUtils.replaceAll("Lorem ipsum  dolor   sit", Pattern.compile("( +)([a-z]+)"), "_$2"));
}
```