# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `5019152951ad0d9fe65961b5f6e0d1527f876bd5`
- B: `0f211efaf1228c3371b2a81de095661a94907f5e`
- test: `src/test/java/org/apache/commons/lang3/concurrent/AtomicSafeInitializerTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/AtomicSafeInitializer.java']`
- old_test_mode: `methods`
- user_chars: `7574`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1995, 'completion_tokens': 1108, 'total_tokens': 3103}`

---

- 新增 `testInitializerThrowsChecked`，覆盖 `AtomicSafeInitializer.get()` 在初始化抛出受检异常时会释放 factory、包装为 `ConcurrentException` 且可再次重试。
- 新增 `testInitializerThrowsUnchecked`，覆盖初始化抛出运行时异常时按原异常类型重新抛出且可再次重试。
- 需要调整 import：新增 `assertThrows`、异常类型、`TimeUnit`、`ExceptionUtils`、`Timeout`、参数化测试相关 import。

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