# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `c0c7112dcdeb75b521d55cd47d0c61be66b0499e`
- B: `9f89fd4626bbb4e34a905835e397bcffbad59307`
- test: `src/test/java/org/apache/commons/lang3/concurrent/MemoizerTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/Memoizer.java']`
- old_test_mode: `methods`
- user_chars: `22895`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5880, 'completion_tokens': 1111, 'total_tokens': 6991}`

---

- 修改 `testOnlyCallComputableOnceIfDoesNotThrowException`：生产代码泛型构造器已现代化，测试同步改用 diamond 构造 `new Memoizer<>(computable)`。
- 修改 `testDefaultBehaviourNotToRecalculateExecutionExceptions`：生产代码仍将 checked exception 包装为 `IllegalStateException` 并缓存异常，测试移除无用局部变量并补充 `fail` 断言消息。
- 修改 `testDoesNotRecalculateWhenSetToFalse`：对应 `recalculate=false` 时缓存异常的行为，测试移除无用局部变量并补充 `fail` 断言消息。
- 修改 `testDoesRecalculateWhenSetToTrue`：对应 `recalculate=true` 时失败后移除缓存并重新计算的行为，测试改用 diamond 构造并补充 `fail` 断言消息。
- 修改 `testWhenComputableThrowsRuntimeException`：对应 `launderException` 直接抛出 `RuntimeException` 的行为，测试改用 diamond 构造。
- 修改 `testWhenComputableThrowsError`：对应 `launderException` 直接抛出 `Error` 的行为，测试改用 diamond 构造。
- 不需要调整 import。

```java
@Test
public void testOnlyCallComputableOnceIfDoesNotThrowException() throws Exception {
    Integer input = 1;
    Memoizer<Integer, Integer> memoizer = new Memoizer<>(computable);
    expect(computable.compute(input)).andReturn(input);
    replay(computable);

    assertEquals("Should call computable first time", input, memoizer.compute(input));
    assertEquals("Should not call the computable the second time", input, memoizer.compute(input));
}

@Test(expected = IllegalStateException.class)
public void testDefaultBehaviourNotToRecalculateExecutionExceptions() throws Exception {
    Integer input = 1;
    Memoizer<Integer, Integer> memoizer = new Memoizer<>(computable);
    InterruptedException interruptedException = new InterruptedException();
    expect(computable.compute(input)).andThrow(interruptedException);
    replay(computable);

    try {
        memoizer.compute(input);
        fail("Expected Throwable to be thrown!");
    } catch (Throwable expected) {
        // Should always be thrown the first time
    }

    memoizer.compute(input);
}

@Test(expected = IllegalStateException.class)
public void testDoesNotRecalculateWhenSetToFalse() throws Exception {
    Integer input = 1;
    Memoizer<Integer, Integer> memoizer = new Memoizer<>(computable, false);
    InterruptedException interruptedException = new InterruptedException();
    expect(computable.compute(input)).andThrow(interruptedException);
    replay(computable);

    try {
        memoizer.compute(input);
        fail("Expected Throwable to be thrown!");
    } catch (Throwable expected) {
        // Should always be thrown the first time
    }

    memoizer.compute(input);
}

@Test
public void testDoesRecalculateWhenSetToTrue() throws Exception {
    Integer input = 1;
    Integer answer = 3;
    Memoizer<Integer, Integer> memoizer = new Memoizer<>(computable, true);
    InterruptedException interruptedException = new InterruptedException();
    expect(computable.compute(input)).andThrow(interruptedException).andReturn(answer);
    replay(computable);

    try {
        memoizer.compute(input);
        fail("Expected Throwable to be thrown!");
    } catch (Throwable expected) {
        // Should always be thrown the first time
    }

    assertEquals(answer, memoizer.compute(input));
}

@Test(expected = RuntimeException.class)
public void testWhenComputableThrowsRuntimeException() throws Exception {
    Integer input = 1;
    Memoizer<Integer, Integer> memoizer = new Memoizer<>(computable);
    RuntimeException runtimeException = new RuntimeException("Some runtime exception");
    expect(computable.compute(input)).andThrow(runtimeException);
    replay(computable);

    memoizer.compute(input);
}

@Test(expected = Error.class)
public void testWhenComputableThrowsError() throws Exception {
    Integer input = 1;
    Memoizer<Integer, Integer> memoizer = new Memoizer<>(computable);
    Error error = new Error();
    expect(computable.compute(input)).andThrow(error);
    replay(computable);

    memoizer.compute(input);
}
```