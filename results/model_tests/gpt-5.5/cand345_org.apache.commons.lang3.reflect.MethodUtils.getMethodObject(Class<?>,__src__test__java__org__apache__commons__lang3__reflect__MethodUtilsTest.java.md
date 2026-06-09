# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `dc9e94626e19615b8970e2ba2532a7d11ea8f5da`
- B: `8a7b0da6fc783127f8272d955d9f06f1966949ec`
- test: `src/test/java/org/apache/commons/lang3/reflect/MethodUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/reflect/MethodUtils.java']`
- old_test_mode: `methods`
- user_chars: `19635`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 4962, 'completion_tokens': 1721, 'total_tokens': 6683}`

---

- 修改 `testGetMethodObject`：覆盖 `getMethodObject` 在 `cls` 或 `name` 为 `null`、以及参数类型数组包含 `null` 时返回 `null` 的新行为；无需调整 import。
- 修改 `testInvokeExactMethod`：`methodName` 为 `null` 时现在通过 `getMethodObject` 返回 `null` 并最终抛出 `NoSuchMethodException`，因此更新对应断言；无需调整 import。
- 修改 `testInvokeMethod`：普通 `invokeMethod` 在目标对象非空但方法名为 `null` 时现在抛出 `NoSuchMethodException`，因此更新对应断言；无需调整 import。

```java
@Test
void testGetMethodObject() throws Exception {
    assertEquals(MutableObject.class.getMethod("getValue", ArrayUtils.EMPTY_CLASS_ARRAY),
            MethodUtils.getMethodObject(MutableObject.class, "getValue", ArrayUtils.EMPTY_CLASS_ARRAY));
    assertNull(MethodUtils.getMethodObject(MutableObject.class, "does not exist, at all", ArrayUtils.EMPTY_CLASS_ARRAY));
    assertNull(MethodUtils.getMethodObject(null, "does not exist, at all", ArrayUtils.EMPTY_CLASS_ARRAY));
    assertNull(MethodUtils.getMethodObject(null, null, ArrayUtils.EMPTY_CLASS_ARRAY));
    assertNull(MethodUtils.getMethodObject(MutableObject.class, null, ArrayUtils.EMPTY_CLASS_ARRAY));
    // 0 args
    assertNull(MethodUtils.getMethodObject(MutableObject.class, "getValue", new Class[] { null }));
    // 1 args
    assertNull(MethodUtils.getMethodObject(MutableObject.class, "equals", new Class[] { null }));
    assertNull(MethodUtils.getMethodObject(MutableObject.class, "equals", new Class[] { String.class, null, String.class }));
}

@Test
void testInvokeExactMethod() throws Exception {
    assertEquals("foo()", MethodUtils.invokeExactMethod(testBean, "foo", (Object[]) ArrayUtils.EMPTY_CLASS_ARRAY));
    assertEquals("foo()", MethodUtils.invokeExactMethod(testBean, "foo"));
    assertEquals("foo()", MethodUtils.invokeExactMethod(testBean, "foo", (Object[]) null));
    assertEquals("foo()", MethodUtils.invokeExactMethod(testBean, "foo", null, null));
    assertEquals("foo(String)", MethodUtils.invokeExactMethod(testBean, "foo", ""));
    assertEquals("foo(Object)", MethodUtils.invokeExactMethod(testBean, "foo", new Object()));
    assertEquals("foo(Integer)", MethodUtils.invokeExactMethod(testBean, "foo", NumberUtils.INTEGER_ONE));
    assertEquals("foo(double)", MethodUtils.invokeExactMethod(testBean, "foo", new Object[] { NumberUtils.DOUBLE_ONE }, new Class[] { Double.TYPE }));
    assertThrows(NoSuchMethodException.class, () -> MethodUtils.invokeExactMethod(testBean, "foo", NumberUtils.BYTE_ONE));
    assertThrows(NoSuchMethodException.class, () -> MethodUtils.invokeExactMethod(testBean, "foo", NumberUtils.LONG_ONE));
    assertThrows(NoSuchMethodException.class, () -> MethodUtils.invokeExactMethod(testBean, "foo", Boolean.TRUE));
    assertThrows(NullPointerException.class, () -> MethodUtils.invokeExactMethod(null, "foo", NumberUtils.BYTE_ONE));
    assertThrows(NoSuchMethodException.class, () -> MethodUtils.invokeExactMethod(testBean, null, NumberUtils.BYTE_ONE));
    assertThrows(NullPointerException.class,
            () -> MethodUtils.invokeExactMethod(null, "foo", new Object[] { NumberUtils.DOUBLE_ONE }, new Class[] { Double.TYPE }));
    assertThrows(NoSuchMethodException.class,
            () -> MethodUtils.invokeExactMethod(testBean, null, new Object[] { NumberUtils.DOUBLE_ONE }, new Class[] { Double.TYPE }));
}

