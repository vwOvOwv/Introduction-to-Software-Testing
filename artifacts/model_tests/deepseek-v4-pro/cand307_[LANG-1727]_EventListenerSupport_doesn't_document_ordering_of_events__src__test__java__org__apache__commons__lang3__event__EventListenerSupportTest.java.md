# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `a6af715f86ef658ceeff12d3ba65d99d1a1f8f0f`
- B: `6e2741da4d1ef471c7c552b91409b2deecbfcec9`
- test: `src/test/java/org/apache/commons/lang3/event/EventListenerSupportTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/event/EventListenerSupport.java']`
- old_test_mode: `methods`
- user_chars: `26705`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6130, 'completion_tokens': 4864, 'total_tokens': 10994, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 3367}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 5746}`

---

- 将 `testAddListenerNoDuplicates` 方法内部格式调整为 B 分支风格：移除多余空行，统一单行注释空格。
- 将 `testEventDispatchOrder` 方法内部格式调整为 B 分支风格：移除多余空行。
- 将 `testGetListeners` 方法内部格式调整为 B 分支风格：移除多余空行，统一单行注释空格。
- 将 `testSerialization` 方法内部格式调整为 B 分支风格：合并反序列化声明为一行，单行注释添加空格并移除多余空行。
- 将 `testSubclassInvocationHandling` 方法内部格式调整为 B 分支风格：移除匿名内部类及方法间的多余空行。
- import 无需调整，已存在必要导入。

```java
@Test
void testAddListenerNoDuplicates() {
    final EventListenerSupport<VetoableChangeListener> listenerSupport = EventListenerSupport.create(VetoableChangeListener.class);
    final VetoableChangeListener[] listeners = listenerSupport.getListeners();
    assertEquals(0, listeners.length);
    assertEquals(VetoableChangeListener.class, listeners.getClass().getComponentType());
    final VetoableChangeListener[] empty = listeners;
    // for fun, show that the same empty instance is used
    assertSame(empty, listenerSupport.getListeners());
    final VetoableChangeListener listener1 = EasyMock.createNiceMock(VetoableChangeListener.class);
    listenerSupport.addListener(listener1);
    assertEquals(1, listenerSupport.getListeners().length);
    listenerSupport.addListener(listener1, false);
    assertEquals(1, listenerSupport.getListeners().length);
    listenerSupport.removeListener(listener1);
    assertSame(empty, listenerSupport.getListeners());
}

@Test
void testEventDispatchOrder() throws PropertyVetoException {
    final EventListenerSupport<VetoableChangeListener> listenerSupport = EventListenerSupport.create(VetoableChangeListener.class);
    final List<VetoableChangeListener> calledListeners = new ArrayList<>();
    final VetoableChangeListener listener1 = createListener(calledListeners);
    final VetoableChangeListener listener2 = createListener(calledListeners);
    listenerSupport.addListener(listener1);
    listenerSupport.addListener(listener2);
    listenerSupport.fire().vetoableChange(new PropertyChangeEvent(new Date(), "Day", 4, 5));
    assertEquals(calledListeners.size(), 2);
    assertSame(calledListeners.get(0), listener1);
    assertSame(calledListeners.get(1), listener2);
}

@Test
void testGetListeners() {
    final EventListenerSupport<VetoableChangeListener> listenerSupport = EventListenerSupport.create(VetoableChangeListener.class);
    final VetoableChangeListener[] listeners = listenerSupport.getListeners();
    assertEquals(0, listeners.length);
    assertEquals(VetoableChangeListener.class, listeners.getClass().getComponentType());
    final VetoableChangeListener[] empty = listeners;
    // for fun, show that the same empty instance is used
    assertSame(empty, listenerSupport.getListeners());
    final VetoableChangeListener listener1 = EasyMock.createNiceMock(VetoableChangeListener.class);
    listenerSupport.addListener(listener1);
    assertEquals(1, listenerSupport.getListeners().length);
    final VetoableChangeListener listener2 = EasyMock.createNiceMock(VetoableChangeListener.class);
    listenerSupport.addListener(listener2);
    assertEquals(2, listenerSupport.getListeners().length);
    listenerSupport.removeListener(listener1);
    assertEquals(1, listenerSupport.getListeners().length);
    listenerSupport.removeListener(listener2);
    assertSame(empty, listenerSupport.getListeners());
}

@Test
void testSerialization() throws IOException, ClassNotFoundException, PropertyVetoException {
    final EventListenerSupport<VetoableChangeListener> listenerSupport = EventListenerSupport.create(VetoableChangeListener.class);
    listenerSupport.addListener(Function.identity()::apply);
    listenerSupport.addListener(EasyMock.createNiceMock(VetoableChangeListener.class));
    // serialize:
    final ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
    try (ObjectOutputStream objectOutputStream = new ObjectOutputStream(outputStream)) {
        objectOutputStream.writeObject(listenerSupport);
    }
    // deserialize:
    @SuppressWarnings("unchecked")
    final EventListenerSupport<VetoableChangeListener> deserializedListenerSupport = (EventListenerSupport<VetoableChangeListener>) new ObjectInputStream(
            new ByteArrayInputStream(outputStream.toByteArray())).readObject();
    // make sure we get a listener array back, of the correct component type, and that it contains only the serializable mock
    final VetoableChangeListener[] listeners = deserializedListenerSupport.getListeners();
    assertEquals(VetoableChangeListener.class, listeners.getClass().getComponentType());
    assertEquals(1, listeners.length);
    // now verify that the mock still receives events; we can infer that the proxy was correctly reconstituted
    final VetoableChangeListener listener = listeners[0];
    final PropertyChangeEvent evt = new PropertyChangeEvent(new Date(), "Day", 7, 9);
    listener.vetoableChange(evt);
    EasyMock.replay(listener);
    deserializedListenerSupport.fire().vetoableChange(evt);
    EasyMock.verify(listener);
    // remove listener and verify we get an empty array of listeners
    deserializedListenerSupport.removeListener(listener);
    assertEquals(0, deserializedListenerSupport.getListeners().length);
}

@Test
void testSubclassInvocationHandling() throws PropertyVetoException {
    final EventListenerSupport<VetoableChangeListener> eventListenerSupport = new EventListenerSupport<VetoableChangeListener>(
            VetoableChangeListener.class) {
        private static final long serialVersionUID = 1L;

        @Override
        protected java.lang.reflect.InvocationHandler createInvocationHandler() {
            return new ProxyInvocationHandler() {
                @Override
                public Object invoke(final Object proxy, final Method method, final Object[] args)
                        throws IllegalAccessException, IllegalArgumentException, InvocationTargetException {
                    return "vetoableChange".equals(method.getName()) && "Hour".equals(((PropertyChangeEvent) args[0]).getPropertyName()) ? null
                            : super.invoke(proxy, method, args);
                }
            };
        }
    };
    final VetoableChangeListener listener = EasyMock.createNiceMock(VetoableChangeListener.class);
    eventListenerSupport.addListener(listener);
    final Object source = new Date();
    final PropertyChangeEvent ignore = new PropertyChangeEvent(source, "Hour", 5, 6);
    final PropertyChangeEvent respond = new PropertyChangeEvent(source, "Day", 6, 7);
    listener.vetoableChange(respond);
    EasyMock.replay(listener);
    eventListenerSupport.fire().vetoableChange(ignore);
    eventListenerSupport.fire().vetoableChange(respond);
    EasyMock.verify(listener);
}
```