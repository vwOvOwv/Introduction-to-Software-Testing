# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `56f0e1053c9aa767ffaeee37cf06a6056a221163`
- B: `b1762bd557c3d7605490e026bdf31096d83b4dde`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `136863`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 33538, 'completion_tokens': 674, 'total_tokens': 34212}`

---

- 修改 `testReplacePattern`：生产代码将 `replacePattern` 改为对 `source`、`regex`、`replacement` 的 `null` 入参 no-op，并明确 DOTALL 行为与空串/正则替换语义，因此扩展对应断言。
- 修改 `testRemovePattern`：`removePattern` 通过新的 null-safe `replacePattern` 实现获得 `null` 正则 no-op 与 DOTALL 行为，因此扩展对应断言。
- import 无需调整：旧测试已包含 `assertEquals`、`assertNull` 和 `@Test` 所需 import。

```java
@Test
public void testReplacePattern() {
    assertNull(StringUtils.replacePattern(null, "", ""));
    assertEquals("any", StringUtils.replacePattern("any", null, ""));
    assertEquals("any", StringUtils.replacePattern("any", "", null));

    assertEquals("zzz", StringUtils.replacePattern("", "", "zzz"));
    assertEquals("zzz", StringUtils.replacePattern("", ".*", "zzz"));
    assertEquals("", StringUtils.replacePattern("", ".+", "zzz"));

    assertEquals("z", StringUtils.replacePattern("<__>\n<__>", "<.*>", "z"));
    assertEquals("z", StringUtils.replacePattern("<__>\\n<__>", "<.*>", "z"));
    assertEquals("X", StringUtils.replacePattern("<A>\nxy\n</A>", "<A>.*</A>", "X"));

    assertEquals("ABC___123", StringUtils.replacePattern("ABCabc123", "[a-z]", "_"));
    assertEquals("ABC_123", StringUtils.replacePattern("ABCabc123", "[^A-Z0-9]+", "_"));
    assertEquals("ABC123", StringUtils.replacePattern("ABCabc123", "[^A-Z0-9]+", ""));
    assertEquals("Lorem_ipsum_dolor_sit",
            StringUtils.replacePattern("Lorem ipsum  dolor   sit", "( +)([a-z]+)", "_$2"));
}

@Test
public void testRemovePattern() {
    assertNull(StringUtils.removePattern(null, ""));
    assertEquals("any", StringUtils.removePattern("any", null));

    assertEquals("", StringUtils.removePattern("", ""));
    assertEquals("", StringUtils.removePattern("", ".*"));
    assertEquals("", StringUtils.removePattern("", ".+"));

    assertEquals("AB", StringUtils.removePattern("A<__>\n<__>B", "<.*>"));
    assertEquals("AB", StringUtils.removePattern("A<__>\\n<__>B", "<.*>"));
    assertEquals("", StringUtils.removePattern("<A>x\\ny</A>", "<A>.*</A>"));
    assertEquals("", StringUtils.removePattern("<A>\nxy\n</A>", "<A>.*</A>"));

    assertEquals("ABC123", StringUtils.removePattern("ABCabc123", "[a-z]"));
}
```