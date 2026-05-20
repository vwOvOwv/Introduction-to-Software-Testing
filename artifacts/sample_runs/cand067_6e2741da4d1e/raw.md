# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `a6af715f86ef658ceeff12d3ba65d99d1a1f8f0f`
- B: `6e2741da4d1ef471c7c552b91409b2deecbfcec9`
- test: `src/test/java/org/apache/commons/lang3/event/EventListenerSupportTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/event/EventListenerSupport.java']`
- old_test_mode: `methods`
- user_chars: `26987`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6191, 'completion_tokens': 1652, 'total_tokens': 7843, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 5935}`

---

- 修改 `testAddListenerNoDuplicates` 方法：调整注释格式（添加空格），移除多余空行。
- 修改 `testEventDispatchOrder` 方法：移除多余空行。
- 修改 `testGetListeners` 方法：调整注释格式（添加空格），移除多余空行。
- 修改 `testSerialization` 方法：调整注释格式（添加空格），移除多余空行，修复 `final` 关键字位置。
- 修改 `testSubclassInvocationHandling` 方法：移除多余空行，添加匿名内部类中的空行。
- 无需调整 import。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;

import java.beans.PropertyChangeEvent;
import java.beans.PropertyVetoException;
import java.beans.VetoableChangeListener;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.function.Function;

import org.apache.commons.lang3.AbstractLangTest;
import org.apache.commons.lang3.event.EventListenerSupport;
import org.easymock.EasyMock;
import org.junit.jupiter.api.Test;
// IMPORTS_END

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