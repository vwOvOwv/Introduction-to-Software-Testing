# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `02e55fc072d1793bd66eebac9fe3f3872bd99699`
- B: `8eef2fc92229e47889e66774edd3df0a9f6d6281`
- test: `src/test/java/org/apache/commons/lang3/tuple/PairTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/tuple/Pair.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `10494`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3098, 'completion_tokens': 560, 'total_tokens': 3658}`

---

- 新增 `testAccept`：覆盖 `Pair.accept(FailableBiConsumer)` 将 pair 的 key/value 传给 consumer 的新行为，需要使用 `Map` 接收结果。
- 新增 `testApply`：覆盖 `Pair.apply(FailableBiFunction)` 返回函数结果并传递 key/value 的新行为，需要使用 `Map.put` 的返回值断言。
- 需要调整 import：新增 `java.util.Map`，其余 import 保持不变。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Calendar;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.commons.lang3.AbstractLangTest;
import org.junit.jupiter.api.Test;
// IMPORTS_END

@Test
public void testAccept() {
    final Pair<String, String> pair1 = Pair.of("A", "D");
    final Pair<String, String> pair2 = Pair.of("B", "C");
    final Map<String, String> map = new HashMap<>();
    pair1.accept(map::put);
    pair2.accept(map::put);
    assertEquals("D", map.get("A"));
    assertEquals("C", map.get("B"));
    pair1.accept(map::put);
    pair2.accept(map::put);
    assertEquals("D", map.get("A"));
    assertEquals("C", map.get("B"));
}

@Test
public void testApply() {
    final Pair<String, String> pair1 = Pair.of("A", "D");
    final Pair<String, String> pair2 = Pair.of("B", "C");
    final Map<String, String> map = new HashMap<>();
    assertEquals(null, pair1.apply(map::put));
    assertEquals(null, pair2.apply(map::put));
    assertEquals("D", map.get("A"));
    assertEquals("C", map.get("B"));
    assertEquals("D", pair1.apply(map::put));
    assertEquals("C", pair2.apply(map::put));
    assertEquals("D", map.get("A"));
    assertEquals("C", map.get("B"));
}
```