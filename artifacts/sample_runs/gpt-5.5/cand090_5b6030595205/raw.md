# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `3a0d3b93a81fd8c795be4da3bc34f693f7ee9ed3`
- B: `5b6030595205f5f843549f1f12a0e1037bf4a50f`
- test: `src/test/java/org/apache/commons/lang3/exception/ExceptionUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/exception/ExceptionUtils.java']`
- old_test_mode: `methods`
- user_chars: `5998`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1824, 'completion_tokens': 630, 'total_tokens': 2454}`

---

- 修改/保留 `testIsChecked_checked`、`testIsChecked_error`、`testIsChecked_null`、`testIsChecked_unchecked`、`testIsUnchecked_checked`、`testIsUnchecked_error`、`testIsUnchecked_unchecked`：生产代码仅调整 `@since` 文档，`isChecked`/`isUnchecked` 行为未变，测试断言保持一致；无需调整 import。

```java
@Test
public void testIsChecked_checked() {
    assertTrue(ExceptionUtils.isChecked(new IOException()));
}

@Test
public void testIsChecked_error() {
    assertFalse(ExceptionUtils.isChecked(new StackOverflowError()));
}

@Test
public void testIsChecked_null() {
    assertFalse(ExceptionUtils.isChecked(null));
}

@Test
public void testIsChecked_unchecked() {
    assertFalse(ExceptionUtils.isChecked(new IllegalArgumentException()));
}

@Test
public void testIsUnchecked_checked() {
    assertFalse(ExceptionUtils.isUnchecked(new IOException()));
}

@Test
public void testIsUnchecked_error() {
    assertTrue(ExceptionUtils.isUnchecked(new StackOverflowError()));
}

@Test
public void testIsUnchecked_unchecked() {
    assertTrue(ExceptionUtils.isUnchecked(new IllegalArgumentException()));
}
```