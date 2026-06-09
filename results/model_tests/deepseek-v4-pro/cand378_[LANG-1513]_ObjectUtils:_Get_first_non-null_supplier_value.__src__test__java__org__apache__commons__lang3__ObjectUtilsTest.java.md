# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `259ac721ce5097312d8bd93aefde26c2785f26e9`
- B: `a606a0328ba4b3061c5bc810a31418fa4251ea16`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `34958`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 8516, 'completion_tokens': 2594, 'total_tokens': 11110, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1939}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 8132}`

---

- 新增 `@Test` 方法 `testGetFirstNonNull`，验证生产代码新增的 `ObjectUtils.getFirstNonNull(Supplier...)` 行为（diff 新增的方法）。
- 在 `import` 区域增加 `import static org.junit.jupiter.api.Assertions.fail;`，因为测试中使用了 `fail(...)`，而旧测试未导入该静态方法。

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
import java.util.Set;
import java.util.function.Supplier;

import org.apache.commons.lang3.exception.CloneFailedException;
import org.apache.commons.lang3.mutable.MutableInt;
import org.apache.commons.lang3.mutable.MutableObject;
import org.apache.commons.lang3.text.StrBuilder;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    public void testGetFirstNonNull() {
        // first non null
        assertEquals("", ObjectUtils.getFirstNonNull(() -> null, () -> ""));
        // first encountered value is used
        assertEquals("1", ObjectUtils.getFirstNonNull(() -> null, () -> "1", () -> "2", () -> null));
        assertEquals("123", ObjectUtils.getFirstNonNull(() -> null, () -> "123", () -> "456"));
        // don't evaluate suppliers after first value is found
        assertEquals("123", ObjectUtils.getFirstNonNull(() -> null, () -> "123", () -> fail("Supplier after first non-null value should not be evaluated")));
        // supplier returning null and null supplier both result in null
        assertNull(ObjectUtils.getFirstNonNull(null, () -> null));
        // Explicitly pass in an empty array of Object type to ensure compiler doesn't complain of unchecked generic array creation
        assertNull(ObjectUtils.getFirstNonNull());
        // supplier is null
        assertNull(ObjectUtils.getFirstNonNull((Supplier<Object>) null));
        // varargs array itself is null
        assertNull(ObjectUtils.getFirstNonNull((Supplier<Object>[]) null));
        // test different types
        assertEquals(1, ObjectUtils.getFirstNonNull(() -> null, () -> 1));
        assertEquals(Boolean.TRUE, ObjectUtils.getFirstNonNull(() -> null, () -> Boolean.TRUE));
    }
```