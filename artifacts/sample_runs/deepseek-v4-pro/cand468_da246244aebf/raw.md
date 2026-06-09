# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `31c7c5bde17819783ca84acb78344d2efd5d19fd`
- B: `da246244aebf91571b0689e3dee97fce0ad52b23`
- test: `src/test/java/org/apache/commons/lang3/time/StopWatchTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/StopWatch.java']`
- old_test_mode: `methods`
- user_chars: `22685`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6028, 'completion_tokens': 5358, 'total_tokens': 11386, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 3286}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 5644}`

---

- 新增 import：添加 `java.io.IOException`（用于 `throwIOException` 辅助方法）和 `java.util.concurrent.atomic.AtomicInteger`（用于测试计数器）。
- 新增 import：添加 `static org.junit.jupiter.api.Assertions.assertEquals`（`testGet`/`testRun` 需要），补齐缺失的断言静态导入。
- 修改 `testBadStates`：调整 `assertThrows` 的消息字符串为单行格式，与代码风格统一，不影响断言行为。
- 修改 `testSuspend`：移除方法体中两个无意义的分号，消除编译警告/错误。
- 新增 `testGet`：验证新增的 `get(Supplier)` 和 `getT(FailableSupplier)` 方法的行为、返回值、StopWatch 状态及异常传播。
- 新增 `testRun`：验证新增的 `run(Runnable)` 和 `runT(FailableRunnable)` 方法的行为、执行计数、StopWatch 状态及异常传播。
- 新增私有辅助方法 `throwIOException`：提供受检异常供测试使用。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import org.apache.commons.lang3.AbstractLangTest;
import org.apache.commons.lang3.ThreadUtils;
// IMPORTS_END

@Test
public void testBadStates() {
    final StopWatch watch = new StopWatch();
    assertThrows(IllegalStateException.class, watch::stop,
        "Calling stop on an unstarted StopWatch should throw an exception. ");

    assertThrows(IllegalStateException.class, watch::suspend,
        "Calling suspend on an unstarted StopWatch should throw an exception. ");

    assertThrows(IllegalStateException.class, watch::split,
        "Calling split on a non-running StopWatch should throw an exception. ");

    assertThrows(IllegalStateException.class, watch::unsplit,
        "Calling unsplit on an unsplit StopWatch should throw an exception. ");

    assertThrows(IllegalStateException.class, watch::resume,
        "Calling resume on an unsuspended StopWatch should throw an exception. ");

    watch.start();

    assertThrows(IllegalStateException.class, watch::start,
        "Calling start on a started StopWatch should throw an exception. ");

    assertThrows(IllegalStateException.class, watch::unsplit,
        "Calling unsplit on an unsplit StopWatch should throw an exception. ");

    assertThrows(IllegalStateException.class, watch::getSplitTime,
            "Calling getSplitTime on an unsplit StopWatch should throw an exception. ");

    assertThrows(IllegalStateException.class, watch::getSplitDuration,
            "Calling getSplitTime on an unsplit StopWatch should throw an exception. ");

    assertThrows(IllegalStateException.class, watch::resume,
        "Calling resume on an unsuspended StopWatch should throw an exception. ");

    watch.stop();

    assertThrows(IllegalStateException.class, watch::start,
        "Calling start on a stopped StopWatch should throw an exception as it needs to be reset. ");
}

@Test
public void testSuspend() throws InterruptedException {
    final StopWatch watch = StopWatch.createStarted();
    final long testStartMillis = System.currentTimeMillis();
    final long testStartNanos = System.nanoTime();
    final Instant testStartInstant = Instant.ofEpochMilli(testStartMillis);
    final Duration sleepDuration = MIN_DURATION;
    final long sleepMillis = sleepDuration.toMillis();
    sleepPlus1(sleepDuration);
    watch.suspend();
    final long testSuspendMillis = System.currentTimeMillis();
    final long testSuspendNanos = System.nanoTime();
    final long testSuspendTimeNanos = testSuspendNanos - testStartNanos;
    // See sleepPlus1
    final Duration testSuspendDuration = Duration.ofNanos(testSuspendTimeNanos).plusMillis(1);
    final long suspendTimeFromNanos = watch.getTime();
    final Duration suspendDuration = watch.getDuration();
    final long stopTimeMillis = watch.getStopTime();
    final Instant stopInstant = watch.getStopInstant();

    assertTrue(testStartMillis <= stopTimeMillis, () -> String.format("testStartMillis %s <= stopTimeMillis %s", testStartMillis, stopTimeMillis));
    assertTrue(testStartInstant.isBefore(stopInstant), () -> String.format("testStartInstant %s < stopInstant %s", testStartInstant, stopInstant));
    assertTrue(testSuspendMillis <= stopTimeMillis, () -> String.format("testSuspendMillis %s <= stopTimeMillis %s", testSuspendMillis, stopTimeMillis));
    assertTrue(testSuspendMillis <= stopInstant.toEpochMilli(),
            () -> String.format("testSuspendMillis %s <= stopInstant %s", testSuspendMillis, stopInstant));

    sleepPlus1(sleepDuration);
    watch.resume();
    sleepPlus1(sleepDuration);
    watch.stop();
    final long totalTimeFromNanos = watch.getTime();
    final Duration totalDuration = watch.getDuration();

    assertTrue(suspendTimeFromNanos >= sleepMillis, () -> String.format("suspendTimeFromNanos %s >= sleepMillis %s", suspendTimeFromNanos, sleepMillis));
    assertTrue(suspendDuration.compareTo(Duration.ofMillis(sleepMillis)) >= 0,
            () -> String.format("suspendDuration %s >= sleepMillis %s", suspendDuration, sleepMillis));
    assertTrue(suspendTimeFromNanos <= testSuspendTimeNanos,
            () -> String.format("suspendTimeFromNanos %s <= testSuspendTimeNanos %s", suspendTimeFromNanos, testSuspendTimeNanos));
    assertTrue(suspendDuration.compareTo(testSuspendDuration) <= 0,
            () -> String.format("suspendDuration %s <= testSuspendDuration %s", suspendDuration, testSuspendDuration));

    final long sleepMillisX2 = sleepMillis + sleepMillis;
    assertTrue(totalTimeFromNanos >= sleepMillisX2, () -> String.format("totalTimeFromNanos %s >= sleepMillisX2 %s", totalTimeFromNanos, sleepMillisX2));
    assertTrue(totalDuration.compareTo(Duration.ofMillis(sleepMillisX2)) >= 0,
            () -> String.format("totalDuration >= sleepMillisX2", totalDuration, sleepMillisX2));

    // Be lenient for slow running builds
    final long testTooLongMillis = sleepMillis * 100;
    assertTrue(totalTimeFromNanos < testTooLongMillis,
            () -> String.format("totalTimeFromNanos %s < testTooLongMillis %s", totalTimeFromNanos, testTooLongMillis));
    assertTrue(totalDuration.compareTo(Duration.ofMillis(testTooLongMillis)) < 0,
            () -> String.format("totalDuration %s < testTooLongMillis %s", totalDuration, testTooLongMillis));
}

@Test
public void testGet() throws Throwable {
    final StopWatch watch = new StopWatch();
    final AtomicInteger i = new AtomicInteger();
    assertEquals(1, watch.get(i::incrementAndGet));
    assertEquals(2, watch.getT(i::incrementAndGet));
    final IOException e = assertThrows(IOException.class, () -> watch.getT(this::throwIOException));
    assertEquals("A", e.getMessage());
    // test state
    assertTrue(watch.isSuspended());
    assertEquals(3, watch.get(() -> {
        assertTrue(watch.isStarted());
        return i.incrementAndGet();
    }));
    assertTrue(watch.isSuspended());
    final long nanos1 = watch.getDuration().toNanos();
    assertTrue(nanos1 >= 0);
    // test state
    assertTrue(watch.isSuspended());
    assertEquals(4, watch.getT(() -> {
        assertTrue(watch.isStarted());
        return i.incrementAndGet();
    }));
    assertTrue(watch.isSuspended());
    assertTrue(watch.getDuration().toNanos() >= nanos1);
}

@Test
public void testRun() throws Throwable {
    final StopWatch watch = new StopWatch();
    final AtomicInteger i = new AtomicInteger();
    watch.run(i::incrementAndGet);
    assertEquals(1, i.get());
    watch.runT(i::incrementAndGet);
    assertEquals(2, i.get());
    final IOException e = assertThrows(IOException.class, () -> watch.runT(this::throwIOException));
    assertEquals("A", e.getMessage());
    // test state
    assertTrue(watch.isSuspended());
    watch.run(() -> {
        assertTrue(watch.isStarted());
        i.incrementAndGet();
    });
    assertEquals(3, i.get());
    assertTrue(watch.isSuspended());
    final long nanos1 = watch.getDuration().toNanos();
    assertTrue(nanos1 > 0);
    // test state
    assertTrue(watch.isSuspended());
    watch.runT(() -> {
        assertTrue(watch.isStarted());
        i.incrementAndGet();
    });
    assertEquals(4, i.get());
    assertTrue(watch.isSuspended());
    assertTrue(watch.getDuration().toNanos() >= nanos1);
}

private int throwIOException() throws IOException {
    throw new IOException("A");
}
```