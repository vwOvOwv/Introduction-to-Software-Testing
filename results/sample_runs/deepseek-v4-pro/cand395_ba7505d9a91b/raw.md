# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `4e9460413a01846265831129eae856cb75ba9edb`
- B: `ba7505d9a91be02088e1309f172f3dc55823c9c0`
- test: `src/test/java/org/apache/commons/lang3/RandomUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `11870`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3332, 'completion_tokens': 1650, 'total_tokens': 4982, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1323}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2948}`

---

- 新增静态导入 `import static org.junit.jupiter.api.Assertions.assertNotEquals;`，因为测试 diff 中新增了对它的使用。
- 新增 `@Test` 方法 `testLargeValueRangeLong()`，该方法验证新实现不会返回上界值，与测试 diff 完全一致。
- 旧测试方法无需修改或删除，它们在 B 上的行为保持不变。

```java
import static org.junit.jupiter.api.Assertions.assertNotEquals;

/**
 * Test a large value for long. A previous implementation using
 * {@link RandomUtils#nextDouble(double, double)} could generate a value equal
 * to the upper limit.
 *
 * <pre>
 * return (long) nextDouble(startInclusive, endExclusive);
 * </pre>
 *
 * <p>See LANG-1592.</p>
 */
@Test
public void testLargeValueRangeLong() {
    final long startInclusive = 12900000000001L;
    final long endExclusive = 12900000000016L;
    // Note: The method using 'return (long) nextDouble(startInclusive, endExclusive)'
    // takes thousands of calls to generate an error. This size loop fails most
    // of the time with the previous method.
    final int n = (int) (endExclusive - startInclusive) * 1000;
    for (int i = 0; i < n; i++) {
        assertNotEquals(endExclusive, RandomUtils.nextLong(startInclusive, endExclusive));
    }
}
```