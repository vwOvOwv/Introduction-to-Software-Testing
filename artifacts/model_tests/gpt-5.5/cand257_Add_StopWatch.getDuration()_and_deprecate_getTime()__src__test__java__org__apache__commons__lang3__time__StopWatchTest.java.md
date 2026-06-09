# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `3ebd20002ef35b690ee0314bac254013df3f85c5`
- B: `263026823515618b42f9549b491e57065cb69c58`
- test: `src/test/java/org/apache/commons/lang3/time/StopWatchTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/StopWatch.java']`
- old_test_mode: `methods`
- user_chars: `19265`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5025, 'completion_tokens': 2356, 'total_tokens': 7381}`

---

- 新增 `testGetDuration`，对应生产代码新增 `StopWatch#getDuration()`，并断言初始值、运行中耗时与字符串表现。
- 新增 `testGetTime`，对应 `getTime()` 被标记为 deprecated 但行为保留，拆出原 `testStopWatchSimpleGet` 覆盖毫秒耗时。
- 将 `testStopWatchGetWithTimeUnit` 替换为 `testGetWithTimeUnit`，仅调整测试方法名以匹配新测试结构。
- 修改 `testLang315`，增加 `getDuration()` 在 suspend/stop 后保持一致的断言。
- 将 `testStopWatchSimple` 替换为 `testSimple`，增加 `getDuration()` 与 reset 后 `Duration.ZERO` 的断言。
- 将 `testStopWatchSplit` 替换为 `testSplit`，增加 split/total duration 断言，并避免提前缓存 split 字符串。
- 将 `testStopWatchStatic` 替换为 `testStatic`，仅调整测试方法名。
- 将 `testStopWatchSuspend` 替换为 `testSuspend`，增加 `getStopInstant()` 与 `getDuration()` 相关断言以覆盖修复后的停止时间语义。
- 需要新增 `java.time.Duration` import；其余已有 `Instant`、`TimeUnit`、JUnit/Hamcrest imports 可保持不变。