@Test
void testInvokeMethod() throws Exception {
    assertEquals("foo()", MethodUtils.invokeMethod(testBean, "foo", (Object[]) ArrayUtils.EMPTY_CLASS_ARRAY));
    assertEquals("foo()", MethodUtils.invokeMethod(testBean, "foo"));
    assertEquals("foo()", MethodUtils.invokeMethod(testBean, "foo", (Object[]) null));
    assertEquals("foo()", MethodUtils.invokeMethod(testBean, "foo", null, null));
    assertEquals("foo(String)", MethodUtils.invokeMethod(testBean, "foo", ""));
    assertEquals("foo(Object)", MethodUtils.invokeMethod(testBean, "foo", new Object()));
    assertEquals("foo(Object)", MethodUtils.invokeMethod(testBean, "foo", Boolean.TRUE));
    assertEquals("foo(Integer)", MethodUtils.invokeMethod(testBean, "foo", NumberUtils.INTEGER_ONE));
    assertEquals("foo(int)", MethodUtils.invokeMethod(testBean, "foo", NumberUtils.BYTE_ONE));
    assertEquals("foo(long)", MethodUtils.invokeMethod(testBean, "foo", NumberUtils.LONG_ONE));
    assertEquals("foo(double)", MethodUtils.invokeMethod(testBean, "foo", NumberUtils.DOUBLE_ONE));
    assertEquals("foo(String...)", MethodUtils.invokeMethod(testBean, "foo", "a", "b", "c"));
    assertEquals("foo(String...)", MethodUtils.invokeMethod(testBean, "foo", "a", "b", "c"));
    assertEquals("foo(int, String...)", MethodUtils.invokeMethod(testBean, "foo", 5, "a", "b", "c"));
    assertEquals("foo(long...)", MethodUtils.invokeMethod(testBean, "foo", 1L, 2L));

    assertThrows(NoSuchMethodException.class, () -> MethodUtils.invokeMethod(testBean, "foo", 1, 2));

    TestBean.verify(new ImmutablePair<>("String...", new String[] { "x", "y" }), MethodUtils.invokeMethod(testBean, "varOverloadEcho", "x", "y"));
    TestBean.verify(new ImmutablePair<>("Number...", new Number[] { 17, 23, 42 }), MethodUtils.invokeMethod(testBean, "varOverloadEcho", 17, 23, 42));
    TestBean.verify(new ImmutablePair<>("String...", new String[] { "x", "y" }), MethodUtils.invokeMethod(testBean, "varOverloadEcho", "x", "y"));
    TestBean.verify(new ImmutablePair<>("Number...", new Number[] { 17, 23, 42 }), MethodUtils.invokeMethod(testBean, "varOverloadEcho", 17, 23, 42));

    assertNullPointerException(() -> MethodUtils.invokeMethod(null, "foo", 1, 2));
    assertThrows(NoSuchMethodException.class, () -> MethodUtils.invokeMethod(testBean, null, 1, 2));
}
```