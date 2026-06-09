# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `56f0e1053c9aa767ffaeee37cf06a6056a221163`
- B: `b1762bd557c3d7605490e026bdf31096d83b4dde`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `136863`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 34312, 'completion_tokens': 1944, 'total_tokens': 36256, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1334}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 33928}`

---

- 修改 `testReplacePattern` 方法：跟随生产代码对 `replacePattern` 的 null 安全改造以及 DOTALL 行为的文档化，补充了包含 null 参数、空字符串和正则示例的断言；原有断言保留。
- 修改 `testRemovePattern` 方法：同样跟随 `removePattern` 的 null 安全改造，补充了 null 参数、空字符串和正则示例的断言；原有断言保留。
- 无需调整 import，已有的 `import static org.junit.Assert.*` 覆盖所有新增断言。

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