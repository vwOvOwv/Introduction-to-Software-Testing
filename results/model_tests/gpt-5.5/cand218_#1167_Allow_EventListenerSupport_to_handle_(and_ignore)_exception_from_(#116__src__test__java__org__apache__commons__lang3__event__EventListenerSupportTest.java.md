# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `2bdecd58af4c42d0e7c404951c634bd27d31027d`
- B: `f962e7b65457640a15db9970487cc858176bd511`
- test: `src/test/java/org/apache/commons/lang3/event/EventListenerSupportTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/event/EventListenerSupport.java']`
- old_test_mode: `methods`
- user_chars: `8382`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2246, 'completion_tokens': 908, 'total_tokens': 3154}`

---

- 修改 `testThrowingListener`：生产代码默认仍通过 `ExceptionUtils::rethrow` 重新抛出监听器异常，测试仅将硬编码监听器数量提取为 `listenerCount`，保持原断言语义。
- 新增 `testThrowingListenerContinues`：覆盖新增的 `ProxyInvocationHandler(FailableConsumer)` 构造器，使用 `FailableConsumer.nop()` 验证监听器抛异常后仍继续调用后续监听器。
- 需要新增 import：`java.lang.reflect.InvocationHandler` 与 `org.apache.commons.lang3.function.FailableConsumer`。

```java
import java.lang.reflect.InvocationHandler;
import org.apache.commons.lang3.function.FailableConsumer;

@Test
public void testThrowingListener() {
    final AtomicInteger count = new AtomicInteger();
    final EventListenerSupport<VetoableChangeListener> listenerSupport = EventListenerSupport.create(VetoableChangeListener.class);
    final int vetoLimit = 1;
    final int listenerCount = 10;
    for (int i = 0; i < listenerCount; ++i) {
        listenerSupport.addListener(evt -> {
            if (count.incrementAndGet() > vetoLimit) {
                throw new PropertyVetoException(count.toString(), evt);
            }
        });
    }
    assertEquals(listenerCount, listenerSupport.getListenerCount());
    assertEquals(0, count.get());
    final Exception e = assertThrows(UndeclaredThrowableException.class,
            () -> listenerSupport.fire().vetoableChange(new PropertyChangeEvent(new Date(), "Day", 0, 1)));
    final Throwable rootCause = ExceptionUtils.getRootCause(e);
    assertTrue(rootCause instanceof PropertyVetoException);
    assertEquals(vetoLimit + 1, count.get());
}

/**
 * Tests that throwing an exception from a listener continues calling the remaining listeners.
 */
@Test
public void testThrowingListenerContinues() throws PropertyVetoException {
    final AtomicInteger count = new AtomicInteger();
    final EventListenerSupport<VetoableChangeListener> listenerSupport = new EventListenerSupport<VetoableChangeListener>(VetoableChangeListener.class) {
        @Override
        protected InvocationHandler createInvocationHandler() {
            return new ProxyInvocationHandler(FailableConsumer.nop());
        }
    };
    final int vetoLimit = 1;
    final int listenerCount = 10;
    for (int i = 0; i < listenerCount; ++i) {
        listenerSupport.addListener(evt -> {
            if (count.incrementAndGet() > vetoLimit) {
                throw new PropertyVetoException(count.toString(), evt);
            }
        });
    }
    assertEquals(listenerCount, listenerSupport.getListenerCount());
    assertEquals(0, count.get());
    listenerSupport.fire().vetoableChange(new PropertyChangeEvent(new Date(), "Day", 0, 1));
    assertEquals(listenerCount, count.get());
}
```