# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `39f4ea2311636e2aac7bce7eddff8575270d827f`
- B: `9b383f3fadccab020874aa5c69704790e03c4f4f`
- test: `src/test/java/org/apache/commons/lang3/SystemPropertiesTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/SystemProperties.java']`
- old_test_mode: `methods`
- user_chars: `5271`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1701, 'completion_tokens': 973, 'total_tokens': 2674}`

---

- 修改 `testGetPropertyStringString`：将显式 `(String) null` 替换为 `StringUtils.NULL`，与测试 diff 中对空默认值表达方式的更新一致。
- 新增 `testIsPropertySet`：覆盖新增生产方法 `SystemProperties.isPropertySet(String)` 在已设置属性上的 `true` 行为。
- 新增 `testIsPropertySetEdges`：覆盖新增生产方法在 `null` 与空字符串属性名上的 `false` 行为。
- 需要调整 import：新增 `assertTrue`、`ParameterizedTest`、`ValueSource` 的导入。

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