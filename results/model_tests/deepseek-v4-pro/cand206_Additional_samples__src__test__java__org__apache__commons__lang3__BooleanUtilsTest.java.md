# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `af74365e311eb55936049bed6efa0d2f3af1ece2`
- B: `eabd95a51c6b70b5503c7ade734fff5b34f80ff6`
- test: `src/test/java/org/apache/commons/lang3/BooleanUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/BooleanUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `39564`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 8786, 'completion_tokens': 846, 'total_tokens': 9632, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 302}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 8402}`

---

- 修改 `test_toBooleanObject_String` 方法：在末尾添加两个新的断言，分别验证带尾随空格的 `"true "` 和 `"ono"` 均返回 `null`，以匹配生产代码 JavaDoc 中新增的示例行为。

```java
    @Test
    public void test_toBooleanObject_String() {
        assertEquals(null, BooleanUtils.toBooleanObject((String) null));
        assertEquals(null, BooleanUtils.toBooleanObject(""));
        assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("false"));
        assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("no"));
        assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("off"));
        assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("FALSE"));
        assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("NO"));
        assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("OFF"));
        assertEquals(null, BooleanUtils.toBooleanObject("oof"));
        assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("true"));
        assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("yes"));
        assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("on"));
        assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("TRUE"));
        assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("ON"));
        assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("YES"));
        assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("TruE"));
        assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("TruE"));

        assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("y")); // yes
        assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("Y"));
        assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("t")); // true
        assertEquals(Boolean.TRUE, BooleanUtils.toBooleanObject("T"));
        assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("f")); // false
        assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("F"));
        assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("n")); // No
        assertEquals(Boolean.FALSE, BooleanUtils.toBooleanObject("N"));
        assertEquals(null, BooleanUtils.toBooleanObject("z"));

        assertEquals(null, BooleanUtils.toBooleanObject("ab"));
        assertEquals(null, BooleanUtils.toBooleanObject("yoo"));
        assertEquals(null, BooleanUtils.toBooleanObject("true "));
        assertEquals(null, BooleanUtils.toBooleanObject("ono"));
    }
```