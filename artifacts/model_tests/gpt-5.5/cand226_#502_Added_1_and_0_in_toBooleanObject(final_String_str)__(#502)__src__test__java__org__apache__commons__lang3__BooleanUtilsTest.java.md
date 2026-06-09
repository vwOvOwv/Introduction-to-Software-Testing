# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ba607f525b842661d40195d0d4778528e2384e70`
- B: `fde46a232d82f2b746f62bc7546e2e3371f20dca`
- test: `src/test/java/org/apache/commons/lang3/BooleanUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/BooleanUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `43885`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9121, 'completion_tokens': 1089, 'total_tokens': 10210}`

---

- 修改 `test_toBooleanObject_String`：生产代码新增 `"1"`/`"0"` 单字符字符串到 `BooleanUtils.toBooleanObject(String)` 的 true/false 识别范围，因此补充对应断言。
- 修改 `test_toBoolean_String`：`BooleanUtils.toBoolean(String)` 依赖 `toBooleanObject(String)` 行为，新增 `"1"` 为 true、`"0"` 为 false 的断言。
- import 无需调整。

```java
@Test
public void test_toBooleanObject_String() {
    assertNull(BooleanUtils.toBooleanObject((String) null));
    assertNull(BooleanUtils.toBooleanObject(""));
    assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("false"));
    assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("no"));
    assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("off"));
    assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("FALSE"));
    assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("NO"));
    assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("OFF"));
    assertNull(BooleanUtils.toBooleanObject("oof"));
    assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("true"));
    assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("yes"));
    assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("on"));
    assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("TRUE"));
    assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("ON"));
    assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("YES"));
    assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("TruE"));
    assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("TruE"));

    assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("y")); // yes
    assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("Y"));
    assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("t")); // true
    assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("T"));
    assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("1"));
    assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("f")); // false
    assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("F"));
    assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("n")); // No
    assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("N"));
    assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("0"));
    assertNull(BooleanUtils.toBooleanObject("z"));

    assertNull(BooleanUtils.toBooleanObject("ab"));
    assertNull(BooleanUtils.toBooleanObject("yoo"));
    assertNull(BooleanUtils.toBooleanObject("true "));
    assertNull(BooleanUtils.toBooleanObject("ono"));
}

@Test
public void test_toBoolean_String() {
    assertFalse(BooleanUtils.toBoolean((String) null));
    assertFalse(BooleanUtils.toBoolean(""));
    assertFalse(BooleanUtils.toBoolean("off"));
    assertFalse(BooleanUtils.toBoolean("oof"));
    assertFalse(BooleanUtils.toBoolean("yep"));
    assertFalse(BooleanUtils.toBoolean("trux"));
    assertFalse(BooleanUtils.toBoolean("false"));
    assertFalse(BooleanUtils.toBoolean("a"));
    assertTrue(BooleanUtils.toBoolean("true")); // interned handled differently
    assertTrue(BooleanUtils.toBoolean(new StringBuilder("tr").append("ue").toString()));
    assertTrue(BooleanUtils.toBoolean("truE"));
    assertTrue(BooleanUtils.toBoolean("trUe"));
    assertTrue(BooleanUtils.toBoolean("trUE"));
    assertTrue(BooleanUtils.toBoolean("tRue"));
    assertTrue(BooleanUtils.toBoolean("tRuE"));
    assertTrue(BooleanUtils.toBoolean("tRUe"));
    assertTrue(BooleanUtils.toBoolean("tRUE"));
    assertTrue(BooleanUtils.toBoolean("TRUE"));
    assertTrue(BooleanUtils.toBoolean("TRUe"));
    assertTrue(BooleanUtils.toBoolean("TRuE"));
    assertTrue(BooleanUtils.toBoolean("TRue"));
    assertTrue(BooleanUtils.toBoolean("TrUE"));
    assertTrue(BooleanUtils.toBoolean("TrUe"));
    assertTrue(BooleanUtils.toBoolean("TruE"));
    assertTrue(BooleanUtils.toBoolean("True"));
    assertTrue(BooleanUtils.toBoolean("on"));
    assertTrue(BooleanUtils.toBoolean("oN"));
    assertTrue(BooleanUtils.toBoolean("On"));
    assertTrue(BooleanUtils.toBoolean("ON"));
    assertTrue(BooleanUtils.toBoolean("yes"));
    assertTrue(BooleanUtils.toBoolean("yeS"));
    assertTrue(BooleanUtils.toBoolean("yEs"));
    assertTrue(BooleanUtils.toBoolean("yES"));
    assertTrue(BooleanUtils.toBoolean("Yes"));
    assertTrue(BooleanUtils.toBoolean("YeS"));
    assertTrue(BooleanUtils.toBoolean("YEs"));
    assertTrue(BooleanUtils.toBoolean("YES"));
    assertTrue(BooleanUtils.toBoolean("1"));
    assertFalse(BooleanUtils.toBoolean("yes?"));
    assertFalse(BooleanUtils.toBoolean("0"));
    assertFalse(BooleanUtils.toBoolean("tru"));

    assertFalse(BooleanUtils.toBoolean("no"));
    assertFalse(BooleanUtils.toBoolean("off"));
    assertFalse(BooleanUtils.toBoolean("yoo"));
}
```