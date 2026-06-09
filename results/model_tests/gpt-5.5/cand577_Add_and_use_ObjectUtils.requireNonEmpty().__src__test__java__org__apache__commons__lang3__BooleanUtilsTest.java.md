# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `43f0424827dfcbc3a301007b5d5ca0e412473948`
- B: `ea344865514a8b75eb4e9d1a159fc8434e5bb7fa`
- test: `src/test/java/org/apache/commons/lang3/BooleanUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/BooleanUtils.java']`
- old_test_mode: `methods`
- user_chars: `11617`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3239, 'completion_tokens': 469, 'total_tokens': 3708}`

---

- 修改 `testAnd_object_nullInput`：生产代码对 `BooleanUtils.and((Boolean[]) null)` 改为通过 `ObjectUtils.requireNonEmpty` 抛出 `NullPointerException`。
- 修改 `testAnd_primitive_nullInput`：生产代码对 `BooleanUtils.and((boolean[]) null)` 改为抛出 `NullPointerException`。
- 修改 `testOr_object_nullInput`：生产代码对 `BooleanUtils.or((Boolean[]) null)` 改为抛出 `NullPointerException`。
- 修改 `testOr_primitive_nullInput`：生产代码对 `BooleanUtils.or((boolean[]) null)` 改为抛出 `NullPointerException`。
- 修改 `testXor_object_nullInput`：生产代码对 `BooleanUtils.xor((Boolean[]) null)` 改为抛出 `NullPointerException`。
- 修改 `testXor_primitive_nullInput`：生产代码对 `BooleanUtils.xor((boolean[]) null)` 改为抛出 `NullPointerException`。
- 不需要调整 import：`NullPointerException` 属于 `java.lang`。

```java
@Test
public void testAnd_object_nullInput() {
    assertThrows(NullPointerException.class, () -> BooleanUtils.and((Boolean[]) null));
}

@Test
public void testAnd_primitive_nullInput() {
    assertThrows(NullPointerException.class, () -> BooleanUtils.and((boolean[]) null));
}

@Test
public void testOr_object_nullInput() {
    assertThrows(NullPointerException.class, () -> BooleanUtils.or((Boolean[]) null));
}

@Test
public void testOr_primitive_nullInput() {
    assertThrows(NullPointerException.class, () -> BooleanUtils.or((boolean[]) null));
}

@Test
public void testXor_object_nullInput() {
    assertThrows(NullPointerException.class, () -> BooleanUtils.xor((Boolean[]) null));
}

@Test
public void testXor_primitive_nullInput() {
    assertThrows(NullPointerException.class, () -> BooleanUtils.xor((boolean[]) null));
}
```