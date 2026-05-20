# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `5019152951ad0d9fe65961b5f6e0d1527f876bd5`
- B: `0f211efaf1228c3371b2a81de095661a94907f5e`
- test: `src/test/java/org/apache/commons/lang3/concurrent/AtomicSafeInitializerTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/AtomicSafeInitializer.java']`
- old_test_mode: `methods`
- user_chars: `7857`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2150, 'completion_tokens': 821, 'total_tokens': 2971, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 1894}`

---

- 新增 `testInitializerThrowsChecked` 和 `testInitializerThrowsUnchecked` 两个 `@ParameterizedTest` 方法，对应生产代码中 `get()` 方法新增的异常处理逻辑（捕获 `Throwable` 并重新抛出）。
- 修改 `testGetThatReturnsNullFirstTime` 方法，移除 `throws ConcurrentException` 声明（因为生产代码中 `get()` 不再抛出该异常，而是内部处理）。
- 新增 import：`java.io.IOException`、`java.nio.file.FileSystemException`、`java.util.concurrent.TimeUnit`、`org.apache.commons.lang3.exception.ExceptionUtils`、`org.junit.jupiter.api.Timeout`、`org.junit.jupiter.api.Timeout.ThreadMode`、`org.junit.jupiter.params.ParameterizedTest`、`org.junit.jupiter.params.provider.ValueSource`，以及 `assertThrows` 静态导入。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.IOException;
import java.nio.file.FileSystemException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

import org.apache.commons.lang3.exception.ExceptionUtils;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.api.Timeout.ThreadMode;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
// IMPORTS_END

    @Test
    void testGetThatReturnsNullFirstTime() {
        final AtomicSafeInitializer<Object> initializer = new AtomicSafeInitializer<Object>() {
            final AtomicBoolean firstRun = new AtomicBoolean(true);

            @Override
            protected Object initialize() {
                if (firstRun.getAndSet(false)) {
                    return null;
                }
                return new Object();
            }
        };

        assertNull(initializer.get());
        assertNull(initializer.get());
    }

    @ParameterizedTest
    @ValueSource(classes = { IOException.class, Exception.class, FileSystemException.class, ReflectiveOperationException.class, ConcurrentException.class })
    @Timeout(value = 5, unit = TimeUnit.SECONDS, threadMode = ThreadMode.SAME_THREAD)
    void testInitializerThrowsChecked(final Class<Exception> throwableClass) throws ConcurrentException {
        final String message = "Initializing";
        final AtomicSafeInitializer<Object> asi = AtomicSafeInitializer.builder().setInitializer(() -> {
            throw throwableClass.getConstructor(String.class).newInstance(message);
        }).get();
        final String expected = throwableClass.getSimpleName() + ": " + message;
        assertEquals(expected, ExceptionUtils.getRootCauseMessage(assertThrows(ConcurrentException.class, asi::get)));
        assertEquals(expected, ExceptionUtils.getRootCauseMessage(assertThrows(ConcurrentException.class, asi::get)));
    }

    @ParameterizedTest
    @ValueSource(classes = { IllegalStateException.class, IllegalArgumentException.class, NullPointerException.class, RuntimeException.class })
    @Timeout(value = 5, unit = TimeUnit.SECONDS, threadMode = ThreadMode.SAME_THREAD)
    void testInitializerThrowsUnchecked(final Class<Exception> throwableClass) throws ConcurrentException {
        final String message = "Initializing";
        final AtomicSafeInitializer<Object> asi = AtomicSafeInitializer.builder().setInitializer(() -> {
            throw throwableClass.getConstructor(String.class).newInstance(message);
        }).get();
        assertEquals(message, assertThrows(throwableClass, asi::get).getMessage());
        assertEquals(message, assertThrows(throwableClass, asi::get).getMessage());
    }
```