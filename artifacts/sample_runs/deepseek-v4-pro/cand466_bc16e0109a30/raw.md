# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9c4d162fdc071170a783bfb91bc631238ebe10c2`
- B: `bc16e0109a30b819c50895e157830fe9b3f8e93f`
- test: `src/test/java/org/apache/commons/lang3/FunctionsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Functions.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `28529`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7740, 'completion_tokens': 4449, 'total_tokens': 12189, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2185}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 7356}`

---

- 新增测试方法：`testAsRunnable` (测试 `Functions.asRunnable`，校验 Runnable 包装异常的转换)
- 新增测试方法：`testAsCallable` (测试 `Functions.asCallable`，校验 Callable 包装异常的转换)
- 新增测试方法：`testAsConsumer` (测试 `Functions.asConsumer`，校验 Consumer 包装异常的转换)
- 新增测试方法：`testAsBiConsumer` (测试 `Functions.asBiConsumer`，校验 BiConsumer 包装异常的转换)
- 新增测试方法：`testAsFunction` (测试 `Functions.asFunction`，校验 Function 包装异常的转换)
- 新增测试方法：`testAsBiFunction` (测试 `Functions.asBiFunction`，校验 BiFunction 包装异常的转换)
- 新增测试方法：`testGetFromSupplier` (测试 `Functions.get` / 通过 run/call 间接测试 Supplier 语义)
- 新增测试方法：`testAsSupplier` (测试 `Functions.asSupplier`，校验 Supplier 包装异常的转换)
- 需要调整 import：添加 `java.util.concurrent.Callable`、`java.util.function.BiConsumer`、`java.util.function.BiFunction`、`java.util.function.Consumer`、`java.util.function.Function`、`java.util.function.Supplier`、`org.apache.commons.lang3.Functions.FailableBiConsumer`、`org.apache.commons.lang3.Functions.FailableBiFunction`、`org.apache.commons.lang3.Functions.FailableCallable`、`org.apache.commons.lang3.Functions.FailableFunction`、`org.apache.commons.lang3.Functions.FailableSupplier` 以及静态导入 `assertFalse`。

```java
// IMPORTS_START
import java.io.IOException;
import java.io.UncheckedIOException;
import java.lang.reflect.UndeclaredThrowableException;
import java.util.concurrent.Callable;
import java.util.function.BiConsumer;
import java.util.function.BiFunction;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Supplier;

import org.apache.commons.lang3.Functions.FailableBiConsumer;
import org.apache.commons.lang3.Functions.FailableBiFunction;
import org.apache.commons.lang3.Functions.FailableCallable;
import org.apache.commons.lang3.Functions.FailableConsumer;
import org.apache.commons.lang3.Functions.FailableFunction;
import org.apache.commons.lang3.Functions.FailableSupplier;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
// IMPORTS_END

    @Test
    void testAsRunnable() {
        FailureOnOddInvocations.invocation = 0;
        Runnable runnable = Functions.asRunnable(() -> new FailureOnOddInvocations());
        UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () ->  runnable.run());
        final Throwable cause = e.getCause();
        assertNotNull(cause);
        assertTrue(cause instanceof SomeException);
        assertEquals("Odd Invocation: 1", cause.getMessage());

        // Even invocation, should not throw an exception
        runnable.run();
    }

    @Test
    void testAsCallable() {
        FailureOnOddInvocations.invocation = 0;
        final FailableCallable<FailureOnOddInvocations,SomeException> failableCallable = () -> { return new FailureOnOddInvocations(); };
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
        final FailableBiConsumer<Testable, Throwable, Throwable> failableBiConsumer = (t, th) -> { t.setThrowable(th); t.test(); }; 
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
        final FailableFunction<Throwable,Integer,Throwable> failableFunction = (th) -> {
        	testable.setThrowable(th);
        	return Integer.valueOf(testable.testInt());
        };
        final Function<Throwable,Integer> function = Functions.asFunction(failableFunction);
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
        final FailableBiFunction<Testable,Throwable,Integer,Throwable> failableBiFunction = (t, th) -> {
        	t.setThrowable(th);
        	return Integer.valueOf(t.testInt());
        };
        final BiFunction<Testable,Throwable,Integer> biFunction = Functions.asBiFunction(failableBiFunction);
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
        FailureOnOddInvocations.invocation = 0;
        UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () ->  Functions.run(FailureOnOddInvocations::new));
        final Throwable cause = e.getCause();
        assertNotNull(cause);
        assertTrue(cause instanceof SomeException);
        assertEquals("Odd Invocation: 1", cause.getMessage());
        final FailureOnOddInvocations instance = Functions.call(FailureOnOddInvocations::new);
        assertNotNull(instance);
    }

    @Test
    public void testAsSupplier() {
        FailureOnOddInvocations.invocation = 0;
        final FailableSupplier<FailureOnOddInvocations,Throwable> failableSupplier = () -> { return new FailureOnOddInvocations(); };
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