# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `3da149382fcc8c8880cc96aba2c93cc575cc4970`
- B: `680f9d5492e2c9c27e5c1178744a9edf36a0272b`
- test: `src/test/java/org/apache/commons/lang3/builder/ToStringBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/ToStringBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `63017`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 16146, 'completion_tokens': 157, 'total_tokens': 16303}`

---

- 新增 `testAppendAsObjectToStringNullPointerException`，对应生产代码为 `appendAsObjectToString(Object)` 明确 `srcObject == null` 时抛出 `NullPointerException` 的行为补充测试；无需调整 import，旧测试已静态导入 `assertThrows`。

```java
@Test
public void testAppendAsObjectToStringNullPointerException() {
    ToStringBuilder builder = new ToStringBuilder(1);
    assertThrows(NullPointerException.class, () -> builder.appendAsObjectToString(null));
    builder.toString();
}
```