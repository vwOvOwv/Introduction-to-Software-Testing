# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `7ee27499f8ddb1ff39e9736c90176c65654ec952`
- B: `fa380309554ce4e0c1efdbec1e3b489444ecbf72`
- test: `src/test/java/org/apache/commons/lang3/text/StrSubstitutorTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/StrSubstitutor.java']`
- old_test_mode: `methods`
- user_chars: `8425`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2464, 'completion_tokens': 1131, 'total_tokens': 3595, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 576}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2080}`

---

- 修改 `testGetSetPrefix` 方法：将两处 `assertThrows(IllegalArgumentException.class, ...)` 替换为 `assertThrows(NullPointerException.class, ...)`，与生产代码抛出的 `NullPointerException` 保持一致。
- 修改 `testGetSetSuffix` 方法：将两处 `assertThrows(IllegalArgumentException.class, ...)` 替换为 `assertThrows(NullPointerException.class, ...)`，与生产代码抛出的 `NullPointerException` 保持一致。
- 无需新增或删除 `@Test` 方法，无需调整 `import` 语句。

```java
@Test
public void testGetSetPrefix() {
    final StrSubstitutor sub = new StrSubstitutor();
    assertTrue(sub.getVariablePrefixMatcher() instanceof StrMatcher.StringMatcher);
    sub.setVariablePrefix('<');
    assertTrue(sub.getVariablePrefixMatcher() instanceof StrMatcher.CharMatcher);

    sub.setVariablePrefix("<<");
    assertTrue(sub.getVariablePrefixMatcher() instanceof StrMatcher.StringMatcher);
    assertThrows(NullPointerException.class, () -> sub.setVariablePrefix(null));
    assertTrue(sub.getVariablePrefixMatcher() instanceof StrMatcher.StringMatcher);

    final StrMatcher matcher = StrMatcher.commaMatcher();
    sub.setVariablePrefixMatcher(matcher);
    assertSame(matcher, sub.getVariablePrefixMatcher());
    assertThrows(NullPointerException.class, () -> sub.setVariablePrefixMatcher(null));
    assertSame(matcher, sub.getVariablePrefixMatcher());
}

@Test
public void testGetSetSuffix() {
    final StrSubstitutor sub = new StrSubstitutor();
    assertTrue(sub.getVariableSuffixMatcher() instanceof StrMatcher.StringMatcher);
    sub.setVariableSuffix('<');
    assertTrue(sub.getVariableSuffixMatcher() instanceof StrMatcher.CharMatcher);

    sub.setVariableSuffix("<<");
    assertTrue(sub.getVariableSuffixMatcher() instanceof StrMatcher.StringMatcher);
    assertThrows(NullPointerException.class, () -> sub.setVariableSuffix(null));
    assertTrue(sub.getVariableSuffixMatcher() instanceof StrMatcher.StringMatcher);

    final StrMatcher matcher = StrMatcher.commaMatcher();
    sub.setVariableSuffixMatcher(matcher);
    assertSame(matcher, sub.getVariableSuffixMatcher());
    assertThrows(NullPointerException.class, () -> sub.setVariableSuffixMatcher(null));
    assertSame(matcher, sub.getVariableSuffixMatcher());
}
```