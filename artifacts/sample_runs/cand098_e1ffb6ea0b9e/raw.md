# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `2cdac973e3d2fa0b9590b4ffb1b02bb4c99c73d7`
- B: `e1ffb6ea0b9e21ea71c4540b0fca4db8e4c1dd93`
- test: `src/test/java/org/apache/commons/lang3/ThreadUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ThreadUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `20926`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5302, 'completion_tokens': 605, 'total_tokens': 5907, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 5046}`

---

- 新增 `testSleepQuietlyInterruptDuringSleep` 测试方法，验证在睡眠期间被中断后中断标志被保留。
- 新增 `testSleepQuietlyInterruptedFlagPreserved` 测试方法，验证当前线程已中断时调用 `sleepQuietly` 后中断标志被保留。
- 新增 `testSleepQuietlyNormalNoInterrupt` 测试方法，验证正常睡眠后中断标志未被设置。
- 新增 import `java.util.concurrent.atomic.AtomicBoolean`。

```java
// IMPORTS_START
import static org.apache.commons.lang3.LangAssertions.assertIllegalArgumentException;
import static org.apache.commons.lang3.LangAssertions.assertNullPointerException;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.time.Duration;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Predicate;

import org.apache.commons.lang3.ThreadUtils.ThreadGroupPredicate;
import org.apache.commons.lang3.ThreadUtils.ThreadPredicate;
import org.apache.commons.lang3.function.Predicates;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    void testSleepQuietlyInterruptDuringSleep() throws Exception {
        final AtomicBoolean isInterrupted = new AtomicBoolean();
        final Thread testThread = new Thread(() -> {
            // This will be interrupted while sleeping
            ThreadUtils.sleepQuietly(Duration.ofSeconds(10));
            isInterrupted.set(Thread.currentThread().isInterrupted());
        });
        testThread.start();
        Thread.sleep(100);
        testThread.interrupt();
        testThread.join(1000);
        assertTrue(isInterrupted.get(), "Interrupted flag should be preserved after InterruptedException");
    }

    @Test
    void testSleepQuietlyInterruptedFlagPreserved() {
        Thread.currentThread().interrupt();
        // Immediately throw InterruptedException and restores the interrupted status
        ThreadUtils.sleepQuietly(Duration.ofMillis(1000));
        assertTrue(Thread.interrupted(), "Interrupted flag should be preserved");
    }

    @Test
    void testSleepQuietlyNormalNoInterrupt() {
        Thread.interrupted();
        ThreadUtils.sleepQuietly(Duration.ofMillis(10));
        assertFalse(Thread.currentThread().isInterrupted(), "Interrupted flag should not be set for normal sleep");
    }
```