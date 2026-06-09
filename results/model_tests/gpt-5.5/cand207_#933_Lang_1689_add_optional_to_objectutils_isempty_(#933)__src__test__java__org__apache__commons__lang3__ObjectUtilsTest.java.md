# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `db606c65b0a329cf4a1005d9f592c0499314f31e`
- B: `eb07b19f4a23d443a1fa1005c344d78f79c0f110`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `42601`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9911, 'completion_tokens': 833, 'total_tokens': 10744}`

---

- 修改 `testIsEmpty`：生产代码新增 `Optional` 空值判定，测试需增加 `Optional.empty()` / `Optional.ofNullable(null)` 为 empty，以及 present `Optional` 为 non-empty 的断言。
- 修改 `testIsNotEmpty`：`isNotEmpty` 依赖新的 `isEmpty(Optional)` 语义，测试需补充 empty `Optional` 为 false、present `Optional` 为 true 的断言。
- 需要调整 import：新增 `java.util.Optional` 导入。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

import java.io.IOException;
import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.function.Supplier;

import org.apache.commons.lang3.exception.CloneFailedException;
import org.apache.commons.lang3.mutable.MutableInt;
import org.apache.commons.lang3.mutable.MutableObject;
import org.apache.commons.lang3.text.StrBuilder;
import org.junit.jupiter.api.Test;
// IMPORTS_END

@Test
public void testIsEmpty() {
    assertTrue(ObjectUtils.isEmpty(null));
    assertTrue(ObjectUtils.isEmpty(""));
    assertTrue(ObjectUtils.isEmpty(new int[] {}));
    assertTrue(ObjectUtils.isEmpty(Collections.emptyList()));
    assertTrue(ObjectUtils.isEmpty(Collections.emptySet()));
    assertTrue(ObjectUtils.isEmpty(Collections.emptyMap()));
    assertTrue(ObjectUtils.isEmpty(Optional.empty()));
    assertTrue(ObjectUtils.isEmpty(Optional.ofNullable(null)));

    assertFalse(ObjectUtils.isEmpty("  "));
    assertFalse(ObjectUtils.isEmpty("ab"));
    assertFalse(ObjectUtils.isEmpty(NON_EMPTY_ARRAY));
    assertFalse(ObjectUtils.isEmpty(NON_EMPTY_LIST));
    assertFalse(ObjectUtils.isEmpty(NON_EMPTY_SET));
    assertFalse(ObjectUtils.isEmpty(NON_EMPTY_MAP));
    assertFalse(ObjectUtils.isEmpty(Optional.of(new Object())));
    assertFalse(ObjectUtils.isEmpty(Optional.ofNullable(new Object())));
}

@Test
public void testIsNotEmpty() {
    assertFalse(ObjectUtils.isNotEmpty(null));
    assertFalse(ObjectUtils.isNotEmpty(""));
    assertFalse(ObjectUtils.isNotEmpty(new int[] {}));
    assertFalse(ObjectUtils.isNotEmpty(Collections.emptyList()));
    assertFalse(ObjectUtils.isNotEmpty(Collections.emptySet()));
    assertFalse(ObjectUtils.isNotEmpty(Collections.emptyMap()));
    assertFalse(ObjectUtils.isNotEmpty(Optional.empty()));
    assertFalse(ObjectUtils.isNotEmpty(Optional.ofNullable(null)));

    assertTrue(ObjectUtils.isNotEmpty("  "));
    assertTrue(ObjectUtils.isNotEmpty("ab"));
    assertTrue(ObjectUtils.isNotEmpty(NON_EMPTY_ARRAY));
    assertTrue(ObjectUtils.isNotEmpty(NON_EMPTY_LIST));
    assertTrue(ObjectUtils.isNotEmpty(NON_EMPTY_SET));
    assertTrue(ObjectUtils.isNotEmpty(NON_EMPTY_MAP));
    assertTrue(ObjectUtils.isNotEmpty(Optional.of(new Object())));
    assertTrue(ObjectUtils.isNotEmpty(Optional.ofNullable(new Object())));
}
```