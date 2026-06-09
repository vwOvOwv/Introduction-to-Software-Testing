# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `0799f01df18c8f2d5695390cfc6db807fe019b18`
- B: `02a98515a337991f0ce05271ac90121fa204d9db`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `129007`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 32390, 'completion_tokens': 777, 'total_tokens': 33167, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 515}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 32006}`

---

我们需要新增 `testRotate_StringInt` 测试方法，因为生产代码新增了 `StringUtils.rotate` 而旧测试类中尚未包含对应的测试。其他已有测试无需修改，import 亦无需调整。

```java
    //-----------------------------------------------------------------------
    @Test
    public void testRotate_StringInt() {
        assertEquals(null, StringUtils.rotate(null, 1));
        assertEquals("", StringUtils.rotate("", 1));
        assertEquals("abcdefg", StringUtils.rotate("abcdefg", 0));
        assertEquals("fgabcde", StringUtils.rotate("abcdefg", 2));
        assertEquals("cdefgab", StringUtils.rotate("abcdefg", -2));
        assertEquals("abcdefg", StringUtils.rotate("abcdefg", 7));
        assertEquals("abcdefg", StringUtils.rotate("abcdefg", -7));
        assertEquals("fgabcde", StringUtils.rotate("abcdefg", 9));
        assertEquals("cdefgab", StringUtils.rotate("abcdefg", -9));
        assertEquals("efgabcd", StringUtils.rotate("abcdefg", 17));
        assertEquals("defgabc", StringUtils.rotate("abcdefg", -17));
    }
```