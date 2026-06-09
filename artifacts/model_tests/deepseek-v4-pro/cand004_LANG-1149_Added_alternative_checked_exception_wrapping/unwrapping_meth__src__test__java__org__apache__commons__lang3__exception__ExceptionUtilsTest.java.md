# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `59022fb870c2c45a27e00943003c5acdeddaeec3`
- B: `03fe88ab71cf2eadaa39654786c3fba713742768`
- test: `src/test/java/org/apache/commons/lang3/exception/ExceptionUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/exception/ExceptionUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `32510`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7528, 'completion_tokens': 1973, 'total_tokens': 9501, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1488}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 7144}`

---

- 新增 `TestThrowable` 内部类（供新增测试方法使用），与生产代码的 `UndeclaredThrowableException` 转换逻辑配套。
- 新增 `@Test testWrapAndUnwrapError()`：验证 `wrapAndThrow` 对 `Error` 的正确抛出与 `hasCause` 配合。
- 新增 `@Test testWrapAndUnwrapRuntimeException()`：验证 `wrapAndThrow` 对 `RuntimeException` 的正确抛出与 `hasCause` 配合。
- 新增 `@Test testWrapAndUnwrapCheckedException()`：验证 `wrapAndThrow` 对检查异常的包装抛出与 `hasCause` 配合。
- 新增 `@Test testWrapAndUnwrapThrowable()`：验证 `wrapAndThrow` 对普通 `Throwable` 的包装抛出与 `hasCause` 配合。
- 无需调整 import；现有静态导入已覆盖 `assertTrue`、`fail` 等。

```java
public static class TestThrowable extends Throwable {
    private static final long serialVersionUID = 1L;
}

@Test
public void testWrapAndUnwrapError() {
    try {
        ExceptionUtils.wrapAndThrow(new OutOfMemoryError());
        Assert.fail("Error not thrown");
    }
    catch(Throwable t) {
        Assert.assertTrue(ExceptionUtils.hasCause(t, Error.class));
    }
}

@Test
public void testWrapAndUnwrapRuntimeException() {
    try {
        ExceptionUtils.wrapAndThrow(new IllegalArgumentException());
        Assert.fail("RuntimeException not thrown");
    }
    catch(Throwable t) {
        Assert.assertTrue(ExceptionUtils.hasCause(t, RuntimeException.class));
    }
}

@Test
public void testWrapAndUnwrapCheckedException() {
    try {
        ExceptionUtils.wrapAndThrow(new IOException());
        Assert.fail("Checked Exception not thrown");
    }
    catch(Throwable t) {
        Assert.assertTrue(ExceptionUtils.hasCause(t, IOException.class));
    }
}

@Test
public void testWrapAndUnwrapThrowable() {
    try {
        ExceptionUtils.wrapAndThrow(new TestThrowable());
        Assert.fail("Checked Exception not thrown");
    }
    catch(Throwable t) {
        Assert.assertTrue(ExceptionUtils.hasCause(t, TestThrowable.class));
    }
}
```