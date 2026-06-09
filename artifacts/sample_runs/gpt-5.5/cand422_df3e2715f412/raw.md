# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `1441ba9f3cd172ccfbd2d0c2ce336f4a9750a0a2`
- B: `df3e2715f41263d8998b7350301d106967748c0e`
- test: `src/test/java/org/apache/commons/lang3/concurrent/TimedSemaphoreTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/TimedSemaphore.java']`
- old_test_mode: `methods`
- user_chars: `32313`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7397, 'completion_tokens': 2626, 'total_tokens': 10023}`

---

- 修改 `testAcquireLimit`：对应测试 diff 仅将 EasyMock 创建与构造调用整理为单行，生产构造器仍委托 builder 后保持相同行为；无需调整 import。
- 修改 `testAcquireMultiplePeriods`：对应测试 diff 仅格式化 `TimedSemaphoreTestImpl` 构造调用；无需调整 import。
- 修改 `testAcquireMultipleThreads`：对应测试 diff 仅格式化 mock 创建与构造调用；无需调整 import。
- 修改 `testAcquireNoLimit`：对应测试 diff 仅格式化 mock 创建与构造调用；无需调整 import。
- 修改 `testGetAvailablePermits`：对应测试 diff 仅格式化 mock 创建与构造调用；无需调整 import。
- 修改 `testGetAverageCallsPerPeriod`：对应测试 diff 仅格式化 mock 创建与构造调用；无需调整 import。
- 修改 `testInit`：对应测试 diff 仅格式化 mock 创建与构造调用；无需调整 import。
- 修改 `testInitDefaultService`：对应测试 diff 仅格式化 executor 获取语句；无需调整 import。
- 修改 `testShutdownMultipleTimes`：对应测试 diff 仅格式化 mock 创建与构造调用；无需调整 import。
- 修改 `testShutdownSharedExecutorNoTask`：对应测试 diff 仅格式化 mock 创建与构造调用；无需调整 import。
- 修改 `testShutdownSharedExecutorTask`：对应测试 diff 仅格式化 mock 创建与构造调用；无需调整 import。
- 修改 `testStartTimer`：对应测试 diff 仅格式化 `TimedSemaphoreTestImpl` 构造调用；无需调整 import。
- 修改 `testTryAcquire`：对应测试 diff 仅格式化 `TimedSemaphore` 构造调用并移除空行；无需调整 import。

```java
    @Test
    void testAcquireLimit() throws InterruptedException {
        final ScheduledExecutorService service = EasyMock.createMock(ScheduledExecutorService.class);
        final ScheduledFuture<?> future = EasyMock.createMock(ScheduledFuture.class);
        prepareStartTimer(service, future);
        EasyMock.replay(service, future);
        final int count = 10;
        final CountDownLatch latch = new CountDownLatch(count - 1);
        final TimedSemaphore semaphore = new TimedSemaphore(service, PERIOD_MILLIS, UNIT, 1);
        final SemaphoreThread t = new SemaphoreThread(semaphore, latch, count, count - 1);
        semaphore.setLimit(count - 1);
        // start a thread that calls the semaphore count times
        t.start();
        latch.await();
        // now the semaphore's limit should be reached and the thread blocked
        assertEquals(count - 1, semaphore.getAcquireCount(), "Wrong semaphore count");
        // this wakes up the thread, it should call the semaphore once more
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
        final TimedSemaphore semaphore = new TimedSemaphore(service, PERIOD_MILLIS, UNIT, LIMIT);
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
        final TimedSemaphore semaphore = new TimedSemaphore(service, PERIOD_MILLIS, UNIT, LIMIT);
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
        final TimedSemaphore semaphore = new TimedSemaphore(service, PERIOD_MILLIS, UNIT, LIMIT);
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
        final TimedSemaphore semaphore = new TimedSemaphore(PERIOD_MILLIS, UNIT, LIMIT);
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
        final TimedSemaphore semaphore = new TimedSemaphore(service, PERIOD_MILLIS, UNIT, LIMIT);
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
        final TimedSemaphore semaphore = new TimedSemaphore(PERIOD_MILLIS, TimeUnit.SECONDS, LIMIT);
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