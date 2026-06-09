# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `133327272a3c7466ff53acff875b473556d0a4b2`
- B: `7f90306f909e6dba46be275c0f492c8de353b492`
- test: `src/test/java/org/apache/commons/lang3/FunctionsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Functions.java']`
- old_test_mode: `methods`
- user_chars: `136231`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 31278, 'completion_tokens': 7910, 'total_tokens': 39188}`

---

- 修改 `Testable` 辅助类：生产代码新增 `FailableDoubleBinaryOperator`/`applyAsDouble`，测试辅助类需区分两个 primitive 入参并统一 `testAs*` 命名。
- 修改 `testAcceptBiConsumer`、`testAcceptDoubleConsumer`、`testAcceptIntConsumer`、`testAcceptLongConsumer`、`testAcceptObjDoubleConsumer`、`testAcceptObjIntConsumer`、`testAcceptObjLongConsumer`：对应测试 diff 中 primitive 记录字段从 `acceptedPrimitiveObject` 拆分为 `acceptedPrimitiveObject1/2`。
- 修改 `testApplyBiFunction`、`testApplyFunction`、`testGetAsBooleanSupplier`、`testGetAsDoubleSupplier`、`testGetAsIntSupplier`、`testGetAsLongSupplier`、`testGetSupplier`：对应测试辅助方法从 `testInteger/test*Primitive` 重命名为 `testAsInteger/testAs*Primitive`。
- 新增 `testApplyDoubleBinaryOperator`：覆盖生产代码新增的 `Functions.applyAsDouble(FailableDoubleBinaryOperator, double, double)`。
- 删除旧测试方法 `testAsBiConsumer`、`testAsBiFunction`、`testAsBiPredicate`、`testAsFunction`、`testAsPredicate`，并新增对应的 `testBiConsumer`、`testBiFunction`、`testBiPredicate`、`testFunction`、`testPredicate`。
- 不需要调整 import：新增/修改的方法继续使用测试类已有的 JUnit、`java.util.function`、`IOException`/`UncheckedIOException` 等 import。

```java
// DELETE_TESTS_START
testAsBiConsumer
testAsBiFunction
testAsBiPredicate
testAsFunction
testAsPredicate
// DELETE_TESTS_END

    public static class Testable<T, P> {
        private T acceptedObject;
        private P acceptedPrimitiveObject1;
        private P acceptedPrimitiveObject2;
        private Throwable throwable;

        Testable(final Throwable throwable) {
            this.throwable = throwable;
        }

        public T getAcceptedObject() {
            return acceptedObject;
        }

        public P getAcceptedPrimitiveObject1() {
            return acceptedPrimitiveObject1;
        }

        public P getAcceptedPrimitiveObject2() {
            return acceptedPrimitiveObject2;
        }

        public void setThrowable(final Throwable throwable) {
            this.throwable = throwable;
        }

        public void test() throws Throwable {
            test(throwable);
        }

        public Object test(Object input1, Object input2) throws Throwable {
            test(throwable);
            return acceptedObject;
        }

        public void test(final Throwable throwable) throws Throwable {
            if (throwable != null) {
                throw throwable;
            }
        }

        public boolean testAsBooleanPrimitive() throws Throwable {
            return testAsBooleanPrimitive(throwable);
        }

        public boolean testAsBooleanPrimitive(final Throwable throwable) throws Throwable {
            if (throwable != null) {
                throw throwable;
            }
            return false;
        }

        public double testAsDoublePrimitive() throws Throwable {
            return testAsDoublePrimitive(throwable);
        }

        public double testAsDoublePrimitive(final Throwable throwable) throws Throwable {
            if (throwable != null) {
                throw throwable;
            }
            return 0;
        }

        public Integer testAsInteger() throws Throwable {
            return testAsInteger(throwable);
        }

        public Integer testAsInteger(final Throwable throwable) throws Throwable {
            if (throwable != null) {
                throw throwable;
            }
            return 0;
        }

        public int testAsIntPrimitive() throws Throwable {
            return testAsIntPrimitive(throwable);
        }

        public int testAsIntPrimitive(final Throwable throwable) throws Throwable {
            if (throwable != null) {
                throw throwable;
            }
            return 0;
        }

        public long testAsLongPrimitive() throws Throwable {
            return testAsLongPrimitive(throwable);
        }

        public long testAsLongPrimitive(final Throwable throwable) throws Throwable {
            if (throwable != null) {
                throw throwable;
            }
            return 0;
        }

        public void testDouble(double i) throws Throwable {
            test(throwable);
            acceptedPrimitiveObject1 = (P) ((Double) i);
        }

        public double testDoubleDouble(double i, double j) throws Throwable {
            test(throwable);
            acceptedPrimitiveObject1 = (P) ((Double) i);
            acceptedPrimitiveObject2 = (P) ((Double) j);
            return 3d;
        }

        public void testInt(int i) throws Throwable {
            test(throwable);
            acceptedPrimitiveObject1 = (P) ((Integer) i);
        }

        public void testLong(long i) throws Throwable {
            test(throwable);
            acceptedPrimitiveObject1 = (P) ((Long) i);
        }

        public void testObjDouble(T object, double i) throws Throwable {
            test(throwable);
            acceptedObject = object;
            acceptedPrimitiveObject1 = (P) ((Double) i);
        }

        public void testObjInt(T object, int i) throws Throwable {
            test(throwable);
            acceptedObject = object;
            acceptedPrimitiveObject1 = (P) ((Integer) i);
        }

        public void testObjLong(T object, long i) throws Throwable {
            test(throwable);
            acceptedObject = object;
            acceptedPrimitiveObject1 = (P) ((Long) i);
        }
    }

    @Test
    void testAcceptBiConsumer() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, ?> testable = new Testable<>(null);
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
    void testAcceptDoubleConsumer() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, Double> testable = new Testable<>(ise);
        Throwable e = assertThrows(IllegalStateException.class, () -> Functions.accept(testable::testDouble, 1d));
        assertSame(ise, e);
        assertNull(testable.getAcceptedPrimitiveObject1());

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(testable::testDouble, 1d));
        assertSame(error, e);
        assertNull(testable.getAcceptedPrimitiveObject1());

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> Functions.accept(testable::testDouble, 1d));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);
        assertNull(testable.getAcceptedPrimitiveObject1());

        testable.setThrowable(null);
        Functions.accept(testable::testDouble, 1d);
        assertEquals(1, testable.getAcceptedPrimitiveObject1());
    }

    @Test
    void testAcceptIntConsumer() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, Integer> testable = new Testable<>(ise);
        Throwable e = assertThrows(IllegalStateException.class, () -> Functions.accept(testable::testInt, 1));
        assertSame(ise, e);
        assertNull(testable.getAcceptedPrimitiveObject1());

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(testable::testInt, 1));
        assertSame(error, e);
        assertNull(testable.getAcceptedPrimitiveObject1());

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> Functions.accept(testable::testInt, 1));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);
        assertNull(testable.getAcceptedPrimitiveObject1());

        testable.setThrowable(null);
        Functions.accept(testable::testInt, 1);
        assertEquals(1, testable.getAcceptedPrimitiveObject1());
    }

    @Test
    void testAcceptLongConsumer() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, Long> testable = new Testable<>(ise);
        Throwable e = assertThrows(IllegalStateException.class, () -> Functions.accept(testable::testLong, 1L));
        assertSame(ise, e);
        assertNull(testable.getAcceptedPrimitiveObject1());

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(testable::testLong, 1L));
        assertSame(error, e);
        assertNull(testable.getAcceptedPrimitiveObject1());

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> Functions.accept(testable::testLong, 1L));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);
        assertNull(testable.getAcceptedPrimitiveObject1());

        testable.setThrowable(null);
        Functions.accept(testable::testLong, 1L);
        assertEquals(1, testable.getAcceptedPrimitiveObject1());
    }

    @Test
    void testAcceptObjDoubleConsumer() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<String, Double> testable = new Testable<>(ise);
        Throwable e = assertThrows(IllegalStateException.class,
            () -> Functions.accept(testable::testObjDouble, "X", 1d));
        assertSame(ise, e);
        assertNull(testable.getAcceptedObject());
        assertNull(testable.getAcceptedPrimitiveObject1());

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(testable::testObjDouble, "X", 1d));
        assertSame(error, e);
        assertNull(testable.getAcceptedObject());
        assertNull(testable.getAcceptedPrimitiveObject1());

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> Functions.accept(testable::testObjDouble, "X", 1d));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);
        assertNull(testable.getAcceptedObject());
        assertNull(testable.getAcceptedPrimitiveObject1());

        testable.setThrowable(null);
        Functions.accept(testable::testObjDouble, "X", 1d);
        assertEquals("X", testable.getAcceptedObject());
        assertEquals(1d, testable.getAcceptedPrimitiveObject1());
    }

    @Test
    void testAcceptObjIntConsumer() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<String, Integer> testable = new Testable<>(ise);
        Throwable e = assertThrows(IllegalStateException.class, () -> Functions.accept(testable::testObjInt, "X", 1));
        assertSame(ise, e);
        assertNull(testable.getAcceptedObject());
        assertNull(testable.getAcceptedPrimitiveObject1());

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(testable::testObjInt, "X", 1));
        assertSame(error, e);
        assertNull(testable.getAcceptedObject());
        assertNull(testable.getAcceptedPrimitiveObject1());

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> Functions.accept(testable::testObjInt, "X", 1));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);
        assertNull(testable.getAcceptedObject());
        assertNull(testable.getAcceptedPrimitiveObject1());

        testable.setThrowable(null);
        Functions.accept(testable::testObjInt, "X", 1);
        assertEquals("X", testable.getAcceptedObject());
        assertEquals(1, testable.getAcceptedPrimitiveObject1());
    }

    @Test
    void testAcceptObjLongConsumer() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<String, Long> testable = new Testable<>(ise);
        Throwable e = assertThrows(IllegalStateException.class, () -> Functions.accept(testable::testObjLong, "X", 1L));
        assertSame(ise, e);
        assertNull(testable.getAcceptedObject());
        assertNull(testable.getAcceptedPrimitiveObject1());

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> Functions.accept(testable::testObjLong, "X", 1L));
        assertSame(error, e);
        assertNull(testable.getAcceptedObject());
        assertNull(testable.getAcceptedPrimitiveObject1());

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> Functions.accept(testable::testObjLong, "X", 1L));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);
        assertNull(testable.getAcceptedObject());
        assertNull(testable.getAcceptedPrimitiveObject1());

        testable.setThrowable(null);
        Functions.accept(testable::testObjLong, "X", 1L);
        assertEquals("X", testable.getAcceptedObject());
        assertEquals(1L, testable.getAcceptedPrimitiveObject1());
    }

    @Test
    public void testApplyBiFunction() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, ?> testable = new Testable<>(null);
        Throwable e = assertThrows(IllegalStateException.class,
            () -> Functions.apply(Testable::testAsInteger, testable, ise));
        assertSame(ise, e);

        final Error error = new OutOfMemoryError();
        e = assertThrows(OutOfMemoryError.class, () -> Functions.apply(Testable::testAsInteger, testable, error));
        assertSame(error, e);

        final IOException ioe = new IOException("Unknown I/O error");
        e = assertThrows(UncheckedIOException.class, () -> Functions.apply(Testable::testAsInteger, testable, ioe));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);

        final Integer i = Functions.apply(Testable::testAsInteger, testable, (Throwable) null);
        assertNotNull(i);
        assertEquals(0, i.intValue());
    }

    @Test
    public void testApplyDoubleBinaryOperator() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, Double> testable = new Testable<>(ise);
        Throwable e = assertThrows(IllegalStateException.class,
            () -> Functions.applyAsDouble(testable::testDoubleDouble, 1d, 2d));
        assertSame(ise, e);

        final Testable<?, Double> testable2 = new Testable<>(null);
        final double i = Functions.applyAsDouble(testable2::testDoubleDouble, 1d, 2d);
        assertEquals(3d, i);
    }

    @Test
    public void testApplyFunction() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, ?> testable = new Testable<>(ise);
        Throwable e = assertThrows(IllegalStateException.class,
            () -> Functions.apply(Testable::testAsInteger, testable));
        assertSame(ise, e);

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> Functions.apply(Testable::testAsInteger, testable));
        assertSame(error, e);

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> Functions.apply(Testable::testAsInteger, testable));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);

        testable.setThrowable(null);
        final Integer i = Functions.apply(Testable::testAsInteger, testable);
        assertNotNull(i);
        assertEquals(0, i.intValue());
    }

    @Test
    void testBiConsumer() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, ?> testable = new Testable<>(null);
        final FailableBiConsumer<Testable<?, ?>, Throwable, Throwable> failableBiConsumer = (t, th) -> {
            t.setThrowable(th);
            t.test();
        };
        final BiConsumer<Testable<?, ?>, Throwable> consumer = Functions.asBiConsumer(failableBiConsumer);
        Throwable e = assertThrows(IllegalStateException.class, () -> consumer.accept(testable, ise));
        assertSame(ise, e);

        final Error error = new OutOfMemoryError();
        e = assertThrows(OutOfMemoryError.class, () -> consumer.accept(testable, error));
        assertSame(error, e);

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> consumer.accept(testable, ioe));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);

        consumer.accept(testable, null);
    }

    @Test
    public void testBiFunction() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, ?> testable = new Testable<>(ise);
        final FailableBiFunction<Testable<?, ?>, Throwable, Integer, Throwable> failableBiFunction = (t, th) -> {
            t.setThrowable(th);
            return Integer.valueOf(t.testAsInteger());
        };
        final BiFunction<Testable<?, ?>, Throwable, Integer> biFunction = Functions.asBiFunction(failableBiFunction);
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
    @DisplayName("Test that asPredicate(FailableBiPredicate) is converted to -> BiPredicate ")
    public void testBiPredicate() {
        FailureOnOddInvocations.invocations = 0;
        final Functions.FailableBiPredicate<Object, Object, Throwable> failableBiPredicate = (t1,
            t2) -> FailureOnOddInvocations.failingBool();
        final BiPredicate<?, ?> predicate = Functions.asBiPredicate(failableBiPredicate);
        final UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class,
            () -> predicate.test(null, null));
        final Throwable cause = e.getCause();
        assertNotNull(cause);
        assertTrue(cause instanceof SomeException);
        assertEquals("Odd Invocation: 1", cause.getMessage());
        final boolean instance = predicate.test(null, null);
        assertNotNull(instance);
    }

    @Test
    public void testFunction() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, ?> testable = new Testable<>(ise);
        final FailableFunction<Throwable, Integer, Throwable> failableFunction = th -> {
            testable.setThrowable(th);
            return Integer.valueOf(testable.testAsInteger());
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
        Throwable e = assertThrows(IllegalStateException.class,
            () -> Functions.getAsBoolean(testable::testAsBooleanPrimitive));
        assertSame(ise, e);

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> Functions.getAsBoolean(testable::testAsBooleanPrimitive));
        assertSame(error, e);

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> Functions.getAsBoolean(testable::testAsBooleanPrimitive));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);

        testable.setThrowable(null);
        assertFalse(Functions.getAsBoolean(testable::testAsBooleanPrimitive));
    }

    @Test
    public void testGetAsDoubleSupplier() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, ?> testable = new Testable<>(ise);
        Throwable e = assertThrows(IllegalStateException.class,
            () -> Functions.getAsDouble(testable::testAsDoublePrimitive));
        assertSame(ise, e);

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> Functions.getAsDouble(testable::testAsDoublePrimitive));
        assertSame(error, e);

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> Functions.getAsDouble(testable::testAsDoublePrimitive));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);

        testable.setThrowable(null);
        assertEquals(0, Functions.getAsDouble(testable::testAsDoublePrimitive));
    }

    @Test
    public void testGetAsIntSupplier() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, ?> testable = new Testable<>(ise);
        Throwable e = assertThrows(IllegalStateException.class, () -> Functions.getAsInt(testable::testAsIntPrimitive));
        assertSame(ise, e);

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> Functions.getAsInt(testable::testAsIntPrimitive));
        assertSame(error, e);

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> Functions.getAsInt(testable::testAsIntPrimitive));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);

        testable.setThrowable(null);
        final int i = Functions.getAsInt(testable::testAsInteger);
        assertEquals(0, i);
    }

    @Test
    public void testGetAsLongSupplier() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, ?> testable = new Testable<>(ise);
        Throwable e = assertThrows(IllegalStateException.class,
            () -> Functions.getAsLong(testable::testAsLongPrimitive));
        assertSame(ise, e);

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> Functions.getAsLong(testable::testAsLongPrimitive));
        assertSame(error, e);

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> Functions.getAsLong(testable::testAsLongPrimitive));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);

        testable.setThrowable(null);
        final long i = Functions.getAsLong(testable::testAsLongPrimitive);
        assertEquals(0, i);
    }

    @Test
    public void testGetSupplier() {
        final IllegalStateException ise = new IllegalStateException();
        final Testable<?, ?> testable = new Testable<>(ise);
        Throwable e = assertThrows(IllegalStateException.class, () -> Functions.get(testable::testAsInteger));
        assertSame(ise, e);

        final Error error = new OutOfMemoryError();
        testable.setThrowable(error);
        e = assertThrows(OutOfMemoryError.class, () -> Functions.get(testable::testAsInteger));
        assertSame(error, e);

        final IOException ioe = new IOException("Unknown I/O error");
        testable.setThrowable(ioe);
        e = assertThrows(UncheckedIOException.class, () -> Functions.get(testable::testAsInteger));
        final Throwable t = e.getCause();
        assertNotNull(t);
        assertSame(ioe, t);

        testable.setThrowable(null);
        final Integer i = Functions.apply(Testable::testAsInteger, testable);
        assertNotNull(i);
        assertEquals(0, i.intValue());
    }

    @Test
    @DisplayName("Test that asPredicate(FailablePredicate) is converted to -> Predicate ")
    public void testPredicate() {
        FailureOnOddInvocations.invocations = 0;
        final Functions.FailablePredicate<Object, Throwable> failablePredicate = t -> FailureOnOddInvocations
            .failingBool();
        final Predicate<?> predicate = Functions.asPredicate(failablePredicate);
        final UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class,
            () -> predicate.test(null));
        final Throwable cause = e.getCause();
        assertNotNull(cause);
        assertTrue(cause instanceof SomeException);
        assertEquals("Odd Invocation: 1", cause.getMessage());
        final boolean instance = predicate.test(null);
        assertNotNull(instance);
    }
```