# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `63d9aa48f3646e6b5a366291747a73f7ad49636a`
- B: `2875a65756da4c72e8d188555b9639857e73684a`
- test: `src/test/java/org/apache/commons/lang3/time/StopWatchTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/StopWatch.java']`
- old_test_mode: `methods`
- user_chars: `8359`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2429, 'completion_tokens': 1380, 'total_tokens': 3809}`

---

- 修改 `testBadStates`：生产代码新增 `getSplitDuration()`，需补充未 split 状态下调用该方法抛出 `IllegalStateException` 的断言；无需调整 import。
- 新增 `testGetSplitDuration`：覆盖新增的 `StopWatch#getSplitDuration()`，断言其返回纳秒级 `Duration`；无需调整 import。
- `testStopWatchGetWithTimeUnit` 仅有人类 diff 中的空行变化，不需要修改测试逻辑；无需调整 import。

```java
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
            "Calling getSplitDuration on an unsplit StopWatch should throw an exception. ");

        assertThrows(IllegalStateException.class, watch::resume,
            "Calling resume on an unsuspended StopWatch should throw an exception. ");

        watch.stop();

        assertThrows(IllegalStateException.class, watch::start,
            "Calling start on a stopped StopWatch should throw an exception as it needs to be reset. ");
    }

    @Test
    public void testGetSplitDuration() {
        final StopWatch watch = StopWatch.createStarted();
        watch.split();

        try {
            final long nanos = 123456L;
            final long currentNanos = System.nanoTime();
            FieldUtils.writeField(watch, "startTimeNanos", currentNanos - nanos, true);
            FieldUtils.writeField(watch, "startTimeMillis", System.currentTimeMillis(), true);
            FieldUtils.writeField(watch, "stopTimeNanos", currentNanos, true);
        } catch (final IllegalAccessException e) {
            fail(e);
        }

        assertEquals(Duration.ofNanos(123456L), watch.getSplitDuration());
    }
```