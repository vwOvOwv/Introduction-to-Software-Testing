# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `1441ba9f3cd172ccfbd2d0c2ce336f4a9750a0a2`
- B: `df3e2715f41263d8998b7350301d106967748c0e`
- test: `src/test/java/org/apache/commons/lang3/concurrent/TimedSemaphoreTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/TimedSemaphore.java']`
- old_test_mode: `methods`
- user_chars: `32589`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 8136, 'completion_tokens': 3552, 'total_tokens': 11688, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 7880}`

---

- 新增 `import java.util.function.Supplier;` 因为 `TimedSemaphore.Builder` 实现了 `Supplier<TimedSemaphore>` 接口。
- 修改 `testAcquireLimit` 方法：将 `new TimedSemaphore(service, PERIOD_MILLIS, UNIT, 1)` 替换为 `TimedSemaphore.builder().setService(service).setPeriod(PERIOD_MILLIS).setTimeUnit(UNIT).setLimit(1).get()`，因为生产代码中公共构造函数已委托给 `builder()`。
- 修改 `testAcquireMultiplePeriods` 方法：将 `new TimedSemaphoreTestImpl(PERIOD_MILLIS / 10, TimeUnit.MILLISECONDS, 1)` 替换为 `new TimedSemaphoreTestImpl(PERIOD_MILLIS / 10, TimeUnit.MILLISECONDS, 1)`（无变化，但需确认构造函数签名不变）。
- 修改 `testAcquireMultipleThreads` 方法：将 `new TimedSemaphoreTestImpl(service, PERIOD_MILLIS, UNIT, 1)` 替换为 `new TimedSemaphoreTestImpl(service, PERIOD_MILLIS, UNIT, 1)`（无变化）。
- 修改 `testAcquireNoLimit` 方法：将 `new TimedSemaphoreTestImpl(service, PERIOD_MILLIS, UNIT, TimedSemaphore.NO_LIMIT)` 替换为 `new TimedSemaphoreTestImpl(service, PERIOD_MILLIS, UNIT, TimedSemaphore.NO_LIMIT)`（无变化）。
- 修改 `testGetAvailablePermits` 方法：将 `new TimedSemaphore(service, PERIOD_MILLIS, UNIT, LIMIT)` 替换为 `TimedSemaphore.builder().setService(service).setPeriod(PERIOD_MILLIS).setTimeUnit(UNIT).setLimit(LIMIT).get()`。
- 修改 `testGetAverageCallsPerPeriod` 方法：将 `new TimedSemaphore(service, PERIOD_MILLIS, UNIT, LIMIT)` 替换为 `TimedSemaphore.builder().setService(service).setPeriod(PERIOD_MILLIS).setTimeUnit(UNIT).setLimit(LIMIT).get()`。
- 修改 `testInit` 方法：将 `new TimedSemaphore(service, PERIOD_MILLIS, UNIT, LIMIT)` 替换为 `TimedSemaphore.builder().setService(service).setPeriod(PERIOD_MILLIS).setTimeUnit(UNIT).setLimit(LIMIT).get()`。
- 修改 `testInitDefaultService` 方法：将 `new TimedSemaphore(PERIOD_MILLIS, UNIT, LIMIT)` 替换为 `TimedSemaphore.builder().setPeriod(PERIOD_MILLIS).setTimeUnit(UNIT).setLimit(LIMIT).get()`。
- 修改 `testShutdownMultipleTimes` 方法：将 `new TimedSemaphoreTestImpl(service, PERIOD_MILLIS, UNIT, LIMIT)` 替换为 `new TimedSemaphoreTestImpl(service, PERIOD_MILLIS, UNIT, LIMIT)`（无变化）。
- 修改 `testShutdownSharedExecutorNoTask` 方法：将 `new TimedSemaphore(service, PERIOD_MILLIS, UNIT, LIMIT)` 替换为 `TimedSemaphore.builder().setService(service).setPeriod(PERIOD_MILLIS).setTimeUnit(UNIT).setLimit(LIMIT).get()`。
- 修改 `testShutdownSharedExecutorTask` 方法：将 `new TimedSemaphoreTestImpl(service, PERIOD_MILLIS, UNIT, LIMIT)` 替换为 `new TimedSemaphoreTestImpl(service, PERIOD_MILLIS, UNIT, LIMIT)`（无变化）。
- 修改 `testStartTimer` 方法：将 `new TimedSemaphoreTestImpl(PERIOD_MILLIS, UNIT, LIMIT)` 替换为 `new TimedSemaphoreTestImpl(PERIOD_MILLIS, UNIT, LIMIT)`（无变化）。
- 修改 `testTryAcquire` 方法：将 `new TimedSemaphore(PERIOD_MILLIS, TimeUnit.SECONDS, LIMIT)` 替换为 `TimedSemaphore.builder().setPeriod(PERIOD_MILLIS).setTimeUnit(TimeUnit.SECONDS).setLimit(LIMIT).get()`。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;

import org.apache.commons.lang3.ThreadUtils;
import org.easymock.EasyMock;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    void testAcquireLimit() throws InterruptedException {
        final ScheduledExecutorService service = EasyMock.createMock(ScheduledExecutorService.class);
        final ScheduledFuture<?> future = EasyMock.createMock(ScheduledFuture.class);
        prepareStartTimer(service, future);
        EasyMock.replay(service, future);
        final int count = 10;
        final CountDownLatch latch = new CountDownLatch(count - 1);
        final TimedSemaphore semaphore = TimedSemaphore.builder().setService(service).setPeriod(PERIOD_MILLIS).setTimeUnit(UNIT).setLimit(1).get();
        final SemaphoreThread t = new SemaphoreThread(semaphore, latch, count, count - 1);
        semaphore.setLimit(count - 1);
        t.start();
        latch.await();
        assertEquals(count - 1, semaphore.getAcquireCount(), "Wrong semaphore count");
        semaphore.endOfPeriod();
        t.join();
        assertEquals(1, semaphore.getAcquireCount(), "Wrong semaphore count (2)");
        assertEquals(count - 1, semaphore.getLastAcquiresPerPeriod(), "Wrong acquire() count");
        EasyMock.verify(service, future);
    }

    @Test
    void testAcquireMultiplePeriods() throws InterruptedException {
        final int count = 1000;
        final TimedSemaphoreTestImpl semaphore = new TimedSemaphoreTestImpl(PERIOD_MILLIS / 10, TimeUnit.MILLISECONDS, 1);
        semaphore.setLimit(count / 4);
        final CountDownLatch latch = new CountDownLatch(count);
        final SemaphoreThread t = new SemaphoreThread(semaphore, latch, count, count);
        t.start();
        latch.await();
        semaphore.shutdown();
        assertTrue(semaphore.getPeriodEnds() > 0, "End of period not reached");
    }

    @Test
    void testAcquireMultipleThreads() throws InterruptedException {
        final ScheduledExecutorService service = EasyMock.createMock(ScheduledExecutorService.class);
        final ScheduledFuture<?> future = EasyMock.createMock(ScheduledFuture.class);
        prepareStartTimer(service, future);
        EasyMock.replay(service, future);
        final TimedSemaphoreTestImpl semaphore = new TimedSemaphoreTestImpl(service, PERIOD_MILLIS, UNIT, 1);
        semaphore.latch = new CountDownLatch(1);
        final int count = 10;
        final SemaphoreThread[] threads = new SemaphoreThread[count];
        for (int i = 0; i < count; i++) {
            threads[i] = new SemaphoreThread(semaphore, null, 1, 0);
            threads[i].start();
        }
        for (int i = 0; i < count; i++) {
            semaphore.latch.await();
            assertEquals(1, semaphore.getAcquireCount(), "Wrong count");
            semaphore.latch = new CountDownLatch(1);
            semaphore.endOfPeriod();
            assertEquals(1, semaphore.getLastAcquiresPerPeriod(), "Wrong acquire count");
        }
        for (int i = 0; i < count; i++) {
            threads[i].join();
        }
        EasyMock.verify(service, future);
    }

    @Test
    void testAcquireNoLimit() throws InterruptedException {
        final ScheduledExecutorService service = EasyMock.createMock(ScheduledExecutorService.class);
        final ScheduledFuture<?> future = EasyMock.createMock(ScheduledFuture.class);
        prepareStartTimer(service, future);
        EasyMock.replay(service, future);
        final TimedSemaphoreTestImpl semaphore = new TimedSemaphoreTestImpl(service, PERIOD_MILLIS, UNIT, TimedSemaphore.NO_LIMIT);
        final int count = 1000;
        final CountDownLatch latch = new CountDownLatch(count);
        final SemaphoreThread t = new SemaphoreThread(semaphore, latch, count, count);
        t.start();
        latch.await();
        EasyMock.verify(service, future);
    }

    @Test
    void testGetAvailablePermits() throws InterruptedException {
        final ScheduledExecutorService service = EasyMock.createMock(ScheduledExecutorService.class);
        final ScheduledFuture<?> future = EasyMock.createMock(ScheduledFuture.class);
        prepareStartTimer(service, future);
        EasyMock.replay(service, future);
        final TimedSemaphore semaphore = TimedSemaphore.builder().setService(service).setPeriod(PERIOD_MILLIS).setTimeUnit(UNIT).setLimit(LIMIT).get();
        for (int i = 0; i < LIMIT; i++) {
            assertEquals(LIMIT - i, semaphore.getAvailablePermits(), "Wrong available count at " + i);
            semaphore.acquire();
        }
        semaphore.endOfPeriod();
        assertEquals(LIMIT, semaphore.getAvailablePermits(), "Wrong available count in new period");
        EasyMock.verify(service, future);
    }

    @Test
    void testGetAverageCallsPerPeriod() throws InterruptedException {
        final ScheduledExecutorService service = EasyMock.createMock(ScheduledExecutorService.class);
        final ScheduledFuture<?> future = EasyMock.createMock(ScheduledFuture.class);
        prepareStartTimer(service, future);
        EasyMock.replay(service, future);
        final TimedSemaphore semaphore = TimedSemaphore.builder().setService(service).setPeriod(PERIOD_MILLIS).setTimeUnit(UNIT).setLimit(LIMIT).get();
        semaphore.acquire();
        semaphore.endOfPeriod();
        assertEquals(1.0, semaphore.getAverageCallsPerPeriod(), .005, "Wrong average (1)");
        semaphore.acquire();
        semaphore.acquire();
        semaphore.endOfPeriod();
        assertEquals(1.5, semaphore.getAverageCallsPerPeriod(), .005, "Wrong average (2)");
        EasyMock.verify(service, future);
    }

    @Test
    void testInit() {
        final ScheduledExecutorService service = EasyMock.createMock(ScheduledExecutorService.class);
        EasyMock.replay(service);
        final TimedSemaphore semaphore = TimedSemaphore.builder().setService(service).setPeriod(PERIOD_MILLIS).setTimeUnit(UNIT).setLimit(LIMIT).get();
        EasyMock.verify(service);
        assertEquals(service, semaphore.getExecutorService(), "Wrong service");
        assertEquals(PERIOD_MILLIS, semaphore.getPeriod(), "Wrong period");
        assertEquals(UNIT, semaphore.getUnit(), "Wrong unit");
        assertEquals(0, semaphore.getLastAcquiresPerPeriod(), "Statistic available");
        assertEquals(0.0, semaphore.getAverageCallsPerPeriod(), .05, "Average available");
        assertFalse(semaphore.isShutdown(), "Already shutdown");
        assertEquals(LIMIT, semaphore.getLimit(), "Wrong limit");
    }

    @Test
    void testInitDefaultService() {
        final TimedSemaphore semaphore = TimedSemaphore.builder().setPeriod(PERIOD_MILLIS).setTimeUnit(UNIT).setLimit(LIMIT).get();
        final ScheduledThreadPoolExecutor exec = (ScheduledThreadPoolExecutor) semaphore.getExecutorService();
        assertFalse(exec.getContinueExistingPeriodicTasksAfterShutdownPolicy(), "Wrong periodic task policy");
        assertFalse(exec.getExecuteExistingDelayedTasksAfterShutdownPolicy(), "Wrong delayed task policy");
        assertFalse(exec.isShutdown(), "Already shutdown");
        semaphore.shutdown();
    }

    @Test
    void testShutdownMultipleTimes() throws InterruptedException {
        final ScheduledExecutorService service = EasyMock.createMock(ScheduledExecutorService.class);
        final ScheduledFuture<?> future = EasyMock.createMock(ScheduledFuture.class);
        prepareStartTimer(service, future);
        EasyMock.expect(Boolean.valueOf(future.cancel(false))).andReturn(Boolean.TRUE);
        EasyMock.replay(service, future);
        final TimedSemaphoreTestImpl semaphore = new TimedSemaphoreTestImpl(service, PERIOD_MILLIS, UNIT, LIMIT);
        semaphore.acquire();
        for (int i = 0; i < 10; i++) {
            semaphore.shutdown();
        }
        EasyMock.verify(service, future);
    }

    @Test
    void testShutdownSharedExecutorNoTask() {
        final ScheduledExecutorService service = EasyMock.createMock(ScheduledExecutorService.class);
        EasyMock.replay(service);
        final TimedSemaphore semaphore = TimedSemaphore.builder().setService(service).setPeriod(PERIOD_MILLIS).setTimeUnit(UNIT).setLimit(LIMIT).get();
        semaphore.shutdown();
        assertTrue(semaphore.isShutdown(), "Not shutdown");
        EasyMock.verify(service);
    }

    @Test
    void testShutdownSharedExecutorTask() throws InterruptedException {
        final ScheduledExecutorService service = EasyMock.createMock(ScheduledExecutorService.class);
        final ScheduledFuture<?> future = EasyMock.createMock(ScheduledFuture.class);
        prepareStartTimer(service, future);
        EasyMock.expect(Boolean.valueOf(future.cancel(false))).andReturn(Boolean.TRUE);
        EasyMock.replay(service, future);
        final TimedSemaphoreTestImpl semaphore = new TimedSemaphoreTestImpl(service, PERIOD_MILLIS, UNIT, LIMIT);
        semaphore.acquire();
        semaphore.shutdown();
        assertTrue(semaphore.isShutdown(), "Not shutdown");
        EasyMock.verify(service, future);
    }

    @Test
    void testStartTimer() throws InterruptedException {
        final TimedSemaphoreTestImpl semaphore = new TimedSemaphoreTestImpl(PERIOD_MILLIS, UNIT, LIMIT);
        final ScheduledFuture<?> future = semaphore.startTimer();
        assertNotNull(future, "No future returned");
        ThreadUtils.sleepQuietly(DURATION);
        final int trials = 10;
        int count = 0;
        do {
            Thread.sleep(PERIOD_MILLIS);
            assertFalse(count++ > trials, "endOfPeriod() not called!");
        } while (semaphore.getPeriodEnds() <= 0);
        semaphore.shutdown();
    }

    @Test
    void testTryAcquire() throws InterruptedException {
        final TimedSemaphore semaphore = TimedSemaphore.builder().setPeriod(PERIOD_MILLIS).setTimeUnit(TimeUnit.SECONDS).setLimit(LIMIT).get();
        final TryAcquireThread[] threads = new TryAcquireThread[3 * LIMIT];
        final CountDownLatch latch = new CountDownLatch(1);
        for (int i = 0; i < threads.length; i++) {
            threads[i] = new TryAcquireThread(semaphore, latch);
            threads[i].start();
        }
        latch.countDown();
        int permits = 0;
        for (final TryAcquireThread t : threads) {
            t.join();
            if (t.acquired) {
                permits++;
            }
        }
        assertEquals(LIMIT, permits, "Wrong number of permits granted");
    }
```