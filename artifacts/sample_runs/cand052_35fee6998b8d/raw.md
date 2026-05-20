# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `82640281c8259511a40f39c105487f269239a47a`
- B: `35fee6998b8d92c047f6db82fde825810fc26f4a`
- test: `src/test/java/org/apache/commons/lang3/concurrent/BasicThreadFactoryTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/concurrent/BasicThreadFactory.java']`
- old_test_mode: `methods`
- user_chars: `7234`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2166, 'completion_tokens': 731, 'total_tokens': 2897, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 1910}`

---

- 修改 `setUp()` 方法：将 `new BasicThreadFactory.Builder()` 替换为 `BasicThreadFactory.builder()`，因为 `Builder` 的公共构造方法已被标记为 `@Deprecated`，并新增了静态工厂方法 `builder()`。
- 新增 `testBuilderDaemon()` 测试方法：测试 `Builder.daemon()` 无参方法，验证其将 daemon 标志设为 `true`。
- 新增 `testBuilderDaemonBoolean()` 测试方法：测试 `Builder.daemon(boolean)` 方法，验证 `true` 和 `false` 两种情形。
- 修改 `testBuilderReset()` 方法：调整代码格式，将链式调用拆分为多行，并添加 `// @formatter:off` / `// @formatter:on` 注释。
- 修改 `testBuilderResetAfterBuild()` 方法：调整代码格式，将链式调用拆分为多行，并添加 `// @formatter:off` / `// @formatter:on` 注释。
- 无需调整 import，因为 `BasicThreadFactory` 已在同一包内，且 `assertTrue`/`assertFalse` 已通过静态导入或继承可用。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.easymock.EasyMock;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    @BeforeEach
    public void setUp() {
        builder = BasicThreadFactory.builder();
    }

    @Test
    public void testBuilderDaemon() {
        builder.daemon();
        assertTrue(builder.build().getDaemonFlag());
    }

    @Test
    public void testBuilderDaemonBoolean() {
        builder.daemon(true);
        assertTrue(builder.build().getDaemonFlag());
        builder.daemon(false);
        assertFalse(builder.build().getDaemonFlag());
    }

    @Test
    public void testBuilderReset() {
        final ThreadFactory wrappedFactory = EasyMock.createMock(ThreadFactory.class);
        final Thread.UncaughtExceptionHandler exHandler = EasyMock
                .createMock(Thread.UncaughtExceptionHandler.class);
        EasyMock.replay(wrappedFactory, exHandler);
        // @formatter:off
        builder.namingPattern(PATTERN)
            .daemon(true)
            .priority(Thread.MAX_PRIORITY)
            .uncaughtExceptionHandler(exHandler)
            .wrappedFactory(wrappedFactory);
        // @formatter:on
        builder.reset();
        final BasicThreadFactory factory = builder.build();
        checkFactoryDefaults(factory);
        assertNotSame(wrappedFactory, factory.getWrappedFactory(), "Wrapped factory not reset");
        EasyMock.verify(wrappedFactory, exHandler);
    }

    @Test
    public void testBuilderResetAfterBuild() {
        // @formatter:off
        builder
            .wrappedFactory(EasyMock.createNiceMock(ThreadFactory.class))
            .namingPattern(PATTERN)
            .daemon(true)
            .build();
        // @formatter:on
        checkFactoryDefaults(builder.build());
    }
```