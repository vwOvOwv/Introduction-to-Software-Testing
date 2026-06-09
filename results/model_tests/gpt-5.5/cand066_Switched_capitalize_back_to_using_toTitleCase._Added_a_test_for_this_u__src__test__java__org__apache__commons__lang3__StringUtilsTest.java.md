# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cc1aed9bdf196403c673a886bbf723101171a9bf`
- B: `421db380d060e9f037a8ecbc446c414efaa6923f`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `127505`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 31178, 'completion_tokens': 318, 'total_tokens': 31496}`

---

- 修改 `testCapitalize`：生产代码将首字符转换从 `Character.toUpperCase` 改为 `Character.toTitleCase`，因此新增断言覆盖 `\u01C9` 被 title case 为 `\u01C8`。
- import 无需调整：新增断言仍使用已有 `assertEquals` 与 `StringUtils`。

```java
@Test
public void testCapitalize() {
    assertNull(StringUtils.capitalize(null));

    assertEquals("capitalize(empty-string) failed",
            "", StringUtils.capitalize(""));
    assertEquals("capitalize(single-char-string) failed",
            "X", StringUtils.capitalize("x"));
    assertEquals("capitalize(String) failed",
            FOO_CAP, StringUtils.capitalize(FOO_CAP));
    assertEquals("capitalize(string) failed",
            FOO_CAP, StringUtils.capitalize(FOO_UNCAP));

    assertEquals("capitalize(String) is not using TitleCase",
            "\u01C8", StringUtils.capitalize("\u01C9"));

    // Javadoc examples
    assertNull(StringUtils.capitalize(null));
    assertEquals("", StringUtils.capitalize(""));
    assertEquals("Cat", StringUtils.capitalize("cat"));
    assertEquals("CAt", StringUtils.capitalize("cAt"));
    assertEquals("'cat'", StringUtils.capitalize("'cat'"));
}
```