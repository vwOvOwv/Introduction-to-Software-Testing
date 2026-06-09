# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `78154f0456f8bbf7139bc1524481eef8f6e228f7`
- B: `f382d61a03778ccf838c6c051bd8692e4834dec2`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `34911`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9279, 'completion_tokens': 2047, 'total_tokens': 11326, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1720}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 8895}`

---

- 新增 `void testRandomWithChars()` 测试方法，以验证使用指定字符数组随机生成字符串的行为（对应生产代码新增的 `ALPHANUMERICAL_CHARS` 优化路径）。
- 在文件头部新增 `import static org.junit.jupiter.api.Assertions.assertNotEquals;`，以便在新测试中调用 `assertNotEquals`。

```java
import static org.junit.jupiter.api.Assertions.assertNotEquals;

/**
 * Test {@code RandomStringUtils.random} works appropriately when chars specified.
 */
@Test
void testRandomWithChars() {
    final char[] digitChars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};

    String r1, r2, r3;

    r1 = RandomStringUtils.random(50, 0, 0, true, true, digitChars);
    assertEquals(50, r1.length(), "randomNumeric(50)");
    for (int i = 0; i < r1.length(); i++) {
        assertTrue(
                Character.isDigit(r1.charAt(i)) && !Character.isLetter(r1.charAt(i)),
                "r1 contains numeric");
    }
    r2 = RandomStringUtils.randomNumeric(50);
    assertNotEquals(r1, r2);

    r3 = RandomStringUtils.random(50, 0, 0, true, true, digitChars);
    assertNotEquals(r1, r3);
    assertNotEquals(r2, r3);
}
```