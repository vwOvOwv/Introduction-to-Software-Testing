# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `744da0e2555dd6439a6c95a927bf8a638ea83f95`
- B: `341aaa797d515a1fce5def6b41cdc481701ad389`
- test: `src/test/java/org/apache/commons/lang3/tuple/ImmutablePairTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/tuple/ImmutablePair.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `12806`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3578, 'completion_tokens': 686, 'total_tokens': 4264}`

---

- 新增 `testComparableLeftOnly`，覆盖新增的 `ImmutablePair.left(left)` 工厂方法及仅 left 有值时的 `compareTo` 行为。
- 新增 `testComparableRightOnly`，覆盖新增的 `ImmutablePair.right(right)` 工厂方法及仅 right 有值时的 `compareTo` 行为。
- 新增 `testToStringLeft`，断言 `ImmutablePair.left("Key")` 的字符串格式为 `(Key,null)`。
- 新增 `testToStringRight`，断言 `ImmutablePair.right("Value")` 的字符串格式为 `(null,Value)`。
- 需要调整 import，新增静态导入 `assertTrue` 以支持比较结果断言。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.TreeMap;

import org.junit.jupiter.api.Test;
// IMPORTS_END

@Test
public void testComparableLeftOnly() {
    final Pair<String, String> pair1 = ImmutablePair.left("A");
    final Pair<String, String> pair2 = ImmutablePair.left("B");
    assertEquals("A", pair1.getLeft());
    assertEquals("B", pair2.getLeft());
    assertEquals(0, pair1.compareTo(pair1));
    assertTrue(pair1.compareTo(pair2) < 0);
    assertEquals(0, pair2.compareTo(pair2));
    assertTrue(pair2.compareTo(pair1) > 0);
}

@Test
public void testComparableRightOnly() {
    final Pair<String, String> pair1 = ImmutablePair.right("A");
    final Pair<String, String> pair2 = ImmutablePair.right("B");
    assertEquals("A", pair1.getRight());
    assertEquals("B", pair2.getRight());
    assertEquals(0, pair1.compareTo(pair1));
    assertTrue(pair1.compareTo(pair2) < 0);
    assertEquals(0, pair2.compareTo(pair2));
    assertTrue(pair2.compareTo(pair1) > 0);
}

@Test
public void testToStringLeft() {
    final Pair<String, String> pair = ImmutablePair.left("Key");
    assertEquals("(Key,null)", pair.toString());
}

@Test
public void testToStringRight() {
    final Pair<String, String> pair = ImmutablePair.right("Value");
    assertEquals("(null,Value)", pair.toString());
}
```