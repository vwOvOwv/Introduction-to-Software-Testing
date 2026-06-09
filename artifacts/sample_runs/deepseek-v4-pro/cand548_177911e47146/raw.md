# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `5a15ccb62eb88ffa41e6b62ac944066fb121afe8`
- B: `177911e47146db0df2e35839d6bd03ad1315916c`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `43431`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 10603, 'completion_tokens': 2197, 'total_tokens': 12800, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1716}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 10219}`

---

- 新增 `testGetIfNullObject` 方法，对应新增的 `ObjectUtils.getIfNull(T, T)` 方法。
- 新增 `testGetIfNullSupplier` 方法，覆盖原有的 `ObjectUtils.getIfNull(T, Supplier<T>)` 方法并提取自旧测试，确保新重载无歧义且断言通过。
- 无需修改或删除任何现存的 `@Test` 方法；`testDefaultIfNull` 仍可编译并成功运行。
- 现有 import 已包含 `Supplier`、`MutableInt` 等所有需要的类型，无需调整 import。

```java
@Test
public void testGetIfNullObject() {
    final Object o = FOO;
    final Object defaultObject = BAR;
    assertNull(ObjectUtils.getIfNull(null, (Object) null));
    assertSame(defaultObject, ObjectUtils.getIfNull(null, defaultObject), "dflt was not returned when o was null");
    assertSame(o, ObjectUtils.getIfNull(o, defaultObject), "dflt was returned when o was not null");
}

@Test
public void testGetIfNullSupplier() {
    final Object o = FOO;
    final Object defaultObject = BAR;
    assertNull(ObjectUtils.getIfNull(null, (Supplier<Object>) null));
    assertSame(defaultObject, ObjectUtils.getIfNull(null, () -> defaultObject), "dflt was not returned when o was null");
    assertSame(o, ObjectUtils.getIfNull(o, () -> defaultObject), "dflt was returned when o was not null");
    assertSame(o, ObjectUtils.getIfNull(FOO, () -> defaultObject), "dflt was returned when o was not null");
    assertSame(o, ObjectUtils.getIfNull("foo", () -> defaultObject), "dflt was returned when o was not null");
    final MutableInt callsCounter = new MutableInt(0);
    final Supplier<Object> countingDefaultSupplier = () -> {
        callsCounter.increment();
        return defaultObject;
    };
    ObjectUtils.getIfNull(o, countingDefaultSupplier);
    assertEquals(0, callsCounter.getValue());
    ObjectUtils.getIfNull(null, countingDefaultSupplier);
    assertEquals(1, callsCounter.getValue());
}
```