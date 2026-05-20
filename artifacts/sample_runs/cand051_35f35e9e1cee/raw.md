# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `f626e5357564a83847f0ccd1d6d0a106208de1fe`
- B: `35f35e9e1cee8b53fd4c562534de79c6213d7aaf`
- test: `src/test/java/org/apache/commons/lang3/time/DurationUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DurationUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `15832`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 4382, 'completion_tokens': 909, 'total_tokens': 5291, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 4126}`

---

- 新增 `testGet` 方法：对应生产代码新增的 `DurationUtils.get(String, TemporalUnit, long)` 方法，测试 null/空 key 返回默认值，以及系统属性设置后的正确值。
- 新增 `testGetMilliseconds` 方法：对应生产代码新增的 `DurationUtils.getMillis(String, long)` 方法，测试 null/空 key 返回默认值，以及系统属性设置后的正确值。
- 新增 `testGetSeconds` 方法：对应生产代码新增的 `DurationUtils.getSeconds(String, long)` 方法，测试 null/空 key 返回默认值，以及系统属性设置后的正确值。
- 新增 import：`java.time.temporal.ChronoUnit`、`org.junitpioneer.jupiter.SetSystemProperty`、`org.junitpioneer.jupiter.SetSystemProperty.SetSystemProperties`。

```java
// IMPORTS_START
import static org.apache.commons.lang3.LangAssertions.assertNullPointerException;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.concurrent.TimeUnit;

import org.apache.commons.lang3.AbstractLangTest;
import org.apache.commons.lang3.math.NumberUtils;
import org.junit.jupiter.api.Test;
import org.junitpioneer.jupiter.SetSystemProperty;
import org.junitpioneer.jupiter.SetSystemProperty.SetSystemProperties;
// IMPORTS_END

    @Test
    @SetSystemProperties({
        @SetSystemProperty(key = "Seconds1", value = "1"),
        @SetSystemProperty(key = "Seconds2", value = "9223372036854775807") }) // Long.MAX_VALUE
    void testGet() {
        // ChronoUnit.SECONDS
        assertEquals(Duration.ofSeconds(0), DurationUtils.get(null, ChronoUnit.SECONDS, 0));
        assertEquals(Duration.ofSeconds(0), DurationUtils.get("", ChronoUnit.SECONDS, 0));
        assertEquals(Duration.ofSeconds(1), DurationUtils.get("Seconds1", ChronoUnit.SECONDS, 0));
        assertEquals(Duration.ofSeconds(Long.MAX_VALUE), DurationUtils.get("Seconds2", ChronoUnit.SECONDS, 0));
        // ChronoUnit.MILLIS
        assertEquals(Duration.ofMillis(0), DurationUtils.get(null, ChronoUnit.MILLIS, 0));
        assertEquals(Duration.ofMillis(0), DurationUtils.get("", ChronoUnit.MILLIS, 0));
        assertEquals(Duration.ofMillis(1), DurationUtils.get("Seconds1", ChronoUnit.MILLIS, 0));
        assertEquals(Duration.ofMillis(Long.MAX_VALUE), DurationUtils.get("Seconds2", ChronoUnit.MILLIS, 0));
    }

    @Test
    @SetSystemProperties({
        @SetSystemProperty(key = "Seconds1", value = "1"),
        @SetSystemProperty(key = "Seconds2", value = "9223372036854775807") }) // Long.MAX_VALUE
    void testGetMilliseconds() {
        assertEquals(Duration.ofMillis(0), DurationUtils.getMillis(null, 0));
        assertEquals(Duration.ofMillis(0), DurationUtils.getMillis("", 0));
        assertEquals(Duration.ofMillis(1), DurationUtils.getMillis("Seconds1", 0));
        assertEquals(Duration.ofMillis(Long.MAX_VALUE), DurationUtils.getMillis("Seconds2", 0));
    }

    @Test
    @SetSystemProperties({
        @SetSystemProperty(key = "Seconds1", value = "1"),
        @SetSystemProperty(key = "Seconds2", value = "9223372036854775807") }) // Long.MAX_VALUE
    void testGetSeconds() {
        assertEquals(Duration.ofSeconds(0), DurationUtils.getSeconds(null, 0));
        assertEquals(Duration.ofSeconds(0), DurationUtils.getSeconds("", 0));
        assertEquals(Duration.ofSeconds(1), DurationUtils.getSeconds("Seconds1", 0));
        assertEquals(Duration.ofSeconds(Long.MAX_VALUE), DurationUtils.getSeconds("Seconds2", 0));
    }
```