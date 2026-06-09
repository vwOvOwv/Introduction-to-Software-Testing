# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `58ba515e4b083f658ef2087df36284a9cd539b31`
- B: `5914a8e80a547301b76bf8ef691053e4dfc901a7`
- test: `src/test/java/org/apache/commons/lang3/concurrent/TimedSemaphoreTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/TimedSemaphore.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `27794`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6815, 'completion_tokens': 2771, 'total_tokens': 9586, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2225}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 6431}`

---

- 新增 `@Test` 方法 `testShutdownWakesBlockedAcquireThreads`，验证 `shutdown()` 调用 `notifyAll()` 能唤醒阻塞在 `acquire()` 的线程并抛出 `IllegalStateException` 或正常终止。
- 新增 import 语句 `import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;`，用于新测试的超时断言。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
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