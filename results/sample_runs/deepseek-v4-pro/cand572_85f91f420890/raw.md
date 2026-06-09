# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `62b5acac4c8bdfe3801e2f0ffe8fd6e889b79e08`
- B: `85f91f4208903bb7ca608d51c941214b667d3c06`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `methods`
- user_chars: `3948`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1499, 'completion_tokens': 906, 'total_tokens': 2405, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 536}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1115}`

---

- 新增测试方法 `testContainsAnyInt`，对应生产代码新增的 `containsAny(int[], int...)` 方法。
- 将旧测试方法 `testContainsAny` 修改为 `testContainsAnyObject`，保留原有对象数组测试逻辑并匹配新方法名。
- 删除旧测试方法 `testContainsAny`，因其已被拆分。
- 无需调整 import，现有引用已满足要求。

```java
// DELETE_TESTS_START
testContainsAny
// DELETE_TESTS_END

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