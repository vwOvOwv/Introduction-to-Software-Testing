# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `1196f03e4f0b5de78416771259cb8ab60fb20e0f`
- B: `3bd1625859000571b99b4193df1360ab18a33910`
- test: `src/test/java/org/apache/commons/lang3/math/NumberUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/math/NumberUtils.java']`
- old_test_mode: `methods`
- user_chars: `7445`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2354, 'completion_tokens': 531, 'total_tokens': 2885}`

---

- 修改 `testIsParsableFullWidthUnicodeJDK8326627`：生产代码现在允许纯全角 Unicode 数字被 `isParsable` 识别，但包含小数点时要求 ASCII 数字，因此新增对应断言。
- 修改 `testLang1729IsParsableDouble`：删除与 Java 23 相关的过期 TODO 注释，保持现有断言。
- 修改 `testLang1729IsParsableFloat`：删除与 Java 23 相关的过期 TODO 注释，保持现有断言。
- 不需要调整 import。

```java
@Test
void testIsParsableFullWidthUnicodeJDK8326627() {
    final String fullWidth123 = "\uFF10\uFF11\uFF12";
    assertThrows(NumberFormatException.class, () -> Double.parseDouble(fullWidth123));
    assertThrows(NumberFormatException.class, () -> Float.parseFloat(fullWidth123));
    assertTrue(NumberUtils.isParsable(fullWidth123));
    assertFalse(NumberUtils.isParsable(fullWidth123 + ".0"));
    assertFalse(NumberUtils.isParsable("0." + fullWidth123));
}

@Test
void testLang1729IsParsableDouble() {
    assertTrue(isParsableDouble("1"));
    assertFalse(isParsableDouble("1 2 3"));
    assertFalse(isParsableDouble("１ ２ ３"));
}

@Test
void testLang1729IsParsableFloat() {
    assertTrue(isParsableFloat("1"));
    assertFalse(isParsableFloat("1 2 3"));
    assertFalse(isParsableFloat("１ ２ ３"));
}
```