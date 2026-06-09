# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `949c911a87c598ac694966bddf203eae59f06e76`
- B: `110ab39cb236fd7e6f517c8dc3b389fa215c0020`
- test: `src/test/java/org/apache/commons/lang3/function/ObjectsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/function/Objects.java']`
- old_test_mode: `methods`
- user_chars: `9983`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2671, 'completion_tokens': 2271, 'total_tokens': 4942, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1386}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2287}`

---

- 修改 testRequireNonNullObject、testRequireNonNullObjectString、testRequireNonNullObjectSupplierString、testRequireNonNullObjectFailableSupplierString 四个测试方法，catch 块异常参数添加 final 修饰符。
- 修改内部类 TestableSupplier 和 TestableFailableSupplier 的构造函数参数添加 final 修饰符。
- 无需调整 import。

```java
// IMPORTS_START
// 无需修改 import
// IMPORTS_END

public static class TestableSupplier<O> implements Supplier<O> {
    private final Supplier<O> supplier;
    private boolean invoked;

    TestableSupplier(final Supplier<O> pSupplier) {
        this.supplier = pSupplier;
    }

    @Override
    public O get() {
        invoked = true;
        return supplier.get();
    }

    public boolean isInvoked() {
        return invoked;
    }
}

public static class TestableFailableSupplier<O, E extends Exception> implements FailableSupplier<O, E> {
    private final FailableSupplier<O, E> supplier;
    private boolean invoked;

    TestableFailableSupplier(final FailableSupplier<O, E> pSupplier) {
        this.supplier = pSupplier;
    }

    @Override
    public O get() throws E {
        invoked = true;
        return supplier.get();
    }

    public boolean isInvoked() {
        return invoked;
    }
}

@Test
void testRequireNonNullObject() {
    assertSame("foo", Objects.requireNonNull("foo"));
    try {
        Objects.requireNonNull(null);
        fail("Expected Exception");
    } catch (final NullPointerException e) {
        assertEquals("The value must not be null.", e.getMessage());
    }
}

@Test
void testRequireNonNullObjectString() {
    assertSame("foo", Objects.requireNonNull("foo", "bar"));
    try {
        Objects.requireNonNull(null, "bar");
        fail("Expected Exception");
    } catch (final NullPointerException e) {
        assertEquals("bar", e.getMessage());
    }
}

@Test
void testRequireNonNullObjectSupplierString() {
    final TestableSupplier<String> supplier = new TestableSupplier<>(() -> "bar");
    assertSame("foo", Objects.requireNonNull("foo", supplier));
    assertFalse(supplier.isInvoked());
    try {
        Objects.requireNonNull(null, supplier);
        fail("Expected Exception");
    } catch (final NullPointerException e) {
        assertEquals("bar", e.getMessage());
        assertTrue(supplier.isInvoked());
    }
}

@Test
void testRequireNonNullObjectFailableSupplierString() {
    final TestableFailableSupplier<String, ?> supplier = new TestableFailableSupplier<>(() -> {
        return null;
    });
    assertSame("foo", Objects.requireNonNull("foo", supplier));
    assertFalse(supplier.isInvoked());
    try {
        Objects.requireNonNull(null, supplier);
        fail("Expected Exception");
    } catch (final NullPointerException e) {
        assertEquals("The supplier must not return null.", e.getMessage());
        assertTrue(supplier.isInvoked());
    }
    final TestableFailableSupplier<String, ?> supplier2 = new TestableFailableSupplier<>(() -> {
        return null;
    });
    try {
        Objects.requireNonNull(null, supplier2);
        fail("Expected Exception");
    } catch (final NullPointerException e) {
        assertEquals("The supplier must not return null.", e.getMessage());
        assertTrue(supplier2.isInvoked());
    }
    final TestableFailableSupplier<String, ?> supplier3 = new TestableFailableSupplier<>(() -> {
        return "bar";
    });
    assertSame("bar", Objects.requireNonNull(null, supplier3));
    final RuntimeException rte = new RuntimeException();
    final TestableFailableSupplier<String, ?> supplier4 = new TestableFailableSupplier<>(() -> {
        throw rte;
    });
    try {
        Objects.requireNonNull(null, supplier4);
        fail("Expected Exception");
    } catch (final RuntimeException e) {
        assertSame(rte, e);
        assertTrue(supplier4.isInvoked());
    }
}
```