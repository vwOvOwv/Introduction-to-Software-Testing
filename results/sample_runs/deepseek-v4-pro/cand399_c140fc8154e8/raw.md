# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `557252762bb29887ddeaf9c99f16572bae19316c`
- B: `c140fc8154e8c680aad63239eaaaac14d85d5683`
- test: `src/test/java/org/apache/commons/lang3/tuple/MutablePairTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/tuple/MutablePair.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `8310`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2479, 'completion_tokens': 1065, 'total_tokens': 3544, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 898}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2095}`

---

- 新增 @Test 方法 `testOfNonNullMapEntry`，对应生产代码新增的 `MutablePair.ofNonNull(Map.Entry)` 方法以及测试 diff 中新增的测试逻辑。
- 无需删除任何旧测试方法。
- 无需调整 import，现有 import 已包含 `java.util.Map.Entry`，且同包可直接使用 `Pair`。

```java
@Test
void testOfNonNullMapEntry() {
    assertNullPointerException(() -> MutablePair.ofNonNull(null));
    final Pair<Integer, String> pair = Pair.of(0, "foo");
    final MutablePair<Integer, String> mutablePair = MutablePair.ofNonNull(pair);
    assertEquals(pair.getLeft(), mutablePair.getLeft());
    assertEquals(pair.getRight(), mutablePair.getRight());
}
```