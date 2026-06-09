# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `439ee3bc05432ca2d980894b35b8b73e4a9d2932`
- B: `f9b486a17171359e880bfa91a14602fe95a5dbf8`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `4514`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1596, 'completion_tokens': 5141, 'total_tokens': 6737, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 4742}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1212}`

---

- 新增静态字段 `HARD_SPACE`，用于在测试中引用不间断空格字符 `\u00A0`。
- 修改 `@Test testNormalizeSpace` 方法，在原有断言之后增加对新行为（硬空格被保留）的验证。
- 无需调整任何 import。

```java
static final String HARD_SPACE = "\u00A0";

@Test
public void testNormalizeSpace() {
    assertEquals(null, StringUtils.normalizeSpace(null));
    assertEquals("", StringUtils.normalizeSpace(""));
    assertEquals("", StringUtils.normalizeSpace(" "));
    assertEquals("", StringUtils.normalizeSpace("\t"));
    assertEquals("", StringUtils.normalizeSpace("\n"));
    assertEquals("", StringUtils.normalizeSpace("\u0009"));
    assertEquals("", StringUtils.normalizeSpace("\u000B"));
    assertEquals("", StringUtils.normalizeSpace("\u000C"));
    assertEquals("", StringUtils.normalizeSpace("\u001C"));
    assertEquals("", StringUtils.normalizeSpace("\u001D"));
    assertEquals("", StringUtils.normalizeSpace("\u001E"));
    assertEquals("", StringUtils.normalizeSpace("\u001F"));
    assertEquals("", StringUtils.normalizeSpace("\f"));
    assertEquals("", StringUtils.normalizeSpace("\r"));
    assertEquals("a", StringUtils.normalizeSpace("  a  "));
    assertEquals("a b c", StringUtils.normalizeSpace("  a  b   c  "));
    assertEquals("a b c", StringUtils.normalizeSpace("a\t\f\r  b\u000B   c\n"));
    assertEquals("a   b c", StringUtils.normalizeSpace("a\t\f\r  " + HARD_SPACE + HARD_SPACE + "b\u000B   c\n"));
}
```