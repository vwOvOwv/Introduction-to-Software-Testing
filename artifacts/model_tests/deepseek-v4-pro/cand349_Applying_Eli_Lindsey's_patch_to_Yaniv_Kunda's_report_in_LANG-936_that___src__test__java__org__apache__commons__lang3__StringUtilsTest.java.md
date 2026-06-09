# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `3a8595f1a57759044be301fc76a2300b7f2efe66`
- B: `8cd2339a9788cf2c6e44b6761d3a19259fbe1df3`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `120563`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 30095, 'completion_tokens': 2734, 'total_tokens': 32829, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1485}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 29711}`

---

- 修改 `testGetLevenshteinDistance_StringStringInt` 方法：在原有 `getLevenshteinDistance` 测试用例之后、异常检验之前，新增 7 行断言，使用 `Integer.MAX_VALUE` 作为阈值，验证生产代码中溢出修复的正确性。
- import 无需变更。

```java
@Test
public void testGetLevenshteinDistance_StringStringInt() {
    // empty strings
    assertEquals(0, StringUtils.getLevenshteinDistance("", "", 0));
    assertEquals(7, StringUtils.getLevenshteinDistance("aaapppp", "", 8));
    assertEquals(7, StringUtils.getLevenshteinDistance("aaapppp", "", 7));
    assertEquals(-1, StringUtils.getLevenshteinDistance("aaapppp", "", 6));

    // unequal strings, zero threshold
    assertEquals(-1, StringUtils.getLevenshteinDistance("b", "a", 0));
    assertEquals(-1, StringUtils.getLevenshteinDistance("a", "b", 0));

    // equal strings
    assertEquals(0, StringUtils.getLevenshteinDistance("aa", "aa", 0));
    assertEquals(0, StringUtils.getLevenshteinDistance("aa", "aa", 2));

    // same length
    assertEquals(-1, StringUtils.getLevenshteinDistance("aaa", "bbb", 2));
    assertEquals(3, StringUtils.getLevenshteinDistance("aaa", "bbb", 3));

    // big stripe
    assertEquals(6, StringUtils.getLevenshteinDistance("aaaaaa", "b", 10));

    // distance less than threshold
    assertEquals(7, StringUtils.getLevenshteinDistance("aaapppp", "b", 8));
    assertEquals(3, StringUtils.getLevenshteinDistance("a", "bbb", 4));

    // distance equal to threshold
    assertEquals(7, StringUtils.getLevenshteinDistance("aaapppp", "b", 7));
    assertEquals(3, StringUtils.getLevenshteinDistance("a", "bbb", 3));

    // distance greater than threshold
    assertEquals(-1, StringUtils.getLevenshteinDistance("a", "bbb", 2));
    assertEquals(-1, StringUtils.getLevenshteinDistance("bbb", "a", 2));
    assertEquals(-1, StringUtils.getLevenshteinDistance("aaapppp", "b", 6));

    // stripe runs off array, strings not similar
    assertEquals(-1, StringUtils.getLevenshteinDistance("a", "bbb", 1));
    assertEquals(-1, StringUtils.getLevenshteinDistance("bbb", "a", 1));

    // stripe runs off array, strings are similar
    assertEquals(-1, StringUtils.getLevenshteinDistance("12345", "1234567", 1));
    assertEquals(-1, StringUtils.getLevenshteinDistance("1234567", "12345", 1));

    // old getLevenshteinDistance test cases
    assertEquals(1, StringUtils.getLevenshteinDistance("frog", "fog",1) );
    assertEquals(3, StringUtils.getLevenshteinDistance("fly", "ant",3) );
    assertEquals(7, StringUtils.getLevenshteinDistance("elephant", "hippo",7) );
    assertEquals(-1, StringUtils.getLevenshteinDistance("elephant", "hippo",6) );
    assertEquals(7, StringUtils.getLevenshteinDistance("hippo", "elephant",7) );
    assertEquals(-1, StringUtils.getLevenshteinDistance("hippo", "elephant",6) );
    assertEquals(8, StringUtils.getLevenshteinDistance("hippo", "zzzzzzzz",8) );
    assertEquals(8, StringUtils.getLevenshteinDistance("zzzzzzzz", "hippo",8) );
    assertEquals(1, StringUtils.getLevenshteinDistance("hello", "hallo",1) );

    assertEquals(1, StringUtils.getLevenshteinDistance("frog", "fog", Integer.MAX_VALUE) );
    assertEquals(3, StringUtils.getLevenshteinDistance("fly", "ant", Integer.MAX_VALUE) );
    assertEquals(7, StringUtils.getLevenshteinDistance("elephant", "hippo", Integer.MAX_VALUE) );
    assertEquals(7, StringUtils.getLevenshteinDistance("hippo", "elephant", Integer.MAX_VALUE) );
    assertEquals(8, StringUtils.getLevenshteinDistance("hippo", "zzzzzzzz", Integer.MAX_VALUE) );
    assertEquals(8, StringUtils.getLevenshteinDistance("zzzzzzzz", "hippo", Integer.MAX_VALUE) );
    assertEquals(1, StringUtils.getLevenshteinDistance("hello", "hallo", Integer.MAX_VALUE) );

    // exceptions
    try {
        @SuppressWarnings("unused")
        final
        int d = StringUtils.getLevenshteinDistance("a", null, 0);
        fail("expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        // empty
    }
    try {
        @SuppressWarnings("unused")
        final
        int d = StringUtils.getLevenshteinDistance(null, "a", 0);
        fail("expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        // empty
    }

    try {
        @SuppressWarnings("unused")
        final
        int d = StringUtils.getLevenshteinDistance("a", "a", -1);
        fail("expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        // empty
    }
}
```