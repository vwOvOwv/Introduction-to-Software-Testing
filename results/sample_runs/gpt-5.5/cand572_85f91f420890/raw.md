# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `62b5acac4c8bdfe3801e2f0ffe8fd6e889b79e08`
- B: `85f91f4208903bb7ca608d51c941214b667d3c06`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `methods`
- user_chars: `3948`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1485, 'completion_tokens': 480, 'total_tokens': 1965}`

---

- 新增 `testContainsAnyInt`，对应生产代码新增 `ArrayUtils.containsAny(int[], int...)` 的覆盖。
- 将旧的 `testContainsAny` 修改并重命名为 `testContainsAnyObject`，以明确覆盖既有对象数组重载并避免与新增 int 重载混淆。
- 不需要调整 import。

```java
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