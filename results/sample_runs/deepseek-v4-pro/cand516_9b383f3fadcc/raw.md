# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `39f4ea2311636e2aac7bce7eddff8575270d827f`
- B: `9b383f3fadccab020874aa5c69704790e03c4f4f`
- test: `src/test/java/org/apache/commons/lang3/SystemPropertiesTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/SystemProperties.java']`
- old_test_mode: `methods`
- user_chars: `5271`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1737, 'completion_tokens': 2195, 'total_tokens': 3932, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1719}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1353}`

---

- 新增 `@ParameterizedTest` 方法 `testIsPropertySet`，覆盖生产新增的 `isPropertySet` 方法，用于验证已设置的属性返回 `true`。
- 新增 `@Test` 方法 `testIsPropertySetEdges`，覆盖 `isPropertySet` 对 `null` 和空字符串的边界情况，返回 `false`。
- 修改 `@Test` 方法 `testGetPropertyStringSimple`（原 `testGetPropertyStringString`）中的 `null` 文本参数为 `StringUtils.NULL`，以匹配生产代码风格或编译要求。
- 需要调整 import：添加 `import static org.junit.jupiter.api.Assertions.assertTrue;`、`import org.junit.jupiter.params.ParameterizedTest;`、`import org.junit.jupiter.params.provider.ValueSource;`。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
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