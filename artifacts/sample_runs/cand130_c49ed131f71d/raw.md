# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `07914b39281e4be500d430b2c25e85499748788f`
- B: `c49ed131f71dae68c1856d58918b322aa4ba6017`
- test: `src/test/java/org/apache/commons/lang3/function/FailableTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/function/Failable.java']`
- old_test_mode: `methods`
- user_chars: `23644`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6681, 'completion_tokens': 1530, 'total_tokens': 8211, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 6425}`

---

- 将 `testApplyNotNull` 方法重命名为 `testApplyNonNull`，并将方法体内所有 `Failable.applyNotNull` 调用改为 `Failable.applyNonNull`。
- 将 `testApplyNotNull2` 方法重命名为 `testApplyNonNull2`，并将方法体内所有 `Failable.applyNotNull` 调用改为 `Failable.applyNonNull`。
- 将 `testApplyNotNull3` 方法重命名为 `testApplyNonNull3`，并将方法体内所有 `Failable.applyNotNull` 调用改为 `Failable.applyNonNull`。
- 无需调整 import，因为方法名变更不涉及新类型引入。

```java
// IMPORTS_START
// 无需新增或修改 import
// IMPORTS_END

    @Test
    void testApplyNonNull() throws SomeException {
        // No checked exceptions in signatures
        assertEquals("A", Failable.applyNonNull("a", String::toUpperCase));
        assertNull(Failable.applyNonNull((String) null, String::toUpperCase));
        assertNull(Failable.applyNonNull("a", s -> null));
        assertThrows(NullPointerException.class, () -> Failable.applyNonNull("a", null));
        // Checked exceptions in signatures
        final FailureOnInvocationCount obj1 = new FailureOnInvocationCount(1);
        assertEquals(1, assertThrows(SomeException.class, () -> Failable.applyNonNull(1, obj1::inc)).value);
        assertEquals(2, Failable.applyNonNull(1, obj1::inc));
    }

    @Test
    void testApplyNonNull2() throws SomeException, IOException {
        // No checked exceptions in signatures
        assertEquals("A", Failable.applyNonNull(" a ", String::toUpperCase, String::trim));
        assertNull(Failable.applyNonNull((String) null, String::toUpperCase, String::trim));
        assertNull(Failable.applyNonNull(" a ", s -> null, String::trim));
        assertNull(Failable.applyNonNull(" a ", String::toUpperCase, s -> null));
        assertThrows(NullPointerException.class, () -> Failable.applyNonNull(" a ", null, String::trim));
        assertThrows(NullPointerException.class, () -> Failable.applyNonNull(" a ", String::toUpperCase, null));
        // Same checked exceptions in signatures
        final FailureOnInvocationCount obj1 = new FailureOnInvocationCount(1);
        final FailureOnInvocationCount obj2 = new FailureOnInvocationCount(2);
        assertEquals(1, assertThrows(SomeException.class, () -> Failable.applyNonNull(1, obj1::inc, obj1::inc)).value);
        assertEquals(2, assertThrows(SomeException.class, () -> Failable.applyNonNull(1, obj2::inc, obj2::inc)).value);
        assertEquals(3, Failable.applyNonNull(1, obj1::inc, obj1::inc));
        assertEquals(3, Failable.applyNonNull(1, obj2::inc, obj2::inc));
        // Different checked exceptions in signatures
        obj1.reset();
        obj2.reset();
        assertEquals(1, assertThrows(SomeException.class, () -> Failable.applyNonNull(1, obj1::inc, obj1::incIo)).value);
        assertEquals(2, ((SomeException) assertThrows(IOException.class, () -> Failable.applyNonNull(1, obj2::inc, obj2::incIo)).getCause()).value);
        assertEquals(3, Failable.applyNonNull(1, obj1::inc, obj1::incIo));
        assertEquals(3, Failable.applyNonNull(1, obj2::inc, obj2::incIo));
    }

    @Test
    void testApplyNonNull3() throws SomeException, IOException, ClassNotFoundException {
        // No checked exceptions in signatures
        assertEquals("CBA", Failable.applyNonNull(" abc ", String::toUpperCase, String::trim, StringUtils::reverse));
        assertNull(Failable.applyNonNull((String) null, String::toUpperCase, String::trim, StringUtils::reverse));
        assertNull(Failable.applyNonNull(" abc ", s -> null, String::trim, StringUtils::reverse));
        assertNull(Failable.applyNonNull(" abc ", String::toUpperCase, s -> null, StringUtils::reverse));
        assertNull(Failable.applyNonNull(" abc ", String::toUpperCase, String::trim, s -> null));
        assertThrows(NullPointerException.class, () -> Failable.applyNonNull(" abc ", null, String::trim, StringUtils::reverse));
        assertThrows(NullPointerException.class, () -> Failable.applyNonNull(" abc ", String::toUpperCase, null, StringUtils::reverse));
        assertThrows(NullPointerException.class, () -> Failable.applyNonNull(" abc ", String::toUpperCase, String::trim, null));
        // Same checked exceptions in signatures
        final FailureOnInvocationCount obj1 = new FailureOnInvocationCount(1);
        final FailureOnInvocationCount obj2 = new FailureOnInvocationCount(2);
        final FailureOnInvocationCount obj3 = new FailureOnInvocationCount(3);
        assertEquals(1, assertThrows(SomeException.class, () -> Failable.applyNonNull(1, obj1::inc, obj1::inc, obj1::inc)).value);
        assertEquals(2, assertThrows(SomeException.class, () -> Failable.applyNonNull(1, obj2::inc, obj2::inc, obj2::inc)).value);
        assertEquals(3, assertThrows(SomeException.class, () -> Failable.applyNonNull(1, obj3::inc, obj3::inc, obj3::inc)).value);
        assertEquals(4, Failable.applyNonNull(1, obj1::inc, obj1::inc, obj1::inc));
        assertEquals(4, Failable.applyNonNull(1, obj2::inc, obj2::inc, obj2::inc));
        assertEquals(4, Failable.applyNonNull(1, obj3::inc, obj3::inc, obj3::inc));
        // Different checked exceptions in signatures
        obj1.reset();
        obj2.reset();
        obj3.reset();
        assertEquals(1, assertThrows(SomeException.class, () -> Failable.applyNonNull(1, obj1::inc, obj1::incIo, obj1::incIo)).value);
        assertEquals(2, ((SomeException) assertThrows(IOException.class, () -> Failable.applyNonNull(1, obj2::inc, obj2::incIo, obj2::incIo)).getCause()).value);
        assertEquals(3, ((SomeException) assertThrows(IOException.class, () -> Failable.applyNonNull(1, obj3::inc, obj3::incIo, obj3::incIo)).getCause()).value);
        assertEquals(4, Failable.applyNonNull(1, obj1::inc, obj1::incIo, obj1::incIo));
        assertEquals(4, Failable.applyNonNull(1, obj2::inc, obj2::incIo, obj2::incIo));
        assertEquals(4, Failable.applyNonNull(1, obj3::inc, obj3::incIo, obj3::incIo));
    }
```