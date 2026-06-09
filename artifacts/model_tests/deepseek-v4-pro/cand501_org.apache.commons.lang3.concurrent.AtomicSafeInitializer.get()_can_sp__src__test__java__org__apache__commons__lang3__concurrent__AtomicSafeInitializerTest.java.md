# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `5019152951ad0d9fe65961b5f6e0d1527f876bd5`
- B: `0f211efaf1228c3371b2a81de095661a94907f5e`
- test: `src/test/java/org/apache/commons/lang3/concurrent/AtomicSafeInitializerTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/AtomicSafeInitializer.java']`
- old_test_mode: `methods`
- user_chars: `7574`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2088, 'completion_tokens': 3448, 'total_tokens': 5536, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2895}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1704}`

---

- 新增两个 @ParameterizedTest 方法 `testInitializerThrowsChecked` 和 `testInitializerThrowsUnchecked`，用于验证生产代码中 `get()` 在初始器抛出受检/非受检异常时的行为。
- 新增相关 import 语句以支持参数化测试、超时控制、断言异常和 `ExceptionUtils` 工具类。
- 现有方法 `testGetThatReturnsNullFirstTime` 无需修改，其行为与新生产代码兼容。

```java
import static org.junit.jupiter.api.Assertions.assertThrows;
import java.io.IOException;
import java.nio.file.FileSystemException;
import java.util.concurrent.TimeUnit;
import org.apache.commons.lang3.exception.ExceptionUtils;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.api.Timeout.ThreadMode;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

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