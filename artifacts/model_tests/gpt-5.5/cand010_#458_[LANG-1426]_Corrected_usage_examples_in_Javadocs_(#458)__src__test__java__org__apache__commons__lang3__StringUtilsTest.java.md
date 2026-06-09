# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `46b381eb4bd5b77b7322e73e7076957c2956860e`
- B: `089b43a0a6de2d6ae49840aec3805aee2c309001`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `10094`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2878, 'completion_tokens': 1297, 'total_tokens': 4175}`

---

- 修改 `@Test` 方法 `testTruncate_StringIntInt`：生产代码现在对负数 `offset` 优先抛出 `IllegalArgumentException`，同步更新相关 `assertThrows` 的失败提示文本。
- 不需要调整 import：本次只修改已有测试方法体中的断言提示字符串。

```java
    @Test
    public void testTruncate_StringIntInt() {
        assertNull(StringUtils.truncate(null, 0, 12));
        assertThrows(
                IllegalArgumentException.class, () -> StringUtils.truncate(null, -1, 0), "offset cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate(null, -10, -4),
                "offset cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate(null, Integer.MIN_VALUE, Integer.MIN_VALUE),
                "offset cannot be negative");
        assertNull(StringUtils.truncate(null, 10, 12));
        assertEquals("", StringUtils.truncate("", 0, 10));
        assertEquals("", StringUtils.truncate("", 2, 10));
        assertEquals("abc", StringUtils.truncate("abcdefghij", 0, 3));
        assertEquals("fghij", StringUtils.truncate("abcdefghij", 5, 6));
        assertEquals("", StringUtils.truncate("abcdefghij", 0, 0));
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate("abcdefghij", 0, -1),
                "maxWith cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate("abcdefghij", 0, -10),
                "maxWith cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate("abcdefghij", 0, -100),
                "maxWith cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate("abcdefghij", 1, -100),
                "maxWith cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate("abcdefghij", 0, Integer.MIN_VALUE),
                "maxWith cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate("abcdefghij", -1, 0),
                "offset cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate("abcdefghij", -10, 0),
                "offset cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate("abcdefghij", -100, 1),
                "offset cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate("abcdefghij", Integer.MIN_VALUE, 0),
                "offset cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate("abcdefghij", -1, -1),
                "offset cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate("abcdefghij", -10, -10),
                "offset cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate("abcdefghij", -100, -100),
                "offset cannot be negative");
        assertThrows(
                IllegalArgumentException.class,
                () -> StringUtils.truncate("abcdefghij", Integer.MIN_VALUE, Integer.MIN_VALUE),
                "offset cannot be negative");
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