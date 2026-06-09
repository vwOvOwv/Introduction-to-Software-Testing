# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ff6c5f65a5f6130465f97cdad6d529cdfeaccb4e`
- B: `5689c91cf2a3a27f0a3a8a362857f2cf0919d4f6`
- test: `src/test/java/org/apache/commons/lang3/time/DurationUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DurationUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `9809`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2817, 'completion_tokens': 1577, 'total_tokens': 4394, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1078}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2433}`

---

- 新增 `testIsPositive` 和 `testToDuration` 两个 `@Test` 方法，对应生产类新增的 `isPositive` 与 `toDuration` 公共方法。
- 新增 import：`import static org.junit.jupiter.api.Assertions.assertFalse;`、`import static org.junit.jupiter.api.Assertions.assertTrue;` 以及 `import java.util.concurrent.TimeUnit;`。
- 无需删除或修改原有测试方法，旧有 `testLongToIntRangeFit` 和 `testToMillisInt` 继续保留。

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