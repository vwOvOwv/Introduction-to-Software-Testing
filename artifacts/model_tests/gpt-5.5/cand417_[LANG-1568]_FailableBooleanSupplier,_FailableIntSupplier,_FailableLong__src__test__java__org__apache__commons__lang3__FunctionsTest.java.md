# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `53aa7a2e9a4d0e186139dc72ddc9709595c2183a`
- B: `d88f70e8ff3e73981809ddc530c19288c1f092c5`
- test: `src/test/java/org/apache/commons/lang3/FunctionsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Functions.java']`
- old_test_mode: `methods`
- user_chars: `38013`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9041, 'completion_tokens': 4301, 'total_tokens': 13342}`

---

- 新增 `testGetSupplier`，对应生产代码中 `Functions.get(FailableSupplier)` 行为补充断言覆盖。
- 新增 `testGetAsBooleanSupplier`，对应新增的 `Functions.getAsBoolean(FailableBooleanSupplier)`。
- 新增 `testGetAsDoubleSupplier`，对应新增的 `Functions.getAsDouble(FailableDoubleSupplier)`。
- 新增 `testGetAsIntSupplier`，对应新增的 `Functions.getAsInt(FailableIntSupplier)`。
- 新增 `testGetAsLongSupplier`，对应新增的 `Functions.getAsLong(FailableLongSupplier)`。
- 修改 `testApplyFunction`、`testAsFunction`、`testApplyBiFunction`、`testAsBiFunction`，将旧的 `Testable::testInt` 调整为新版测试辅助方法 `Testable::testInteger`。
- 修改 `testRunnable`、`testAsRunnable`、`testCallable`、`testAsCallable`、`testGetFromSupplier`、`testAsPredicate`、`testAsBiPredicate`、`testAsSupplier`，将 `FailureOnOddInvocations.invocation` 调整为 `invocations`。
- 需要新增静态 import：`assertFalse`，用于 boolean supplier 成功路径断言。

```java
import static org.junit.jupiter.api.Assertions.assertFalse;

@Test
void testRunnable() {
    FailureOnOddInvocations.invocations = 0;
    final UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () ->  Functions.run(FailureOnOddInvocations::new));
    final Throwable cause = e.getCause();
    assertNotNull(cause);
    assertTrue(cause instanceof SomeException);
    assertEquals("Odd Invocation: 1", cause.getMessage());

    // Even invocations, should not throw an exception
    Functions.run(FailureOnOddInvocations::new);
}

@Test
void testAsRunnable() {
    FailureOnOddInvocations.invocations = 0;
    final Runnable runnable = Functions.asRunnable(FailureOnOddInvocations::new);
    final UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () ->  runnable.run());
    final Throwable cause = e.getCause();
    assertNotNull(cause);
    assertTrue(cause instanceof SomeException);
    assertEquals("Odd Invocation: 1", cause.getMessage());

    // Even invocations, should not throw an exception
    runnable.run();
}

@Test
void testCallable() {
    FailureOnOddInvocations.invocations = 0;
    final UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () ->  Functions.run(FailureOnOddInvocations::new));
    final Throwable cause = e.getCause();
    assertNotNull(cause);
    assertTrue(cause instanceof SomeException);
    assertEquals("Odd Invocation: 1", cause.getMessage());
    final FailureOnOddInvocations instance = Functions.call(FailureOnOddInvocations::new);
    assertNotNull(instance);
}

@Test
void testAsCallable() {
    FailureOnOddInvocations.invocations = 0;
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
public void testApplyFunction() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable testable = new Testable(ise);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.apply(Testable::testInteger, testable));
    assertSame(ise, e);

    final Error error = new OutOfMemoryError();
    testable.setThrowable(error);
    e = assertThrows(OutOfMemoryError.class, () -> Functions.apply(Testable::testInteger, testable));
    assertSame(error, e);

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.apply(Testable::testInteger, testable));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);

    testable.setThrowable(null);
    final Integer i = Functions.apply(Testable::testInteger, testable);
    assertNotNull(i);
    assertEquals(0, i.intValue());
}

@Test
public void testAsFunction() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable testable = new Testable(ise);
    final FailableFunction<Throwable, Integer, Throwable> failableFunction = th -> {
        testable.setThrowable(th);
        return Integer.valueOf(testable.testInteger());
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
public void testApplyBiFunction() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable testable = new Testable(null);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.apply(Testable::testInteger, testable, ise));
    assertSame(ise, e);

    final Error error = new OutOfMemoryError();
    e = assertThrows(OutOfMemoryError.class, () -> Functions.apply(Testable::testInteger, testable, error));
    assertSame(error, e);

    final IOException ioe = new IOException("Unknown I/O error");
    e = assertThrows(UncheckedIOException.class, () -> Functions.apply(Testable::testInteger, testable, ioe));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);

    final Integer i = Functions.apply(Testable::testInteger, testable, (Throwable) null);
    assertNotNull(i);
    assertEquals(0, i.intValue());
}

