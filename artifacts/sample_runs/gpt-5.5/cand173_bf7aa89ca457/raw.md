# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `acaf4582781c17952b25fe86abafcefa0489c2a6`
- B: `bf7aa89ca45706ad1f40cacdf7448626529dd6b0`
- test: `src/test/java/org/apache/commons/lang3/concurrent/LocksTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/Locks.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `20598`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5149, 'completion_tokens': 587, 'total_tokens': 5736}`

---

- 修改 `testWriteLock`：生产代码仍需验证写锁互斥行为，旧测试缺少 `@Test` 注解导致未执行，需补回。
- 新增 `testResultValidation`：对应 `lockApplyUnlock` 新增“禁止返回 hidden object 本身”的校验，断言正常返回新对象且返回隐藏对象时抛出 `IllegalStateException`。
- 需要调整 import：新增 `assertEquals`、`assertNotNull`、`assertNotSame`、`fail` 的静态导入，保留原有 `assertTrue` 等导入。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

import java.util.function.LongConsumer;

import org.apache.commons.lang3.concurrent.Locks.Lock;
import org.apache.commons.lang3.function.FailableConsumer;
import org.junit.jupiter.api.Test;
// IMPORTS_END

@Test
public void testWriteLock() throws Exception {
    final long DELAY = 100;
    /** If our threads are running concurrently, then we expect to be no faster
     * than running one after the other.
     */
    runTest(DELAY, true, l -> assertTrue(l >= NUMBER_OF_THREADS * DELAY));
}

@Test
public void testResultValidation() {
    final Object hidden = new Object();
    final Lock<Object> lock = Locks.lock(hidden);

    final Object o1 = lock.applyReadLocked(h -> new Object());
    assertNotNull(o1);
    assertNotSame(hidden, o1);

    final Object o2 = lock.applyWriteLocked(h -> new Object());
    assertNotNull(o2);
    assertNotSame(hidden, o2);

    try {
        lock.applyReadLocked(h -> hidden);
        fail("Expected Exception");
    } catch (final IllegalStateException e) {
        assertEquals("The returned object is, in fact, the hidden object.", e.getMessage());
    }

    try {
        lock.applyWriteLocked(h -> hidden);
        fail("Expected Exception");
    } catch (final IllegalStateException e) {
        assertEquals("The returned object is, in fact, the hidden object.", e.getMessage());
    }
}
```