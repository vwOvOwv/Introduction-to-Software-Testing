# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `75c6b5877735da8558e49aec29a91f8453ff268a`
- B: `b1b409ae4096664a33787bf52be32d9d2eb0cb31`
- test: `src/test/java/org/apache/commons/lang3/builder/DiffResultTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/DiffResult.java']`
- old_test_mode: `methods`
- user_chars: `9836`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3000, 'completion_tokens': 2690, 'total_tokens': 5690, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1785}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2616}`

---

- 新增 `testDefaultStyle` 方法，验证 `DiffResult` 的 `toStringFormat` 必须非 `null` 后，默认样式仍可通过 getter 获取。  
- 修改 `testIterator`、`testLeftAndRightGetters`、`testListIsNonModifiable`、`testNullLhs`、`testNullList`、`testNullRhs` 方法，将 `DiffResult` 构造调用从 4 参数改为 5 参数，新增第 5 参数 `DiffBuilder.TO_STRING_FORMAT`（`testNullList` 中第 5 参数传 `null`，因其 diffList 为 `null` 仍会先抛出 `NullPointerException`）。  
- 删除 `testNullStyle` 方法，因为构造函数不再允许 `style` 为 `null`。  
- 需要新增 `import org.apache.commons.lang3.builder.DiffBuilder;`，因为使用了 `DiffBuilder.TO_STRING_FORMAT`。

```java
// IMPORTS_START
import org.apache.commons.lang3.builder.DiffBuilder;
// IMPORTS_END

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