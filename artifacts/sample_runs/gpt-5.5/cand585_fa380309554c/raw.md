# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `7ee27499f8ddb1ff39e9736c90176c65654ec952`
- B: `fa380309554ce4e0c1efdbec1e3b489444ecbf72`
- test: `src/test/java/org/apache/commons/lang3/text/StrSubstitutorTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/StrSubstitutor.java']`
- old_test_mode: `methods`
- user_chars: `8425`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2303, 'completion_tokens': 496, 'total_tokens': 2799}`

---

- 修改 `testGetSetPrefix`：生产代码将 `setVariablePrefix(null)` 与 `setVariablePrefixMatcher(null)` 的异常从 `IllegalArgumentException` 改为 `NullPointerException`，测试断言同步更新。
- 修改 `testGetSetSuffix`：生产代码将 `setVariableSuffix(null)` 与 `setVariableSuffixMatcher(null)` 的异常从 `IllegalArgumentException` 改为 `NullPointerException`，测试断言同步更新。
- 不需要调整 import。

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