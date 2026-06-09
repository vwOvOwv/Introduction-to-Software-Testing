# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `c3de2d69ce9ad778a0bc22971cb8ff36dd0ee062`
- B: `2a11642511a3c69bac5aa1abd83d3219871395e3`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `35720`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 8468, 'completion_tokens': 974, 'total_tokens': 9442}`

---

- 新增 `testIsEmpty`：覆盖生产代码新增的 `ObjectUtils.isEmpty(Object)` 对 `null`、空字符串、空数组、空集合/Map 以及非空对象的判断。
- 新增 `testIsNotEmpty`：覆盖生产代码新增的 `ObjectUtils.isNotEmpty(Object)`，断言其与 `isEmpty` 相反的行为。
- 需要调整 import：新增 `java.util.Collections`，用于构造空集合、空 Map 以及非空 Set/Map 测试数据。

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
import java.util.List;

import org.apache.commons.lang3.exception.CloneFailedException;
import org.apache.commons.lang3.mutable.MutableObject;
import org.apache.commons.lang3.text.StrBuilder;
import org.junit.Test;
// IMPORTS_END

@Test
public void testIsEmpty() {
    final String[] nonEmptyArray = new String[] { FOO, BAR };
    final List<String> nonEmptyList = Arrays.asList(nonEmptyArray);

    assertTrue(ObjectUtils.isEmpty(null));
    assertTrue(ObjectUtils.isEmpty(""));
    assertTrue(ObjectUtils.isEmpty(new int[] {}));
    assertTrue(ObjectUtils.isEmpty(Collections.emptyList()));
    assertTrue(ObjectUtils.isEmpty(Collections.emptySet()));
    assertTrue(ObjectUtils.isEmpty(Collections.emptyMap()));

    assertFalse(ObjectUtils.isEmpty("  "));
    assertFalse(ObjectUtils.isEmpty("ab"));
    assertFalse(ObjectUtils.isEmpty(nonEmptyArray));
    assertFalse(ObjectUtils.isEmpty(nonEmptyList));
    assertFalse(ObjectUtils.isEmpty(Collections.singleton(FOO)));
    assertFalse(ObjectUtils.isEmpty(Collections.singletonMap(FOO, BAR)));
}

@Test
public void testIsNotEmpty() {
    final String[] nonEmptyArray = new String[] { FOO, BAR };
    final List<String> nonEmptyList = Arrays.asList(nonEmptyArray);

    assertFalse(ObjectUtils.isNotEmpty(null));
    assertFalse(ObjectUtils.isNotEmpty(""));
    assertFalse(ObjectUtils.isNotEmpty(new int[] {}));
    assertFalse(ObjectUtils.isNotEmpty(Collections.emptyList()));
    assertFalse(ObjectUtils.isNotEmpty(Collections.emptySet()));
    assertFalse(ObjectUtils.isNotEmpty(Collections.emptyMap()));

    assertTrue(ObjectUtils.isNotEmpty("  "));
    assertTrue(ObjectUtils.isNotEmpty("ab"));
    assertTrue(ObjectUtils.isNotEmpty(nonEmptyArray));
    assertTrue(ObjectUtils.isNotEmpty(nonEmptyList));
    assertTrue(ObjectUtils.isNotEmpty(Collections.singleton(FOO)));
    assertTrue(ObjectUtils.isNotEmpty(Collections.singletonMap(FOO, BAR)));
}
```