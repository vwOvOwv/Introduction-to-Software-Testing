# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `f544897e49fc6c3e3970bf06ff74940bcd6d3505`
- B: `3d4ed4a8ac63db1e51601ffc31fed44dccbb276c`
- test: `src/test/java/org/apache/commons/lang3/LocksTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Locks.java']`
- old_test_mode: `methods`
- user_chars: `12299`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3767, 'completion_tokens': 2761, 'total_tokens': 6528, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2146}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 3383}`

---

- 调整导入：
  - 将 `import static org.junit.jupiter.api.Assertions.*;` 改为 `import static org.junit.jupiter.api.Assertions.assertTrue;`。
  - 新增 `import java.util.function.LongConsumer;`。
- 新增常量 `NUMBER_OF_THREADS`，用于线程数。
- 修改 `testReadLock` 方法，改为调用通用的 `runTest` 辅助方法，并验证运行时间小于串行时间。
- 新增 `testWriteLock` 方法（添加 `@Test` 注解），使用写锁调用 `runTest`，并验证运行时间大于等于串行时间。
- 新增 `runTest` 辅助方法，封装读/写锁的线程创建、运行及时间校验逻辑。

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
    runTest(DELAY, false, (l) -> assertTrue(l < NUMBER_OF_THREADS * DELAY));
}

@Test
void testWriteLock() throws Exception {
    final long DELAY = 100;
    runTest(DELAY, true, (l) -> assertTrue(l >= NUMBER_OF_THREADS * DELAY));
}

private void runTest(long delay, boolean exclusiveLock, LongConsumer runTimeCheck) throws InterruptedException {
    final boolean[] booleanValues = new boolean[10];
    final Lock<boolean[]> lock = Locks.lock(booleanValues);
    final boolean[] runningValues = new boolean[10];

    final long startTime = System.currentTimeMillis();
    for (int i = 0; i < booleanValues.length; i++) {
        final int index = i;
        final FailableConsumer<boolean[], ?> consumer = (b) -> {
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