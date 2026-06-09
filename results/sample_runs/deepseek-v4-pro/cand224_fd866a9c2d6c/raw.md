# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `d1bf9bfe747d5ad8a14cc1f65e6876a30a1bc866`
- B: `fd866a9c2d6c69f9f6462a5e498b58293597d611`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `41719`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 11026, 'completion_tokens': 2437, 'total_tokens': 13463, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1513}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 10642}`

---

- 新增 `testNonASCIILetters` 参数化测试，对应生产代码对非 ASCII 字母范围的优化与检查。
- 新增 `testNonASCIINumbers` 参数化测试，对应生产代码对非 ASCII 数字范围的优化与检查。
- 原有其它 `@Test` 与 `@ParameterizedTest` 方法无需修改，均可编译并通过断言；import 亦无需调整。

```java
/**
 * Test {@code RandomStringUtils.random} works appropriately when letters=true
 * and the range does not only include ASCII letters.
 * Fails with probability less than 2^-40 (in practice this never happens).
 */
@ParameterizedTest
@MethodSource("randomProvider")
void testNonASCIILetters(final RandomStringUtils rsu) {
    // Check that the following create a string with 10 characters 0x4e00 (a non-ASCII letter)
    String r1 = rsu.next(10, 0x4e00, 0x4e01, true, false);
    assertEquals(10, r1.length(), "wrong length");
    for (int i = 0; i < r1.length(); i++) {
        assertEquals(0x4e00, r1.charAt(i), "characters not all equal to 0x4e00");
    }

    // Same with both letters=true and numbers=true
    r1 = rsu.next(10, 0x4e00, 0x4e01, true, true);
    assertEquals(10, r1.length(), "wrong length");
    for (int i = 0; i < r1.length(); i++) {
        assertEquals(0x4e00, r1.charAt(i), "characters not all equal to 0x4e00");
    }

    // Check that at least one letter is not ASCII
    boolean found = false;
    r1 = rsu.next(40, 'F', 0x3000, true, false);
    assertEquals(40, r1.length(), "wrong length");
    for (int i = 0; i < r1.length(); i++) {
        assertTrue(Character.isLetter(r1.charAt(i)), "characters not all letters");
        if (r1.charAt(i) > 0x7f) {
            found = true;
        }
    }
    assertTrue(found, "no non-ASCII letter generated");
}

/**
 * Test {@code RandomStringUtils.random} works appropriately when numbers=true
 * and the range does not only include ASCII numbers/digits.
 * Fails with probability less than 2^-40 (in practice this never happens).
 */
@ParameterizedTest
@MethodSource("randomProvider")
void testNonASCIINumbers(final RandomStringUtils rsu) {
    // Check that the following create a string with 10 characters 0x0660 (a non-ASCII digit)
    String r1 = rsu.next(10, 0x0660, 0x0661, false, true);
    assertEquals(10, r1.length(), "wrong length");
    for (int i = 0; i < r1.length(); i++) {
        assertEquals(0x0660, r1.charAt(i), "characters not all equal to 0x0660");
    }

    // Same with both letters=true and numbers=true
    r1 = rsu.next(10, 0x0660, 0x0661, true, true);
    assertEquals(10, r1.length(), "wrong length");
    for (int i = 0; i < r1.length(); i++) {
        assertEquals(0x0660, r1.charAt(i), "characters not all equal to 0x0660");
    }

    // Check that at least one letter is not ASCII
    boolean found = false;
    r1 = rsu.next(40, 'F', 0x3000, false, true);
    assertEquals(40, r1.length(), "wrong length");
    for (int i = 0; i < r1.length(); i++) {
        assertTrue(Character.isDigit(r1.charAt(i)), "characters not all numbers");
        if (r1.charAt(i) > 0x7f) {
            found = true;
        }
    }
    assertTrue(found, "no non-ASCII number generated");
}
```