# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9babe58d895a0e4d6563268ca188794fbf066b38`
- B: `234c6a9b84cb4bfb03e54c717df3ccd940b9884a`
- test: `src/test/java/org/apache/commons/lang3/function/ConsumersTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/function/Consumers.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `4968`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1622, 'completion_tokens': 401, 'total_tokens': 2023}`

---

- 新增 `testAccept`：对应生产代码新增 `Consumers.accept(Object, Consumer)`，覆盖 consumer 非空、object 为 `null`、consumer 为 `null` 三种场景。
- 需要调整 import：新增 `assertEquals` 与 `assertTrue` 的 JUnit 5 静态导入，用于 `testAccept` 断言。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.function.Consumer;
import java.util.stream.Stream;

import org.apache.commons.lang3.AbstractLangTest;
import org.junit.jupiter.api.Test;
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
    public void accept(final T t) {
        isCalled = true;
    }
}
```