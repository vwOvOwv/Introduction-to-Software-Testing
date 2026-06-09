# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `f13d18cff3f0932e727dda04bf80008fc2fbbc70`
- B: `f643b4fa939e89348618ddffae20a804f4461363`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `28976`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7382, 'completion_tokens': 4413, 'total_tokens': 11795, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 4172}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 6998}`

---

- 将新增 `@Test` 方法 `testCharOverflow`；无需调整任何 import。

```java
    /**
     * Test for LANG-1286. Creates situation where old code would
     * overflow a char and result in a code point outside the specified
     * range.
     * 
     * @throws Exception
     */
    @Test
    public void testCharOverflow() throws Exception {
        int start = Character.MAX_VALUE;
        int end = Integer.MAX_VALUE;
        
        @SuppressWarnings("serial")
        Random fixedRandom = new Random() {
            @Override
            public int nextInt(int n) {
                // Prevents selection of 'start' as the character
                return super.nextInt(n - 1) + 1;
            }
        };
        
        String result = RandomStringUtils.random(2, start, end, false, false, null, fixedRandom);
        int c = result.codePointAt(0);
        assertTrue(String.format("Character '%d' not in range [%d,%d).", c, start, end), c >= start && c < end);
    }
```