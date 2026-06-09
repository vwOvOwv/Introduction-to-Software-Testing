# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `3c44319a177428fe4867b8b1a7886e04b8f1677b`
- B: `9feaf9d7ffe3f4438ccdace378f49f1d4dadd418`
- test: `src/test/java/org/apache/commons/lang3/builder/DiffResultTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/DiffResult.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `8170`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2308, 'completion_tokens': 246, 'total_tokens': 2554}`

---

- 新增 `testLeftAndRightGetters`：覆盖生产代码新增的 `DiffResult#getLeft()` 与 `DiffResult#getRight()`，断言分别返回构造 `DiffResult` 时传入的左右对象。
- import 无需调整：新增测试仅使用已有的 `List`、`Diff`、`DiffResult`、`assertEquals` 和 `@Test`。

```java
    @Test
    public void testLeftAndRightGetters() {
        final SimpleClass left = new SimpleClass(true);
        final SimpleClass right = new SimpleClass(false);

        final List<Diff<?>> diffs = left.diff(right).getDiffs();
        final DiffResult diffResult = new DiffResult(left, right, diffs, SHORT_STYLE);

        assertEquals(left, diffResult.getLeft());
        assertEquals(right, diffResult.getRight());
    }
```