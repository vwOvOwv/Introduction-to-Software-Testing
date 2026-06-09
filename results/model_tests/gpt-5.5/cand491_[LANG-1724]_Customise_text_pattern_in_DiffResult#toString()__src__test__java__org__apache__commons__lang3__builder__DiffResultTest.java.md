# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `75c6b5877735da8558e49aec29a91f8453ff268a`
- B: `b1b409ae4096664a33787bf52be32d9d2eb0cb31`
- test: `src/test/java/org/apache/commons/lang3/builder/DiffResultTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/DiffResult.java']`
- old_test_mode: `methods`
- user_chars: `9836`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2830, 'completion_tokens': 1071, 'total_tokens': 3901}`

---

- 新增 `testDefaultStyle`：生产代码构造器不再接受 `null` style 并改为显式传入 `ToStringStyle.DEFAULT_STYLE` 与 `DiffBuilder.TO_STRING_FORMAT`。
- 修改 `testIterator`：`DiffResult` 构造器新增 `toStringFormat` 参数，需要传入 `DiffBuilder.TO_STRING_FORMAT`。
- 修改 `testLeftAndRightGetters`：`DiffResult` 构造器新增 `toStringFormat` 参数，需要传入 `DiffBuilder.TO_STRING_FORMAT`。
- 修改 `testListIsNonModifiable`：`DiffResult` 构造器新增 `toStringFormat` 参数，需要传入 `DiffBuilder.TO_STRING_FORMAT`。
- 修改 `testNullLhs`：`DiffResult` 构造器新增 `toStringFormat` 参数，需要传入 `DiffBuilder.TO_STRING_FORMAT`。
- 修改 `testNullList`：构造器现在对 `diffList`、`style`、`toStringFormat` 均要求非空，保留断言 `diffList` 为 `null` 时抛出异常。
- 修改 `testNullRhs`：`DiffResult` 构造器新增 `toStringFormat` 参数，需要传入 `DiffBuilder.TO_STRING_FORMAT`。
- 删除 `testNullStyle`：生产代码不再将 `null` style 默认化为 `ToStringStyle.DEFAULT_STYLE`，而是直接抛出 `NullPointerException`。
- import 无需调整。

```java
// DELETE_TESTS_START
testNullStyle
// DELETE_TESTS_END

    @Test
    public void testDefaultStyle() {
        final DiffResult<SimpleClass> diffResult = new DiffResult<>(SIMPLE_TRUE, SIMPLE_FALSE, SIMPLE_TRUE.diff(SIMPLE_FALSE).getDiffs(),
                ToStringStyle.DEFAULT_STYLE, DiffBuilder.TO_STRING_FORMAT);
        assertEquals(ToStringStyle.DEFAULT_STYLE, diffResult.getToStringStyle());
    }

    @Test
    public void testIterator() {
        final SimpleClass lhs = new SimpleClass(true);
        final SimpleClass rhs = new SimpleClass(false);

        final List<Diff<?>> diffs = lhs.diff(rhs).getDiffs();
        final Iterator<Diff<?>> expectedIterator = diffs.iterator();

        final DiffResult<SimpleClass> list = new DiffResult<>(lhs, rhs, diffs, SHORT_STYLE, DiffBuilder.TO_STRING_FORMAT);
        final Iterator<Diff<?>> iterator = list.iterator();

        while (iterator.hasNext()) {
            assertTrue(expectedIterator.hasNext());
            assertEquals(expectedIterator.next(), iterator.next());
        }
    }

    @Test
    public void testLeftAndRightGetters() {
        final SimpleClass left = new SimpleClass(true);
        final SimpleClass right = new SimpleClass(false);

        final List<Diff<?>> diffs = left.diff(right).getDiffs();
        final DiffResult diffResult = new DiffResult(left, right, diffs, SHORT_STYLE, DiffBuilder.TO_STRING_FORMAT);

        assertEquals(left, diffResult.getLeft());
        assertEquals(right, diffResult.getRight());
    }

    @Test
    public void testListIsNonModifiable() {
        final SimpleClass lhs = new SimpleClass(true);
        final SimpleClass rhs = new SimpleClass(false);

        final List<Diff<?>> diffs = lhs.diff(rhs).getDiffs();

        final DiffResult<SimpleClass> list = new DiffResult<>(lhs, rhs, diffs, SHORT_STYLE, DiffBuilder.TO_STRING_FORMAT);
        assertEquals(diffs, list.getDiffs());
        assertEquals(1, list.getNumberOfDiffs());
        assertThrows(UnsupportedOperationException.class, () -> list.getDiffs().remove(0));
    }

    @Test
    public void testNullLhs() {
        assertThrows(NullPointerException.class,
            () -> new DiffResult<>(null, SIMPLE_FALSE, SIMPLE_TRUE.diff(SIMPLE_FALSE).getDiffs(), SHORT_STYLE, DiffBuilder.TO_STRING_FORMAT));
    }

    @Test
    public void testNullList() {
        assertThrows(NullPointerException.class,
            () -> new DiffResult<>(SIMPLE_TRUE, SIMPLE_FALSE, null, SHORT_STYLE, null));
    }

    @Test
    public void testNullRhs() {
        assertThrows(NullPointerException.class,
            () -> new DiffResult<>(SIMPLE_TRUE, null, SIMPLE_TRUE.diff(SIMPLE_FALSE).getDiffs(), SHORT_STYLE, DiffBuilder.TO_STRING_FORMAT));
    }
```