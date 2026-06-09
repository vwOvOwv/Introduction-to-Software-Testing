# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `c42806cfa03979023e1a683edd0a221c51e6789c`
- B: `a32c188c32fd0c4a8149bcda524d704dd609da6e`
- test: `src/test/java/org/apache/commons/lang3/FunctionsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Functions.java']`
- old_test_mode: `methods`
- user_chars: `13185`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3715, 'completion_tokens': 1927, 'total_tokens': 5642}`

---

- 新增 `testAsPredicate`：覆盖 `asPredicate(FailablePredicate)` 现在通过 `test(...)` 委托后仍会把受检异常包装为 `UndeclaredThrowableException`。
- 新增 `testAsBiPredicate`：覆盖 `asBiPredicate(FailableBiPredicate)` 现在通过 `test(...)` 委托后仍会把受检异常包装为 `UndeclaredThrowableException`。
- 修改 `testAsSupplier`：仅将 supplier lambda 简化为表达式形式，与生产代码委托改造后的行为断言保持一致。
- 需要调整 import：新增 `DisplayName`、`BiPredicate`、`Predicate`，并保留现有断言与函数类型 import。

```java
// IMPORTS_START
import org.apache.commons.lang3.Functions.FailableBiConsumer;
import org.apache.commons.lang3.Functions.FailableBiFunction;
import org.apache.commons.lang3.Functions.FailableCallable;
import org.apache.commons.lang3.Functions.FailableConsumer;
import org.apache.commons.lang3.Functions.FailableFunction;
import org.apache.commons.lang3.Functions.FailableSupplier;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

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

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
// IMPORTS_END

    @Test
    @DisplayName("Test that asPredicate(FailablePredicate) is converted to -> Predicate ")
    public void testAsPredicate() {
        FailureOnOddInvocations.invocation = 0;
        final Functions.FailablePredicate<Object, Throwable> failablePredicate = t -> new FailureOnOddInvocations() != null;
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
        FailureOnOddInvocations.invocation = 0;
        final Functions.FailableBiPredicate<Object, Object, Throwable> failableBiPredicate = (t1, t2) -> new FailureOnOddInvocations() != null;
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
        FailureOnOddInvocations.invocation = 0;
        final FailableSupplier<FailureOnOddInvocations, Throwable> failableSupplier = () -> new FailureOnOddInvocations();
        final Supplier<FailureOnOddInvocations> supplier = Functions.asSupplier(failableSupplier);
        final UndeclaredThrowableException e = assertThrows(UndeclaredThrowableException.class, () ->  supplier.get());
        final Throwable cause = e.getCause();
        assertNotNull(cause);
        assertTrue(cause instanceof SomeException);
        assertEquals("Odd Invocation: 1", cause.getMessage());
        final FailureOnOddInvocations instance = supplier.get();
        assertNotNull(instance);
    }
```