# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `7d419b9a6bcaa628b88389b67f9c138187fff3cb`
- B: `94f612b31fd934c17850b9a1c8f1eded2cbdc842`
- test: `src/test/java/org/apache/commons/lang3/math/FractionTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/math/Fraction.java']`
- old_test_mode: `methods`
- user_chars: `5944`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2172, 'completion_tokens': 601, 'total_tokens': 2773, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 1916}`

---

- 修改 `testHashCode` 方法：移除 LANG-1764 的断言（这些断言已移至新的参数化测试），保留原有基本 hashCode 测试逻辑。
- 新增 `testHashCodeNotEquals` 方法：使用 `@ParameterizedTest` 和 `@CsvSource` 测试 LANG-1764 的 hashCode 不相等场景。
- 新增 import：`org.junit.jupiter.params.ParameterizedTest` 和 `org.junit.jupiter.params.provider.CsvSource`。

```java
// IMPORTS_START
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
// IMPORTS_END

    @Test
    public void testHashCode() {
        final Fraction f1 = Fraction.getFraction(3, 5);
        Fraction f2 = Fraction.getFraction(3, 5);
        assertEquals(f1.hashCode(), f2.hashCode());
        f2 = Fraction.getFraction(2, 5);
        assertTrue(f1.hashCode() != f2.hashCode());
        f2 = Fraction.getFraction(6, 10);
        assertTrue(f1.hashCode() != f2.hashCode());
    }

    /**
     * Tests https://issues.apache.org/jira/browse/LANG-1764
     */
    @ParameterizedTest
    // @formatter:off
    @CsvSource({
        "0, 37, -464320789, 46",
        "0, 37, -464320788, 9",
        "0, 37, 1857283155, 38",
        "0, 25185704, 1161454280, 1050304",
        "0, 38817068, 1509581512, 18875972",
        "0, 38817068, -2146369536, 2145078572",
        "1400217380, 128, 2092630052, 150535040",
        "1400217380, 128, -580400986, 268435638",
        "1400217380, 2147483592, -2147483648, 268435452",
        "1756395909, 4194598, 1174949894, 42860673"
    })
    // @formatter:on
    public void testHashCodeNotEquals(int f1n, int f1d, int f2n, int f2d) {
        assertNotEquals(Fraction.getFraction(f1n, f1d), Fraction.getFraction(f2n, f2d));
        assertNotEquals(Fraction.getFraction(f1n, f1d).hashCode(), Fraction.getFraction(f2n, f2d).hashCode());
    }
```