# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `f909f466e3d0bdaf8789ed1ae3ebcbbef0966665`
- B: `3a0d3b93a81fd8c795be4da3bc34f693f7ee9ed3`
- test: `src/test/java/org/apache/commons/lang3/exception/ExceptionUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/exception/ExceptionUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `42530`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9779, 'completion_tokens': 712, 'total_tokens': 10491, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 432}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 9395}`

---

- 新增 `testIsChecked_null`、`testIsChecked_unchecked`、`testIsChecked_checked`、`testIsChecked_error`、`testIsUnchecked_unchecked`、`testIsUnchecked_checked`、`testIsUnchecked_error` 七个测试方法，覆盖新增的 `isChecked` 和 `isUnchecked` 方法。
- import 语句无需调整，`IOException` 已在旧测试头部导入，`StackOverflowError` 属于 `java.lang` 默认可见。

```java
@Test
public void testIsChecked_null() {
    assertFalse(ExceptionUtils.isChecked(null));
}

@Test
public void testIsChecked_unchecked() {
    assertFalse(ExceptionUtils.isChecked(new IllegalArgumentException()));
}

@Test
public void testIsChecked_checked() {
    assertTrue(ExceptionUtils.isChecked(new IOException()));
}

@Test
public void testIsChecked_error() {
    assertFalse(ExceptionUtils.isChecked(new StackOverflowError()));
}

@Test
public void testIsUnchecked_unchecked() {
    assertTrue(ExceptionUtils.isUnchecked(new IllegalArgumentException()));
}

@Test
public void testIsUnchecked_checked() {
    assertFalse(ExceptionUtils.isUnchecked(new IOException()));
}

@Test
public void testIsUnchecked_error() {
    assertTrue(ExceptionUtils.isUnchecked(new StackOverflowError()));
}
```