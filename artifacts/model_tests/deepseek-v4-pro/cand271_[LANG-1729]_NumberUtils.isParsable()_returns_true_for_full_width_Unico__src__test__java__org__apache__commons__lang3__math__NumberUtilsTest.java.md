# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `1196f03e4f0b5de78416771259cb8ab60fb20e0f`
- B: `3bd1625859000571b99b4193df1360ab18a33910`
- test: `src/test/java/org/apache/commons/lang3/math/NumberUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/math/NumberUtils.java']`
- old_test_mode: `methods`
- user_chars: `7445`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2391, 'completion_tokens': 2131, 'total_tokens': 4522, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1768}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2007}`

---

- 修改 `testIsParsableFullWidthUnicodeJDK8326627`：新增三个断言，验证 `isParsable` 对全角数字字符串的正确处理（全角无小数点应可解析，含小数点则不可解析）。
- 修改 `testLang1729IsParsableDouble`：移除被注释掉的过时期望断言（该断言原本依赖 Java 23 修复，现已由新的测试覆盖）。
- 修改 `testLang1729IsParsableFloat`：同样移除被注释掉的过时断言。
- 无需新增 import，所有引用类均已在测试文件中存在。

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