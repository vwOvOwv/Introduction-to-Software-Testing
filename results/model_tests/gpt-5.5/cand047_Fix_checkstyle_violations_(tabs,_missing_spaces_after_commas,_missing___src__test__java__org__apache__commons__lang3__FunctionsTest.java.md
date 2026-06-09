# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `102a6d75650b7578e31bf18b840e0b613e83e439`
- B: `26bc45fdeeeda2bee38cc2a08ce99e41fd48e0d6`
- test: `src/test/java/org/apache/commons/lang3/FunctionsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Functions.java']`
- old_test_mode: `methods`
- user_chars: `24236`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6305, 'completion_tokens': 2951, 'total_tokens': 9256}`

---

- 修改 `testAsCallable`：生产代码仅调整泛型空格/Javadoc，测试同步格式化 lambda 与缩进，断言不变。
- 修改 `testAsConsumer`：生产代码仅格式化 `asConsumer`，测试去除尾随空格，断言不变。
- 修改 `testAsBiConsumer`：生产代码仅格式化 `asBiConsumer`，测试同步展开 lambda，断言不变。
- 修改 `testAsFunction`：生产代码仅格式化泛型声明，测试同步泛型空格与缩进，断言不变。
- 修改 `testAsBiFunction`：生产代码仅格式化泛型声明，测试同步泛型空格与缩进，断言不变。
- 修改 `testAsSupplier`：生产代码仅格式化泛型声明，测试同步展开 lambda，断言不变。
- 需要调整 import：删除未使用的 `assertFalse` 静态导入。

```java
// IMPORTS_START
import java.io.IOException;
import java.io.UncheckedIOException;
import java.lang.reflect.UndeclaredThrowableException;
import java.util.concurrent.Callable;
import java.util.function.BiConsumer;
import java.util.function.BiFunction;
import java.util.function.BiPredicate;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.Supplier;

import org.apache.commons.lang3.Functions.FailableBiConsumer;
import org.apache.commons.lang3.Functions.FailableBiFunction;
import org.apache.commons.lang3.Functions.FailableBiPredicate;
import org.apache.commons.lang3.Functions.FailableCallable;
import org.apache.commons.lang3.Functions.FailableConsumer;
import org.apache.commons.lang3.Functions.FailableFunction;
import org.apache.commons.lang3.Functions.FailablePredicate;
import org.apache.commons.lang3.Functions.FailableRunnable;
import org.apache.commons.lang3.Functions.FailableSupplier;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
// IMPORTS_END

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