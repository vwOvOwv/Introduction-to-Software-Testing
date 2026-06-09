# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cde4c529034e182a982fd842252ec410d213c34c`
- B: `b5f5449cf338376d12404d0190054525987f4276`
- test: `src/test/java/org/apache/commons/lang3/CharSequenceUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/CharSequenceUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `11436`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3095, 'completion_tokens': 696, 'total_tokens': 3791, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 458}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2711}`

---

- 新增 `@Test` 方法 `testLastIndexOfSupplementaryCharacters`：对照测试 diff B 新增，用于验证 `lastIndexOf` 支持增补字符。
- 新增 `@Test` 方法 `testIndexOfSupplementaryCharacters`：对照测试 diff B 新增，用于验证 `indexOf` 支持增补字符。
- 无需调整 import，已有 `import static org.junit.Assert.*;`。

```java
    @Test
    public void testLastIndexOfSupplementaryCharacters(){
    	final int CODE_POINT = 0x2070E;
    	StringBuilder builder = new StringBuilder();
    	builder.appendCodePoint(CODE_POINT);
    	assertEquals(0, CharSequenceUtils.lastIndexOf(builder, CODE_POINT, 0));
    }
    
    @Test
    public void testIndexOfSupplementaryCharacters(){
    	final int CODE_POINT = 0x2070E;
    	StringBuilder builder = new StringBuilder();
    	builder.appendCodePoint(CODE_POINT);
    	assertEquals(0, CharSequenceUtils.indexOf(builder, CODE_POINT, 0));
    }
```