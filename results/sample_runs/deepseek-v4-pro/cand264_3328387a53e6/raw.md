# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `1181552e7d260e860b7f62def1c39f7b0fcae4a4`
- B: `3328387a53e6abc26e171b97d8d3dc1c2b5d4971`
- test: `src/test/java/org/apache/commons/lang3/text/StrBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/StrBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `76440`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 18798, 'completion_tokens': 1644, 'total_tokens': 20442, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1472}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 18414}`

---

- 新增 @Test 方法 `testAppendCharBuffer`，以覆盖生产代码中新增的 `append(CharBuffer)` 及 `append(CharBuffer, int, int)` 重载；无需调整 import（`CharBuffer` 已导入）。

```java
    //-----------------------------------------------------------------------
    @Test
    public void testAppendCharBuffer() {
        final StrBuilder sb1 = new StrBuilder();
        final CharBuffer buf = CharBuffer.allocate(10);
        buf.append("0123456789");
        buf.flip();
        sb1.append(buf);
        assertEquals("0123456789", sb1.toString());

        final StrBuilder sb2 = new StrBuilder();
        sb2.append(buf, 1, 8);
        assertEquals("12345678", sb2.toString());
    }
```