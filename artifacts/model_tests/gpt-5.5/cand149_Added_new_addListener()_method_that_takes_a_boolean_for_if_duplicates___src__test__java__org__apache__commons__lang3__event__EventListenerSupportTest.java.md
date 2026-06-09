# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `71d7c3264239c55b6e2daf89c44c5685085f26dd`
- B: `a48071b0d489420bfdc0c2ed7254d1dba243f700`
- test: `src/test/java/org/apache/commons/lang3/event/EventListenerSupportTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/event/EventListenerSupport.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `13157`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3157, 'completion_tokens': 349, 'total_tokens': 3506}`

---

- 新增 `testAddListenerNoDuplicates`：覆盖生产代码新增的 `addListener(listener, allowDuplicate)` 在 `allowDuplicate=false` 时不重复添加同一监听器对象的行为。
- import 无需调整：新增测试复用现有 `assertEquals`、`assertSame`、`EasyMock`、`VetoableChangeListener` 与 `@Test` 导入。

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