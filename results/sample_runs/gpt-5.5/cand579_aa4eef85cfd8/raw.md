# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `d0f012d73699b99fdb8e6addaa793a9519b6a5b3`
- B: `aa4eef85cfd88e55677df238b44c6cc463d0af91`
- test: `src/test/java/org/apache/commons/lang3/builder/DiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/DiffBuilder.java']`
- old_test_mode: `methods`
- user_chars: `36466`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9735, 'completion_tokens': 859, 'total_tokens': 10594}`

---

- 新增 `testByteArrayEqualAsObject1`，用于覆盖生产代码新增的 `DiffBuilder.builder()` fluent builder API 创建方式。
- 新增 `testByteArrayEqualAsObjectDeprecated`，保留对已标记 `@Deprecated` 的旧构造器行为验证。
- 删除旧的 `testByteArrayEqualAsObject`，因为金标准将其拆分为 builder API 与 deprecated constructor 两个测试。
- import 无需调整。

```java
// DELETE_TESTS_START
testByteArrayEqualAsObject
// DELETE_TESTS_END

@Test
public void testByteArrayEqualAsObject1() {
    // @formatter:off
    final DiffResult<String> list = DiffBuilder.<String>builder().setLeft("String1").setRight("String2").setStyle(SHORT_STYLE).build()
            .append("foo", new boolean[] { false }, new boolean[] { false })
            .append("foo", new byte[] { 0x01 }, new byte[] { 0x01 })
            .append("foo", new char[] { 'a' }, new char[] { 'a' })
            .append("foo", new double[] { 1.0 }, new double[] { 1.0 })
            .append("foo", new float[] { 1.0F }, new float[] { 1.0F })
            .append("foo", new int[] { 1 }, new int[] { 1 })
            .append("foo", new long[] { 1L }, new long[] { 1L })
            .append("foo", new short[] { 1 }, new short[] { 1 })
            .append("foo", new Object[] { 1, "two" }, new Object[] { 1, "two" })
            .build();
    // @formatter:off
    assertEquals(0, list.getNumberOfDiffs());
}

@Test
public void testByteArrayEqualAsObjectDeprecated() {
    // @formatter:off
    final DiffResult<String> list = new DiffBuilder<>("String1", "String2", SHORT_STYLE)
            .append("foo", new boolean[] { false }, new boolean[] { false })
            .append("foo", new byte[] { 0x01 }, new byte[] { 0x01 })
            .append("foo", new char[] { 'a' }, new char[] { 'a' })
            .append("foo", new double[] { 1.0 }, new double[] { 1.0 })
            .append("foo", new float[] { 1.0F }, new float[] { 1.0F })
            .append("foo", new int[] { 1 }, new int[] { 1 })
            .append("foo", new long[] { 1L }, new long[] { 1L })
            .append("foo", new short[] { 1 }, new short[] { 1 })
            .append("foo", new Object[] { 1, "two" }, new Object[] { 1, "two" })
            .build();
    // @formatter:off
    assertEquals(0, list.getNumberOfDiffs());
}
```