# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `7912894eb8545ea076732a95dc0124d6426b3e76`
- B: `70b2250f80ac098e3fbb136bcd765ad90e8d3c0e`
- test: `src/test/java/org/apache/commons/lang3/exception/ExceptionUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/exception/ExceptionUtils.java']`
- old_test_mode: `methods`
- user_chars: `11064`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3154, 'completion_tokens': 6427, 'total_tokens': 9581, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 5405}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2770}`

---

- 新增 `import java.util.ArrayList;` 和 `import java.util.stream.Collectors;`，为 `testForEach_*`、`testStream_*` 中的集合操作与收集器提供支持。  
- 新增 6 个 `@Test` 方法：`testForEach_jdkNoCause`、`testForEach_nested`、`testForEach_null`、`testForEach_recursiveCause`、`testForEach_withCause`、`testForEach_withoutCause`，对应生产代码新增的 `forEach` 方法。  
- 新增 6 个 `@Test` 方法：`testStream_jdkNoCause`、`testStream_nested`、`testStream_null`、`testStream_recursiveCause`、`testStream_withCause`、`testStream_withoutCause`，对应生产代码新增的 `stream` 方法。  
- 不包括删除或修改旧测试方法；原 `testIndexOfType_ThrowableClassInt` 保持不变。

```java
// IMPORTS_START
import java.util.ArrayList;
import java.util.stream.Collectors;
// IMPORTS_END

@Test
public void testForEach_jdkNoCause() {
    final List<Throwable> throwables = new ArrayList<>();
    ExceptionUtils.forEach(jdkNoCause, throwables::add);
    assertEquals(1, throwables.size());
    assertSame(jdkNoCause, throwables.get(0));
}

@Test
public void testForEach_nested() {
    final List<Throwable> throwables = new ArrayList<>();
    ExceptionUtils.forEach(nested, throwables::add);
    assertEquals(2, throwables.size());
    assertSame(nested, throwables.get(0));
    assertSame(withoutCause, throwables.get(1));
}

@Test
public void testForEach_null() {
    final List<Throwable> throwables = new ArrayList<>();
    ExceptionUtils.forEach(null, throwables::add);
    assertEquals(0, throwables.size());
}

@Test
public void testForEach_recursiveCause() {
    final List<Throwable> throwables = new ArrayList<>();
    ExceptionUtils.forEach(cyclicCause, throwables::add);
    assertEquals(3, throwables.size());
    assertSame(cyclicCause, throwables.get(0));
    assertSame(cyclicCause.getCause(), throwables.get(1));
    assertSame(cyclicCause.getCause().getCause(), throwables.get(2));
}

@Test
public void testForEach_withCause() {
    final List<Throwable> throwables = new ArrayList<>();
    ExceptionUtils.forEach(withCause, throwables::add);
    assertEquals(3, throwables.size());
    assertSame(withCause, throwables.get(0));
    assertSame(nested, throwables.get(1));
    assertSame(withoutCause, throwables.get(2));
}

@Test
public void testForEach_withoutCause() {
    final List<Throwable> throwables = new ArrayList<>();
    ExceptionUtils.forEach(withoutCause, throwables::add);
    assertEquals(1, throwables.size());
    assertSame(withoutCause, throwables.get(0));
}

@Test
public void testStream_jdkNoCause() {
    assertEquals(1, ExceptionUtils.stream(jdkNoCause).count());
    assertSame(jdkNoCause, ExceptionUtils.stream(jdkNoCause).toArray()[0]);
}

@Test
public void testStream_nested() {
    assertEquals(2, ExceptionUtils.stream(nested).count());
    final Object[] array = ExceptionUtils.stream(nested).toArray();
    assertSame(nested, array[0]);
    assertSame(withoutCause, array[1]);
}

@Test
public void testStream_null() {
    assertEquals(0, ExceptionUtils.stream(null).count());
}

@Test
public void testStream_recursiveCause() {
    final List<?> throwables = ExceptionUtils.stream(cyclicCause).collect(Collectors.toList());
    assertEquals(3, throwables.size());
    assertSame(cyclicCause, throwables.get(0));
    assertSame(cyclicCause.getCause(), throwables.get(1));
    assertSame(cyclicCause.getCause().getCause(), throwables.get(2));
}

@Test
public void testStream_withCause() {
    final List<?> throwables = ExceptionUtils.stream(withCause).collect(Collectors.toList());
    assertEquals(3, throwables.size());
    assertSame(withCause, throwables.get(0));
    assertSame(nested, throwables.get(1));
    assertSame(withoutCause, throwables.get(2));
}

@Test
public void testStream_withoutCause() {
    final List<?> throwables = ExceptionUtils.stream(withoutCause).collect(Collectors.toList());
    assertEquals(1, throwables.size());
    assertSame(withoutCause, throwables.get(0));
}
```