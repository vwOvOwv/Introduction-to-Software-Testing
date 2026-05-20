# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `6b079573792690b91f2afd1e0a94f622f0e1dee9`
- B: `ae28edfbddde9ed45fb0501ec6765a2af5c451f0`
- test: `src/test/java/org/apache/commons/lang3/concurrent/locks/LockingVisitorsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/locks/LockingVisitors.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `14723`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3923, 'completion_tokens': 924, 'total_tokens': 4847, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 3667}`

---

- 新增 `testReentrantLock` 测试方法，对应生产代码新增的 `ReentrantLockVisitor` 和 `reentrantLockVisitor` 方法。
- 新增 `testReentrantLockFairness` 参数化测试方法，对应生产代码新增的 `create` 方法（接受 `ReentrantLock` 参数）。
- 新增 `import java.util.concurrent.locks.ReentrantLock`，对应测试 diff 中新增的导入。
- 新增 `import org.junit.jupiter.params.ParameterizedTest` 和 `import org.junit.jupiter.params.provider.ValueSource`，对应测试 diff 中新增的导入。
- 修改 `runTest` 方法：注释掉 `startTimeMillis` 和 `endTimeMillis` 变量声明及计算，并注释掉 `runTimeCheck` 断言调用，对应测试 diff 中的变更。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.function.LongConsumer;

import org.apache.commons.lang3.AbstractLangTest;
import org.apache.commons.lang3.ArrayUtils;
import org.apache.commons.lang3.ThreadUtils;
import org.apache.commons.lang3.concurrent.locks.LockingVisitors.LockVisitor;
import org.apache.commons.lang3.concurrent.locks.LockingVisitors.StampedLockVisitor;
import org.apache.commons.lang3.function.FailableConsumer;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
// IMPORTS_END

    private void runTest(final Duration delay, final boolean exclusiveLock, final LongConsumer runTimeCheck,
            final boolean[] booleanValues, final LockVisitor<boolean[], ?> visitor) throws InterruptedException {
        assertNotNull(visitor.getLock());
        assertNotNull(visitor.getObject());
        final boolean[] runningValues = new boolean[10];
        // final long startTimeMillis = System.currentTimeMillis();
        for (int i = 0; i < booleanValues.length; i++) {
            final int index = i;
            final FailableConsumer<boolean[], ?> consumer = b -> {
                b[index] = false;
                ThreadUtils.sleep(delay);
                b[index] = true;
                set(runningValues, index, false);
            };
            final Thread t = new Thread(() -> {
                if (exclusiveLock) {
                    visitor.acceptWriteLocked(consumer);
                } else {
                    visitor.acceptReadLocked(consumer);
                }
            });
            set(runningValues, i, true);
            t.start();
        }
        while (containsTrue(runningValues)) {
            ThreadUtils.sleep(SHORT_DELAY);
        }
        // final long endTimeMillis = System.currentTimeMillis();
        for (final boolean booleanValue : booleanValues) {
            assertTrue(booleanValue);
        }
        // WRONG assumption
        // runTimeCheck.accept(endTimeMillis - startTimeMillis);
    }

    @Test
    void testReentrantLock() throws Exception {
        // If our threads are running concurrently, then we expect to be faster than running one after the other.
        final boolean[] booleanValues = new boolean[10];
        runTest(DELAY, false, millis -> assertTrue(millis < TOTAL_DELAY.toMillis()), booleanValues, LockingVisitors.reentrantLockVisitor(booleanValues));
    }

    @ParameterizedTest
    @ValueSource(booleans = { true, false })
    void testReentrantLockFairness(final boolean fairness) throws Exception {
        // If our threads are running concurrently, then we expect to be faster than running one after the other.
        final boolean[] booleanValues = new boolean[10];
        runTest(DELAY, false, millis -> assertTrue(millis < TOTAL_DELAY.toMillis()), booleanValues,
                LockingVisitors.create(booleanValues, new ReentrantLock(fairness)));
    }
```