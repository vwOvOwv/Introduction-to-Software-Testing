# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9babe58d895a0e4d6563268ca188794fbf066b38`
- B: `234c6a9b84cb4bfb03e54c717df3ccd940b9884a`
- test: `src/test/java/org/apache/commons/lang3/function/ConsumersTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/function/Consumers.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `4968`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1650, 'completion_tokens': 740, 'total_tokens': 2390, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 434}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1266}`

---

- 新增 `testAccept` 测试方法，用于覆盖 `Consumers.accept(Object, Consumer)` 的各种调用场景（传入非空消费者、传入 null 对象但消费者非空、传入 null 消费者）。
- 新增私有静态内部类 `TestConsumer<T>`，作为测试辅助消费者，记录是否被调用。
- 需要添加两个静态 import：`org.junit.jupiter.api.Assertions.assertEquals` 和 `org.junit.jupiter.api.Assertions.assertTrue`，因为测试方法中使用了这两个断言。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
// IMPORTS_END

    /**
     * Tests {@link Consumers#accept(Object, Consumer)}.
     */
    @Test
    public void testAccept() {
        final StringBuilder builder = new StringBuilder("foo");
        Consumers.accept(builder, sb -> sb.append("-bar"));
        assertEquals("foo-bar", builder.toString());

        final TestConsumer<String> consumer = new TestConsumer<>();
        Consumers.accept(null, consumer);
        assertTrue(consumer.isCalled);

        final StringBuilder builder2 = new StringBuilder("foo");
        Consumers.accept(builder2, null);
        assertEquals("foo", builder2.toString());
    }

    private static final class TestConsumer<T> implements Consumer<T> {
        private boolean isCalled;

        @Override
        public void accept(T t) {
            isCalled = true;
        }
    }
```