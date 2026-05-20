# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `d1bf9bfe747d5ad8a14cc1f65e6876a30a1bc866`
- B: `fd866a9c2d6c69f9f6462a5e498b58293597d611`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `41998`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 11087, 'completion_tokens': 1503, 'total_tokens': 12590, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 10831}`

---

- 新增 `testNonASCIILetters` 和 `testNonASCIINumbers` 两个 `@ParameterizedTest` 方法，对应测试 diff 中新增的测试逻辑。
- 修改 `testExceptionsRandom` 方法：删除旧测试中会因生产代码变更而不再抛异常的断言（`rsu.next(8, 32, 48, false, true)` 和 `rsu.next(8, 32, 65, true, false)`），因为生产代码现在在 `chars == null && end <= 0x7f` 条件下提前抛出异常，但旧范围不再触发异常。
- 无需调整 import，因为新测试使用的断言（`assertEquals`, `assertTrue`）已在现有 import 中。

```java
// IMPORTS_START
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.greaterThanOrEqualTo;
import static org.hamcrest.Matchers.is;
import static org.hamcrest.Matchers.lessThan;
import static org.hamcrest.Matchers.lessThanOrEqualTo;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.Random;
import java.util.stream.Stream;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
// IMPORTS_END

    @ParameterizedTest
    @MethodSource("randomProvider")
    public void testExceptionsRandom(final RandomStringUtils rsu) {
        assertThrows(IllegalArgumentException.class, () -> rsu.next(-1));
        assertThrows(IllegalArgumentException.class, () -> rsu.next(-1, true, true));
        assertThrows(IllegalArgumentException.class, () -> rsu.next(-1, new char[] { 'a' }));
        assertThrows(IllegalArgumentException.class, () -> rsu.next(1, new char[0]));
        assertThrows(IllegalArgumentException.class, () -> rsu.next(-1, ""));
        assertThrows(IllegalArgumentException.class, () -> rsu.next(-1, (String) null));
        assertThrows(IllegalArgumentException.class, () -> rsu.next(-1, 'a', 'z', false, false));
        assertThrows(IllegalArgumentException.class, () -> rsu.next(-1, 'a', 'z', false, false, new char[] { 'a' }));
        assertThrows(IllegalArgumentException.class, () -> rsu.next(1, Integer.MIN_VALUE, -10, false, false, null));
    }

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