@Test
public void testAsBiFunction() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable testable = new Testable(ise);
    final FailableBiFunction<Testable, Throwable, Integer, Throwable> failableBiFunction = (t, th) -> {
        t.setThrowable(th);
        return Integer.valueOf(t.testInteger());
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
public void testGetFromSupplier() {
    FailureOnOddInvocations.invocations = 0;
    final UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () ->  Functions.run(FailureOnOddInvocations::new));
    final Throwable cause = e.getCause();
    assertNotNull(cause);
    assertTrue(cause instanceof SomeException);
    assertEquals("Odd Invocation: 1", cause.getMessage());
    final FailureOnOddInvocations instance = Functions.call(FailureOnOddInvocations::new);
    assertNotNull(instance);
}

@Test
public void testGetSupplier() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable testable = new Testable(ise);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.get(testable::testInteger));
    assertSame(ise, e);

    final Error error = new OutOfMemoryError();
    testable.setThrowable(error);
    e = assertThrows(OutOfMemoryError.class, () -> Functions.get(testable::testInteger));
    assertSame(error, e);

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.get(testable::testInteger));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);

    testable.setThrowable(null);
    final Integer i = Functions.get(testable::testInteger);
    assertNotNull(i);
    assertEquals(0, i.intValue());
}

@Test
public void testGetAsBooleanSupplier() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable testable = new Testable(ise);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.getAsBoolean(testable::testBooleanPrimitive));
    assertSame(ise, e);

    final Error error = new OutOfMemoryError();
    testable.setThrowable(error);
    e = assertThrows(OutOfMemoryError.class, () -> Functions.getAsBoolean(testable::testBooleanPrimitive));
    assertSame(error, e);

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.getAsBoolean(testable::testBooleanPrimitive));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);

    testable.setThrowable(null);
    assertFalse(Functions.getAsBoolean(testable::testBooleanPrimitive));
}

@Test
public void testGetAsDoubleSupplier() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable testable = new Testable(ise);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.getAsDouble(testable::testDoublePrimitive));
    assertSame(ise, e);

    final Error error = new OutOfMemoryError();
    testable.setThrowable(error);
    e = assertThrows(OutOfMemoryError.class, () -> Functions.getAsDouble(testable::testDoublePrimitive));
    assertSame(error, e);

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.getAsDouble(testable::testDoublePrimitive));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);

    testable.setThrowable(null);
    assertEquals(0, Functions.getAsDouble(testable::testDoublePrimitive));
}

@Test
public void testGetAsIntSupplier() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable testable = new Testable(ise);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.getAsInt(testable::testIntPrimitive));
    assertSame(ise, e);

    final Error error = new OutOfMemoryError();
    testable.setThrowable(error);
    e = assertThrows(OutOfMemoryError.class, () -> Functions.getAsInt(testable::testIntPrimitive));
    assertSame(error, e);

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.getAsInt(testable::testIntPrimitive));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);

    testable.setThrowable(null);
    final int i = Functions.getAsInt(testable::testIntPrimitive);
    assertEquals(0, i);
}

@Test
public void testGetAsLongSupplier() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable testable = new Testable(ise);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.getAsLong(testable::testLongPrimitive));
    assertSame(ise, e);

    final Error error = new OutOfMemoryError();
    testable.setThrowable(error);
    e = assertThrows(OutOfMemoryError.class, () -> Functions.getAsLong(testable::testLongPrimitive));
    assertSame(error, e);

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.getAsLong(testable::testLongPrimitive));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);

    testable.setThrowable(null);
    final long i = Functions.getAsLong(testable::testLongPrimitive);
    assertEquals(0, i);
}

@Test
@DisplayName("Test that asPredicate(FailablePredicate) is converted to -> Predicate ")
public void testAsPredicate() {
    FailureOnOddInvocations.invocations = 0;
    final Functions.FailablePredicate<Object, Throwable> failablePredicate = t -> FailureOnOddInvocations.failingBool();
    final Predicate<?> predicate = Functions.asPredicate(failablePredicate);
    final UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () -> predicate.test(null));
    final Throwable cause = e.getCause();
    assertNotNull(cause);
    assertTrue(cause instanceof SomeException);
    assertEquals("Odd Invocation: 1", cause.getMessage());
    final boolean instance = predicate.test(null);
    assertNotNull(instance);
}

@Test
@DisplayName("Test that asPredicate(FailableBiPredicate) is converted to -> BiPredicate ")
public void testAsBiPredicate() {
    FailureOnOddInvocations.invocations = 0;
    final Functions.FailableBiPredicate<Object, Object, Throwable> failableBiPredicate = (t1, t2) -> FailureOnOddInvocations.failingBool();
    final BiPredicate<?, ?> predicate = Functions.asBiPredicate(failableBiPredicate);
    final UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () -> predicate.test(null, null));
    final Throwable cause = e.getCause();
    assertNotNull(cause);
    assertTrue(cause instanceof SomeException);
    assertEquals("Odd Invocation: 1", cause.getMessage());
    final boolean instance = predicate.test(null, null);
    assertNotNull(instance);
}

@Test
public void testAsSupplier() {
    FailureOnOddInvocations.invocations = 0;
    final FailableSupplier<FailureOnOddInvocations, Throwable> failableSupplier = FailureOnOddInvocations::new;
    final Supplier<FailureOnOddInvocations> supplier = Functions.asSupplier(failableSupplier);
    final UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () ->  supplier.get());
    final Throwable cause = e.getCause();
    assertNotNull(cause);
    assertTrue(cause instanceof SomeException);
    assertEquals("Odd Invocation: 1", cause.getMessage());
    assertNotNull(supplier.get());
}
```