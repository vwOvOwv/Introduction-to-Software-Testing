# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `2bdecd58af4c42d0e7c404951c634bd27d31027d`
- B: `f962e7b65457640a15db9970487cc858176bd511`
- test: `src/test/java/org/apache/commons/lang3/event/EventListenerSupportTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/event/EventListenerSupport.java']`
- old_test_mode: `methods`
- user_chars: `8382`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2297, 'completion_tokens': 4184, 'total_tokens': 6481, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 3530}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1913}`

---

- 修改 @Test 方法 `testThrowingListener`：引入 `listenerCount` 常量替换硬编码数字 10，保持与生产变更无关但提高可读性，行为不变，在 B 版本仍断言通过。
- 新增 @Test 方法 `testThrowingListenerContinues`：验证默认 `handle` 被替换为 `FailableConsumer.nop()` 后，即使监听器抛出异常也能继续调用后续监听器。
- 调整 import：增加 `java.lang.reflect.InvocationHandler` 与 `org.apache.commons.lang3.function.FailableConsumer` 以支持新测试。

```java
// IMPORTS_START
import java.lang.reflect.InvocationHandler;
import org.apache.commons.lang3.function.FailableConsumer;
// IMPORTS_END

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