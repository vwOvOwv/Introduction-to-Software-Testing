# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `c8e648b92cc133a604b5e1f4da1ced943788e64b`
- B: `9b3257e4d1a63e0a4d971a331eaf7b9a08d98040`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `161460`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 40517, 'completion_tokens': 1450, 'total_tokens': 41967, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1264}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 40133}`

---

- 新增 `@Test` 方法 `testGetDigits`，以覆盖生产代码新增的 `StringUtils.getDigits` 方法。
- 无需修改或删除任何已有的测试方法。
- 现有 import 已满足需求，无需额外添加或调整。

```java
    @Test
    public void testGetDigits() {
        assertEquals(null, StringUtils.getDigits(null));
        assertEquals("", StringUtils.getDigits(""));
        assertEquals("", StringUtils.getDigits("abc"));
        assertEquals("1000", StringUtils.getDigits("1000$"));
        assertEquals("12345", StringUtils.getDigits("123password45"));
        assertEquals("5417543010", StringUtils.getDigits("(541) 754-3010"));
        assertEquals("\u0967\u0968\u0969", StringUtils.getDigits("\u0967\u0968\u0969"));
    }
```