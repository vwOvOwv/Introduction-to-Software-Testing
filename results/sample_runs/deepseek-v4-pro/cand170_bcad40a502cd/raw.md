# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `5e9736adf2b27f0a65cfa3fff9180cb34fac30c0`
- B: `bcad40a502cd45b49a5e025938b9711d95c7bde7`
- test: `src/test/java/org/apache/commons/lang3/reflect/TypeUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/reflect/TypeUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `66167`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 15379, 'completion_tokens': 1533, 'total_tokens': 16912, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1044}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 14995}`

---

- 新增 @Test 方法 `testIsAssignable_ClassWithParameterizedType`，以验证生产代码新增的 `Class` 参数化类型严格赋值规则。
- 新增内部接口 `TestIF<T>`、内部类 `TestImpl<T>` 和 `TestImpl2<R>`，作为测试方法所需的类型 fixture。
- 无需调整 import，现有 import 已覆盖所有用到的类型。

```java
    private interface TestIF<T> {
    }

    private static class TestImpl<T> implements TestIF<T> {
    }

    private static class TestImpl2<R> implements TestIF<Number> {
    }

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
```