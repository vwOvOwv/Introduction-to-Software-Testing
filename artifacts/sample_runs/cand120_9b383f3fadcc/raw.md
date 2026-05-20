# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `39f4ea2311636e2aac7bce7eddff8575270d827f`
- B: `9b383f3fadccab020874aa5c69704790e03c4f4f`
- test: `src/test/java/org/apache/commons/lang3/SystemPropertiesTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/SystemProperties.java']`
- old_test_mode: `methods`
- user_chars: `5549`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1797, 'completion_tokens': 610, 'total_tokens': 2407, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 1541}`

---

- 新增 `testIsPropertySet` 和 `testIsPropertySetEdges` 两个测试方法，对应生产代码新增的 `isPropertySet` 方法。
- 修改 `testGetPropertyStringString` 方法，将 `(String) null` 替换为 `StringUtils.NULL`，对应测试 diff 中的断言调整。
- 新增 `import static org.junit.jupiter.api.Assertions.assertTrue`、`import org.junit.jupiter.params.ParameterizedTest` 和 `import org.junit.jupiter.params.provider.ValueSource`，对应测试 diff 中的 import 变更。
- 将 `KEY_SPACE_1` 和 `KEY_TAB_1` 的访问修饰符从 `private` 改为 `static`（实际已为 `static`，但测试 diff 中改为 `static`，此处保持原样，因为旧测试中已是 `static`，无需修改）。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.util.function.Supplier;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.ThrowingSupplier;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junitpioneer.jupiter.SetSystemProperty;
import org.junitpioneer.jupiter.SetSystemProperty.SetSystemProperties;
// IMPORTS_END

    @Test
    void testGetPropertyStringString() {
        assertNull(SystemProperties.getProperty(null, StringUtils.NULL));
        assertNull(SystemProperties.getProperty(StringUtils.EMPTY, StringUtils.NULL));
        assertEquals("value1", SystemProperties.getProperty(KEY_SPACE_1, StringUtils.NULL));
        assertEquals("value2", SystemProperties.getProperty("\t", StringUtils.NULL));
        assertEquals("x", SystemProperties.getProperty(null, "x"));
        assertEquals("x", SystemProperties.getProperty(StringUtils.EMPTY, "x"));
        assertEquals("value1", SystemProperties.getProperty(KEY_SPACE_1, "v"));
        assertEquals("value2", SystemProperties.getProperty("\t", "v"));
    }

    @ParameterizedTest
    @ValueSource(strings = { KEY_SPACE_1, KEY_TAB_1 })
    void testIsPropertySet(final String property) {
        assertTrue(SystemProperties.isPropertySet(property));
    }

    @Test
    void testIsPropertySetEdges() {
        assertFalse(SystemProperties.isPropertySet(StringUtils.NULL));
        assertFalse(SystemProperties.isPropertySet(StringUtils.EMPTY));
    }
```