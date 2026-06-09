# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e2ec4f2fdb2bb8d97f64a33e9ac288d52854a530`
- B: `fc73151cfca36ea2641f340700dbe339b9e1f103`
- test: `src/test/java/org/apache/commons/lang3/text/StrBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/StrBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `73764`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 18168, 'completion_tokens': 1059, 'total_tokens': 19227, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 961}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 17784}`

---

- 新增 @Test 方法 test_LANG_1131_EqualsWithNullStrBuilder：验证 StrBuilder.equals(StrBuilder) 对 null 参数返回 false，与生产代码新增的 null 检查保持一致。

```java
@Test
public void test_LANG_1131_EqualsWithNullStrBuilder() throws Exception {
    final StrBuilder sb = new StrBuilder();
    final StrBuilder other = null;
    assertFalse(sb.equals(other));
}
```