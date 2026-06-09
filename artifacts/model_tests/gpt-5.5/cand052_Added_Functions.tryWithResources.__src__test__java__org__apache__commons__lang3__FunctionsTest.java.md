# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `11d9eb47a40359e74a5e24daf681beacd71b35f0`
- B: `2ebc17ba3f244ae44aae46273aeef7e321f9542a`
- test: `src/test/java/org/apache/commons/lang3/FunctionsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Functions.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `17111`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5120, 'completion_tokens': 1001, 'total_tokens': 6121}`

---

- 新增 `testTryWithResources`，覆盖新增的 `Functions.tryWithResources(...)` 在运行时异常、`Error`、`IOException` 和无异常场景下都会执行资源关闭动作。
- 需要调整 import：新增 `org.apache.commons.lang3.Functions.FailableConsumer`，用于声明可抛异常的错误触发 consumer。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.lang.reflect.UndeclaredThrowableException;

import org.apache.commons.lang3.Functions.FailableConsumer;
import org.junit.jupiter.api.Test;
// IMPORTS_END

	@Test
	public void testTryWithResources() {
		final boolean[] closed = new boolean[1];
		final FailableConsumer<Throwable, ? extends Throwable> consumer = th -> {
			if (th != null) {
				throw th;
			}
		};

		final IllegalStateException ise = new IllegalStateException();
		try {
			Functions.tryWithResources(() -> consumer.accept(ise), () -> closed[0] = true);
			fail("Expected Exception");
		} catch (IllegalStateException e) {
			assertSame(ise, e);
		}
		assertTrue(closed[0]);

		closed[0] = false;
		final Error error = new OutOfMemoryError();
		try {
			Functions.tryWithResources(() -> consumer.accept(error), () -> closed[0] = true);
			fail("Expected Exception");
		} catch (OutOfMemoryError e) {
			assertSame(error, e);
		}
		assertTrue(closed[0]);

		closed[0] = false;
		final IOException ioe = new IOException("Unknown I/O error");
		try {
			Functions.tryWithResources(() -> consumer.accept(ioe), () -> closed[0] = true);
			fail("Expected Exception");
		} catch (UncheckedIOException e) {
			final IOException cause = e.getCause();
			assertSame(ioe, cause);
		}
		assertTrue(closed[0]);

		closed[0] = false;
		Functions.tryWithResources(() -> consumer.accept(null), () -> closed[0] = true);
		assertTrue(closed[0]);
	}
```