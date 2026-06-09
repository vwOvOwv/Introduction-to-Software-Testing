# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e910e9c908f4808a524d600737edaeb0ff8c6f0f`
- B: `670a832d4d78c0206180ec2106a5e09592f65cc0`
- test: `src/test/java/org/apache/commons/lang3/tuple/ImmutablePairTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/tuple/ImmutablePair.java']`
- old_test_mode: `methods`
- user_chars: `6652`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2173, 'completion_tokens': 2762, 'total_tokens': 4935, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2000}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1789}`

---

- 修改 `testBasic` 方法：用新的 `ImmutablePair.of(ImmutablePair)` 循环验证替换原来的直接构造断言。
- 删除旧的 `testPairOf` 方法，因为其功能已被拆分为 `testPairOfObjects`（扩展 null 测试）和新增的 `testPairOfMapEntry`。
- 新增 `testPairOfObjects` 方法：保留原有 `of(L,R)` 测试内容，并在末尾增加对 `of(null,null)` 的断言。
- 新增 `testPairOfMapEntry` 方法：测试新增的 `ImmutablePair.of(Map.Entry)` 工厂方法。
- 需要调整 import：新增 `java.util.HashMap` 和 `java.util.Map.Entry`，并确保 `org.apache.commons.lang3.tuple.Pair` 已导入（供 `Pair` 引用）。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.*;
import java.util.HashMap;
import java.util.Map.Entry;
import org.apache.commons.lang3.tuple.ImmutablePair;
import org.apache.commons.lang3.tuple.Pair;
import org.junit.jupiter.api.Test;
// IMPORTS_END

// DELETE_TESTS_START
testPairOf
// DELETE_TESTS_END

@Test
public void testBasic() {
    ImmutablePair<Integer, String> oldPair = new ImmutablePair<>(0, "foo");
    ImmutablePair<Integer, String> nowPair;
    for (int i=0; i<4; i++) {
        nowPair = ImmutablePair.of(oldPair);
        assertEquals(0, nowPair.left.intValue());
        assertEquals(0, nowPair.getLeft().intValue());
        assertEquals("foo", nowPair.right);
        assertEquals("foo", nowPair.getRight());
        assertEquals(oldPair, nowPair);
        oldPair = nowPair;
    }

    ImmutablePair<Object, String> oldPair2 = new ImmutablePair<>(null, "bar");
    ImmutablePair<Object, String> nowPair2;
    for (int i=0; i<4; i++) {
        nowPair2 = ImmutablePair.of(oldPair2);
        assertNull(nowPair2.left);
        assertNull(nowPair2.getLeft());
        assertEquals("bar", nowPair2.right);
        assertEquals("bar", nowPair2.getRight());
        oldPair2 = nowPair2;
    }
}

@Test
public void testPairOfObjects() {
    final ImmutablePair<Integer, String> pair = ImmutablePair.of(0, "foo");
    assertEquals(0, pair.left.intValue());
    assertEquals(0, pair.getLeft().intValue());
    assertEquals("foo", pair.right);
    assertEquals("foo", pair.getRight());
    final ImmutablePair<Object, String> pair2 = ImmutablePair.of(null, "bar");
    assertNull(pair2.left);
    assertNull(pair2.getLeft());
    assertEquals("bar", pair2.right);
    assertEquals("bar", pair2.getRight());
    ImmutablePair pair3 = ImmutablePair.of(null, null);
    assertNull(pair3.left);
    assertNull(pair3.right);
}

@Test
public void testPairOfMapEntry() {
    final HashMap<Integer, String> map = new HashMap<>();
    map.put(0, "foo");
    final Entry<Integer, String> entry = map.entrySet().iterator().next();
    final Pair<Integer, String> pair = ImmutablePair.of(entry);
    assertEquals(entry.getKey(), pair.getLeft());
    assertEquals(entry.getValue(), pair.getRight());
}
```