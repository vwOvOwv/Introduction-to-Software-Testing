# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `da7c755ff431dae5e0c5d2cef211a7de9cda492f`
- B: `b6f72e73ee96feb63e17096933fd5b7f313fb77b`
- test: `src/test/java/org/apache/commons/lang3/concurrent/locks/LockingVisitorsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/locks/LockingVisitors.java']`
- old_test_mode: `methods`
- user_chars: `24328`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6309, 'completion_tokens': 2246, 'total_tokens': 8555, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 6053}`

---

- 新增 `testBuilderLockVisitor` 方法：测试 `LockVisitor.LVBuilder` 构建器，对应生产代码新增的 `LVBuilder` 内部类。
- 新增 `testBuilderReadWriteLockVisitor` 方法：测试 `ReadWriteLockVisitor.Builder` 构建器，对应生产代码新增的 `ReadWriteLockVisitor.Builder` 内部类。
- 新增 `testBuilderReentrantLockVisitor` 方法：测试 `ReentrantLockVisitor.Builder` 构建器，对应生产代码新增的 `ReentrantLockVisitor.Builder` 内部类。
- 新增 `testBuilderReentrantReadWriteLockVisitor` 方法：测试 `ReadWriteLockVisitor.Builder` 构建器与 `ReentrantReadWriteLock`，对应生产代码新增的构建器模式。
- 新增 `testBuilderReentrantStampedLockVisitor` 方法：测试 `StampedLockVisitor.Builder` 构建器，对应生产代码新增的 `StampedLockVisitor.Builder` 内部类。
- 修改 `testCreate` 方法：重命名局部变量 `res` 为 `obj`，`rwLock` 为 `lock`，对应测试 diff 中的变量重命名。
- 修改 `testReentrantLock` 方法：将 `runTest` 的第二个参数从 `false` 改为 `true`，断言从 `millis < TOTAL_DELAY.toMillis()` 改为 `millis >= TOTAL_DELAY.toMillis()`，对应测试 diff 中的逻辑调整。
- 修改 `testReentrantLockFairness` 方法：将 `runTest` 的第二个参数从 `false` 改为 `true`，断言从 `millis < TOTAL_DELAY.toMillis()` 改为 `millis >= TOTAL_DELAY.toMillis()`，对应测试 diff 中的逻辑调整。
- 修改 `testReentrantReadWriteLockExclusive` 方法：将 `runTest` 的第二个参数从 `true` 改为 `false`，断言从 `millis >= TOTAL_DELAY.toMillis()` 改为 `millis < TOTAL_DELAY.toMillis()`，对应测试 diff 中的逻辑调整。
- 修改 `testReentrantReadWriteLockNotExclusive` 方法：将 `runTest` 的第二个参数从 `false` 改为 `true`，断言从 `millis < TOTAL_DELAY.toMillis()` 改为 `millis >= TOTAL_DELAY.toMillis()`，对应测试 diff 中的逻辑调整。
- 新增 import：`java.util.concurrent.locks.StampedLock`、`org.apache.commons.lang3.concurrent.locks.LockingVisitors.ReadWriteLockVisitor`、`org.apache.commons.lang3.concurrent.locks.LockingVisitors.ReentrantLockVisitor`，对应测试 diff 中的新增导入。

```java
// IMPORTS_START
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.concurrent.locks.StampedLock;
import java.util.function.LongConsumer;

