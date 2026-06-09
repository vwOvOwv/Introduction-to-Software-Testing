# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `557252762bb29887ddeaf9c99f16572bae19316c`
- B: `c140fc8154e8c680aad63239eaaaac14d85d5683`
- test: `src/test/java/org/apache/commons/lang3/tuple/MutablePairTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/tuple/MutablePair.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `8310`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2446, 'completion_tokens': 264, 'total_tokens': 2710}`

---

- 新增 `testOfNonNullMapEntry`：覆盖生产代码新增的 `MutablePair.ofNonNull(Map.Entry<L, R>)`，断言 `null` 入参抛出 `NullPointerException`，并验证从 `Pair` 复制左右值。
- import 无需调整：现有静态断言和同包 `Pair`/`MutablePair` 均已满足新增测试需求。

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