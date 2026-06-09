# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `7912894eb8545ea076732a95dc0124d6426b3e76`
- B: `70b2250f80ac098e3fbb136bcd765ad90e8d3c0e`
- test: `src/test/java/org/apache/commons/lang3/exception/ExceptionUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/exception/ExceptionUtils.java']`
- old_test_mode: `methods`
- user_chars: `11064`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3148, 'completion_tokens': 1712, 'total_tokens': 4860}`

---

- 新增 `testForEach_jdkNoCause`，覆盖新增的 `ExceptionUtils.forEach(Throwable, Consumer)` 对无 cause 异常的遍历行为；需要新增 `ArrayList` import。
- 新增 `testForEach_nested`，覆盖 `forEach` 对嵌套 cause 链的遍历顺序。
- 新增 `testForEach_null`，覆盖 `forEach` 对 `null` 输入返回空遍历的行为。
- 新增 `testForEach_recursiveCause`，覆盖 `forEach` 对循环 cause 链的去重/截断行为。
- 新增 `testForEach_withCause`，覆盖 `forEach` 对多级 cause 链的遍历顺序。
- 新增 `testForEach_withoutCause`，覆盖 `forEach` 对无 cause 自定义异常的遍历行为。
- 新增 `testStream_jdkNoCause`，覆盖新增的 `ExceptionUtils.stream(Throwable)` 对无 cause 异常返回单元素 stream 的行为。
- 新增 `testStream_nested`，覆盖 `stream` 对嵌套 cause 链的顺序。
- 新增 `testStream_null`，覆盖 `stream` 对 `null` 输入返回空 stream 的行为。
- 新增 `testStream_recursiveCause`，覆盖 `stream` 对循环 cause 链的去重/截断行为；需要新增 `Collectors` import。
- 新增 `testStream_withCause`，覆盖 `stream` 对多级 cause 链的顺序。
- 新增 `testStream_withoutCause`，覆盖 `stream` 对无 cause 自定义异常返回单元素 stream 的行为。

```java
import java.util.ArrayList;
import java.util.stream.Collectors;

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