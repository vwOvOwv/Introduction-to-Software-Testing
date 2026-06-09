# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `c8e648b92cc133a604b5e1f4da1ced943788e64b`
- B: `9b3257e4d1a63e0a4d971a331eaf7b9a08d98040`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `161460`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 39490, 'completion_tokens': 239, 'total_tokens': 39729}`

---

- 新增 `testGetDigits`：生产代码新增 `StringUtils.getDigits(String)`，测试覆盖 `null`、空串、无数字、ASCII 数字混合文本、电话号码格式以及 Unicode 数字提取行为。
- import 无需调整：旧测试已包含 `assertEquals` 与 `@Test` 所需静态/普通 import。

```java
@Test
public void testGetDigits() {
    assertEquals(null, StringUtils.getDigits(null));
    assertEquals("", StringUtils.getDigits(""));
    assertEquals("", StringUtils.getDigits("abc"));
    assertEquals("1000", StringUtils.getDigits("1000$"));
    assertEquals("12345", StringUtils.getDigits("123password45"));
    assertEquals("5417543010", StringUtils.getDigits("(541) 754-3010"));
    assertEquals("\u0967\u0968\u0969", StringUtils.getDigits("\u0967\u0968\u0969"));
}
```