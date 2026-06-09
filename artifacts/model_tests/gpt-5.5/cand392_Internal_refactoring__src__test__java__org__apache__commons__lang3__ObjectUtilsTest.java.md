# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `b9f15bc007be2bb0ba9633559482396e0352785a`
- B: `b7b52fc506ca531ce97c936b4b6d70f72a1125d3`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `40043`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9286, 'completion_tokens': 491, 'total_tokens': 9777}`

---

- 修改 `testGetFirstNonNull`：生产代码现在会先过滤掉 `null` supplier 再调用 `Supplier::get`，因此新增断言覆盖首个 vararg supplier 为 `null` 时仍返回后续非空值；无需调整 import。

```java
    @Test
    public void testGetFirstNonNull() {
        // first non-null
        assertEquals("", ObjectUtils.getFirstNonNull(null, () -> ""));
        assertEquals("", ObjectUtils.getFirstNonNull(Suppliers.nul(), () -> ""));
        // first encountered value is used
        assertEquals("1", ObjectUtils.getFirstNonNull(Suppliers.nul(), () -> "1", () -> "2", Suppliers.nul()));
        assertEquals("123", ObjectUtils.getFirstNonNull(() -> "123", Suppliers.nul(), () -> "456"));
        // don't evaluate suppliers after first value is found
        assertEquals("123", ObjectUtils.getFirstNonNull(Suppliers.nul(), () -> "123", () -> fail("Supplier after first non-null value should not be evaluated")));
        // supplier returning null and null supplier both result in null
        assertNull(ObjectUtils.getFirstNonNull(null, Suppliers.nul()));
        // Explicitly pass in an empty array of Object type to ensure compiler doesn't complain of unchecked generic array creation
        assertNull(ObjectUtils.getFirstNonNull());
        // supplier is null
        assertNull(ObjectUtils.getFirstNonNull((Supplier<Object>) null));
        // varargs array itself is null
        assertNull(ObjectUtils.getFirstNonNull((Supplier<Object>[]) null));
        // test different types
        assertEquals(1, ObjectUtils.getFirstNonNull(Suppliers.nul(), () -> 1));
        assertEquals(Boolean.TRUE, ObjectUtils.getFirstNonNull(Suppliers.nul(), () -> Boolean.TRUE));
    }
```