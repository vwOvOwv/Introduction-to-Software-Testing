# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `a72a5ced53067d3516ffbebf00a633743bbfeb5c`
- B: `e55aaa5706f031df2e8d68bdf088604c79944246`
- test: `src/test/java/org/apache/commons/lang3/text/StrSubstitutorTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/StrSubstitutor.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `31374`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7494, 'completion_tokens': 241, 'total_tokens': 7735}`

---

- 新增 `testSubstitutePreserveEscape`：覆盖新增的 `preserveEscapes` 开关、默认值以及转义符保留/移除两种替换行为；无需调整 import。

```java
@Test
public void testSubstitutePreserveEscape() {
    final String org = "${not-escaped} $${escaped}";
    final Map<String, String> map = new HashMap<String, String>();
    map.put("not-escaped", "value");

    final StrSubstitutor sub = new StrSubstitutor(map, "${", "}", '$');
    assertFalse(sub.isPreserveEscapes());
    assertEquals("value ${escaped}", sub.replace(org));

    sub.setPreserveEscapes(true);
    assertTrue(sub.isPreserveEscapes());
    assertEquals("value $${escaped}", sub.replace(org));
}
```