# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `78154f0456f8bbf7139bc1524481eef8f6e228f7`
- B: `f382d61a03778ccf838c6c051bd8692e4834dec2`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `34911`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9026, 'completion_tokens': 703, 'total_tokens': 9729}`

---

- 新增 `testRandomWithChars`：覆盖生产代码中 `chars != null` 分支改为基于 `randomValue` 索引后的字符数组随机生成行为。
- 需要调整 import：新增 `assertNotEquals` 静态导入，用于断言多次随机结果不同。

```java
// IMPORTS_START
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.greaterThanOrEqualTo;
import static org.hamcrest.Matchers.is;
import static org.hamcrest.Matchers.lessThan;
import static org.hamcrest.Matchers.lessThanOrEqualTo;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.Random;

import org.junit.jupiter.api.Test;
// IMPORTS_END

/**
 * Test {@code RandomStringUtils.random} works appropriately when chars specified.
 */
@Test
void testRandomWithChars() {
    final char[] digitChars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};

    String r1, r2, r3;

    r1 = RandomStringUtils.random(50, 0, 0, true, true, digitChars);
    assertEquals(50, r1.length(), "randomNumeric(50)");
    for (int i = 0; i < r1.length(); i++) {
        assertTrue(
                Character.isDigit(r1.charAt(i)) && !Character.isLetter(r1.charAt(i)),
                "r1 contains numeric");
    }
    r2 = RandomStringUtils.randomNumeric(50);
    assertNotEquals(r1, r2);

    r3 = RandomStringUtils.random(50, 0, 0, true, true, digitChars);
    assertNotEquals(r1, r3);
    assertNotEquals(r2, r3);
}
```