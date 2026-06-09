# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `4b77d24042a411204c25f81bf4e5f38e43ab94a1`
- B: `1ec6c0ae9a28ef0d1a10adbded66d2b00ea840d4`
- test: `src/test/java/org/apache/commons/lang3/exception/ExceptionUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/exception/ExceptionUtils.java']`
- old_test_mode: `methods`
- user_chars: `24292`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6378, 'completion_tokens': 4826, 'total_tokens': 11204, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1488}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 5994}`

---

- 修改 `testIndexOf_ThrowableClass` 方法：为 `ExceptionUtils.indexOfThrowable` 增加对 `Throwable.class` 的断言，与生产代码新增的 API 行为保持一致。
- 修改 `testIndexOf_ThrowableClassInt` 方法：为 `ExceptionUtils.indexOfThrowable` 增加对 `Throwable.class` 的断言。
- 修改 `testIndexOfType_ThrowableClass` 方法：为 `ExceptionUtils.indexOfType` 增加对 `Throwable.class` 的断言。
- 修改 `testIndexOfType_ThrowableClassInt` 方法：为 `ExceptionUtils.indexOfType` 增加对 `Throwable.class` 的断言。
- 新增 `testThrowableOf_ThrowableClass` 方法：测试新 API `throwableOfThrowable(Throwable, Class<T>)`。
- 新增 `testThrowableOf_ThrowableClassInt` 方法：测试新 API `throwableOfThrowable(Throwable, Class<T>, int)`。
- 新增 `testThrowableOfType_ThrowableClass` 方法：测试新 API `throwableOfType(Throwable, Class<T>)`。
- 新增 `testThrowableOfType_ThrowableClassInt` 方法：测试新 API `throwableOfType(Throwable, Class<T>, int)`。
- 修改内部类 `ExceptionWithoutCause` 的 `getTargetException()` 方法体，添加 `// noop` 注释（仅格式调整，不影响编译）。
- 无需调整 import。

