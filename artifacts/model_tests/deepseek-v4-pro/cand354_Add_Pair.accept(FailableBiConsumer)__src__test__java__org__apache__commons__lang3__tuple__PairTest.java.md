# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `02e55fc072d1793bd66eebac9fe3f3872bd99699`
- B: `8eef2fc92229e47889e66774edd3df0a9f6d6281`
- test: `src/test/java/org/apache/commons/lang3/tuple/PairTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/tuple/Pair.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `10494`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3131, 'completion_tokens': 1738, 'total_tokens': 4869, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1259}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2747}`

---

- 新增 `@Test` 方法 `testAccept()` 和 `testApply()`，对应生产代码 `Pair` 中新增的 `accept(FailableBiConsumer)` 和 `apply(FailableBiFunction)` 方法。
- 新增 `import java.util.Map;`，因为测试中使用了 `Map<String, String>` 局部变量类型声明。

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