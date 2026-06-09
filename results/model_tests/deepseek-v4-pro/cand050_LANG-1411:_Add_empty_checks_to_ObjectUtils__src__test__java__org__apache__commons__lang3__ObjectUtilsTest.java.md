# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `c3de2d69ce9ad778a0bc22971cb8ff36dd0ee062`
- B: `2a11642511a3c69bac5aa1abd83d3219871395e3`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `35720`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 8671, 'completion_tokens': 3694, 'total_tokens': 12365, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2902}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 8287}`

---

- 新增 `testIsEmpty` 测试方法，对应生产代码新增的 `ObjectUtils.isEmpty`。
- 新增 `testIsNotEmpty` 测试方法，对应生产代码新增的 `ObjectUtils.isNotEmpty`。
- 需要调整 import：新增 `java.util.Collections`、`java.util.HashMap`、`java.util.HashSet`、`java.util.Map`、`java.util.Set` 以支持新测试中的集合与静态常量。
- 新增静态常量 `NON_EMPTY_ARRAY`、`NON_EMPTY_LIST`、`NON_EMPTY_SET`、`NON_EMPTY_MAP` 及相应的静态初始化块，供新测试方法使用。

```java
// IMPORTS_START
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNotSame;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertSame;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

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

import org.apache.commons.lang3.exception.CloneFailedException;
import org.apache.commons.lang3.mutable.MutableObject;
import org.apache.commons.lang3.text.StrBuilder;
import org.apache.commons.lang3.Validate;
// IMPORTS_END

    private static final String[] NON_EMPTY_ARRAY = new String[] { FOO, BAR, };
    private static final List<String> NON_EMPTY_LIST = Arrays.asList(NON_EMPTY_ARRAY);
    private static final Set<String> NON_EMPTY_SET = new HashSet<>(NON_EMPTY_LIST);
    private static final Map<String, String> NON_EMPTY_MAP = new HashMap<>();
    static {
        NON_EMPTY_MAP.put(FOO, BAR);
    }

    @Test
    public void testIsEmpty() {
        assertTrue(ObjectUtils.isEmpty(null));
        assertTrue(ObjectUtils.isEmpty(""));
        assertTrue(ObjectUtils.isEmpty(new int[] {}));
        assertTrue(ObjectUtils.isEmpty(Collections.emptyList()));
        assertTrue(ObjectUtils.isEmpty(Collections.emptySet()));
        assertTrue(ObjectUtils.isEmpty(Collections.emptyMap()));

        assertFalse(ObjectUtils.isEmpty("  "));
        assertFalse(ObjectUtils.isEmpty("ab"));
        assertFalse(ObjectUtils.isEmpty(NON_EMPTY_ARRAY));
        assertFalse(ObjectUtils.isEmpty(NON_EMPTY_LIST));
        assertFalse(ObjectUtils.isEmpty(NON_EMPTY_SET));
        assertFalse(ObjectUtils.isEmpty(NON_EMPTY_MAP));
    }

    @Test
    public void testIsNotEmpty() {
        assertFalse(ObjectUtils.isNotEmpty(null));
        assertFalse(ObjectUtils.isNotEmpty(""));
        assertFalse(ObjectUtils.isNotEmpty(new int[] {}));
        assertFalse(ObjectUtils.isNotEmpty(Collections.emptyList()));
        assertFalse(ObjectUtils.isNotEmpty(Collections.emptySet()));
        assertFalse(ObjectUtils.isNotEmpty(Collections.emptyMap()));

        assertTrue(ObjectUtils.isNotEmpty("  "));
        assertTrue(ObjectUtils.isNotEmpty("ab"));
        assertTrue(ObjectUtils.isNotEmpty(NON_EMPTY_ARRAY));
        assertTrue(ObjectUtils.isNotEmpty(NON_EMPTY_LIST));
        assertTrue(ObjectUtils.isNotEmpty(NON_EMPTY_SET));
        assertTrue(ObjectUtils.isNotEmpty(NON_EMPTY_MAP));
    }
```