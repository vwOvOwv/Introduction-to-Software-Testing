# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `259ac721ce5097312d8bd93aefde26c2785f26e9`
- B: `a606a0328ba4b3061c5bc810a31418fa4251ea16`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `34958`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 8285, 'completion_tokens': 571, 'total_tokens': 8856}`

---

- 新增 `testGetFirstNonNull`：覆盖新增生产方法 `ObjectUtils.getFirstNonNull(Supplier<T>...)` 的惰性求值、空 supplier、空 varargs、null varargs 与不同返回类型行为。
- 调整 import：新增 `org.junit.jupiter.api.Assertions.fail` 的静态导入，用于断言找到首个非 null 值后后续 supplier 不会被执行。

```java
import static org.junit.jupiter.api.Assertions.fail;

@Test
public void testGetFirstNonNull() {
    // first non null
    assertEquals("", ObjectUtils.getFirstNonNull(() -> null, () -> ""));
    // first encountered value is used
    assertEquals("1", ObjectUtils.getFirstNonNull(() -> null, () -> "1", () -> "2", () -> null));
    assertEquals("123", ObjectUtils.getFirstNonNull(() -> "123", () -> null, () -> "456"));
    // don't evaluate suppliers after first value is found
    assertEquals("123", ObjectUtils.getFirstNonNull(() -> null, () -> "123", () -> fail("Supplier after first non-null value should not be evaluated")));
    // supplier returning null and null supplier both result in null
    assertNull(ObjectUtils.getFirstNonNull(null, () -> null));
    // Explicitly pass in an empty array of Object type to ensure compiler doesn't complain of unchecked generic array creation
    assertNull(ObjectUtils.getFirstNonNull());
    // supplier is null
    assertNull(ObjectUtils.getFirstNonNull((Supplier<Object>) null));
    // varargs array itself is null
    assertNull(ObjectUtils.getFirstNonNull((Supplier<Object>[]) null));
    // test different types
    assertEquals(1, ObjectUtils.getFirstNonNull(() -> null, () -> 1));
    assertEquals(Boolean.TRUE, ObjectUtils.getFirstNonNull(() -> null, () -> Boolean.TRUE));
}
```