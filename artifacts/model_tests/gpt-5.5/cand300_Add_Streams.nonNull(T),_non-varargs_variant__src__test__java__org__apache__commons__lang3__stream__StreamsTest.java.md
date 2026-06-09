# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `45ad8976cb94010bcc36688f885fbf119f146252`
- B: `64736630706adf9e2cbb482fbfcbdc81a9dc02f7`
- test: `src/test/java/org/apache/commons/lang3/stream/StreamsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/stream/Streams.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `15014`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3955, 'completion_tokens': 231, 'total_tokens': 4186}`

---

- 新增 `testNonNull`：覆盖生产代码新增的 `Streams.nonNull(E)` 单元素重载，并同时验证已有可变参数 `nonNull` 对空参数和含 null 元素的过滤行为；无需调整 import。

```java
@Test
public void testNonNull() {
    assertEquals(0, Streams.nonNull().collect(Collectors.toList()).size());
    assertEquals(1, Streams.nonNull("A").collect(Collectors.toList()).size());
    assertEquals(1, Streams.nonNull("A", null).collect(Collectors.toList()).size());
    assertEquals(1, Streams.nonNull(null, "A").collect(Collectors.toList()).size());
}
```