# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ffdc4272f4d67e2673910cc3a361144dd34ca22f`
- B: `bdb5d9723056941a0a29aabc2eaf81b2c96956b5`
- test: `src/test/java/org/apache/commons/lang3/concurrent/AtomicSafeInitializerTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/AtomicSafeInitializer.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `16048`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3752, 'completion_tokens': 1709, 'total_tokens': 5461}`

---

- 新增 `testExceptionOnInitialize`，覆盖 `AtomicSafeInitializer.get()` 在 `initialize()` 抛出 `ConcurrentException` 时并发调用也能传播异常的新行为。
- 新增 `testInterruptedWaitingOnInitialize`，覆盖等待其他线程完成初始化时被中断会包装为 `ConcurrentException` 的新分支。
- 新增 `testOneThreadWaitingForAnotherToInitialize`，覆盖一个线程等待另一个线程完成初始化后取得同一初始化结果的新分支。
- 需要调整 import：新增 `assertFalse`、`assertSame`、`assertTrue` 静态断言以及 `CountDownLatch`。

```java
// IMPORTS_START
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertSame;
import static org.junit.Assert.assertTrue;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

import org.junit.Before;
import org.junit.Test;
// IMPORTS_END

/** The instance to be tested. */
private AtomicSafeInitializerTestImpl initializer;
private ExceptionThrowingAtomicSafeInitializerTestImpl exceptionThrowingInitializer;
private Exception testCauseException;
private String testExceptionMessage;

@Before
public void setUp() throws Exception {
    initializer = new AtomicSafeInitializerTestImpl();
    exceptionThrowingInitializer = new ExceptionThrowingAtomicSafeInitializerTestImpl();
    testExceptionMessage = "x-test-exception-message-x";
    testCauseException = new Exception(testExceptionMessage);
}

/**
 * Returns the exception-throwing initializer to be tested.
 *
 * @return the {@code AtomicSafeInitializer} under test when validating
 * exception handling
 */
@Override
protected ConcurrentInitializer<Object> createExceptionThrowingInitializer() {
    return exceptionThrowingInitializer;
}

@Test
public void testExceptionOnInitialize() throws ConcurrentException,
        InterruptedException {

    testGetConcurrentWithException(testExceptionMessage, testCauseException);
}

/**
 * Validate the handling of an interrupted exception on a thread waiting for another thread to finish calling the
 * initialize() method.
 *
 * @throws Exception
 */
@Test(timeout = 3000)
public void testInterruptedWaitingOnInitialize() throws Exception {
    this.execTestWithWaitingOnInitialize(true);
}

/**
 * Test the success path of two threads reaching the initialization point at the same time.
 */
@Test(timeout = 3000)
public void testOneThreadWaitingForAnotherToInitialize() throws Exception {
    execTestWithWaitingOnInitialize(false);
}

/**
 * Execute a test that requires one thread to be waiting on the initialize() method of another thread. This test
 * uses latches to guarantee the code path being tested.
 *
 * @throws Exception
 */
protected void execTestWithWaitingOnInitialize(boolean interruptInd) throws Exception {
    final CountDownLatch startLatch = new CountDownLatch(1);
    final CountDownLatch finishLatch = new CountDownLatch(1);
    final WaitingInitializerTestImpl initializer = new WaitingInitializerTestImpl(startLatch, finishLatch);

    InitializerTestThread execThread1 = new InitializerTestThread(initializer);
    InitializerTestThread execThread2 = new InitializerTestThread(initializer);

    execThread1.start();
    startLatch.await();

    execThread2.start();

    if (interruptInd) {
        execThread2.interrupt();
        execThread2.join();
    }

    finishLatch.countDown();

    execThread1.join();

    if (!interruptInd) {
        execThread2.join();
    }

    assertFalse(execThread1.isCaughtException());
    assertSame(initializer.getAnswer(), execThread1.getResult());

    if (interruptInd) {
        assertTrue(execThread2.isCaughtException());
        Exception exc = (Exception) execThread2.getResult();
        assertTrue(exc.getCause() instanceof InterruptedException);
        assertEquals("interrupted waiting for initialization to complete", exc.getMessage());
    } else {
        assertFalse(execThread2.isCaughtException());
        assertSame(initializer.getAnswer(), execThread2.getResult());
    }
}

/**
 * A concrete test implementation of {@code AtomicSafeInitializer}. This
 * implementation always throws an exception.
 */
private class ExceptionThrowingAtomicSafeInitializerTestImpl extends AtomicSafeInitializer<Object> {
    @Override
    protected Object initialize() throws ConcurrentException {
        throw new ConcurrentException(testExceptionMessage, testCauseException);
    }
}

/**
 * Initializer that signals it has started and waits to complete until signalled in order to enable a guaranteed
 * order-of-operations.
 */
private class WaitingInitializerTestImpl extends AtomicSafeInitializer<Object> {
    private final CountDownLatch startedLatch;
    private final CountDownLatch finishLatch;
    private final Object answer = new Object();

    public WaitingInitializerTestImpl(CountDownLatch startedLatch, CountDownLatch finishLatch) {
        this.startedLatch = startedLatch;
        this.finishLatch = finishLatch;
    }

    @Override
    protected Object initialize() throws ConcurrentException {
        this.startedLatch.countDown();
        try {
            this.finishLatch.await();
        } catch (InterruptedException intExc) {
            throw new ConcurrentException(intExc);
        }

        return answer;
    }

    public Object getAnswer() {
        return answer;
    }
}

/**
 * Test executor of the initializer get() operation that captures the result.
 */
private class InitializerTestThread extends Thread {
    private AtomicSafeInitializer<Object> initializer;
    private Object result;
    private boolean caughtException;

    public InitializerTestThread(AtomicSafeInitializer<Object> initializer) {
        super("AtomicSafeInitializer test thread");
        this.initializer = initializer;
    }

    @Override
    public void run() {
        try {
            this.result = initializer.get();
        } catch (ConcurrentException concurrentExc) {
            this.caughtException = true;
            this.result = concurrentExc;
        }
    }

    public Object getResult() {
        return this.result;
    }

    public boolean isCaughtException() {
        return this.caughtException;
    }
}
```