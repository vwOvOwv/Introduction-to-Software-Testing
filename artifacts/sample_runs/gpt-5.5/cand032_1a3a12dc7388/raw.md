# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `13b9bd612a29ea756f0c7f3cc0b4f900be50e54f`
- B: `1a3a12dc7388a177c4ae64f5e3c96a7d462c003d`
- test: `src/test/java/org/apache/commons/lang3/function/FunctionsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/function/Functions.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `12241`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3496, 'completion_tokens': 759, 'total_tokens': 4255}`

---

- 新增 `testApplyNotNull`，覆盖新增的一参 mapper `Functions.applyNotNull` 的正常映射、输入为 `null`、mapper 返回 `null` 以及 mapper 为 `null` 的异常行为。
- 新增 `testApplyNotNull2`，覆盖新增的两级 mapper 链式 `Functions.applyNotNull` 的短路与空 mapper 异常行为。
- 新增 `testApplyNotNull3`，覆盖新增的三级 mapper 链式 `Functions.applyNotNull`，并使用 `StringUtils::reverse` 验证最终链式结果。
- 需要调整 import：新增 `assertThrows` 静态导入以及 `org.apache.commons.lang3.StringUtils` 导入。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Function;

import org.apache.commons.lang3.StringUtils;
import org.junit.jupiter.api.Test;
// IMPORTS_END

@Test
void testApplyNotNull() {
    assertEquals("A", Functions.applyNotNull("a", String::toUpperCase));
    assertNull(Functions.applyNotNull((String) null, String::toUpperCase));
    assertNull(Functions.applyNotNull("a", s -> null));
    assertThrows(NullPointerException.class, () -> Functions.applyNotNull("a", null));
}

@Test
void testApplyNotNull2() {
    assertEquals("A", Functions.applyNotNull(" a ", String::toUpperCase, String::trim));
    assertNull(Functions.applyNotNull((String) null, String::toUpperCase, String::trim));
    assertNull(Functions.applyNotNull(" a ", s -> null, String::trim));
    assertNull(Functions.applyNotNull(" a ", String::toUpperCase, s -> null));
    assertThrows(NullPointerException.class, () -> Functions.applyNotNull(" a ", null, String::trim));
    assertThrows(NullPointerException.class, () -> Functions.applyNotNull(" a ", String::toUpperCase, null));
}

@Test
void testApplyNotNull3() {
    assertEquals("CBA", Functions.applyNotNull(" abc ", String::toUpperCase, String::trim, StringUtils::reverse));
    assertNull(Functions.applyNotNull((String) null, String::toUpperCase, String::trim, StringUtils::reverse));
    assertNull(Functions.applyNotNull(" abc ", s -> null, String::trim, StringUtils::reverse));
    assertNull(Functions.applyNotNull(" abc ", String::toUpperCase, s -> null, StringUtils::reverse));
    assertNull(Functions.applyNotNull(" abc ", String::toUpperCase, String::trim, s -> null));
    assertThrows(NullPointerException.class, () -> Functions.applyNotNull(" abc ", null, String::trim, StringUtils::reverse));
    assertThrows(NullPointerException.class, () -> Functions.applyNotNull(" abc ", String::toUpperCase, null, StringUtils::reverse));
    assertThrows(NullPointerException.class, () -> Functions.applyNotNull(" abc ", String::toUpperCase, String::trim, null));
}
```