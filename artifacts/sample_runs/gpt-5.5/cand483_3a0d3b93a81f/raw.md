# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `f909f466e3d0bdaf8789ed1ae3ebcbbef0966665`
- B: `3a0d3b93a81fd8c795be4da3bc34f693f7ee9ed3`
- test: `src/test/java/org/apache/commons/lang3/exception/ExceptionUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/exception/ExceptionUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `42530`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9587, 'completion_tokens': 405, 'total_tokens': 9992}`

---

- 新增 `testIsChecked_null`：覆盖新增 `ExceptionUtils.isChecked(null)` 返回 `false` 的行为；无需调整 import。
- 新增 `testIsChecked_unchecked`：覆盖 `RuntimeException` 属于 unchecked，`isChecked` 返回 `false`；无需调整 import。
- 新增 `testIsChecked_checked`：覆盖普通 checked exception，`isChecked` 返回 `true`；无需调整 import。
- 新增 `testIsChecked_error`：覆盖 `Error` 属于 unchecked，`isChecked` 返回 `false`；无需调整 import。
- 新增 `testIsUnchecked_unchecked`：覆盖 `ExceptionUtils.isUnchecked(RuntimeException)` 返回 `true`；无需调整 import。
- 新增 `testIsUnchecked_checked`：覆盖 checked exception 的 `isUnchecked` 返回 `false`；无需调整 import。
- 新增 `testIsUnchecked_error`：覆盖 `Error` 的 `isUnchecked` 返回 `true`；无需调整 import。

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