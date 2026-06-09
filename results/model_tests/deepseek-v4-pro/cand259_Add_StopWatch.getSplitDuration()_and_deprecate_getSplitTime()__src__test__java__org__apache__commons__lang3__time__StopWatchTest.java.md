# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `63d9aa48f3646e6b5a366291747a73f7ad49636a`
- B: `2875a65756da4c72e8d188555b9639857e73684a`
- test: `src/test/java/org/apache/commons/lang3/time/StopWatchTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/StopWatch.java']`
- old_test_mode: `methods`
- user_chars: `8359`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2522, 'completion_tokens': 2899, 'total_tokens': 5421, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2363}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2138}`

---

- 修改 `testBadStates` 方法：添加对 `watch::getSplitDuration` 的断言，与生产代码新增 `getSplitDuration` 方法对应；将原有单行注释改为 Javadoc 注释。测试方法其余逻辑保持不变，包括仍保留原有 `getSplitTime` 异常断言。
- 无需修改 `testStopWatchGetWithTimeUnit`（空行变动不影响编译与断言）。
- 无需新增或删除其他测试方法。
- 无需调整 import。

```java
    /**
     * Tests bad states.
     */
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
```