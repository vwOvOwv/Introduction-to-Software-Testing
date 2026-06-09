# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `58ba515e4b083f658ef2087df36284a9cd539b31`
- B: `5914a8e80a547301b76bf8ef691053e4dfc901a7`
- test: `src/test/java/org/apache/commons/lang3/concurrent/TimedSemaphoreTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/TimedSemaphore.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `27794`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6363, 'completion_tokens': 703, 'total_tokens': 7066}`

---

- 新增 `testShutdownWakesBlockedAcquireThreads`：覆盖 `shutdown()` 新增 `notifyAll()` 后必须唤醒阻塞在 `acquire()` 中线程，并验证 `acquire()` 被唤醒后因 shutdown 抛出 `IllegalStateException`。
- 调整 import：新增静态导入 `assertTimeoutPreemptively`，用于防止该并发回归测试在失败实现上挂起。

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

    /**
     * TimedSemaphore.shutdown() must wake threads blocked in acquire().
     */
    @Test
    public void testShutdownWakesBlockedAcquireThreads() {
        assertTimeoutPreemptively(Duration.ofSeconds(10), () -> {
            final TimedSemaphore sem = TimedSemaphore.builder().setPeriod(60).setTimeUnit(TimeUnit.SECONDS).setLimit(1).get();
            sem.acquire();

            final Thread blocker = new Thread(() -> {
                try {
                    sem.acquire();
                } catch (final InterruptedException e) {
                    Thread.currentThread().interrupt();
                } catch (final IllegalStateException e) {
                    // Expected after shutdown wakes the blocked acquire().
                }
            }, "testShutdownWakesBlockedAcquireThreads");

            blocker.setDaemon(true);
            blocker.start();

            final long parkDeadline = System.nanoTime() + Duration.ofSeconds(2).toNanos();
            while (System.nanoTime() < parkDeadline && blocker.getState() != Thread.State.WAITING) {
                Thread.sleep(10);
            }

            sem.shutdown();

            blocker.join(5000);
            assertFalse(blocker.isAlive(), "TimedSemaphore.shutdown() failed to wake thread blocked in acquire(): blocker still alive in state="
                    + blocker.getState() + " 5s after shutdown().");
        });
    }
```