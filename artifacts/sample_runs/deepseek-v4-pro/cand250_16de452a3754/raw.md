# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `eb2bc4d3b7c9c74085d52286a96321bd23ee48ab`
- B: `16de452a3754bfb2b36d8f6cd4a0b55432803455`
- test: `src/test/java/org/apache/commons/lang3/time/DurationUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DurationUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `10729`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3062, 'completion_tokens': 1709, 'total_tokens': 4771, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1383}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2678}`

---

- 新增 @Test 方法：`testOfRunnble`、`testOfConsumer`、`testOfRunnbleThrowing`，以覆盖新的 `DurationUtils.of(FailableRunnable)` 和 `DurationUtils.of(FailableConsumer)` 以及异常传播。
- 调整 import：新增静态导入 `org.junit.jupiter.api.Assertions.assertThrows`，新增 `java.io.IOException`，以支持异常断言和受检异常类型。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.util.concurrent.TimeUnit;

import org.apache.commons.lang3.math.NumberUtils;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    public void testOfRunnble() {
        assertTrue(DurationUtils.of(() -> testSince()).compareTo(Duration.ZERO) >= 0);
    }

    @Test
    public void testOfConsumer() {
        assertTrue(DurationUtils.of(start -> assertTrue(start.compareTo(Instant.now()) >= 0)).compareTo(Duration.ZERO) >= 0);
    }

    @Test
    public void testOfRunnbleThrowing() {
        assertThrows(IOException.class, () -> DurationUtils.of(() -> {
            throw new IOException();
        }));
    }
```