# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `3f7868e1b22dbcf9442579d7b66f55a9b5b7e22e`
- B: `c2260f094d78c236bb8a2e3e153d422c7d7ad6bf`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `39686`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 10467, 'completion_tokens': 2870, 'total_tokens': 13337, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2508}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 10083}`

---

- 新增 `@ParameterizedTest` 方法 `testHugeStrings`，用于测试超大字符串长度生成，需要相应的 import 和常量 `MAX_SAFE_COUNT`。
- 新增 `import org.junit.jupiter.api.condition.EnabledIfSystemProperty` 和 `import org.junit.jupiter.params.provider.ValueSource`。
- 旧测试方法无需删除或修改。

```java
// IMPORTS_START
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
import org.junit.jupiter.api.condition.EnabledIfSystemProperty;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;
// IMPORTS_END

private static final int MAX_SAFE_COUNT = 63_913_201;

@ParameterizedTest
@ValueSource(ints = {MAX_SAFE_COUNT, MAX_SAFE_COUNT + 1})
@EnabledIfSystemProperty(named = "test.large.heap", matches = "true")
public void testHugeStrings(final int expectedLength) {
    final String hugeString = RandomStringUtils.random(expectedLength);
    assertEquals(expectedLength, hugeString.length(), "hugeString.length() == expectedLength");
}
```