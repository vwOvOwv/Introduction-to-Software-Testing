# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e910e9c908f4808a524d600737edaeb0ff8c6f0f`
- B: `670a832d4d78c0206180ec2106a5e09592f65cc0`
- test: `src/test/java/org/apache/commons/lang3/tuple/ImmutablePairTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/tuple/ImmutablePair.java']`
- old_test_mode: `methods`
- user_chars: `6652`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2148, 'completion_tokens': 1038, 'total_tokens': 3186}`

---

- 修改 `testBasic`：生产代码新增 `ImmutablePair.of(Map.Entry)`，测试改为反复用已有 `ImmutablePair` 作为 `Map.Entry` 创建新 `ImmutablePair` 并断言值一致。
- 删除旧的 `testPairOf`：该测试被拆分为对象工厂方法测试和 `Map.Entry` 工厂方法测试。
- 新增 `testPairOfMapEntry`：覆盖新增的 `ImmutablePair.of(Map.Entry)` 工厂方法。
- 新增 `testPairOfObjects`：保留并扩展原 `ImmutablePair.of(left, right)` 行为断言。
- 需要新增 import：`HashMap` 和 `Map.Entry`。

```java
import java.util.HashMap;
import java.util.Map.Entry;

// DELETE_TESTS_START
testPairOf
// DELETE_TESTS_END

    @Test
    public void testBasic() {
        ImmutablePair<Integer, String> oldPair = new ImmutablePair<>(0, "foo");
        ImmutablePair<Integer, String> nowPair;
        for (int i = 0; i < 4; i++) {
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
        for (int i = 0; i < 4; i++) {
            nowPair2 = ImmutablePair.of(oldPair2);
            assertNull(nowPair2.left);
            assertNull(nowPair2.getLeft());
            assertEquals("bar", nowPair2.right);
            assertEquals("bar", nowPair2.getRight());
            oldPair2 = nowPair2;
        }
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
        final ImmutablePair<?, ?> pair3 = ImmutablePair.of(null, null);
        assertNull(pair3.left);
        assertNull(pair3.right);
    }
```