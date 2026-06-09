# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `a93703d002bc4850e7adcdfc9b51664fca7b8836`
- B: `be370cd0ef134bb44fde733e4ee91661a012dae5`
- test: `src/test/java/org/apache/commons/lang3/text/ExtendedMessageFormatTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/ExtendedMessageFormat.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `24360`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6054, 'completion_tokens': 1904, 'total_tokens': 7958, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1723}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 5670}`

---

- 新增 @Test 方法 `testEmbeddedPatternInChoice`，用于验证生产代码修复在 choice 嵌套模式中保留子格式的行为；无需修改或删除其他已有测试方法，import 保持现有即可。

```java
    /**
     * Test Bug LANG-917 - IndexOutOfBoundsException and/or infinite loop when using a choice pattern
     */
    @Test
    public void testEmbeddedPatternInChoice() {
        final String pattern = "Hi {0,lower}, got {1,choice,0#none|1#one|1<{1,number}}, {2,upper}!";
        final ExtendedMessageFormat emf = new ExtendedMessageFormat(pattern, registry);
        assertEquals(emf.format(new Object[] {"there", 3, "great"}), "Hi there, got 3, GREAT!");
    }
```