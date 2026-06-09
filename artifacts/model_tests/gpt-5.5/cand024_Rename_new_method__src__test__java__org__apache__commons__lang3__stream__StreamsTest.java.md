# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e0818e3383f71ddff62854f85712cb6b7d187c9b`
- B: `152b1777fddc5127e77f9b14637d6abae18eaf05`
- test: `src/test/java/org/apache/commons/lang3/stream/StreamsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/stream/Streams.java']`
- old_test_mode: `methods`
- user_chars: `8213`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2533, 'completion_tokens': 364, 'total_tokens': 2897}`

---

- 新增 `testOfCollectionNotNull`：生产代码将 `toStream(Collection)` 重命名/替换为 `of(Collection)`，需要覆盖非 null 集合场景。
- 新增 `testOfCollectionNull`：生产代码新增 `Streams.of(Collection)` 的 null 安全行为，需要覆盖 null 集合场景。
- 删除 `testToStreamNotNull`：`Streams.toStream(Collection)` 已从生产代码删除，旧测试在 B 上无法编译。
- 删除 `testToStreamNull`：`Streams.toStream(Collection)` 已从生产代码删除，旧测试在 B 上无法编译。
- `testInstanceOfStream` 与 `testNullSafeStreamNotNull` 无需修改；import 无需调整。

```java
// DELETE_TESTS_START
testToStreamNotNull
testToStreamNull
// DELETE_TESTS_END

@Test
public void testOfCollectionNotNull() {
    assertEquals(2, Streams.of(Arrays.asList("A", "B")).collect(Collectors.toList()).size());
}

@Test
public void testOfCollectionNull() {
    final List<String> input = null;
    assertEquals(0, Streams.of(input).collect(Collectors.toList()).size());
}
```