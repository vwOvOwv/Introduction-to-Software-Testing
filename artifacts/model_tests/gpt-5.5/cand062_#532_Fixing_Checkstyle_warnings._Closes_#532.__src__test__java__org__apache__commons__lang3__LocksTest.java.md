# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `f544897e49fc6c3e3970bf06ff74940bcd6d3505`
- B: `3d4ed4a8ac63db1e51601ffc31fed44dccbb276c`
- test: `src/test/java/org/apache/commons/lang3/LocksTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Locks.java']`
- old_test_mode: `methods`
- user_chars: `12299`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3558, 'completion_tokens': 1022, 'total_tokens': 4580}`

---

- 修改 `testReadLock`：按测试 diff 将并发读锁耗时断言抽取到 `runTest`，并使用 `NUMBER_OF_THREADS` 统一线程数量。
- 新增 `testWriteLock`：覆盖写锁互斥行为，断言写锁总耗时不小于串行执行时间。
- 新增辅助方法 `runTest`：复用读锁/写锁线程启动与耗时校验逻辑。
- 调整 import：将 JUnit 断言 wildcard 改为 `assertTrue`，并新增 `java.util.function.LongConsumer`。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.function.LongConsumer;

import org.apache.commons.lang3.Functions.FailableConsumer;
import org.apache.commons.lang3.Locks.Lock;
import org.junit.jupiter.api.Test;
// IMPORTS_END

private static final int NUMBER_OF_THREADS = 10;

@Test
void testReadLock() throws Exception {
    final long DELAY = 3000;
    runTest(DELAY, false, l -> assertTrue(l < NUMBER_OF_THREADS * DELAY));
}

@Test
void testWriteLock() throws Exception {
    final long DELAY = 100;
    runTest(DELAY, true, l -> assertTrue(l >= NUMBER_OF_THREADS * DELAY));
}

private void runTest(final long delay, final boolean exclusiveLock, final LongConsumer runTimeCheck) throws InterruptedException {
    final boolean[] booleanValues = new boolean[NUMBER_OF_THREADS];
    final Lock<boolean[]> lock = Locks.lock(booleanValues);
    final boolean[] runningValues = new boolean[NUMBER_OF_THREADS];

    final long startTime = System.currentTimeMillis();
    for (int i = 0; i < booleanValues.length; i++) {
        final int index = i;
        final FailableConsumer<boolean[], ?> consumer = b -> {
            b[index] = false;
            Thread.sleep(delay);
            b[index] = true;
            modify(runningValues, index, false);
        };
        final Thread t = new Thread(() -> {
            if (exclusiveLock) {
                lock.runWriteLocked(consumer);
            } else {
                lock.runReadLocked(consumer);
            }
        });
        modify(runningValues, i, true);
        t.start();
    }
    while (someValueIsTrue(runningValues)) {
        Thread.sleep(100);
    }
    final long endTime = System.currentTimeMillis();
    for (int i = 0; i < booleanValues.length; i++) {
        assertTrue(booleanValues[i]);
    }
    runTimeCheck.accept(endTime - startTime);
}
```