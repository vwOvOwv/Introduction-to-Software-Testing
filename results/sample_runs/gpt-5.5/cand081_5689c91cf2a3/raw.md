# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ff6c5f65a5f6130465f97cdad6d529cdfeaccb4e`
- B: `5689c91cf2a3a27f0a3a8a362857f2cf0919d4f6`
- test: `src/test/java/org/apache/commons/lang3/time/DurationUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DurationUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `9809`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2741, 'completion_tokens': 514, 'total_tokens': 3255}`

---

- 新增 `testIsPositive`：覆盖生产代码新增的 `DurationUtils.isPositive(Duration)`，验证零、负数、正数三种情况。
- 新增 `testToDuration`：覆盖生产代码新增的 `DurationUtils.toDuration(long, TimeUnit)`，验证各 `TimeUnit` 到 `Duration` 的转换以及正负零数值。
- 需要调整 import：新增 `assertFalse`、`assertTrue` 静态导入，以及 `java.util.concurrent.TimeUnit` 导入。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.concurrent.TimeUnit;

import org.apache.commons.lang3.math.NumberUtils;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    public void testIsPositive() {
        assertFalse(DurationUtils.isPositive(Duration.ZERO));
        assertFalse(DurationUtils.isPositive(Duration.ofMillis(-1)));
        assertTrue(DurationUtils.isPositive(Duration.ofMillis(1)));
    }

    @Test
    public void testToDuration() {
        assertEquals(Duration.ofDays(1), DurationUtils.toDuration(1, TimeUnit.DAYS));
        assertEquals(Duration.ofHours(1), DurationUtils.toDuration(1, TimeUnit.HOURS));
        assertEquals(Duration.ofMillis(1), DurationUtils.toDuration(1_000, TimeUnit.MICROSECONDS));
        assertEquals(Duration.ofMillis(1), DurationUtils.toDuration(1, TimeUnit.MILLISECONDS));
        assertEquals(Duration.ofMinutes(1), DurationUtils.toDuration(1, TimeUnit.MINUTES));
        assertEquals(Duration.ofNanos(1), DurationUtils.toDuration(1, TimeUnit.NANOSECONDS));
        assertEquals(Duration.ofSeconds(1), DurationUtils.toDuration(1, TimeUnit.SECONDS));
        assertEquals(1, DurationUtils.toDuration(1, TimeUnit.MILLISECONDS).toMillis());
        assertEquals(-1, DurationUtils.toDuration(-1, TimeUnit.MILLISECONDS).toMillis());
        assertEquals(0, DurationUtils.toDuration(0, TimeUnit.SECONDS).toMillis());
    }
```