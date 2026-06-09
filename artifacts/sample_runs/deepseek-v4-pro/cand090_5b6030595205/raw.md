# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `3a0d3b93a81fd8c795be4da3bc34f693f7ee9ed3`
- B: `5b6030595205f5f843549f1f12a0e1037bf4a50f`
- test: `src/test/java/org/apache/commons/lang3/exception/ExceptionUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/exception/ExceptionUtils.java']`
- old_test_mode: `methods`
- user_chars: `5998`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1871, 'completion_tokens': 2043, 'total_tokens': 3914, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1644}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1487}`

---

- 删除旧位置的 `testIsChecked_checked`、`testIsChecked_error`、`testIsChecked_null`、`testIsChecked_unchecked`、`testIsUnchecked_checked`、`testIsUnchecked_error`、`testIsUnchecked_unchecked` 测试方法，以避免与移动后新增的方法产生重复定义，保证编译通过。
- 新增这些测试方法（内容不变），以便与生产代码 `@since 3.13.0` 注释更新后的版本 B 测试文件结构一致，断言会直接通过（生产逻辑未变）。
- 无需调整 import 语句，所用异常类均来自 `java.lang`，无需额外导入。

```java
// DELETE_TESTS_START
testIsChecked_checked
testIsChecked_error
testIsChecked_null
testIsChecked_unchecked
testIsUnchecked_checked
testIsUnchecked_error
testIsUnchecked_unchecked
// DELETE_TESTS_END

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