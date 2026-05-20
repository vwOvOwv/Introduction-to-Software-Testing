# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `557252762bb29887ddeaf9c99f16572bae19316c`
- B: `c140fc8154e8c680aad63239eaaaac14d85d5683`
- test: `src/test/java/org/apache/commons/lang3/tuple/MutablePairTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/tuple/MutablePair.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `8583`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2540, 'completion_tokens': 242, 'total_tokens': 2782, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 2284}`

---

- 新增 `testOfNonNullMapEntry` 测试方法，用于测试 `MutablePair.ofNonNull(Map.Entry)` 方法。
- 无需调整 import，因为 `assertNullPointerException` 已在旧测试中导入。

```java
// IMPORTS_START
import static org.apache.commons.lang3.LangAssertions.assertNullPointerException;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

import java.util.HashMap;
import java.util.Map.Entry;

import org.apache.commons.lang3.AbstractLangTest;
import org.apache.commons.lang3.SerializationUtils;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    @Test
    void testOfNonNullMapEntry() {
        assertNullPointerException(() -> MutablePair.ofNonNull(null));
        final Pair<Integer, String> pair = Pair.of(0, "foo");
        final MutablePair<Integer, String> mutablePair = MutablePair.ofNonNull(pair);
        assertEquals(pair.getLeft(), mutablePair.getLeft());
        assertEquals(pair.getRight(), mutablePair.getRight());
    }
```