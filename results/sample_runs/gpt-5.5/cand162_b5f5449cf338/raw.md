# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cde4c529034e182a982fd842252ec410d213c34c`
- B: `b5f5449cf338376d12404d0190054525987f4276`
- test: `src/test/java/org/apache/commons/lang3/CharSequenceUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/CharSequenceUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `11436`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3051, 'completion_tokens': 303, 'total_tokens': 3354}`

---

- 新增 `testLastIndexOfSupplementaryCharacters`：覆盖生产代码中 `lastIndexOf` 对 supplementary code point 的新处理逻辑。
- 新增 `testIndexOfSupplementaryCharacters`：覆盖生产代码中 `indexOf` 对 supplementary code point 的新处理逻辑。
- 不需要调整 import：旧测试已包含 `org.junit.Test` 与静态断言导入。

```java
@Test
public void testLastIndexOfSupplementaryCharacters() {
    final int CODE_POINT = 0x2070E;
    final StringBuilder builder = new StringBuilder();
    builder.appendCodePoint(CODE_POINT);
    assertEquals(0, CharSequenceUtils.lastIndexOf(builder, CODE_POINT, 0));
}

@Test
public void testIndexOfSupplementaryCharacters() {
    final int CODE_POINT = 0x2070E;
    final StringBuilder builder = new StringBuilder();
    builder.appendCodePoint(CODE_POINT);
    assertEquals(0, CharSequenceUtils.indexOf(builder, CODE_POINT, 0));
}
```