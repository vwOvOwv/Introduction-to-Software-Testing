# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `71d7c3264239c55b6e2daf89c44c5685085f26dd`
- B: `a48071b0d489420bfdc0c2ed7254d1dba243f700`
- test: `src/test/java/org/apache/commons/lang3/event/EventListenerSupportTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/event/EventListenerSupport.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `13157`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3210, 'completion_tokens': 1455, 'total_tokens': 4665, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1195}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2826}`

---

- 新增 `@Test` 方法 `testAddListenerNoDuplicates`，验证生产代码新增的 `addListener(listener, boolean allowDuplicate)` 方法在 `allowDuplicate=false` 时能防止重复添加监听器。

```java
@Test
public void testAddListenerNoDuplicates() {
    final EventListenerSupport<VetoableChangeListener> listenerSupport = EventListenerSupport.create(VetoableChangeListener.class);

    final VetoableChangeListener[] listeners = listenerSupport.getListeners();
    assertEquals(0, listeners.length);
    assertEquals(VetoableChangeListener.class, listeners.getClass().getComponentType());
    final VetoableChangeListener[] empty = listeners;
    //for fun, show that the same empty instance is used 
    assertSame(empty, listenerSupport.getListeners());

    final VetoableChangeListener listener1 = EasyMock.createNiceMock(VetoableChangeListener.class);
    listenerSupport.addListener(listener1);
    assertEquals(1, listenerSupport.getListeners().length);
    listenerSupport.addListener(listener1, false);
    assertEquals(1, listenerSupport.getListeners().length);
    listenerSupport.removeListener(listener1);
    assertSame(empty, listenerSupport.getListeners());
}
```