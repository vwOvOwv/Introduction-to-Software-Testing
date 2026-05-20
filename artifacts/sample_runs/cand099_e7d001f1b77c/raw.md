# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `6e0c4f9cc9df28853afc025d33ca6512b292926f`
- B: `e7d001f1b77c382f99ee7fe01d8563d8219697df`
- test: `src/test/java/org/apache/commons/lang3/RegExUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RegExUtils.java']`
- old_test_mode: `methods`
- user_chars: `6312`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2154, 'completion_tokens': 599, 'total_tokens': 2753, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 1898}`

---

- 新增 `testRemovePattern` 方法，对应生产代码新增的 `removePattern(CharSequence, String)` 重载方法，测试参数类型改为 `CharSequence`。
- 将旧方法 `testRemovePattern_StringString` 重命名为 `testRemovePatternDeprecated`，对应生产代码中旧 `removePattern(String, String)` 被标记为 `@Deprecated`，测试保持不变。
- 无需调整 import。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    public void testRemovePattern() {
        assertNull(RegExUtils.removePattern((CharSequence) null, ""));
        assertEquals("any", RegExUtils.removePattern((CharSequence) "any", (String) null));

        assertEquals("", RegExUtils.removePattern((CharSequence) "", ""));
        assertEquals("", RegExUtils.removePattern((CharSequence) "", ".*"));
        assertEquals("", RegExUtils.removePattern((CharSequence) "", ".+"));

        assertEquals("AB", RegExUtils.removePattern((CharSequence) "A<__>\n<__>B", "<.*>"));
        assertEquals("AB", RegExUtils.removePattern((CharSequence) "A<__>\\n<__>B", "<.*>"));
        assertEquals("", RegExUtils.removePattern((CharSequence) "<A>x\\ny</A>", "<A>.*</A>"));
        assertEquals("", RegExUtils.removePattern((CharSequence) "<A>\nxy\n</A>", "<A>.*</A>"));

        assertEquals("ABC123", RegExUtils.removePattern((CharSequence) "ABCabc123", "[a-z]"));
    }

    @Test
    public void testRemovePatternDeprecated() {
        assertNull(RegExUtils.removePattern(null, ""));
        assertEquals("any", RegExUtils.removePattern("any", (String) null));

        assertEquals("", RegExUtils.removePattern("", ""));
        assertEquals("", RegExUtils.removePattern("", ".*"));
        assertEquals("", RegExUtils.removePattern("", ".+"));

        assertEquals("AB", RegExUtils.removePattern("A<__>\n<__>B", "<.*>"));
        assertEquals("AB", RegExUtils.removePattern("A<__>\\n<__>B", "<.*>"));
        assertEquals("", RegExUtils.removePattern("<A>x\\ny</A>", "<A>.*</A>"));
        assertEquals("", RegExUtils.removePattern("<A>\nxy\n</A>", "<A>.*</A>"));

        assertEquals("ABC123", RegExUtils.removePattern("ABCabc123", "[a-z]"));
    }
```