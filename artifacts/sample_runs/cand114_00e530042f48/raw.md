# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `892c9703496079e0b65eccea0252cf52a44c4512`
- B: `00e530042f481d1000be27584cf05be939a42bb0`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `methods`
- user_chars: `6266`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1967, 'completion_tokens': 816, 'total_tokens': 2783, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 1711}`

---

- 将 `testExceptions` 方法重命名为 `testExceptionsRandom`，并移除 `randomAlphabetic`、`randomAscii`、`randomGraph`、`randomNumeric`、`randomPrint` 的断言，同时将 `DUMMY` 局部变量替换为内联 `new char[] { 'a' }`，并新增对 `random(1, Integer.MIN_VALUE, -10, false, false, null)` 的断言。
- 新增 `testExceptionsRandomAlphabetic` 方法，包含 `randomAlphabetic(-1)` 的断言。
- 新增 `testExceptionsRandomAscii` 方法，包含 `randomAscii(-1)` 的断言。
- 新增 `testExceptionsRandomGraph` 方法，包含 `randomGraph(-1)` 的断言。
- 新增 `testExceptionsRandomNumeric` 方法，包含 `randomNumeric(-1)` 的断言。
- 新增 `testExceptionsRandomPrint` 方法，包含 `randomPrint(-1)` 的断言。
- 无需调整 import。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertThrows;
import java.util.Random;
import org.apache.commons.lang3.RandomStringUtils;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    public void testExceptionsRandom() {
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1));
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, true, true));
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, new char[] { 'a' }));
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(1, new char[0]));
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, ""));
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, (String) null));
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, 'a', 'z', false, false));
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, 'a', 'z', false, false, new char[] { 'a' }));
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, 'a', 'z', false, false, new char[] { 'a' }, new Random()));
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(8, 32, 48, false, true));
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(8, 32, 65, true, false));
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(1, Integer.MIN_VALUE, -10, false, false, null));
    }

    @Test
    public void testExceptionsRandomAlphabetic() {
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.randomAlphabetic(-1));
    }

    @Test
    public void testExceptionsRandomAscii() {
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.randomAscii(-1));
    }

    @Test
    public void testExceptionsRandomGraph() {
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.randomGraph(-1));
    }

    @Test
    public void testExceptionsRandomNumeric() {
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.randomNumeric(-1));
    }

    @Test
    public void testExceptionsRandomPrint() {
        assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.randomPrint(-1));
    }
```