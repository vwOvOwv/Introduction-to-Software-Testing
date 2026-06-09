# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `59022fb870c2c45a27e00943003c5acdeddaeec3`
- B: `03fe88ab71cf2eadaa39654786c3fba713742768`
- test: `src/test/java/org/apache/commons/lang3/exception/ExceptionUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/exception/ExceptionUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `32510`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7521, 'completion_tokens': 635, 'total_tokens': 8156}`

---

- 新增辅助内部类 `TestThrowable`，用于覆盖 `wrapAndThrow(Throwable)` 包装普通受检 `Throwable` 后由 `hasCause` 解包判断的场景；无需调整 import。
- 新增 `@Test` 方法 `testWrapAndUnwrapError`，对应生产代码中 `wrapAndThrow` 对 `Error` 原样抛出、`hasCause` 直接识别类型的行为；无需调整 import。
- 新增 `@Test` 方法 `testWrapAndUnwrapRuntimeException`，对应生产代码中 `wrapAndThrow` 对 `RuntimeException` 原样抛出、`hasCause` 直接识别类型的行为；无需调整 import。
- 新增 `@Test` 方法 `testWrapAndUnwrapCheckedException`，对应生产代码中 `wrapAndThrow` 将受检异常包装为 `UndeclaredThrowableException`、`hasCause` 解包识别 cause 的行为；无需调整 import。
- 新增 `@Test` 方法 `testWrapAndUnwrapThrowable`，对应生产代码中 `wrapAndThrow` 将普通 `Throwable` 包装后由 `hasCause` 解包识别自定义类型的行为；无需调整 import。

```java
public static class TestThrowable extends Throwable {
    private static final long serialVersionUID = 1L;
}

@Test
public void testWrapAndUnwrapError() {
    try {
        ExceptionUtils.wrapAndThrow(new OutOfMemoryError());
        Assert.fail("Error not thrown");
    } catch (final Throwable t) {
        Assert.assertTrue(ExceptionUtils.hasCause(t, Error.class));
    }
}

@Test
public void testWrapAndUnwrapRuntimeException() {
    try {
        ExceptionUtils.wrapAndThrow(new IllegalArgumentException());
        Assert.fail("RuntimeException not thrown");
    } catch (final Throwable t) {
        Assert.assertTrue(ExceptionUtils.hasCause(t, RuntimeException.class));
    }
}

@Test
public void testWrapAndUnwrapCheckedException() {
    try {
        ExceptionUtils.wrapAndThrow(new IOException());
        Assert.fail("Checked Exception not thrown");
    } catch (final Throwable t) {
        Assert.assertTrue(ExceptionUtils.hasCause(t, IOException.class));
    }
}

@Test
public void testWrapAndUnwrapThrowable() {
    try {
        ExceptionUtils.wrapAndThrow(new TestThrowable());
        Assert.fail("Checked Exception not thrown");
    } catch (final Throwable t) {
        Assert.assertTrue(ExceptionUtils.hasCause(t, TestThrowable.class));
    }
}
```