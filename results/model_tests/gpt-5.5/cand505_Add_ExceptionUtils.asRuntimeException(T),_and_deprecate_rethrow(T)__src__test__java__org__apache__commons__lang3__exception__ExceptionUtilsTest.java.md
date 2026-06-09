# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ce5522f60dc87fb1b1ee115427519ebe1d33760f`
- B: `3935fa2f193a0cc652300677beeb61b535eedf4c`
- test: `src/test/java/org/apache/commons/lang3/exception/ExceptionUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/exception/ExceptionUtils.java']`
- old_test_mode: `methods`
- user_chars: `9030`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2569, 'completion_tokens': 350, 'total_tokens': 2919}`

---

- 新增 `testAsRuntimeException`，对应生产代码新增 `ExceptionUtils.asRuntimeException(Throwable)`，验证其以原异常实例方式抛出。
- 修改 `testThrow` 为 `testRethrow`，对应生产代码中 `rethrow(Throwable)` 被标记为 deprecated 但行为保持不变，仅更新测试命名以匹配语义。
- 不需要调整 import，现有 `@Test`、`assertThrows`、`assertSame` 相关 import 可继续复用。

```java
    @Test
    public void testAsRuntimeException() {
        final Exception expected = new InterruptedException();
        final Exception actual = assertThrows(Exception.class, () -> ExceptionUtils.asRuntimeException(expected));
        assertSame(expected, actual);
    }

    @Test
    public void testRethrow() {
        final Exception expected = new InterruptedException();
        final Exception actual = assertThrows(Exception.class, () -> ExceptionUtils.rethrow(expected));
        assertSame(expected, actual);
    }
```