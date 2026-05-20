# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `58ba515e4b083f658ef2087df36284a9cd539b31`
- B: `5914a8e80a547301b76bf8ef691053e4dfc901a7`
- test: `src/test/java/org/apache/commons/lang3/concurrent/TimedSemaphoreTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/TimedSemaphore.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `28070`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6877, 'completion_tokens': 726, 'total_tokens': 7603, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 6621}`

---

- 新增 `import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;` 以支持新测试方法中的超时断言。
- 新增 `@Test` 方法 `testShutdownWakesBlockedAcquireThreads`：对应生产代码中 `shutdown()` 添加 `notifyAll()` 和 `acquire()` 添加 `shutdown` 检查，测试 `shutdown()` 能唤醒阻塞在 `acquire()` 中的线程并抛出 `IllegalStateException`。

```java
// IMPORTS_START
import static org.apache.commons.lang3.LangAssertions.assertIllegalArgumentException;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

import org.apache.commons.lang3.AbstractLangTest;
import org.apache.commons.lang3.ThreadUtils;
import org.easymock.EasyMock;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    public void testShutdownWakesBlockedAcquireThreads() {
        assertTimeoutPreemptively(Duration.ofSeconds(10), () -> {
            // Period of 60s ensures endOfPeriod() does NOT fire during the test
            // window. The only way the blocker can wake is via shutdown() calling
            // notifyAll().
            final TimedSemaphore sem = TimedSemaphore.builder().setPeriod(60).setTimeUnit(TimeUnit.SECONDS).setLimit(1).get();
            sem.acquire(); // consume the only permit for this period.
            final Thread blocker = new Thread(() -> {
                try {
                    sem.acquire(); // limit=1 already taken => blocks in wait().
                } catch (final InterruptedException e) {
                    Thread.currentThread().interrupt();
                } catch (final IllegalStateException e) {
                    // Acceptable post-patch outcome: re-check of shutdown flag throws.
                }
            }, "testShutdownWakesBlockedAcquireThreads");
            blocker.setDaemon(true);
            blocker.start();
            // Wait until blocker is parked in Object.wait() inside acquire().
            final long parkDeadline = System.nanoTime() + Duration.ofSeconds(2).toNanos();
            while (System.nanoTime() < parkDeadline && blocker.getState() != Thread.State.WAITING) {
                Thread.sleep(10);
            }
            sem.shutdown();
            // At HEAD (patched): blocker wakes from notifyAll(), re-checks flag,
            // throws ISE, and terminates within milliseconds.
            // At baseline: blocker stays in WAITING for 60s — well past this join.
            blocker.join(5000);
            assertFalse(blocker.isAlive(), "TimedSemaphore.shutdown() failed to wake thread blocked in acquire(): blocker still alive in state="
                    + blocker.getState() + " 5s after shutdown(). Bug present (shutdown() does not call notifyAll()).");
        });
    }
```