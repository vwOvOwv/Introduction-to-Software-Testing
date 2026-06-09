# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `03e181b8a059c744f62645eaea22cbe4f16d8355`
- B: `b2e66fe50ba8af3986edc3d06a9dd3c8489cfd36`
- test: `src/test/java/org/apache/commons/lang3/EnumUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/EnumUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `41431`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 11504, 'completion_tokens': 1211, 'total_tokens': 12715}`

---

- 新增 `@Test` 方法 `testGetFirstEnumToIntFunction`，覆盖生产代码新增的 `EnumUtils.getFirstEnum(Class, int, ToIntFunction, defaultEnum)`。
- 不删除现有 `@Test` / `@ParameterizedTest` 方法，`testGetFirstEnumIgnoreCase_defaultEnum` 保持原断言以对应未改变的字符串匹配行为。
- 需要调整 import：新增 `java.util.function.ToIntFunction`，供新增测试方法使用。
- 需要修改测试辅助枚举 `Traffic2`：增加 `value` 字段、构造参数和 `getValue()`，以支持 `ToIntFunction<Traffic2>`。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.function.ToIntFunction;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
// IMPORTS_END

@Test
public void testGetFirstEnumToIntFunction() {
    final ToIntFunction<Traffic2> f = Traffic2::getValue;
    assertEquals(Traffic2.RED, EnumUtils.getFirstEnum(Traffic2.class, 1, f, Traffic2.AMBER));
    assertEquals(Traffic2.AMBER, EnumUtils.getFirstEnum(Traffic2.class, 2, f, Traffic2.GREEN));
    assertEquals(Traffic2.GREEN, EnumUtils.getFirstEnum(Traffic2.class, 3, f, Traffic2.RED));
    assertEquals(Traffic2.AMBER, EnumUtils.getFirstEnum(Traffic2.class, 4, f, Traffic2.AMBER));
    assertEquals(Traffic2.GREEN, EnumUtils.getFirstEnum(Traffic2.class, 5, f, Traffic2.GREEN));
    assertEquals(Traffic2.RED, EnumUtils.getFirstEnum(Traffic2.class, 6, f, Traffic2.RED));
    assertEquals(Traffic2.AMBER, EnumUtils.getFirstEnum(Traffic2.class, 0, f, Traffic2.AMBER));
    assertEquals(Traffic2.GREEN, EnumUtils.getFirstEnum(Traffic2.class, -1, f, Traffic2.GREEN));
    assertEquals(Traffic2.RED, EnumUtils.getFirstEnum(Traffic2.class, 0, f, Traffic2.RED));
    assertNull(EnumUtils.getFirstEnum(Traffic2.class, 7, f, null));
}

enum Traffic2 {

    RED("***Red***", 1), AMBER("**Amber**", 2), GREEN("*green*", 3);

    final String label;
    final int value;

    Traffic2(final String label, final int value) {
        this.label = label;
        this.value = value;
    }

    public String getLabel() {
        return label;
    }

    public int getValue() {
        return value;
    }
}
```