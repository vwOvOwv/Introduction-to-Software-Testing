# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `53def501409cd1f9e20ac43edba6f2949bb366c8`
- B: `7c19a1ff4c217f03c0be62baf1169d689f566825`
- test: `src/test/java/org/apache/commons/lang3/CharEncodingTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/CharEncoding.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `7013`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2097, 'completion_tokens': 811, 'total_tokens': 2908}`

---

- 不新增、修改或删除任何 `@Test` 方法；生产代码将 `CharEncoding` 标记为 `@Deprecated`，因此仅需在测试类级别添加 `@SuppressWarnings("deprecation")`。
- import 不需要调整；现有 JUnit 4 `Assert` 与 `Test` import 仍可用。

```java
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