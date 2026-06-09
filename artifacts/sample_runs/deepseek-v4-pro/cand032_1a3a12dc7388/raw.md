# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `13b9bd612a29ea756f0c7f3cc0b4f900be50e54f`
- B: `1a3a12dc7388a177c4ae64f5e3c96a7d462c003d`
- test: `src/test/java/org/apache/commons/lang3/function/FunctionsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/function/Functions.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `12241`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3455, 'completion_tokens': 1956, 'total_tokens': 5411, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1293}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 3071}`

---

- 新增 `@Test` 方法 `testApplyNotNull`：测试单参数的 `applyNotNull` 方法。
- 新增 `@Test` 方法 `testApplyNotNull2`：测试双参数的 `applyNotNull` 方法。
- 新增 `@Test` 方法 `testApplyNotNull3`：测试三参数的 `applyNotNull` 方法。
- 调整 `import`：新增静态导入 `org.junit.jupiter.api.Assertions.assertThrows`，新增类导入 `org.apache.commons.lang3.StringUtils`。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Function;

import org.apache.commons.lang3.StringUtils;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    void testApplyNotNull() {
        assertEquals("A", Functions.applyNotNull("a", String::toUpperCase));
        assertNull(Functions.applyNotNull((String) null, String::toUpperCase));
        assertNull(Functions.applyNotNull("a", s -> null));
        assertThrows(NullPointerException.class, () -> Functions.applyNotNull("a", null));
    }

    @Test
    void testApplyNotNull2() {
        assertEquals("A", Functions.applyNotNull(" a ", String::toUpperCase, String::trim));
        assertNull(Functions.applyNotNull((String) null, String::toUpperCase, String::trim));
        assertNull(Functions.applyNotNull(" a ", s -> null, String::trim));
        assertNull(Functions.applyNotNull(" a ", String::toUpperCase, s -> null));
        assertThrows(NullPointerException.class, () -> Functions.applyNotNull(" a ", null, String::trim));
        assertThrows(NullPointerException.class, () -> Functions.applyNotNull(" a ", String::toUpperCase, null));
    }

    @Test
    void testApplyNotNull3() {
        assertEquals("CBA", Functions.applyNotNull(" abc ", String::toUpperCase, String::trim, StringUtils::reverse));
        assertNull(Functions.applyNotNull((String) null, String::toUpperCase, String::trim, StringUtils::reverse));
        assertNull(Functions.applyNotNull(" abc ", s -> null, String::trim, StringUtils::reverse));
        assertNull(Functions.applyNotNull(" abc ", String::toUpperCase, s -> null, StringUtils::reverse));
        assertNull(Functions.applyNotNull(" abc ", String::toUpperCase, String::trim, s -> null));
        assertThrows(NullPointerException.class, () -> Functions.applyNotNull(" abc ", null, String::trim, StringUtils::reverse));
        assertThrows(NullPointerException.class, () -> Functions.applyNotNull(" abc ", String::toUpperCase, null, StringUtils::reverse));
        assertThrows(NullPointerException.class, () -> Functions.applyNotNull(" abc ", String::toUpperCase, String::trim, null));
    }
```