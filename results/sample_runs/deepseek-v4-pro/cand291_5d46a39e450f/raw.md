# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e63e9c7902b5c9d0b79de9fdc1fb7f983f3eb4a8`
- B: `5d46a39e450f5dd69027329c9bc0542c113a04be`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `46166`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 11841, 'completion_tokens': 2666, 'total_tokens': 14507, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2235}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 11457}`

---

- 修改 import 区块：新增 `import static org.junit.jupiter.api.Assertions.assertThrows;` 和 `import org.junit.jupiter.api.Timeout;`，使其与最终金标准一致。
- 新增两个 `@Test` 方法：`testFilterLetters` 和 `testFilterNumbers`，用于验证当 `letters` 或 `digits` 分别为 `true` 但区间内没有对应字符时抛出 `IllegalArgumentException`，并加上 `@Timeout`。

```java
// IMPORTS_START
import static org.apache.commons.lang3.LangAssertions.assertIllegalArgumentException;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.Random;
import java.util.stream.Stream;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.api.condition.EnabledIfSystemProperty;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;
// IMPORTS_END

@Test
@Timeout(value = 2, threadMode = Timeout.ThreadMode.SAME_THREAD)
void testFilterLetters() {
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(5, 0x80, 0xA0, true, false, null, new Random()));
}

@Test
@Timeout(value = 2, threadMode = Timeout.ThreadMode.SAME_THREAD)
void testFilterNumbers() {
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(5, 0x80, 0xA0, false, true, null, new Random()));
}
```