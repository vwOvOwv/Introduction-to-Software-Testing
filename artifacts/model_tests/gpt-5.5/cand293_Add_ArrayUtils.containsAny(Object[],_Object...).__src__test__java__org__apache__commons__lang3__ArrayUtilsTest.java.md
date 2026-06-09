# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `4369537d8b1387b94a1126a36a4fc400a35d35cc`
- B: `5def1c8d634f12a265662f38188cd611aa1e574b`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `methods`
- user_chars: `3921`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1440, 'completion_tokens': 415, 'total_tokens': 1855}`

---

- 修改 `testContains`：对照测试 diff，仅调整 `null` 命中断言的位置，保持 `contains` 既有行为断言。
- 新增 `testContainsAny`：对照生产 diff 新增的 `ArrayUtils.containsAny(Object[], Object...)` 方法，覆盖空数组、命中、未命中和查找 `null` 的场景。
- import 无需调整：新增测试复用现有 `@Test` 与断言静态导入。

```java
    @Test
    public void testContains() {
        final Object[] array = {"0", "1", "2", "3", null, "0"};
        assertFalse(ArrayUtils.contains(null, null));
        assertFalse(ArrayUtils.contains(null, "1"));
        assertTrue(ArrayUtils.contains(array, "0"));
        assertTrue(ArrayUtils.contains(array, "1"));
        assertTrue(ArrayUtils.contains(array, "2"));
        assertTrue(ArrayUtils.contains(array, "3"));
        assertFalse(ArrayUtils.contains(array, "notInArray"));
        assertTrue(ArrayUtils.contains(array, null));
    }

    @Test
    public void testContainsAny() {
        final Object[] array = {"0", "1", "2", "3", null, "0"};
        assertFalse(ArrayUtils.containsAny(null, null));
        assertFalse(ArrayUtils.containsAny(null, "1"));
        assertTrue(ArrayUtils.containsAny(array, "0"));
        assertTrue(ArrayUtils.containsAny(array, "1"));
        assertTrue(ArrayUtils.containsAny(array, "2"));
        assertTrue(ArrayUtils.containsAny(array, "3"));
        assertFalse(ArrayUtils.containsAny(array, "notInArray"));
        assertTrue(ArrayUtils.containsAny(array, new String[] {null}));
    }
```