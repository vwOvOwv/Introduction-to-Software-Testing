# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `de0819cb86fcd597961b99fd8cb71b8b74fd8cec`
- B: `c6fac966ab314769d27e117bab05aee1a72df760`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `150190`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 38002, 'completion_tokens': 2625, 'total_tokens': 40627, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 665}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 37618}`

---

- 新增 `testTruncate_StringInt` 测试方法，对应生产代码新增的 `truncate(String, int)` 方法，覆盖 null、负数、正常截断及边界情况。
- 新增 `testTruncate_StringIntInt` 测试方法，对应生产代码新增的 `truncate(String, int, int)` 方法，覆盖 null、offset 负数、maxWidth 负数、各种截断及边界情况。
- 无需修改或删除已有测试方法，导入已足够，无需调整 import。

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
        fail("maxWith cannot be negative"); // actually offset exception will be thrown first
    } catch (Exception e) {
        assertTrue(e instanceof IllegalArgumentException);
    }
    try {
        StringUtils.truncate(null, -10, -4);
        fail("maxWith cannot be negative"); // actually offset exception will be thrown first
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