# DeepSeek 输出

- repo: `/home/netro/Introduction-to-Software-Testing/commons-lang`
- A: `62b5acac4c8bdfe3801e2f0ffe8fd6e889b79e08`
- B: `85f91f4208903bb7ca608d51c941214b667d3c06`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `methods`
- user_chars: `4220`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1559, 'completion_tokens': 363, 'total_tokens': 1922, 'prompt_tokens_details': {'cached_tokens': 256}, 'prompt_cache_hit_tokens': 256, 'prompt_cache_miss_tokens': 1303}`

---

- 将原有的 `testContainsAny` 方法重命名为 `testContainsAnyObject`，并保留其原有断言逻辑。
- 新增 `testContainsAnyInt` 方法，用于测试新增的 `containsAny(int[], int...)` 方法。
- 无需调整 import，因为测试类中已包含所需的静态导入。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
// IMPORTS_END

    @Test
    public void testContainsAnyInt() {
        final int[] array = {0, 1, 2, 3, 0};
        assertFalse(ArrayUtils.containsAny((int[]) null, 1));
        assertTrue(ArrayUtils.containsAny(array, 0));
        assertTrue(ArrayUtils.containsAny(array, 1));
        assertTrue(ArrayUtils.containsAny(array, 2));
        assertTrue(ArrayUtils.containsAny(array, 3));
    }

    @Test
    public void testContainsAnyObject() {
        final Object[] array = {"0", "1", "2", "3", null, "0"};
        assertFalse(ArrayUtils.containsAny(null, (Object) null));
        assertFalse(ArrayUtils.containsAny(null, "1"));
        assertTrue(ArrayUtils.containsAny(array, "0"));
        assertTrue(ArrayUtils.containsAny(array, "1"));
        assertTrue(ArrayUtils.containsAny(array, "2"));
        assertTrue(ArrayUtils.containsAny(array, "3"));
        assertFalse(ArrayUtils.containsAny(array, "notInArray"));
        assertTrue(ArrayUtils.containsAny(array, (Object[]) new String[] { null }));
    }
```