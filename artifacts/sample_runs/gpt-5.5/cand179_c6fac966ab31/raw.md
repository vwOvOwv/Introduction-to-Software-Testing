# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `de0819cb86fcd597961b99fd8cb71b8b74fd8cec`
- B: `c6fac966ab314769d27e117bab05aee1a72df760`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `150190`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 37022, 'completion_tokens': 1960, 'total_tokens': 38982}`

---

- 新增 `testTruncate_StringInt`：生产代码新增 `StringUtils.truncate(String, int)`，测试覆盖 null、空串、正常截断、零宽度、超大宽度和负 `maxWidth` 异常。
- 新增 `testTruncate_StringIntInt`：生产代码新增 `StringUtils.truncate(String, int, int)`，测试覆盖 offset 截断、越界 offset、负 offset、负 `maxWidth`、Integer 边界值等行为。
- import 无需调整：旧测试文件已包含 `assertEquals`、`assertNull`、`assertTrue`、`fail` 和 `org.junit.Test`。

```java
    @Test
    public void testTruncate_StringInt() {
        assertNull(StringUtils.truncate(null, 12));
        try {
            StringUtils.truncate(null, -1);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate(null, -10);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate(null, Integer.MIN_VALUE);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        assertEquals("", StringUtils.truncate("", 10));
        assertEquals("", StringUtils.truncate("", 10));
        assertEquals("abc", StringUtils.truncate("abcdefghij", 3));
        assertEquals("abcdef", StringUtils.truncate("abcdefghij", 6));
        assertEquals("", StringUtils.truncate("abcdefghij", 0));
        try {
            StringUtils.truncate("abcdefghij", -1);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", -100);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", Integer.MIN_VALUE);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        assertEquals("abcdefghij", StringUtils.truncate("abcdefghijklmno", 10));
        assertEquals("abcdefghijklmno", StringUtils.truncate("abcdefghijklmno", Integer.MAX_VALUE));
        assertEquals("abcde", StringUtils.truncate("abcdefghijklmno", 5));
        assertEquals("abc", StringUtils.truncate("abcdefghijklmno", 3));
    }

    @Test
    public void testTruncate_StringIntInt() {
        assertNull(StringUtils.truncate(null, 0, 12));
        try {
            StringUtils.truncate(null, -1, 0);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate(null, -10, -4);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate(null, Integer.MIN_VALUE, Integer.MIN_VALUE);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        assertNull(StringUtils.truncate(null, 10, 12));
        assertEquals("", StringUtils.truncate("", 0, 10));
        assertEquals("", StringUtils.truncate("", 2, 10));
        assertEquals("abc", StringUtils.truncate("abcdefghij", 0, 3));
        assertEquals("fghij", StringUtils.truncate("abcdefghij", 5, 6));
        assertEquals("", StringUtils.truncate("abcdefghij", 0, 0));
        try {
            StringUtils.truncate("abcdefghij", 0, -1);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", 0, -10);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", 0, -100);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", 1, -100);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", 0, Integer.MIN_VALUE);
            fail("maxWith cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", -1, 0);
            fail("offset cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", -10, 0);
            fail("offset cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", -100, 1);
            fail("offset cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", Integer.MIN_VALUE, 0);
            fail("offset cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", -1, -1);
            fail("offset cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", -10, -10);
            fail("offset cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", -100, -100);
            fail("offset  cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        try {
            StringUtils.truncate("abcdefghij", Integer.MIN_VALUE, Integer.MIN_VALUE);
            fail("offset  cannot be negative");
        } catch (Exception e) {
            assertTrue(e instanceof IllegalArgumentException);
        }
        final String raspberry = "raspberry peach";
        assertEquals("peach", StringUtils.truncate(raspberry, 10, 15));
        assertEquals("abcdefghij", StringUtils.truncate("abcdefghijklmno", 0, 10));
        assertEquals("abcdefghijklmno", StringUtils.truncate("abcdefghijklmno", 0, Integer.MAX_VALUE));
        assertEquals("bcdefghijk", StringUtils.truncate("abcdefghijklmno", 1, 10));
        assertEquals("cdefghijkl", StringUtils.truncate("abcdefghijklmno", 2, 10));
        assertEquals("defghijklm", StringUtils.truncate("abcdefghijklmno", 3, 10));
        assertEquals("efghijklmn", StringUtils.truncate("abcdefghijklmno", 4, 10));
        assertEquals("fghijklmno", StringUtils.truncate("abcdefghijklmno", 5, 10));
        assertEquals("fghij", StringUtils.truncate("abcdefghijklmno", 5, 5));
        assertEquals("fgh", StringUtils.truncate("abcdefghijklmno", 5, 3));
        assertEquals("klm", StringUtils.truncate("abcdefghijklmno", 10, 3));
        assertEquals("klmno", StringUtils.truncate("abcdefghijklmno", 10, Integer.MAX_VALUE));
        assertEquals("n", StringUtils.truncate("abcdefghijklmno", 13, 1));
        assertEquals("no", StringUtils.truncate("abcdefghijklmno", 13, Integer.MAX_VALUE));
        assertEquals("o", StringUtils.truncate("abcdefghijklmno", 14, 1));
        assertEquals("o", StringUtils.truncate("abcdefghijklmno", 14, Integer.MAX_VALUE));
        assertEquals("", StringUtils.truncate("abcdefghijklmno", 15, 1));
        assertEquals("", StringUtils.truncate("abcdefghijklmno", 15, Integer.MAX_VALUE));
        assertEquals("", StringUtils.truncate("abcdefghijklmno", Integer.MAX_VALUE, Integer.MAX_VALUE));
    }
```