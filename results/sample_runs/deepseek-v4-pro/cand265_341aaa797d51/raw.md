# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `744da0e2555dd6439a6c95a927bf8a638ea83f95`
- B: `341aaa797d515a1fce5def6b41cdc481701ad389`
- test: `src/test/java/org/apache/commons/lang3/tuple/ImmutablePairTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/tuple/ImmutablePair.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `12806`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3674, 'completion_tokens': 1316, 'total_tokens': 4990, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 846}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 3290}`

---

- 新增 `testComparableLeftOnly` 测试方法，验证使用 `ImmutablePair.left()` 创建 pair 后的比较行为。
- 新增 `testComparableRightOnly` 测试方法，验证使用 `ImmutablePair.right()` 创建 pair 后的比较行为。
- 新增 `testToStringLeft` 测试方法，验证 `ImmutablePair.left()` 的 `toString()` 格式。
- 新增 `testToStringRight` 测试方法，验证 `ImmutablePair.right()` 的 `toString()` 格式。
- 需要在文件头新增导入 `import static org.junit.jupiter.api.Assertions.assertTrue;`。

```java
import static org.junit.jupiter.api.Assertions.assertTrue;

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