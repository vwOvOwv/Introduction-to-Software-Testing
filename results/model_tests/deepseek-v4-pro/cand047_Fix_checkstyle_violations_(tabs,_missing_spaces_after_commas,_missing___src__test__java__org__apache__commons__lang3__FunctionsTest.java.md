# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `102a6d75650b7578e31bf18b840e0b613e83e439`
- B: `26bc45fdeeeda2bee38cc2a08ce99e41fd48e0d6`
- test: `src/test/java/org/apache/commons/lang3/FunctionsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Functions.java']`
- old_test_mode: `methods`
- user_chars: `24236`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6701, 'completion_tokens': 4229, 'total_tokens': 10930, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2607}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 6317}`

---

- 修改 `testAsCallable` 方法：调整 lambda 格式与类型参数中的空白字符，使其与提交 B 的代码风格一致。
- 修改 `testAsConsumer` 方法：移除 `Functions.asConsumer(...)` 调用中末尾多余空格，与 B 对齐。
- 修改 `testAsBiConsumer` 方法：将 `FailableBiConsumer` 构造中的 lambda 拆分为多行，并移除多余空格。
- 修改 `testAsFunction` 方法：调整 `FailableFunction` 类型参数空白与 lambda 内部缩进，使其符合 B 的风格。
- 修改 `testAsBiFunction` 方法：调整 `FailableBiFunction` 类型参数空白与 lambda 块格式，与 B 对齐。
- 修改 `testAsSupplier` 方法：调整 `FailableSupplier` 类型参数空白及 lambda 块格式。
- 删除不再使用的静态导入 `import static org.junit.jupiter.api.Assertions.assertFalse;`。

```java
// DELETE_IMPORT: import static org.junit.jupiter.api.Assertions.assertFalse;

    @Test
    void testAsCallable() {
        FailureOnOddInvocations.invocation = 0;
        final FailableCallable<FailureOnOddInvocations, SomeException> failableCallable = () -> {
            return new FailureOnOddInvocations();
        };
        final Callable<FailureOnOddInvocations> callable = Functions.asCallable(failableCallable);
        UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () ->  callable.call());
        final Throwable cause = e.getCause();
        assertNotNull(cause);
        assertTrue(cause instanceof SomeException);
        assertEquals("Odd Invocation: 1", cause.getMessage());
        final FailureOnOddInvocations instance;
        try {
            instance = callable.call();
        } catch (Exception ex) {
            throw Functions.rethrow(ex);
        }
        assertNotNull(instance);
    }

    @Test
    void testAsConsumer() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable testable = new Testable(ise);
        final Consumer<Testable> consumer = Functions.asConsumer((t) -> t.test());
        Throwable e = assertThrows(IllegalStateException.class, () -> consumer.accept(testable));
        assertSame(ise, e);

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> consumer.accept(testable));
        assertSame(error, e);

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> consumer.accept(testable));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);

        testable.setThrowable(null);
        Functions.accept(Testable::test, testable);
    }

    @Test
    void testAsBiConsumer() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable testable = new Testable(null);
        final FailableBiConsumer<Testable, Throwable, Throwable> failableBiConsumer = (t, th) -> {
            t.setThrowable(th); t.test();
        };
        final BiConsumer<Testable, Throwable> consumer = Functions.asBiConsumer(failableBiConsumer);
        Throwable e = assertThrows(IllegalStateException.class, () -> consumer.accept(testable, ise));
        assertSame(ise, e);

        final Error error = new OutOfMemoryError();
        e = assertThrows(OutOfMemoryError.class, () -> consumer.accept(testable, error));
        assertSame(error, e);

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> consumer.accept(testable,  ioe));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);

        consumer.accept(testable, null);
    }

    @Test
    public void testAsFunction() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable testable = new Testable(ise);
        final FailableFunction<Throwable, Integer, Throwable> failableFunction = (th) -> {
            testable.setThrowable(th);
            return Integer.valueOf(testable.testInt());
        };
        final Function<Throwable, Integer> function = Functions.asFunction(failableFunction);
        Throwable e = assertThrows(IllegalStateException.class, () -> function.apply(ise));
        assertSame(ise, e);

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> function.apply(error));
        assertSame(error, e);

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> function.apply(ioe));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);

        assertEquals(0, function.apply(null).intValue());
    }

    @Test
    public void testAsBiFunction() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable testable = new Testable(ise);
        final FailableBiFunction<Testable, Throwable, Integer, Throwable> failableBiFunction = (t, th) -> {
            t.setThrowable(th);
            return Integer.valueOf(t.testInt());
        };
        final BiFunction<Testable, Throwable, Integer> biFunction = Functions.asBiFunction(failableBiFunction);
        Throwable e = assertThrows(IllegalStateException.class, () -> biFunction.apply(testable, ise));
        assertSame(ise, e);

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> biFunction.apply(testable, error));
        assertSame(error, e);

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> biFunction.apply(testable, ioe));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);

        assertEquals(0, biFunction.apply(testable, null).intValue());
    }

    @Test
    public void testAsSupplier() {
        FailureOnOddInvocations.invocation = 0;
        final FailableSupplier<FailureOnOddInvocations, Throwable> failableSupplier = () -> {
            return new FailureOnOddInvocations();
        };
        final Supplier<FailureOnOddInvocations> supplier = Functions.asSupplier(failableSupplier);
        UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () ->  supplier.get());
        final Throwable cause = e.getCause();
        assertNotNull(cause);
        assertTrue(cause instanceof SomeException);
        assertEquals("Odd Invocation: 1", cause.getMessage());
        final FailureOnOddInvocations instance = supplier.get();
        assertNotNull(instance);
    }
```