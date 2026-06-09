# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `496506dedda231ceaecb81d62bb611889ba38be9`
- B: `809e2bed22f02264e0ac58bba070f6d84386cfc5`
- test: `src/test/java/org/apache/commons/lang3/concurrent/TimedSemaphoreTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/TimedSemaphore.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `29111`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6673, 'completion_tokens': 660, 'total_tokens': 7333}`

---

- 新增 `testTryAcquire`，对应生产代码新增的非阻塞 `TimedSemaphore.tryAcquire()`，验证并发竞争时最多只授予 `LIMIT` 个许可；无需调整 import。
- 新增 `testTryAcquireAfterShutdown`，对应 `tryAcquire()` 复用 `prepareAcquire()` 后在 shutdown 状态抛出 `IllegalStateException` 的行为；无需调整 import。
- 新增内部辅助类 `TryAcquireThread`，用于 `testTryAcquire` 并发调用 `tryAcquire()`；无需调整 import。

```java
    /**
     * Tests the tryAcquire() method. It is checked whether the semaphore can be acquired
     * by a bunch of threads the expected number of times and not more.
     */
    @Test
    public void testTryAcquire() throws InterruptedException {
        final TimedSemaphore semaphore = new TimedSemaphore(PERIOD, TimeUnit.SECONDS,
                LIMIT);
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
        assertEquals("Wrong number of permits granted", LIMIT, permits);
    }

    /**
     * Tries to call tryAcquire() after shutdown(). This should cause an exception.
     */
    @Test(expected = IllegalStateException.class)
    public void testTryAcquireAfterShutdown() {
        final TimedSemaphore semaphore = new TimedSemaphore(PERIOD, UNIT, LIMIT);
        semaphore.shutdown();
        semaphore.tryAcquire();
    }

    /**
     * A test thread class which invokes {@code tryAcquire()} on the test semaphore and
     * records the return value.
     */
    private static class TryAcquireThread extends Thread {
        /** The semaphore. */
        private final TimedSemaphore semaphore;

        /** A latch for communication with the main thread. */
        private final CountDownLatch latch;

        /** Flag whether a permit could be acquired. */
        private boolean acquired;

        public TryAcquireThread(final TimedSemaphore s, final CountDownLatch l) {
            semaphore = s;
            latch = l;
        }

        @Override
        public void run() {
            try {
                if (latch.await(10, TimeUnit.SECONDS)) {
                    acquired = semaphore.tryAcquire();
                }
            } catch (final InterruptedException iex) {
                // ignore
            }
        }
    }
```