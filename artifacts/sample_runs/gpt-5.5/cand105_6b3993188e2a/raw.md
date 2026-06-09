# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `25a0fd71c28c60bdca99702fc214cce025a0f946`
- B: `6b3993188e2a6396f94461c0e7fbd5738ecaa14c`
- test: `src/test/java/org/apache/commons/lang3/BooleanUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/BooleanUtils.java']`
- old_test_mode: `methods`
- user_chars: `22048`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 4790, 'completion_tokens': 1456, 'total_tokens': 6246}`

---

- 删除旧的 `testIsOneTrue_*` 测试方法，并新增对应的 `testIsExactlyOneTrue_*` 方法，因为生产方法 `BooleanUtils.isOneTrue(...)` 已重命名为 `BooleanUtils.isExactlyOneTrue(...)`。
- 所有断言逻辑保持不变，仅将调用目标改为新的 `isExactlyOneTrue` 重载方法；不需要调整 import。

```java
// DELETE_TESTS_START
testIsOneTrue_object_emptyInput
testIsOneTrue_object_nullElementInput
testIsOneTrue_object_nullInput
testIsOneTrue_object_validInput_2items
testIsOneTrue_object_validInput_3items
testIsOneTrue_primitive_emptyInput
testIsOneTrue_primitive_nullInput
testIsOneTrue_primitive_validInput_2items
testIsOneTrue_primitive_validInput_3items
// DELETE_TESTS_END

@Test(expected = IllegalArgumentException.class)
public void testIsExactlyOneTrue_object_emptyInput() {
    BooleanUtils.isExactlyOneTrue(new Boolean[] {});
}

@Test(expected = IllegalArgumentException.class)
public void testIsExactlyOneTrue_object_nullElementInput() {
    BooleanUtils.isExactlyOneTrue(new Boolean[] {null});
}

@Test(expected = IllegalArgumentException.class)
public void testIsExactlyOneTrue_object_nullInput() {
    BooleanUtils.isExactlyOneTrue((Boolean[]) null);
}

@Test
public void testIsExactlyOneTrue_object_validInput_2items() {
    assertFalse(
            "false, false",
            BooleanUtils
                    .isExactlyOneTrue(new Boolean[] { Boolean.FALSE, Boolean.FALSE })
                    .booleanValue());

    assertTrue(
            "false, true",
            BooleanUtils
                    .isExactlyOneTrue(new Boolean[] { Boolean.FALSE, Boolean.TRUE })
                    .booleanValue());

    assertTrue(
            "true, false",
            BooleanUtils
                    .isExactlyOneTrue(new Boolean[] { Boolean.TRUE, Boolean.FALSE })
                    .booleanValue());

    assertFalse(
            "true, true",
            BooleanUtils
                    .isExactlyOneTrue(new Boolean[] { Boolean.TRUE, Boolean.TRUE })
                    .booleanValue());
}

@Test
public void testIsExactlyOneTrue_object_validInput_3items() {
    assertFalse(
            "false, false, false",
            BooleanUtils.isExactlyOneTrue(
                    new Boolean[] {
                            Boolean.FALSE,
                            Boolean.FALSE,
                            Boolean.FALSE })
                    .booleanValue());

    assertTrue(
            "false, false, true",
            BooleanUtils
                    .isExactlyOneTrue(
                            new Boolean[] {
                                    Boolean.FALSE,
                                    Boolean.FALSE,
                                    Boolean.TRUE })
                    .booleanValue());

    assertTrue(
            "false, true, false",
            BooleanUtils
                    .isExactlyOneTrue(
                            new Boolean[] {
                                    Boolean.FALSE,
                                    Boolean.TRUE,
                                    Boolean.FALSE })
                    .booleanValue());

    assertTrue(
            "true, false, false",
            BooleanUtils
                    .isExactlyOneTrue(
                            new Boolean[] {
                                    Boolean.TRUE,
                                    Boolean.FALSE,
                                    Boolean.FALSE })
                    .booleanValue());

    assertFalse(
            "true, false, true",
            BooleanUtils.isExactlyOneTrue(
                    new Boolean[] {
                            Boolean.TRUE,
                            Boolean.FALSE,
                            Boolean.TRUE })
                    .booleanValue());

    assertFalse(
            "true, true, false",
            BooleanUtils.isExactlyOneTrue(
                    new Boolean[] {
                            Boolean.TRUE,
                            Boolean.TRUE,
                            Boolean.FALSE })
                    .booleanValue());

    assertFalse(
            "false, true, true",
            BooleanUtils.isExactlyOneTrue(
                    new Boolean[] {
                            Boolean.FALSE,
                            Boolean.TRUE,
                            Boolean.TRUE })
                    .booleanValue());

    assertFalse(
            "true, true, true",
            BooleanUtils
                    .isExactlyOneTrue(new Boolean[] { Boolean.TRUE, Boolean.TRUE, Boolean.TRUE })
                    .booleanValue());
}

@Test(expected = IllegalArgumentException.class)
public void testIsExactlyOneTrue_primitive_emptyInput() {
    BooleanUtils.isExactlyOneTrue(new boolean[] {});
}

@Test(expected = IllegalArgumentException.class)
public void testIsExactlyOneTrue_primitive_nullInput() {
    BooleanUtils.isExactlyOneTrue((boolean[]) null);
}

@Test
public void testIsExactlyOneTrue_primitive_validInput_2items() {
    assertFalse(
            "true, true",
            BooleanUtils.isExactlyOneTrue(new boolean[] { true, true }));

    assertFalse(
            "false, false",
            BooleanUtils.isExactlyOneTrue(new boolean[] { false, false }));

    assertTrue(
            "true, false",
            BooleanUtils.isExactlyOneTrue(new boolean[] { true, false }));

    assertTrue(
            "false, true",
            BooleanUtils.isExactlyOneTrue(new boolean[] { false, true }));
}

@Test
public void testIsExactlyOneTrue_primitive_validInput_3items() {
    assertFalse(
            "false, false, false",
            BooleanUtils.isExactlyOneTrue(new boolean[] { false, false, false }));

    assertTrue(
            "false, false, true",
            BooleanUtils.isExactlyOneTrue(new boolean[] { false, false, true }));

    assertTrue(
            "false, true, false",
            BooleanUtils.isExactlyOneTrue(new boolean[] { false, true, false }));

    assertFalse(
            "false, true, true",
            BooleanUtils.isExactlyOneTrue(new boolean[] { false, true, true }));

    assertTrue(
            "true, false, false",
            BooleanUtils.isExactlyOneTrue(new boolean[] { true, false, false }));

    assertFalse(
            "true, false, true",
            BooleanUtils.isExactlyOneTrue(new boolean[] { true, false, true }));

    assertFalse(
            "true, true, false",
            BooleanUtils.isExactlyOneTrue(new boolean[] { true, true, false }));

    assertFalse(
            "true, true, true",
            BooleanUtils.isExactlyOneTrue(new boolean[] { true, true, true }));
}
```