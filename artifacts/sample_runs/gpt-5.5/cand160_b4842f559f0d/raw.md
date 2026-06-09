# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `94184ce3837e4268f3d0a7459f90e6bb920dd54a`
- B: `b4842f559f0d8b8b5a98a19b1f3795a42c1a2614`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `138497`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 34019, 'completion_tokens': 642, 'total_tokens': 34661}`

---

- 新增 `testRemoveAll`，对应生产代码新增 `StringUtils.removeAll(String, String)`，覆盖 null/空正则/DOTALL 差异/非法正则异常等行为；不需要调整 import，因为旧测试已导入 `PatternSyntaxException`、`fail` 等依赖。
- 新增 `testRemoveFirst`，对应生产代码新增 `StringUtils.removeFirst(String, String)`，覆盖仅移除首个匹配、DOTALL 差异及非法正则异常；不需要调整 import。

```java
@Test
public void testRemoveAll() {
    assertNull(StringUtils.removeAll(null, ""));
    assertEquals("any", StringUtils.removeAll("any", null));

    assertEquals("any", StringUtils.removeAll("any", ""));
    assertEquals("", StringUtils.removeAll("any", ".*"));
    assertEquals("", StringUtils.removeAll("any", ".+"));
    assertEquals("", StringUtils.removeAll("any", ".?"));

    assertEquals("A\nB", StringUtils.removeAll("A<__>\n<__>B", "<.*>"));
    assertEquals("AB", StringUtils.removeAll("A<__>\n<__>B", "(?s)<.*>"));
    assertEquals("ABC123", StringUtils.removeAll("ABCabc123abc", "[a-z]"));

    try {
        StringUtils.removeAll("any", "{badRegexSyntax}");
        fail("StringUtils.removeAll expecting PatternSyntaxException");
    } catch (final PatternSyntaxException ex) {
        // empty
    }
}

@Test
public void testRemoveFirst() {
    assertNull(StringUtils.removeFirst(null, ""));
    assertEquals("any", StringUtils.removeFirst("any", null));

    assertEquals("any", StringUtils.removeFirst("any", ""));
    assertEquals("", StringUtils.removeFirst("any", ".*"));
    assertEquals("", StringUtils.removeFirst("any", ".+"));
    assertEquals("bc", StringUtils.removeFirst("abc", ".?"));

    assertEquals("A\n<__>B", StringUtils.removeFirst("A<__>\n<__>B", "<.*>"));
    assertEquals("AB", StringUtils.removeFirst("A<__>\n<__>B", "(?s)<.*>"));
    assertEquals("ABCbc123", StringUtils.removeFirst("ABCabc123", "[a-z]"));
    assertEquals("ABC123abc", StringUtils.removeFirst("ABCabc123abc", "[a-z]+"));

    try {
        StringUtils.removeFirst("any", "{badRegexSyntax}");
        fail("StringUtils.removeFirst expecting PatternSyntaxException");
    } catch (final PatternSyntaxException ex) {
        // empty
    }
}
```