```java
@Test
public void testIndexOf_ThrowableClass() {
    assertEquals(-1, ExceptionUtils.indexOfThrowable(null, null));
    assertEquals(-1, ExceptionUtils.indexOfThrowable(null, NestableException.class));

    assertEquals(-1, ExceptionUtils.indexOfThrowable(withoutCause, null));
    assertEquals(-1, ExceptionUtils.indexOfThrowable(withoutCause, ExceptionWithCause.class));
    assertEquals(-1, ExceptionUtils.indexOfThrowable(withoutCause, NestableException.class));
    assertEquals(0, ExceptionUtils.indexOfThrowable(withoutCause, ExceptionWithoutCause.class));

    assertEquals(-1, ExceptionUtils.indexOfThrowable(nested, null));
    assertEquals(-1, ExceptionUtils.indexOfThrowable(nested, ExceptionWithCause.class));
    assertEquals(0, ExceptionUtils.indexOfThrowable(nested, NestableException.class));
    assertEquals(1, ExceptionUtils.indexOfThrowable(nested, ExceptionWithoutCause.class));

    assertEquals(-1, ExceptionUtils.indexOfThrowable(withCause, null));
    assertEquals(0, ExceptionUtils.indexOfThrowable(withCause, ExceptionWithCause.class));
    assertEquals(1, ExceptionUtils.indexOfThrowable(withCause, NestableException.class));
    assertEquals(2, ExceptionUtils.indexOfThrowable(withCause, ExceptionWithoutCause.class));

    assertEquals(-1, ExceptionUtils.indexOfThrowable(withCause, Exception.class));
    assertEquals(-1, ExceptionUtils.indexOfThrowable(withCause, Throwable.class));
}

@Test
public void testThrowableOf_ThrowableClass() {
    assertEquals(null, ExceptionUtils.throwableOfThrowable(null, null));
    assertEquals(null, ExceptionUtils.throwableOfThrowable(null, NestableException.class));

    assertEquals(null, ExceptionUtils.throwableOfThrowable(withoutCause, null));
    assertEquals(null, ExceptionUtils.throwableOfThrowable(withoutCause, ExceptionWithCause.class));
    assertEquals(null, ExceptionUtils.throwableOfThrowable(withoutCause, NestableException.class));
    assertEquals(withoutCause, ExceptionUtils.throwableOfThrowable(withoutCause, ExceptionWithoutCause.class));

    assertEquals(null, ExceptionUtils.throwableOfThrowable(nested, null));
    assertEquals(null, ExceptionUtils.throwableOfThrowable(nested, ExceptionWithCause.class));
    assertEquals(nested, ExceptionUtils.throwableOfThrowable(nested, NestableException.class));
    assertEquals(nested.getCause(), ExceptionUtils.throwableOfThrowable(nested, ExceptionWithoutCause.class));

    assertEquals(null, ExceptionUtils.throwableOfThrowable(withCause, null));
    assertEquals(withCause, ExceptionUtils.throwableOfThrowable(withCause, ExceptionWithCause.class));
    assertEquals(withCause.getCause(), ExceptionUtils.throwableOfThrowable(withCause, NestableException.class));
    assertEquals(withCause.getCause().getCause(), ExceptionUtils.throwableOfThrowable(withCause, ExceptionWithoutCause.class));

    assertEquals(null, ExceptionUtils.throwableOfThrowable(withCause, Exception.class));
    assertEquals(null, ExceptionUtils.throwableOfThrowable(withCause, Throwable.class));
}

@Test
public void testIndexOf_ThrowableClassInt() {
    assertEquals(-1, ExceptionUtils.indexOfThrowable(null, null, 0));
    assertEquals(-1, ExceptionUtils.indexOfThrowable(null, NestableException.class, 0));

    assertEquals(-1, ExceptionUtils.indexOfThrowable(withoutCause, null, 0));
    assertEquals(-1, ExceptionUtils.indexOfThrowable(withoutCause, ExceptionWithCause.class, 0));
    assertEquals(-1, ExceptionUtils.indexOfThrowable(withoutCause, NestableException.class, 0));
    assertEquals(0, ExceptionUtils.indexOfThrowable(withoutCause, ExceptionWithoutCause.class, 0));

    assertEquals(-1, ExceptionUtils.indexOfThrowable(nested, null, 0));
    assertEquals(-1, ExceptionUtils.indexOfThrowable(nested, ExceptionWithCause.class, 0));
    assertEquals(0, ExceptionUtils.indexOfThrowable(nested, NestableException.class, 0));
    assertEquals(1, ExceptionUtils.indexOfThrowable(nested, ExceptionWithoutCause.class, 0));

    assertEquals(-1, ExceptionUtils.indexOfThrowable(withCause, null, 0));
    assertEquals(0, ExceptionUtils.indexOfThrowable(withCause, ExceptionWithCause.class, 0));
    assertEquals(1, ExceptionUtils.indexOfThrowable(withCause, NestableException.class, 0));
    assertEquals(2, ExceptionUtils.indexOfThrowable(withCause, ExceptionWithoutCause.class, 0));

    assertEquals(0, ExceptionUtils.indexOfThrowable(withCause, ExceptionWithCause.class, -1));
    assertEquals(0, ExceptionUtils.indexOfThrowable(withCause, ExceptionWithCause.class, 0));
    assertEquals(-1, ExceptionUtils.indexOfThrowable(withCause, ExceptionWithCause.class, 1));
    assertEquals(-1, ExceptionUtils.indexOfThrowable(withCause, ExceptionWithCause.class, 9));

    assertEquals(-1, ExceptionUtils.indexOfThrowable(withCause, Exception.class, 0));
    assertEquals(-1, ExceptionUtils.indexOfThrowable(withCause, Throwable.class, 0));
}

@Test
public void testThrowableOf_ThrowableClassInt() {
    assertEquals(null, ExceptionUtils.throwableOfThrowable(null, null, 0));
    assertEquals(null, ExceptionUtils.throwableOfThrowable(null, NestableException.class, 0));

    assertEquals(null, ExceptionUtils.throwableOfThrowable(withoutCause, null));
    assertEquals(null, ExceptionUtils.throwableOfThrowable(withoutCause, ExceptionWithCause.class, 0));
    assertEquals(null, ExceptionUtils.throwableOfThrowable(withoutCause, NestableException.class, 0));
    assertEquals(withoutCause, ExceptionUtils.throwableOfThrowable(withoutCause, ExceptionWithoutCause.class, 0));

    assertEquals(null, ExceptionUtils.throwableOfThrowable(nested, null, 0));
    assertEquals(null, ExceptionUtils.throwableOfThrowable(nested, ExceptionWithCause.class, 0));
    assertEquals(nested, ExceptionUtils.throwableOfThrowable(nested, NestableException.class, 0));
    assertEquals(nested.getCause(), ExceptionUtils.throwableOfThrowable(nested, ExceptionWithoutCause.class, 0));

    assertEquals(null, ExceptionUtils.throwableOfThrowable(withCause, null));
    assertEquals(withCause, ExceptionUtils.throwableOfThrowable(withCause, ExceptionWithCause.class, 0));
    assertEquals(withCause.getCause(), ExceptionUtils.throwableOfThrowable(withCause, NestableException.class, 0));
    assertEquals(withCause.getCause().getCause(), ExceptionUtils.throwableOfThrowable(withCause, ExceptionWithoutCause.class, 0));

    assertEquals(withCause, ExceptionUtils.throwableOfThrowable(withCause, ExceptionWithCause.class, -1));
    assertEquals(withCause, ExceptionUtils.throwableOfThrowable(withCause, ExceptionWithCause.class, 0));
    assertEquals(null, ExceptionUtils.throwableOfThrowable(withCause, ExceptionWithCause.class, 1));
    assertEquals(null, ExceptionUtils.throwableOfThrowable(withCause, ExceptionWithCause.class, 9));

    assertEquals(null, ExceptionUtils.throwableOfThrowable(withCause, Exception.class, 0));
    assertEquals(null, ExceptionUtils.throwableOfThrowable(withCause, Throwable.class, 0));
}

@Test
public void testIndexOfType_ThrowableClass() {
    assertEquals(-1, ExceptionUtils.indexOfType(null, null));
    assertEquals(-1, ExceptionUtils.indexOfType(null, NestableException.class));

    assertEquals(-1, ExceptionUtils.indexOfType(withoutCause, null));
    assertEquals(-1, ExceptionUtils.indexOfType(withoutCause, ExceptionWithCause.class));
    assertEquals(-1, ExceptionUtils.indexOfType(withoutCause, NestableException.class));
    assertEquals(0, ExceptionUtils.indexOfType(withoutCause, ExceptionWithoutCause.class));

    assertEquals(-1, ExceptionUtils.indexOfType(nested, null));
    assertEquals(-1, ExceptionUtils.indexOfType(nested, ExceptionWithCause.class));
    assertEquals(0, ExceptionUtils.indexOfType(nested, NestableException.class));
    assertEquals(1, ExceptionUtils.indexOfType(nested, ExceptionWithoutCause.class));

    assertEquals(-1, ExceptionUtils.indexOfType(withCause, null));
    assertEquals(0, ExceptionUtils.indexOfType(withCause, ExceptionWithCause.class));
    assertEquals(1, ExceptionUtils.indexOfType(withCause, NestableException.class));
    assertEquals(2, ExceptionUtils.indexOfType(withCause, ExceptionWithoutCause.class));

    assertEquals(0, ExceptionUtils.indexOfType(withCause, Exception.class));
    assertEquals(0, ExceptionUtils.indexOfType(withCause, Throwable.class));
}

@Test
public void testThrowableOfType_ThrowableClass() {
    assertEquals(null, ExceptionUtils.throwableOfType(null, null));
    assertEquals(null, ExceptionUtils.throwableOfType(null, NestableException.class));

    assertEquals(null, ExceptionUtils.throwableOfType(withoutCause, null));
    assertEquals(null, ExceptionUtils.throwableOfType(withoutCause, ExceptionWithCause.class));
    assertEquals(null, ExceptionUtils.throwableOfType(withoutCause, NestableException.class));
    assertEquals(withoutCause, ExceptionUtils.throwableOfType(withoutCause, ExceptionWithoutCause.class));

    assertEquals(null, ExceptionUtils.throwableOfType(nested, null));
    assertEquals(null, ExceptionUtils.throwableOfType(nested, ExceptionWithCause.class));
    assertEquals(nested, ExceptionUtils.throwableOfType(nested, NestableException.class));
    assertEquals(nested.getCause(), ExceptionUtils.throwableOfType(nested, ExceptionWithoutCause.class));

    assertEquals(null, ExceptionUtils.throwableOfType(withCause, null));
    assertEquals(withCause, ExceptionUtils.throwableOfType(withCause, ExceptionWithCause.class));
    assertEquals(withCause.getCause(), ExceptionUtils.throwableOfType(withCause, NestableException.class));
    assertEquals(withCause.getCause().getCause(), ExceptionUtils.throwableOfType(withCause, ExceptionWithoutCause.class));

    assertEquals(withCause, ExceptionUtils.throwableOfType(withCause, Exception.class));
    assertEquals(withCause, ExceptionUtils.throwableOfType(withCause, Throwable.class));
}

@Test
public void testIndexOfType_ThrowableClassInt() {
    assertEquals(-1, ExceptionUtils.indexOfType(null, null, 0));
    assertEquals(-1, ExceptionUtils.indexOfType(null, NestableException.class, 0));

    assertEquals(-1, ExceptionUtils.indexOfType(withoutCause, null, 0));
    assertEquals(-1, ExceptionUtils.indexOfType(withoutCause, ExceptionWithCause.class, 0));
    assertEquals(-1, ExceptionUtils.indexOfType(withoutCause, NestableException.class, 0));
    assertEquals(0, ExceptionUtils.indexOfType(withoutCause, ExceptionWithoutCause.class, 0));

    assertEquals(-1, ExceptionUtils.indexOfType(nested, null, 0));
    assertEquals(-1, ExceptionUtils.indexOfType(nested, ExceptionWithCause.class, 0));
    assertEquals(0, ExceptionUtils.indexOfType(nested, NestableException.class, 0));
    assertEquals(1, ExceptionUtils.indexOfType(nested, ExceptionWithoutCause.class, 0));

    assertEquals(-1, ExceptionUtils.indexOfType(withCause, null, 0));
    assertEquals(0, ExceptionUtils.indexOfType(withCause, ExceptionWithCause.class, 0));
    assertEquals(1, ExceptionUtils.indexOfType(withCause, NestableException.class, 0));
    assertEquals(2, ExceptionUtils.indexOfType(withCause, ExceptionWithoutCause.class, 0));

    assertEquals(0, ExceptionUtils.indexOfType(withCause, ExceptionWithCause.class, -1));
    assertEquals(0, ExceptionUtils.indexOfType(withCause, ExceptionWithCause.class, 0));
    assertEquals(-1, ExceptionUtils.indexOfType(withCause, ExceptionWithCause.class, 1));
    assertEquals(-1, ExceptionUtils.indexOfType(withCause, ExceptionWithCause.class, 9));

    assertEquals(0, ExceptionUtils.indexOfType(withCause, Exception.class, 0));
    assertEquals(0, ExceptionUtils.indexOfType(withCause, Throwable.class, 0));
}

@Test
public void testThrowableOfType_ThrowableClassInt() {
    assertEquals(null, ExceptionUtils.throwableOfType(null, null, 0));
    assertEquals(null, ExceptionUtils.throwableOfType(null, NestableException.class, 0));

    assertEquals(null, ExceptionUtils.throwableOfType(withoutCause, null));
    assertEquals(null, ExceptionUtils.throwableOfType(withoutCause, ExceptionWithCause.class, 0));
    assertEquals(null, ExceptionUtils.throwableOfType(withoutCause, NestableException.class, 0));
    assertEquals(withoutCause, ExceptionUtils.throwableOfType(withoutCause, ExceptionWithoutCause.class, 0));

    assertEquals(null, ExceptionUtils.throwableOfType(nested, null, 0));
    assertEquals(null, ExceptionUtils.throwableOfType(nested, ExceptionWithCause.class, 0));
    assertEquals(nested, ExceptionUtils.throwableOfType(nested, NestableException.class, 0));
    assertEquals(nested.getCause(), ExceptionUtils.throwableOfType(nested, ExceptionWithoutCause.class, 0));

    assertEquals(null, ExceptionUtils.throwableOfType(withCause, null));
    assertEquals(withCause, ExceptionUtils.throwableOfType(withCause, ExceptionWithCause.class, 0));
    assertEquals(withCause.getCause(), ExceptionUtils.throwableOfType(withCause, NestableException.class, 0));
    assertEquals(withCause.getCause().getCause(), ExceptionUtils.throwableOfType(withCause, ExceptionWithoutCause.class, 0));

    assertEquals(withCause, ExceptionUtils.throwableOfType(withCause, ExceptionWithCause.class, -1));
    assertEquals(withCause, ExceptionUtils.throwableOfType(withCause, ExceptionWithCause.class, 0));
    assertEquals(null, ExceptionUtils.throwableOfType(withCause, ExceptionWithCause.class, 1));
    assertEquals(null, ExceptionUtils.throwableOfType(withCause, ExceptionWithCause.class, 9));

    assertEquals(withCause, ExceptionUtils.throwableOfType(withCause, Exception.class, 0));
    assertEquals(withCause, ExceptionUtils.throwableOfType(withCause, Throwable.class, 0));
}

@SuppressWarnings("unused")
public void getTargetException() {
    // noop
}
```