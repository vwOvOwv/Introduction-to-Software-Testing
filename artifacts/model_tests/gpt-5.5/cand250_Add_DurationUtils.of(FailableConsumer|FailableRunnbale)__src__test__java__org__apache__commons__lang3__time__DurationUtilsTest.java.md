# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `eb2bc4d3b7c9c74085d52286a96321bd23ee48ab`
- B: `16de452a3754bfb2b36d8f6cd4a0b55432803455`
- test: `src/test/java/org/apache/commons/lang3/time/DurationUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DurationUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `10729`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2958, 'completion_tokens': 1076, 'total_tokens': 4034}`

---

- 新增 `testOfRunnble`，覆盖新增的 `DurationUtils.of(FailableRunnable)` 正常执行并返回非负耗时。
- 新增 `testOfConsumer`，覆盖新增的 `DurationUtils.of(FailableConsumer<Instant, E>)` 会把开始时间传入 consumer 并返回非负耗时。
- 新增 `testOfRunnbleThrowing`，覆盖新增的 `DurationUtils.of(FailableRunnable)` 会透传 lambda 抛出的异常。
- 需要调整 import：新增 `assertThrows` 静态导入和 `java.io.IOException` 导入。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

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
        assertTrue(DurationUtils.of(start -> assertTrue(start.compareTo(Instant.now()) <= 0)).compareTo(Duration.ZERO) >= 0);
    }

    @Test
    public void testOfRunnbleThrowing() {
        assertThrows(IOException.class, () -> DurationUtils.of(() -> {
            throw new IOException();
        }));
    }
```