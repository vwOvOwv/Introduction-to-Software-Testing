# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `53def501409cd1f9e20ac43edba6f2949bb366c8`
- B: `7c19a1ff4c217f03c0be62baf1169d689f566825`
- test: `src/test/java/org/apache/commons/lang3/CharEncodingTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/CharEncoding.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `7013`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2147, 'completion_tokens': 1924, 'total_tokens': 4071, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1471}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1763}`

---

- 无需新增、修改或删除任何 `@Test` 方法；只在测试类声明上添加 `@SuppressWarnings("deprecation")` 注解以消除对已弃用 `CharEncoding` 类的编译警告。
- 无需调整 `import`；`@SuppressWarnings` 位于 `java.lang` 包，自动导入。

```java
package org.apache.commons.lang3;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

/**
 * Tests CharEncoding.
 * 
 * @see CharEncoding
 */
@SuppressWarnings("deprecation")
public class CharEncodingTest  {

    private void assertSupportedEncoding(final String name) {
        assertTrue("Encoding should be supported: " + name, CharEncoding.isSupported(name));
    }

    /**
     * The class can be instantiated.
     */
    @Test
    public void testConstructor() {
        new CharEncoding();
    }

    @Test
    public void testMustBeSupportedJava1_3_1_and_above() {
        this.assertSupportedEncoding(CharEncoding.ISO_8859_1);
        this.assertSupportedEncoding(CharEncoding.US_ASCII);
        this.assertSupportedEncoding(CharEncoding.UTF_16);
        this.assertSupportedEncoding(CharEncoding.UTF_16BE);
        this.assertSupportedEncoding(CharEncoding.UTF_16LE);
        this.assertSupportedEncoding(CharEncoding.UTF_8);
    }

    @Test
    public void testSupported() {
        assertTrue(CharEncoding.isSupported("UTF8"));
        assertTrue(CharEncoding.isSupported("UTF-8"));
        assertTrue(CharEncoding.isSupported("ASCII"));
    }

    @Test
    public void testNotSupported() {
        assertFalse(CharEncoding.isSupported(null));
        assertFalse(CharEncoding.isSupported(""));
        assertFalse(CharEncoding.isSupported(" "));
        assertFalse(CharEncoding.isSupported("\t\r\n"));
        assertFalse(CharEncoding.isSupported("DOESNOTEXIST"));
        assertFalse(CharEncoding.isSupported("this is not a valid encoding name"));
    }
}
```