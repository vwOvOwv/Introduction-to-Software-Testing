# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e63927afd575ba22f41a1d5b23b2d85745e82d24`
- B: `313d877d57abefdbb1ad0c42781bf719b83d5a35`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `47859`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 12289, 'completion_tokens': 4959, 'total_tokens': 17248, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 4242}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 11905}`

---

- 将新增 `testCustomLetterCharsArrayDoesNotThrowIAE` 测试方法，修正 chars 数组提供且仅请求字母时不当抛出 IllegalArgumentException 的 bug。
- 将新增 `testOnlyRejectedCodePoints` 测试方法，验证当指定范围仅包含 UNASSIGNED/PRIVATE_USE/SURROGATE 等代码点时不再死循环，而是快速抛出 IllegalArgumentException。
- import 调整：新增静态导入 `assertDoesNotThrow` 和 `assertTimeout`，新增 `java.time.Duration` 导入，以支撑新增测试的编译。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertTimeout;
import java.time.Duration;
// IMPORTS_END

/**
 * A custom chars array throws IllegalArgumentException because validation loops treat the loop index as a char code point instead of an index into the
 * chars array.
 * <p>
 * Pre-patch: random(5, 0, 0, true, false, new char[]{'a','b','c'}, rng) enters the "letters && !digits" loop, iterates i from 0 to chars.length, but checks
 * Character.isLetter(i) where i=0,1,2 are control characters, so it throws IAE "No letters exist between start 0 and end 3".
 * </p>
 *
 * <p>
 * Post-patch: validation skips index-based char check when chars array is provided, or correctly checks chars[i] instead of i.
 * </p>
 */
@Test
public void testCustomLetterCharsArrayDoesNotThrowIAE() {
    final char[] letters = { 'a', 'b', 'c' };
    assertDoesNotThrow(() -> {
        final String result = RandomStringUtils.random(5, 0, 0, true, false, letters, new Random(42));
        assertEquals(5, result.length());
        for (final char c : result.toCharArray()) {
            assertTrue(c == 'a' || c == 'b' || c == 'c', () -> "Expected char from {a,b,c} but got: " + c);
        }
    }, "RandomStringUtils.random() threw IAE for valid letter chars array - pre-patch behavior");
}

/**
 * random() hangs when the specified [start, end) range contains ONLY rejected code points (UNASSIGNED, PRIVATE_USE, SURROGATE). The loop increments count
 * and retries indefinitely.
 * <p>
 * The private-use area U+E000..U+F8FF (0xE000..0xF900) contains only PRIVATE_USE code points, so random(1, 0xE000, 0xF900, false, false, null, rng) hangs
 * forever pre-patch.
 * </p>
 * <ul>
 * <li>Pre-patch: hangs indefinitely.</li>
 * <li>Post-patch: throws IllegalArgumentException quickly.</li>
 * </ul>
 */
@Test
public void testOnlyRejectedCodePoints() {
    assertTimeout(Duration.ofSeconds(2),
            () -> assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(1, 0xE000, 0xF900, false, false, null, new Random(42))));
}
```