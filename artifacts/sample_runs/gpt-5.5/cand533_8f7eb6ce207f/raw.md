# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e968ad5a3f42f9eb7b3bd9ed95f827918d884e77`
- B: `8f7eb6ce207f354c83157b95bdf9848d59944650`
- test: `src/test/java/org/apache/commons/lang3/FunctionsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Functions.java']`
- old_test_mode: `methods`
- user_chars: `4879`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1603, 'completion_tokens': 500, 'total_tokens': 2103}`

---

- 修改 `testAsCallable`：对照测试 diff，将 `FailableCallable` 的 lambda 构造调用改为构造方法引用 `FailureOnOddInvocations::new`，无需调整 import。
- 修改 `testAsConsumer`：对照测试 diff，将 `Functions.asConsumer(t -> t.test())` 改为方法引用 `Functions.asConsumer(Testable::test)`，无需调整 import。

```java
@Test
void testAsCallable() {
    FailureOnOddInvocations.invocation = 0;
    final FailableCallable<FailureOnOddInvocations, SomeException> failableCallable = FailureOnOddInvocations::new;
    final Callable<FailureOnOddInvocations> callable = Functions.asCallable(failableCallable);
    final UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () ->  callable.call());
    final Throwable cause = e.getCause();
    assertNotNull(cause);
    assertTrue(cause instanceof SomeException);
    assertEquals("Odd Invocation: 1", cause.getMessage());
    final FailureOnOddInvocations instance;
    try {
        instance = callable.call();
    } catch (final Exception ex) {
        throw Functions.rethrow(ex);
    }
    assertNotNull(instance);
}

@Test
void testAsConsumer() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable testable = new Testable(ise);
    final Consumer<Testable> consumer = Functions.asConsumer(Testable::test);
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
```