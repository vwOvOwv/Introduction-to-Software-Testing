# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `1e4a4906776f7300a9639a7599fccc545791583d`
- B: `eccf213204b776e40efcc031f4c0df560b9421e9`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `155892`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 39277, 'completion_tokens': 4260, 'total_tokens': 43537, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2552}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 38893}`

---

- 新增四个测试方法：`testReplaceIgnoreCase_StringStringString`、`testReplaceIgnoreCase_StringStringStringInt`、`testReplaceOnceIgnoreCase_StringStringString`、`testRemoveIgnoreCase_String`，分别对应生产代码新增的 `replaceIgnoreCase`、`replaceOnceIgnoreCase`、`removeIgnoreCase` 方法。无需调整 import，现有静态导入已涵盖所需断言方法。

```java
    @Test
    public void testReplaceIgnoreCase_StringStringString() {
        assertEquals(null, StringUtils.replaceIgnoreCase(null, null, null));
        assertEquals(null, StringUtils.replaceIgnoreCase(null, null, "any"));
        assertEquals(null, StringUtils.replaceIgnoreCase(null, "any", null));
        assertEquals(null, StringUtils.replaceIgnoreCase(null, "any", "any"));

        assertEquals("", StringUtils.replaceIgnoreCase("", null, null));
        assertEquals("", StringUtils.replaceIgnoreCase("", null, "any"));
        assertEquals("", StringUtils.replaceIgnoreCase("", "any", null));
        assertEquals("", StringUtils.replaceIgnoreCase("", "any", "any"));

        assertEquals("FOO", StringUtils.replaceIgnoreCase("FOO", "", "any"));
        assertEquals("FOO", StringUtils.replaceIgnoreCase("FOO", null, "any"));
        assertEquals("FOO", StringUtils.replaceIgnoreCase("FOO", "F", null));
        assertEquals("FOO", StringUtils.replaceIgnoreCase("FOO", null, null));

        assertEquals("", StringUtils.replaceIgnoreCase("foofoofoo", "foo", ""));
        assertEquals("barbarbar", StringUtils.replaceIgnoreCase("foofoofoo", "foo", "bar"));
        assertEquals("farfarfar", StringUtils.replaceIgnoreCase("foofoofoo", "oo", "ar"));

        // IgnoreCase
        assertEquals("", StringUtils.replaceIgnoreCase("foofoofoo", "FOO", ""));
        assertEquals("barbarbar", StringUtils.replaceIgnoreCase("fooFOOfoo", "foo", "bar"));
        assertEquals("farfarfar", StringUtils.replaceIgnoreCase("foofOOfoo", "OO", "ar"));
    }

    @Test
    public void testReplaceIgnoreCase_StringStringStringInt() {
        assertEquals(null, StringUtils.replaceIgnoreCase(null, null, null, 2));
        assertEquals(null, StringUtils.replaceIgnoreCase(null, null, "any", 2));
        assertEquals(null, StringUtils.replaceIgnoreCase(null, "any", null, 2));
        assertEquals(null, StringUtils.replaceIgnoreCase(null, "any", "any", 2));

        assertEquals("", StringUtils.replaceIgnoreCase("", null, null, 2));
        assertEquals("", StringUtils.replaceIgnoreCase("", null, "any", 2));
        assertEquals("", StringUtils.replaceIgnoreCase("", "any", null, 2));
        assertEquals("", StringUtils.replaceIgnoreCase("", "any", "any", 2));

        String str = new String(new char[] { 'o', 'o', 'f', 'o', 'o' });
        assertSame(str, StringUtils.replaceIgnoreCase(str, "x", "", -1));

        assertEquals("f", StringUtils.replaceIgnoreCase("oofoo", "o", "", -1));
        assertEquals("oofoo", StringUtils.replaceIgnoreCase("oofoo", "o", "", 0));
        assertEquals("ofoo", StringUtils.replaceIgnoreCase("oofoo", "o", "", 1));
        assertEquals("foo", StringUtils.replaceIgnoreCase("oofoo", "o", "", 2));
        assertEquals("fo", StringUtils.replaceIgnoreCase("oofoo", "o", "", 3));
        assertEquals("f", StringUtils.replaceIgnoreCase("oofoo", "o", "", 4));

        assertEquals("f", StringUtils.replaceIgnoreCase("oofoo", "o", "", -5));
        assertEquals("f", StringUtils.replaceIgnoreCase("oofoo", "o", "", 1000));

        // IgnoreCase
        assertEquals("f", StringUtils.replaceIgnoreCase("oofoo", "O", "", -1));
        assertEquals("oofoo", StringUtils.replaceIgnoreCase("oofoo", "O", "", 0));
        assertEquals("ofoo", StringUtils.replaceIgnoreCase("oofoo", "O", "", 1));
        assertEquals("foo", StringUtils.replaceIgnoreCase("oofoo", "O", "", 2));
        assertEquals("fo", StringUtils.replaceIgnoreCase("oofoo", "O", "", 3));
        assertEquals("f", StringUtils.replaceIgnoreCase("oofoo", "O", "", 4));

        assertEquals("f", StringUtils.replaceIgnoreCase("oofoo", "O", "", -5));
        assertEquals("f", StringUtils.replaceIgnoreCase("oofoo", "O", "", 1000));
    }

    @Test
    public void testReplaceOnceIgnoreCase_StringStringString() {
        assertEquals(null, StringUtils.replaceOnceIgnoreCase(null, null, null));
        assertEquals(null, StringUtils.replaceOnceIgnoreCase(null, null, "any"));
        assertEquals(null, StringUtils.replaceOnceIgnoreCase(null, "any", null));
        assertEquals(null, StringUtils.replaceOnceIgnoreCase(null, "any", "any"));

        assertEquals("", StringUtils.replaceOnceIgnoreCase("", null, null));
        assertEquals("", StringUtils.replaceOnceIgnoreCase("", null, "any"));
        assertEquals("", StringUtils.replaceOnceIgnoreCase("", "any", null));
        assertEquals("", StringUtils.replaceOnceIgnoreCase("", "any", "any"));

        assertEquals("FOO", StringUtils.replaceOnceIgnoreCase("FOO", "", "any"));
        assertEquals("FOO", StringUtils.replaceOnceIgnoreCase("FOO", null, "any"));
        assertEquals("FOO", StringUtils.replaceOnceIgnoreCase("FOO", "F", null));
        assertEquals("FOO", StringUtils.replaceOnceIgnoreCase("FOO", null, null));

        assertEquals("foofoo", StringUtils.replaceOnceIgnoreCase("foofoofoo", "foo", ""));

        // Ignore Case
        assertEquals("Foofoo", StringUtils.replaceOnceIgnoreCase("FoOFoofoo", "foo", ""));
    }

    @Test
    public void testRemoveIgnoreCase_String() {
        // StringUtils.removeIgnoreCase(null, *) = null
        assertEquals(null, StringUtils.removeIgnoreCase(null, null));
        assertEquals(null, StringUtils.removeIgnoreCase(null, ""));
        assertEquals(null, StringUtils.removeIgnoreCase(null, "a"));

        // StringUtils.removeIgnoreCase("", *) = ""
        assertEquals("", StringUtils.removeIgnoreCase("", null));
        assertEquals("", StringUtils.removeIgnoreCase("", ""));
        assertEquals("", StringUtils.removeIgnoreCase("", "a"));

        // StringUtils.removeIgnoreCase(*, null) = *
        assertEquals(null, StringUtils.removeIgnoreCase(null, null));
        assertEquals("", StringUtils.removeIgnoreCase("", null));
        assertEquals("a", StringUtils.removeIgnoreCase("a", null));

        // StringUtils.removeIgnoreCase(*, "") = *
        assertEquals(null, StringUtils.removeIgnoreCase(null, ""));
        assertEquals("", StringUtils.removeIgnoreCase("", ""));
        assertEquals("a", StringUtils.removeIgnoreCase("a", ""));

        // StringUtils.removeIgnoreCase("queued", "ue") = "qd"
        assertEquals("qd", StringUtils.removeIgnoreCase("queued", "ue"));

        // StringUtils.removeIgnoreCase("queued", "zz") = "queued"
        assertEquals("queued", StringUtils.removeIgnoreCase("queued", "zz"));

        // IgnoreCase
        // StringUtils.removeIgnoreCase("quEUed", "UE") = "qd"
        assertEquals("qd", StringUtils.removeIgnoreCase("quEUed", "UE"));

        // StringUtils.removeIgnoreCase("queued", "zZ") = "queued"
        assertEquals("queued", StringUtils.removeIgnoreCase("queued", "zZ"));
    }
```