```java
import java.time.Duration;

// DELETE_TESTS_START
testStopWatchGetWithTimeUnit
testStopWatchSimple
testStopWatchSimpleGet
testStopWatchSplit
testStopWatchStatic
testStopWatchSuspend
// DELETE_TESTS_END

    @Test
    public void testGetDuration() throws InterruptedException {
        final StopWatch watch = new StopWatch();
        assertEquals(Duration.ZERO, watch.getDuration());
        assertEquals(ZERO_TIME_ELAPSED, watch.toString());
        watch.start();
        sleep(MILLIS_550);
        assertThat("watch.getDuration()", watch.getDuration().toMillis(), lessThan(2000L));
    }

    @Test
    public void testGetTime() throws InterruptedException {
        final StopWatch watch = new StopWatch();
        assertEquals(0, watch.getTime());
        assertEquals(ZERO_TIME_ELAPSED, watch.toString());
        watch.start();
        sleep(MILLIS_550);
        assertThat("watch.getTime()", watch.getTime(), lessThan(2000L));
    }

    @Test
    public void testGetWithTimeUnit() {
        // Create a mock StopWatch with a time of 2:59:01.999
        // @formatter:off
        final StopWatch watch = createMockStopWatch(
            TimeUnit.HOURS.toNanos(2)
                    + TimeUnit.MINUTES.toNanos(59)
                    + TimeUnit.SECONDS.toNanos(1)
                    + TimeUnit.MILLISECONDS.toNanos(999));
        // @formatter:on
        assertEquals(2L, watch.getTime(TimeUnit.HOURS));
        assertEquals(179L, watch.getTime(TimeUnit.MINUTES));
        assertEquals(10741L, watch.getTime(TimeUnit.SECONDS));
        assertEquals(10741999L, watch.getTime(TimeUnit.MILLISECONDS));
    }

    @Test
    public void testLang315() throws InterruptedException {
        final StopWatch watch = StopWatch.createStarted();
        sleep(MILLIS_200);
        watch.suspend();
        final long suspendTime = watch.getTime();
        final Duration suspendDuration = watch.getDuration();
        sleep(MILLIS_200);
        watch.stop();
        final long totalTime = watch.getTime();
        final Duration totalDuration = watch.getDuration();
        assertEquals(suspendTime, totalTime);
        assertEquals(suspendDuration, totalDuration);
    }

    @Test
    public void testSimple() throws InterruptedException {
        final StopWatch watch = StopWatch.createStarted();
        sleep(MILLIS_550);
        watch.stop();
        final long time = watch.getTime();
        final Duration duration = watch.getDuration();
        assertEquals(time, watch.getTime());
        assertEquals(duration, watch.getDuration());
        assertThat("time", time, allOf(greaterThanOrEqualTo(500L), lessThan(2000L)));
        assertThat("duration", duration.toMillis(), allOf(greaterThanOrEqualTo(500L), lessThan(2000L)));
        watch.reset();
        assertEquals(0, watch.getTime());
        assertEquals(Duration.ZERO, watch.getDuration());
    }

    @Test
    public void testSplit() throws InterruptedException {
        final StopWatch watch = StopWatch.createStarted();
        sleep(MILLIS_550);
        // slept ~550 millis
        watch.split();
        final long splitTime = watch.getSplitTime();
        final Duration splitDuration = watch.getSplitDuration();
        assertEquals(splitTime, watch.getSplitDuration().toMillis());
        assertEquals(12, watch.toSplitString().length(), "Formatted split string not the correct length");
        sleep(MILLIS_550);
        // slept ~1100 millis
        watch.unsplit();
        sleep(MILLIS_550);
        // slept ~1650 millis
        watch.stop();
        final long totalTime = watch.getTime();
        final Duration totalDuration = watch.getDuration();
        assertThat("splitTime", splitTime, allOf(greaterThanOrEqualTo(500L), lessThan(1000L)));
        assertThat("splitDuration", splitDuration.toMillis(), allOf(greaterThanOrEqualTo(500L), lessThan(1000L)));
        assertThat("totalTime", totalTime, allOf(greaterThanOrEqualTo(1500L), lessThan(2100L)));
        assertThat("totalDuration", totalDuration.toMillis(), allOf(greaterThanOrEqualTo(1500L), lessThan(2100L)));
    }

    @Test
    public void testStatic() {
        final StopWatch watch = StopWatch.createStarted();
        assertTrue(watch.isStarted());
    }

    @Test
    public void testSuspend() throws InterruptedException {
        // Watch out comparing measurements from System.currentTimeMillis() vs. System.nanoTime()
        final StopWatch watch = StopWatch.createStarted();
        final long testStartMillis = System.currentTimeMillis();
        final long testStartNanos = System.nanoTime();
        final Instant testStartInstant = Instant.ofEpochMilli(testStartMillis);
        sleep(MILLIS_550);
        watch.suspend();
        final long testSuspendMillis = System.currentTimeMillis();
        final long testSuspendNanos = System.nanoTime();
        final long testSuspendTimeNanos = testSuspendNanos - testStartNanos;
        final Duration testSuspendDuration = Duration.ofNanos(testSuspendTimeNanos);
        final long suspendTimeFromNanos = watch.getTime();
        final Duration suspendDuration = watch.getDuration();
        final long stopTimeMillis = watch.getStopTime();
        final Instant stopInstant = watch.getStopInstant();

        assertThat("testStartMillis <= stopTimeMillis", testStartMillis, lessThanOrEqualTo(stopTimeMillis));
        assertThat("testStartInstant <= stopInstant", testStartInstant, lessThanOrEqualTo(stopInstant));
        assertThat("testSuspendMillis <= stopTimeMillis", testSuspendMillis, lessThanOrEqualTo(stopTimeMillis));
        assertThat("testSuspendMillis <= stopInstant", testSuspendMillis, lessThanOrEqualTo(stopInstant.toEpochMilli()));

        sleep(MILLIS_550);
        watch.resume();
        sleep(MILLIS_550);
        watch.stop();
        final long totalTimeFromNanos = watch.getTime();
        final Duration totalDuration = watch.getDuration();

        assertThat("suspendTimeFromNanos", suspendTimeFromNanos, greaterThanOrEqualTo(500L));
        assertThat("suspendDuration", suspendDuration, greaterThanOrEqualTo(Duration.ofMillis(500L)));
        assertThat("suspendTimeFromNanos <= testSuspendTimeNanos", suspendTimeFromNanos, lessThanOrEqualTo(testSuspendTimeNanos));
        assertThat("suspendDuration <= testSuspendDuration", suspendDuration, lessThanOrEqualTo(testSuspendDuration));
        assertThat("totalTimeFromNanos", totalTimeFromNanos, greaterThanOrEqualTo(1000L));
        assertThat("totalDuration", totalDuration, greaterThanOrEqualTo(Duration.ofMillis(1000L)));
        // Be lenient for slow running builds
        assertThat("totalTimeFromNanos", totalTimeFromNanos, lessThan(2500L));
        assertThat("totalDuration", totalDuration, lessThan(Duration.ofMillis(2500L)));
    }
```