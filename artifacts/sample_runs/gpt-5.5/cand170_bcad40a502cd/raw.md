# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `5e9736adf2b27f0a65cfa3fff9180cb34fac30c0`
- B: `bcad40a502cd45b49a5e025938b9711d95c7bde7`
- test: `src/test/java/org/apache/commons/lang3/reflect/TypeUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/reflect/TypeUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `66167`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 14733, 'completion_tokens': 613, 'total_tokens': 15346}`

---

- 新增 `testIsAssignable_ClassWithParameterizedType`，覆盖生产代码对 `Class<T>` 参数化类型赋值规则收紧后的行为断言。
- 新增测试辅助嵌套类型 `TestIF`、`TestImpl`、`TestImpl2`，用于构造 `Class<TestIF>` / `Class<TestImpl>` / `Class<TestImpl2>` 的参数化类型场景。
- 不需要调整 import，旧测试文件中已有 `assertFalse`、`ParameterizedType`、`Type` 和 `@Test` 所需导入。

```java
@Test
void testIsAssignable_ClassWithParameterizedType() {
    final ParameterizedType topre1 = TypeUtils.parameterize(TestIF.class, TypeUtils.wildcardType().build());
    final Type to1 = TypeUtils.parameterize(Class.class, TypeUtils.wildcardType().withUpperBounds(topre1).build());
    final Type from1 = TypeUtils.parameterize(Class.class, TestIF.class);
    assertFalse(TypeUtils.isAssignable(from1, to1), "Class<TestIF> should not be assignable to Class<? extends TestIF<?>>");

    final ParameterizedType topre2 = TypeUtils.parameterize(TestIF.class, TypeUtils.wildcardType().build());
    final Type to2 = TypeUtils.parameterize(Class.class, TypeUtils.wildcardType().withUpperBounds(topre2).build());
    final Type from2 = TypeUtils.parameterize(Class.class, TestImpl.class);
    assertFalse(TypeUtils.isAssignable(from2, to2), "Class<TestImpl> should not be assignable to Class<? extends TestIF<?>>");

    final ParameterizedType topre3 = TypeUtils.parameterize(TestIF.class, Number.class);
    final Type to3 = TypeUtils.parameterize(Class.class, TypeUtils.wildcardType().withUpperBounds(topre3).build());
    final Type from3 = TypeUtils.parameterize(Class.class, TestImpl2.class);
    assertFalse(TypeUtils.isAssignable(from3, to3), "Class<TestImpl2> should not be assignable to Class<? extends TestIF<Number>>");
}

private interface TestIF<T> {
}

private static class TestImpl<T> implements TestIF<T> {
}

private static class TestImpl2<R> implements TestIF<Number> {
}
```