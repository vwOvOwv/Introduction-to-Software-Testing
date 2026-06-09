# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `21bab1d3a0b48c37592686fed7e1b2025fbf78aa`
- B: `ad648cf8a8a90bdee129266ca7b686a5b9a87561`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `7209`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2320, 'completion_tokens': 3165, 'total_tokens': 5485, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2384}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1936}`

---

- 需要将 `testWrap_StringChar`、`testWrapIfMissing_StringChar`、`testUnwrap_StringChar` 三个测试方法中使用的 `'\0'` 替换为 `CharUtils.NUL` 以匹配生产代码的变更。
- 需要新增一条 import：`import org.apache.commons.lang3.CharUtils;`。
- 无需删除任何原有测试方法。

```java
import org.apache.commons.lang3.CharUtils;

    @Test
    public void testWrap_StringChar() {
        assertNull(StringUtils.wrap(null, CharUtils.NUL));
        assertNull(StringUtils.wrap(null, '1'));

        assertEquals("", StringUtils.wrap("", CharUtils.NUL));
        assertEquals("xabx", StringUtils.wrap("ab", 'x'));
        assertEquals("\"ab\"", StringUtils.wrap("ab", '\"'));
        assertEquals("\"\"ab\"\"", StringUtils.wrap("\"ab\"", '\"'));
        assertEquals("'ab'", StringUtils.wrap("ab", '\''));
        assertEquals("''abcd''", StringUtils.wrap("'abcd'", '\''));
        assertEquals("'\"abcd\"'", StringUtils.wrap("\"abcd\"", '\''));
        assertEquals("\"'abcd'\"", StringUtils.wrap("'abcd'", '\"'));
    }

    @Test
    public void testWrapIfMissing_StringChar() {
        assertNull(StringUtils.wrapIfMissing(null, CharUtils.NUL));
        assertNull(StringUtils.wrapIfMissing(null, '1'));

        assertEquals("", StringUtils.wrapIfMissing("", CharUtils.NUL));
        assertEquals("xabx", StringUtils.wrapIfMissing("ab", 'x'));
        assertEquals("\"ab\"", StringUtils.wrapIfMissing("ab", '\"'));
        assertEquals("\"ab\"", StringUtils.wrapIfMissing("\"ab\"", '\"'));
        assertEquals("'ab'", StringUtils.wrapIfMissing("ab", '\''));
        assertEquals("'abcd'", StringUtils.wrapIfMissing("'abcd'", '\''));
        assertEquals("'\"abcd\"'", StringUtils.wrapIfMissing("\"abcd\"", '\''));
        assertEquals("\"'abcd'\"", StringUtils.wrapIfMissing("'abcd'", '\"'));
        assertEquals("/x/", StringUtils.wrapIfMissing("x", '/'));
        assertEquals("/x/y/z/", StringUtils.wrapIfMissing("x/y/z", '/'));
        assertEquals("/x/y/z/", StringUtils.wrapIfMissing("/x/y/z", '/'));
        assertEquals("/x/y/z/", StringUtils.wrapIfMissing("x/y/z/", '/'));
        assertEquals("/", StringUtils.wrapIfMissing("/", '/'));
    }

    @Test
    public void testUnwrap_StringChar() {
        assertNull(StringUtils.unwrap(null, null));
        assertNull(StringUtils.unwrap(null, CharUtils.NUL));
        assertNull(StringUtils.unwrap(null, '1'));

        assertEquals("abc", StringUtils.unwrap("abc", null));
        assertEquals("abc", StringUtils.unwrap("\'abc\'", '\''));
        assertEquals("abc", StringUtils.unwrap("AabcA", 'A'));
        assertEquals("AabcA", StringUtils.unwrap("AAabcAA", 'A'));
        assertEquals("abc", StringUtils.unwrap("abc", 'b'));
        assertEquals("#A", StringUtils.unwrap("#A", '#'));
        assertEquals("A#", StringUtils.unwrap("A#", '#'));
        assertEquals("ABA", StringUtils.unwrap("AABAA", 'A'));
    }
```