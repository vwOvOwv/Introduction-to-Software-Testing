# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `949c911a87c598ac694966bddf203eae59f06e76`
- B: `110ab39cb236fd7e6f517c8dc3b389fa215c0020`
- test: `src/test/java/org/apache/commons/lang3/function/ObjectsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/function/Objects.java']`
- old_test_mode: `methods`
- user_chars: `9983`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2670, 'completion_tokens': 934, 'total_tokens': 3604}`

---

- 修改 `testRequireNonNullObject`：对应生产方法参数改为 `final` 的代码风格调整，将 `catch` 参数改为 `final`；无需调整 import。
- 修改 `testRequireNonNullObjectString`：对应生产方法参数改为 `final` 的代码风格调整，将 `catch` 参数改为 `final`；无需调整 import。
- 修改 `testRequireNonNullObjectSupplierString`：对应生产方法参数改为 `final` 的代码风格调整，将 `catch` 参数改为 `final`；无需调整 import。
- 修改 `testRequireNonNullObjectFailableSupplierString`：对应生产方法参数及 `catch` 变量改为 `final` 的代码风格调整，将各 `catch` 参数改为 `final`；无需调整 import。

```java
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
```