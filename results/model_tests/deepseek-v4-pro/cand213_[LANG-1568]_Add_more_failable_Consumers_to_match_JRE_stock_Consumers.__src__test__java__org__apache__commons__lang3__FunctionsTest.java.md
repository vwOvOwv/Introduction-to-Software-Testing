# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `62393bd601d62b96c741e797fc3302bb30f644c5`
- B: `f5e9f55283788fc15a38191baea2cf765a227f4e`
- test: `src/test/java/org/apache/commons/lang3/FunctionsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Functions.java']`
- old_test_mode: `methods`
- user_chars: `40009`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 10148, 'completion_tokens': 6775, 'total_tokens': 16923, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1267}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 9764}`

---

- 需要新增静态导入 `import static org.junit.jupiter.api.Assertions.assertNull;`，因为新增测试方法中使用了 `assertNull`。
- 修改 `testAcceptBiConsumer` 方法：将 `Testable` 改为 `Testable<?, ?>` 泛型形式，适配 `Testable` 内部类的泛型化。
- 修改 `testAcceptConsumer` 方法：同上，使用 `Testable<?, ?>`。
- 修改 `testApplyBiFunction` 方法：使用 `Testable<?, ?>`。
- 修改 `testApplyFunction` 方法：使用 `Testable<?, ?>`。
- 修改 `testAsBiConsumer` 方法：使用 `Testable<?, ?>`。
- 修改 `testAsBiFunction` 方法：使用 `Testable<?, ?>`。
- 修改 `testAsConsumer` 方法：使用 `Testable<?, ?>`。
- 修改 `testAsFunction` 方法：使用 `Testable<?, ?>`。
- 修改 `testGetAsBooleanSupplier` 方法：使用 `Testable<?, ?>`。
- 修改 `testGetAsDoubleSupplier` 方法：使用 `Testable<?, ?>`。
- 修改 `testGetAsIntSupplier` 方法：使用 `Testable<?, ?>`，并把最后的 `Functions.getAsInt` 调用改为 `testable::testInteger`（与 B diff 一致）。
- 修改 `testGetAsLongSupplier` 方法：使用 `Testable<?, ?>`。
- 修改 `testGetSupplier` 方法：使用 `Testable<?, ?>`，并将最后的 `Functions.apply(Testable::testInteger, testable)` 改为 `Functions.get(testable::testInteger)`（与 B diff 一致）。
- 新增 `testAcceptDoubleConsumer` 方法：测试新的 `FailableDoubleConsumer` 与 `Functions.accept` 重载。
- 新增 `testAcceptIntConsumer` 方法：测试新的 `FailableIntConsumer` 与 `Functions.accept` 重载。
- 新增 `testAcceptLongConsumer` 方法：测试新的 `FailableLongConsumer` 与 `Functions.accept` 重载。
- 新增 `testAcceptObjDoubleConsumer` 方法：测试新的 `FailableObjDoubleConsumer` 与 `Functions.accept` 重载。
- 新增 `testAcceptObjIntConsumer` 方法：测试新的 `FailableObjIntConsumer` 与 `Functions.accept` 重载。
- 新增 `testAcceptObjLongConsumer` 方法：测试新的 `FailableObjLongConsumer` 与 `Functions.accept` 重载。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertNull;
// IMPORTS_END

@Test
void testAcceptBiConsumer() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, ?> testable = new Testable(null);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.accept(Testable::test, testable, ise));
    assertSame(ise, e);

    final Error error = new OutOfMemoryError();
    e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(Testable::test, testable, error));
    assertSame(error, e);

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.accept(Testable::test, testable, ioe));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);

    testable.setThrowable(null);
    Functions.accept(Testable::test, testable, (Throwable) null);
}

@Test
void testAcceptConsumer() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, ?> testable = new Testable<>(ise);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.accept(Testable::test, testable));
    assertSame(ise, e);

    final Error error = new OutOfMemoryError();
    testable.setThrowable(error);
    e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(Testable::test, testable));
    assertSame(error, e);

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.accept(Testable::test, testable));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);

    testable.setThrowable(null);
    Functions.accept(Testable::test, testable);
}

@Test
void testAcceptDoubleConsumer() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, Double> testable = new Testable<>(ise);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.accept(testable::testDouble, 1d));
    assertSame(ise, e);
    assertNull(testable.getAcceptedPrimitiveObject());

    final Error error = new OutOfMemoryError();
    testable.setThrowable(error);
    e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(testable::testDouble, 1d));
    assertSame(error, e);
    assertNull(testable.getAcceptedPrimitiveObject());

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.accept(testable::testDouble, 1d));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);
    assertNull(testable.getAcceptedPrimitiveObject());

    testable.setThrowable(null);
    Functions.accept(testable::testDouble, 1d);
    assertEquals(1, testable.getAcceptedPrimitiveObject());
}

@Test
void testAcceptIntConsumer() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, Integer> testable = new Testable<>(ise);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.accept(testable::testInt, 1));
    assertSame(ise, e);
    assertNull(testable.getAcceptedPrimitiveObject());

    final Error error = new OutOfMemoryError();
    testable.setThrowable(error);
    e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(testable::testInt, 1));
    assertSame(error, e);
    assertNull(testable.getAcceptedPrimitiveObject());

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.accept(testable::testInt, 1));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);
    assertNull(testable.getAcceptedPrimitiveObject());

    testable.setThrowable(null);
    Functions.accept(testable::testInt, 1);
    assertEquals(1, testable.getAcceptedPrimitiveObject());
}

@Test
void testAcceptLongConsumer() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, Long> testable = new Testable<>(ise);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.accept(testable::testLong, 1L));
    assertSame(ise, e);
    assertNull(testable.getAcceptedPrimitiveObject());

    final Error error = new OutOfMemoryError();
    testable.setThrowable(error);
    e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(testable::testLong, 1L));
    assertSame(error, e);
    assertNull(testable.getAcceptedPrimitiveObject());

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.accept(testable::testLong, 1L));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);
    assertNull(testable.getAcceptedPrimitiveObject());

    testable.setThrowable(null);
    Functions.accept(testable::testLong, 1L);
    assertEquals(1, testable.getAcceptedPrimitiveObject());
}

@Test
void testAcceptObjDoubleConsumer() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<String, Double> testable = new Testable<>(ise);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.accept(testable::testObjDouble, "X", 1d));
    assertSame(ise, e);
    assertNull(testable.getAcceptedObject());
    assertNull(testable.getAcceptedPrimitiveObject());

    final Error error = new OutOfMemoryError();
    testable.setThrowable(error);
    e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(testable::testObjDouble, "X", 1d));
    assertSame(error, e);
    assertNull(testable.getAcceptedObject());
    assertNull(testable.getAcceptedPrimitiveObject());

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.accept(testable::testObjDouble, "X", 1d));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);
    assertNull(testable.getAcceptedObject());
    assertNull(testable.getAcceptedPrimitiveObject());

    testable.setThrowable(null);
    Functions.accept(testable::testObjDouble, "X", 1d);
    assertEquals("X", testable.getAcceptedObject());
    assertEquals(1d, testable.getAcceptedPrimitiveObject());
}

@Test
void testAcceptObjIntConsumer() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<String, Integer> testable = new Testable<>(ise);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.accept(testable::testObjInt, "X", 1));
    assertSame(ise, e);
    assertNull(testable.getAcceptedObject());
    assertNull(testable.getAcceptedPrimitiveObject());

    final Error error = new OutOfMemoryError();
    testable.setThrowable(error);
    e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(testable::testObjInt, "X", 1));
    assertSame(error, e);
    assertNull(testable.getAcceptedObject());
    assertNull(testable.getAcceptedPrimitiveObject());

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.accept(testable::testObjInt, "X", 1));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);
    assertNull(testable.getAcceptedObject());
    assertNull(testable.getAcceptedPrimitiveObject());

    testable.setThrowable(null);
    Functions.accept(testable::testObjInt, "X", 1);
    assertEquals("X", testable.getAcceptedObject());
    assertEquals(1, testable.getAcceptedPrimitiveObject());
}

@Test
void testAcceptObjLongConsumer() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<String, Long> testable = new Testable<>(ise);
    Throwable e = assertThrows(IllegalStateException.class, () -> Functions.accept(testable::testObjLong, "X", 1L));
    assertSame(ise, e);
    assertNull(testable.getAcceptedObject());
    assertNull(testable.getAcceptedPrimitiveObject());

    final Error error = new OutOfMemoryError();
    testable.setThrowable(error);
    e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(testable::testObjLong, "X", 1L));
    assertSame(error, e);
    assertNull(testable.getAcceptedObject());
    assertNull(testable.getAcceptedPrimitiveObject());

    final IOException ioe = new IOException("Unknown I/O error");
    testable.setThrowable(ioe);
    e = assertThrows(UncheckedIOException.class, () -> Functions.accept(testable::testObjLong, "X", 1L));
    final Throwable t = e.getCause();
    assertNotNull(t);
    assertSame(ioe, t);
    assertNull(testable.getAcceptedObject());
    assertNull(testable.getAcceptedPrimitiveObject());

    testable.setThrowable(null);
    Functions.accept(testable::testObjLong, "X", 1L);
    assertEquals("X", testable.getAcceptedObject());
    assertEquals(1L, testable.getAcceptedPrimitiveObject());
}

@Test
public void testApplyBiFunction() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, ?> testable = new Testable(null);
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
public void testApplyFunction() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, ?> testable = new Testable<>(ise);
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
void testAsBiConsumer() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, ?> testable = new Testable(null);
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
public void testAsBiFunction() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, ?> testable = new Testable<>(ise);
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
void testAsConsumer() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, ?> testable = new Testable<>(ise);
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

@Test
public void testAsFunction() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, ?> testable = new Testable<>(ise);
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
public void testGetAsBooleanSupplier() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, ?> testable = new Testable<>(ise);
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
    final Testable<?, ?> testable = new Testable<>(ise);
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
    final Testable<?, ?> testable = new Testable<>(ise);
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
    final int i = Functions.getAsInt(testable::testInteger);
    assertEquals(0, i);
}

@Test
public void testGetAsLongSupplier() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, ?> testable = new Testable<>(ise);
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
public void testGetSupplier() {
    final IllegalStateException ise = new IllegalStateException();
    final Testable<?, ?> testable = new Testable<>(ise);
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
```