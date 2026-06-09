# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `496506dedda231ceaecb81d62bb611889ba38be9`
- B: `809e2bed22f02264e0ac58bba070f6d84386cfc5`
- test: `src/test/java/org/apache/commons/lang3/concurrent/TimedSemaphoreTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/TimedSemaphore.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `29111`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7104, 'completion_tokens': 1619, 'total_tokens': 8723, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1051}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 6720}`

---

- 新增 `testTryAcquire` 和 `testTryAcquireAfterShutdown` 两个 `@Test` 方法，用于测试生产代码新增的 `tryAcquire()` 非阻塞获取许可的行为。
- 新增内部类 `TryAcquireThread` 以支持 `tryAcquire` 多线程测试。
- 无需新增或调整任何 import 语句，现有 import 已满足要求。

```java
/**
 * Tests the tryAcquire() method. It is checked whether the semaphore can be acquired
 * by a bunch of threads the expected number of times and not more.
 */
@Test
public void testTryAcquire() throws InterruptedException {
    final TimedSemaphore semaphore = new TimedSemaphore(PERIOD, TimeUnit.SECONDS,
            LIMIT);
    TryAcquireThread[] threads = new TryAcquireThread[3 * LIMIT];
    CountDownLatch latch = new CountDownLatch(1);
    for (int i = 0; i < threads.length; i++) {
        threads[i] = new TryAcquireThread(semaphore, latch);
        threads[i].start();
    }

    latch.countDown();
    int permits = 0;
    for (TryAcquireThread t : threads) {
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

    public TryAcquireThread(TimedSemaphore s, CountDownLatch l) {
        semaphore = s;
        latch = l;
    }

    @Override
    public void run() {
        try {
            if (latch.await(10, TimeUnit.SECONDS)) {
                acquired = semaphore.tryAcquire();
            }
        } catch (InterruptedException iex) {
            // ignore
        }
    }
}
```