import org.apache.commons.lang3.AbstractLangTest;
import org.apache.commons.lang3.ArrayUtils;
import org.apache.commons.lang3.ThreadUtils;
import org.apache.commons.lang3.concurrent.locks.LockingVisitors.LockVisitor;
import org.apache.commons.lang3.concurrent.locks.LockingVisitors.ReadWriteLockVisitor;
import org.apache.commons.lang3.concurrent.locks.LockingVisitors.ReentrantLockVisitor;
import org.apache.commons.lang3.concurrent.locks.LockingVisitors.StampedLockVisitor;
import org.apache.commons.lang3.function.FailableConsumer;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
// IMPORTS_END

    @ParameterizedTest
    @ValueSource(booleans = { true, false })
    void testBuilderLockVisitor(final boolean fair) {
        final AtomicInteger obj = new AtomicInteger();
        final ReadWriteLock lock = new ReentrantReadWriteLock(fair);
        // @formatter:off
        final LockVisitor<AtomicInteger, ReadWriteLock> lockVisitor = new LockVisitor.LVBuilder()
          .setObject(obj)
          .setLock(lock)
          .setReadLockSupplier(lock::readLock)
          .setWriteLockSupplier(lock::writeLock)
          .get();
        // @formatter:on
        lockVisitor.acceptReadLocked(AtomicInteger::incrementAndGet);
        assertEquals(1, obj.get());
        lockVisitor.acceptReadLocked(AtomicInteger::incrementAndGet);
        assertEquals(2, obj.get());
    }

    @ParameterizedTest
    @ValueSource(booleans = { true, false })
    void testBuilderReadWriteLockVisitor(final boolean fair) {
        final AtomicInteger obj = new AtomicInteger();
        final ReadWriteLock lock = new ReentrantReadWriteLock(fair);
        // @formatter:off
        final LockingVisitors.ReadWriteLockVisitor<AtomicInteger> lockVisitor = ReadWriteLockVisitor.<AtomicInteger>builder()
          .setObject(obj)
          .setLock(lock)
          .get();
        // @formatter:on
        lockVisitor.acceptReadLocked(AtomicInteger::incrementAndGet);
        assertEquals(1, obj.get());
        lockVisitor.acceptReadLocked(AtomicInteger::incrementAndGet);
        assertEquals(2, obj.get());
    }

    @ParameterizedTest
    @ValueSource(booleans = { true, false })
    void testBuilderReentrantLockVisitor(final boolean fair) {
        final AtomicInteger obj = new AtomicInteger();
        final ReentrantLock lock = new ReentrantLock(fair);
        // @formatter:off
        final LockingVisitors.ReentrantLockVisitor<AtomicInteger> lockVisitor = ReentrantLockVisitor.<AtomicInteger>builder()
          .setObject(obj)
          .setLock(lock)
          .get();
        // @formatter:on
        lockVisitor.acceptReadLocked(AtomicInteger::incrementAndGet);
        assertEquals(1, obj.get());
        lockVisitor.acceptReadLocked(AtomicInteger::incrementAndGet);
        assertEquals(2, obj.get());
    }

    @ParameterizedTest
    @ValueSource(booleans = { true, false })
    void testBuilderReentrantReadWriteLockVisitor(final boolean fair) {
        final AtomicInteger obj = new AtomicInteger();
        final ReentrantReadWriteLock lock = new ReentrantReadWriteLock(fair);
        // @formatter:off
        final LockingVisitors.ReadWriteLockVisitor<AtomicInteger> lockVisitor = ReadWriteLockVisitor.<AtomicInteger>builder()
          .setObject(obj)
          .setLock(lock)
          .get();
        // @formatter:on
        lockVisitor.acceptReadLocked(AtomicInteger::incrementAndGet);
        assertEquals(1, obj.get());
        lockVisitor.acceptReadLocked(AtomicInteger::incrementAndGet);
        assertEquals(2, obj.get());
    }

    @Test
    void testBuilderReentrantStampedLockVisitor() {
        final AtomicInteger obj = new AtomicInteger();
        final StampedLock lock = new StampedLock();
        // @formatter:off
        final LockingVisitors.StampedLockVisitor<AtomicInteger> lockVisitor = StampedLockVisitor.<AtomicInteger>builder()
          .setObject(obj)
          .setLock(lock)
          .get();
        // @formatter:on
        lockVisitor.acceptReadLocked(AtomicInteger::incrementAndGet);
        assertEquals(1, obj.get());
        lockVisitor.acceptReadLocked(AtomicInteger::incrementAndGet);
        assertEquals(2, obj.get());
    }

    @Test
    void testCreate() {
        final AtomicInteger obj = new AtomicInteger();
        final ReadWriteLock lock = new ReentrantReadWriteLock();
        LockingVisitors.create(obj, lock).acceptReadLocked(AtomicInteger::incrementAndGet);
        LockingVisitors.create(obj, lock).acceptReadLocked(null);
        assertEquals(1, obj.get());
        LockingVisitors.create(obj, lock).acceptWriteLocked(AtomicInteger::incrementAndGet);
        LockingVisitors.create(obj, lock).acceptWriteLocked(null);
        assertEquals(2, obj.get());
    }

    @Test
    void testReentrantLock() throws Exception {
        // If our threads are running concurrently, then we expect to be no faster than running one after the other.
        final boolean[] booleanValues = new boolean[10];
        runTest(DELAY, true, millis -> assertTrue(millis >= TOTAL_DELAY.toMillis()), booleanValues, LockingVisitors.reentrantLockVisitor(booleanValues));
    }

    @ParameterizedTest
    @ValueSource(booleans = { true, false })
    void testReentrantLockFairness(final boolean fairness) throws Exception {
        // If our threads are running concurrently, then we expect to be no faster than running one after the other.
        final boolean[] booleanValues = new boolean[10];
        runTest(DELAY, true, millis -> assertTrue(millis >= TOTAL_DELAY.toMillis()), booleanValues,
                LockingVisitors.create(booleanValues, new ReentrantLock(fairness)));
    }

    @Test
    void testReentrantReadWriteLockExclusive() throws Exception {
        // If our threads are running concurrently, then we expect to be faster than running one after the other.
        final boolean[] booleanValues = new boolean[10];
        runTest(DELAY, false, millis -> assertTrue(millis < TOTAL_DELAY.toMillis()), booleanValues,
                LockingVisitors.reentrantReadWriteLockVisitor(booleanValues));
    }

    @Test
    void testReentrantReadWriteLockNotExclusive() throws Exception {
        // If our threads are running concurrently, then we expect to be no faster than running one after the other.
        final boolean[] booleanValues = new boolean[10];
        runTest(DELAY, true, millis -> assertTrue(millis >= TOTAL_DELAY.toMillis()), booleanValues,
                LockingVisitors.reentrantReadWriteLockVisitor(booleanValues));
    }
```