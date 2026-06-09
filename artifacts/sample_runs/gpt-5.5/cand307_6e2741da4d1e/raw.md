# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `a6af715f86ef658ceeff12d3ba65d99d1a1f8f0f`
- B: `6e2741da4d1ef471c7c552b91409b2deecbfcec9`
- test: `src/test/java/org/apache/commons/lang3/event/EventListenerSupportTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/event/EventListenerSupport.java']`
- old_test_mode: `methods`
- user_chars: `26705`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5999, 'completion_tokens': 1559, 'total_tokens': 7558}`

---

- 修改 `testAddListenerNoDuplicates`：仅对照测试 diff 调整空行与注释格式，生产行为未变；不需要调整 import。
- 修改 `testEventDispatchOrder`：仅删除多余空行以匹配测试 diff，生产代码明确监听器按添加顺序调用；不需要调整 import。
- 修改 `testGetListeners`：仅对照测试 diff 调整空行与注释格式，生产行为未变；不需要调整 import。
- 修改 `testSerialization`：仅对照测试 diff 调整注释、换行与局部变量声明格式，生产序列化逻辑行为未变；不需要调整 import。
- 修改 `testSubclassInvocationHandling`：仅对照测试 diff 调整空行与匿名类格式，生产代理创建/调用行为未变；不需要调整 import。

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