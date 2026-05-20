# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `1196f03e4f0b5de78416771259cb8ab60fb20e0f`
- B: `3bd1625859000571b99b4193df1360ab18a33910`
- test: `src/test/java/org/apache/commons/lang3/math/NumberUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/math/NumberUtils.java']`
- old_test_mode: `methods`
- user_chars: `7718`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2451, 'completion_tokens': 494, 'total_tokens': 2945, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 2195}`

---

- 新增 `testIsParsableFullWidthUnicodeJDK8326627` 方法，添加对全角数字的 `isParsable` 断言，对应生产代码中 `isParsableDecimal` 新增的 ASCII 数字检查逻辑。
- 修改 `testLang1729IsParsableDouble` 方法，取消注释并启用 `assertTrue(isParsableDouble("１２３"))`，删除 `assertFalse(isParsableDouble("１ ２ ３"))`，对应生产代码中 `isParsableDecimal` 对全角数字的支持。
- 修改 `testLang1729IsParsableFloat` 方法，取消注释并启用 `assertTrue(isParsableFloat("１２３"))`，删除 `assertFalse(isParsableFloat("１ ２ ３"))`，对应生产代码中 `isParsableDecimal` 对全角数字的支持。
- 无需调整 import，因为 `assertTrue` 和 `assertFalse` 已静态导入。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
// IMPORTS_END

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
        assertTrue(isParsableDouble("１２３"));
    }

    @Test
    void testLang1729IsParsableFloat() {
        assertTrue(isParsableFloat("1"));
        assertFalse(isParsableFloat("1 2 3"));
        assertTrue(isParsableFloat("１２３"));
    }
```