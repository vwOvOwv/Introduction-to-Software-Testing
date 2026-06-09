# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `bc22af91e7e8fd7a530de48cd164056ef05829e0`
- B: `0769eb977b3a56adf5ec8bd4e9f123b75bdf38ed`
- test: `src/test/java/org/apache/commons/lang3/concurrent/ConcurrentUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/ConcurrentUtils.java']`
- old_test_mode: `methods`
- user_chars: `11623`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3021, 'completion_tokens': 1723, 'total_tokens': 4744}`

---

- 修改 `testExtractCauseUnchecked` 为 `testExtractCauseUncheckedException`，继续验证 `extractCause()` 对 unchecked cause 会原样抛出，避免与新增的 `extractCauseUnchecked()` 测试命名混淆；无需调整 import。
- 修改 `testHandleCauseUnchecked` 为 `testHandleCauseUncheckedException`，继续验证 `handleCause()` 对 unchecked cause 会原样抛出，避免与新增的 `handleCauseUnchecked()` 测试命名混淆；无需调整 import。
- 新增 `testConcurrentRuntimeExceptionCauseUnchecked`、`testConcurrentRuntimeExceptionCauseError`、`testConcurrentRuntimeExceptionCauseNull`，覆盖新增 unchecked 包装异常对非法 cause 的校验；无需调整 import。
- 新增 `testExtractCauseUncheckedNull`、`testExtractCauseUncheckedNullCause`、`testExtractCauseUncheckedError`、`testExtractCauseUncheckedUncheckedException`、`testExtractCauseUncheckedChecked`，覆盖新增 `ConcurrentUtils.extractCauseUnchecked()` 的 null、error、runtime、checked cause 行为；无需调整 import。
- 新增 `testHandleCauseUncheckedError`、`testHandleCauseUncheckedUncheckedException`、`testHandleCauseUncheckedChecked`、`testHandleCauseUncheckedNull`，覆盖新增 `ConcurrentUtils.handleCauseUnchecked()` 的 runtime exception 包装/透传行为；无需调整 import。

```java
    /**
     * Tries to create a ConcurrentRuntimeException with a runtime as cause.
     */
    @Test(expected = IllegalArgumentException.class)
    public void testConcurrentRuntimeExceptionCauseUnchecked() {
        new ConcurrentRuntimeException(new RuntimeException());
    }

    /**
     * Tries to create a ConcurrentRuntimeException with an error as cause.
     */
    @Test(expected = IllegalArgumentException.class)
    public void testConcurrentRuntimeExceptionCauseError() {
        new ConcurrentRuntimeException("An error", new Error());
    }

    /**
     * Tries to create a ConcurrentRuntimeException with null as cause.
     */
    @Test(expected = IllegalArgumentException.class)
    public void testConcurrentRuntimeExceptionCauseNull() {
        new ConcurrentRuntimeException(null);
    }

    /**
     * Tests extractCause() if the cause is an unchecked exception.
     */
    @Test
    public void testExtractCauseUncheckedException() {
        RuntimeException rex = new RuntimeException("Test");
        try {
            ConcurrentUtils.extractCause(new ExecutionException(rex));
            fail("Runtime exception not thrown!");
        } catch (RuntimeException r) {
            assertEquals("Wrong exception", rex, r);
        }
    }

    /**
     * Tests extractCauseUnchecked() for a null exception.
     */
    @Test
    public void testExtractCauseUncheckedNull() {
        assertNull("Non null result", ConcurrentUtils.extractCauseUnchecked(null));
    }

    /**
     * Tests extractCauseUnchecked() if the cause of the passed in exception is null.
     */
    @Test
    public void testExtractCauseUncheckedNullCause() {
        assertNull("Non null result", ConcurrentUtils
                .extractCauseUnchecked(new ExecutionException("Test", null)));
    }

    /**
     * Tests extractCauseUnchecked() if the cause is an error.
     */
    @Test
    public void testExtractCauseUncheckedError() {
        Error err = new AssertionError("Test");
        try {
            ConcurrentUtils.extractCauseUnchecked(new ExecutionException(err));
            fail("Error not thrown!");
        } catch (Error e) {
            assertEquals("Wrong error", err, e);
        }
    }

    /**
     * Tests extractCauseUnchecked() if the cause is an unchecked exception.
     */
    @Test
    public void testExtractCauseUncheckedUncheckedException() {
        RuntimeException rex = new RuntimeException("Test");
        try {
            ConcurrentUtils.extractCauseUnchecked(new ExecutionException(rex));
            fail("Runtime exception not thrown!");
        } catch (RuntimeException r) {
            assertEquals("Wrong exception", rex, r);
        }
    }

    /**
     * Tests extractCauseUnchecked() if the cause is a checked exception.
     */
    @Test
    public void testExtractCauseUncheckedChecked() {
        Exception ex = new Exception("Test");
        ConcurrentRuntimeException cex = ConcurrentUtils
                .extractCauseUnchecked(new ExecutionException(ex));
        assertSame("Wrong cause", ex, cex.getCause());
    }

    /**
     * Tests handleCause() if the cause is an unchecked exception.
     */
    @Test
    public void testHandleCauseUncheckedException() throws ConcurrentException {
        RuntimeException rex = new RuntimeException("Test");
        try {
            ConcurrentUtils.handleCause(new ExecutionException(rex));
            fail("Runtime exception not thrown!");
        } catch (RuntimeException r) {
            assertEquals("Wrong exception", rex, r);
        }
    }

    /**
     * Tests handleCauseUnchecked() if the cause is an error.
     */
    @Test
    public void testHandleCauseUncheckedError() throws ConcurrentException {
        Error err = new AssertionError("Test");
        try {
            ConcurrentUtils.handleCauseUnchecked(new ExecutionException(err));
            fail("Error not thrown!");
        } catch (Error e) {
            assertEquals("Wrong error", err, e);
        }
    }

    /**
     * Tests handleCauseUnchecked() if the cause is an unchecked exception.
     */
    @Test
    public void testHandleCauseUncheckedUncheckedException()
            throws ConcurrentException {
        RuntimeException rex = new RuntimeException("Test");
        try {
            ConcurrentUtils.handleCauseUnchecked(new ExecutionException(rex));
            fail("Runtime exception not thrown!");
        } catch (RuntimeException r) {
            assertEquals("Wrong exception", rex, r);
        }
    }

    /**
     * Tests handleCauseUnchecked() if the cause is a checked exception.
     */
    @Test
    public void testHandleCauseUncheckedChecked() {
        Exception ex = new Exception("Test");
        try {
            ConcurrentUtils.handleCauseUnchecked(new ExecutionException(ex));
            fail("ConcurrentRuntimeException not thrown!");
        } catch (ConcurrentRuntimeException crex) {
            assertEquals("Wrong cause", ex, crex.getCause());
        }
    }

    /**
     * Tests handleCauseUnchecked() for a null parameter or a null cause. In
     * this case the method should do nothing. We can only test that no
     * exception is thrown.
     */
    @Test
    public void testHandleCauseUncheckedNull() throws ConcurrentException {
        ConcurrentUtils.handleCauseUnchecked(null);
        ConcurrentUtils.handleCauseUnchecked(new ExecutionException("Test",
                null));
    }
```