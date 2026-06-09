# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `3f7868e1b22dbcf9442579d7b66f55a9b5b7e22e`
- B: `c2260f094d78c236bb8a2e3e153d422c7d7ad6bf`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `39686`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 10165, 'completion_tokens': 554, 'total_tokens': 10719}`

---

- 新增 `testHugeStrings` 参数化测试，对应生产代码中缓存大小计算改为 `long` 并限制上限，验证超大 `count` 不再因缓存大小溢出导致失败。
- 需要调整 import：新增 `EnabledIfSystemProperty` 和 `ValueSource`，分别用于按系统属性启用大堆测试和提供两个超大长度参数。

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

    @ParameterizedTest
    @ValueSource(ints = {63_913_201, 63_913_202})
    @EnabledIfSystemProperty(named = "test.large.heap", matches = "true")
    public void testHugeStrings(final int expectedLength) {
        final String hugeString = RandomStringUtils.random(expectedLength);
        assertEquals(expectedLength, hugeString.length(), "hugeString.length() == expectedLength");
    }
```