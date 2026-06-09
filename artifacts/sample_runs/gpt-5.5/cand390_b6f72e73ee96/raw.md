# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `da7c755ff431dae5e0c5d2cef211a7de9cda492f`
- B: `b6f72e73ee96feb63e17096933fd5b7f313fb77b`
- test: `src/test/java/org/apache/commons/lang3/concurrent/locks/LockingVisitorsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/locks/LockingVisitors.java']`
- old_test_mode: `methods`
- user_chars: `24051`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5913, 'completion_tokens': 1732, 'total_tokens': 7645}`

---

- 新增 `testBuilderLockVisitor`，覆盖新增的通用 `LockVisitor.LVBuilder` 构建流程，并需要使用已有 `LockVisitor` import。
- 新增 `testBuilderReadWriteLockVisitor`，覆盖新增的 `ReadWriteLockVisitor.builder()`，需要新增 `ReadWriteLockVisitor` import。
- 新增 `testBuilderReentrantLockVisitor`，覆盖新增的 `ReentrantLockVisitor.builder()`，需要新增 `ReentrantLockVisitor` import。
- 新增 `testBuilderReentrantReadWriteLockVisitor`，覆盖 `ReadWriteLockVisitor.Builder#setLock` 对 `ReentrantReadWriteLock` 的支持。
- 新增 `testBuilderReentrantStampedLockVisitor`，覆盖新增的 `StampedLockVisitor.builder()`，需要新增 `StampedLock` import。
- 修改 `testCreate`，仅按新测试命名同步局部变量为 `obj` / `lock`，断言行为不变。
- 需要调整 import：新增 `java.util.concurrent.locks.StampedLock`、`LockingVisitors.ReadWriteLockVisitor`、`LockingVisitors.ReentrantLockVisitor`。

```java
import java.util.concurrent.locks.StampedLock;
import org.apache.commons.lang3.concurrent.locks.LockingVisitors.ReadWriteLockVisitor;
import org.apache.commons.lang3.concurrent.locks.LockingVisitors.ReentrantLockVisitor;

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
```