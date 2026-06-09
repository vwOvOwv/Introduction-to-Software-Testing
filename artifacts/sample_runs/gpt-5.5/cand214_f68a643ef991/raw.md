# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `6ea4e39087cca04ecb57385acd6c8d8f699186b9`
- B: `f68a643ef99189d10a6753167367dcc8f943d634`
- test: `src/test/java/org/apache/commons/lang3/exception/ExceptionUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/exception/ExceptionUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `41929`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9407, 'completion_tokens': 107, 'total_tokens': 9514}`

---

- 新增 `testIsUnchecked_null`：对应生产代码 `isUnchecked` 对 `null` 从旧逻辑的 `!isChecked(null)` 调整为显式返回 `false`，需要补充空值断言；无需调整 import。

```java
@Test
public void testIsUnchecked_null() {
    assertFalse(ExceptionUtils.isUnchecked(null));
}
```