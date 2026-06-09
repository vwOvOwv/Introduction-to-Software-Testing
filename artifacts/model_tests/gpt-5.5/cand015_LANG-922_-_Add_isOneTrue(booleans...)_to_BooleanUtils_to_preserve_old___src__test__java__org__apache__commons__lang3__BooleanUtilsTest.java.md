# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `aadbea734d78e8d535d3a5837643336ca1384bd2`
- B: `0de9354f505f415c7ad35fe735cebab4900a698a`
- test: `src/test/java/org/apache/commons/lang3/BooleanUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/BooleanUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `49706`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 10644, 'completion_tokens': 1492, 'total_tokens': 12136}`

---

- 新增 `testIsOneTrue_primitive_nullInput`，覆盖新增的 `BooleanUtils.isOneTrue(boolean...)` 对 `null` 数组抛出 `IllegalArgumentException` 的行为；无需调整 import。
- 新增 `testIsOneTrue_primitive_emptyInput`，覆盖新增的 `BooleanUtils.isOneTrue(boolean...)` 对空数组抛出 `IllegalArgumentException` 的行为；无需调整 import。
- 新增 `testIsOneTrue_primitive_validInput_2items`，覆盖新增的 primitive 两元素“恰好一个 true”判断逻辑；无需调整 import。
- 新增 `testIsOneTrue_primitive_validInput_3items`，覆盖新增的 primitive 三元素“恰好一个 true”判断逻辑；无需调整 import。
- 新增 `testIsOneTrue_object_nullInput`，覆盖新增的 `BooleanUtils.isOneTrue(Boolean...)` 对 `null` 数组抛出 `IllegalArgumentException` 的行为；无需调整 import。
- 新增 `testIsOneTrue_object_emptyInput`，覆盖新增的 `BooleanUtils.isOneTrue(Boolean...)` 对空数组抛出 `IllegalArgumentException` 的行为；无需调整 import。
- 新增 `testIsOneTrue_object_nullElementInput`，覆盖新增的 `BooleanUtils.isOneTrue(Boolean...)` 对包含 `null` 元素数组抛出 `IllegalArgumentException` 的行为；无需调整 import。
- 新增 `testIsOneTrue_object_validInput_2items`，覆盖新增的 Boolean 对象两元素“恰好一个 true”判断逻辑；无需调整 import。
- 新增 `testIsOneTrue_object_validInput_3items`，覆盖新增的 Boolean 对象三元素“恰好一个 true”判断逻辑；无需调整 import。

```java
@Test(expected = IllegalArgumentException.class)
public void testIsOneTrue_primitive_nullInput() {
    BooleanUtils.isOneTrue((boolean[]) null);
}

@Test(expected = IllegalArgumentException.class)
public void testIsOneTrue_primitive_emptyInput() {
    BooleanUtils.isOneTrue(new boolean[] {});
}

@Test
public void testIsOneTrue_primitive_validInput_2items() {
    assertFalse(
            "true, true",
            BooleanUtils.isOneTrue(new boolean[] { true, true }));

    assertFalse(
            "false, false",
            BooleanUtils.isOneTrue(new boolean[] { false, false }));

    assertTrue(
            "true, false",
            BooleanUtils.isOneTrue(new boolean[] { true, false }));

    assertTrue(
            "false, true",
            BooleanUtils.isOneTrue(new boolean[] { false, true }));
}

@Test
public void testIsOneTrue_primitive_validInput_3items() {
    assertFalse(
            "false, false, false",
            BooleanUtils.isOneTrue(new boolean[] { false, false, false }));

    assertTrue(
            "false, false, true",
            BooleanUtils.isOneTrue(new boolean[] { false, false, true }));

    assertTrue(
            "false, true, false",
            BooleanUtils.isOneTrue(new boolean[] { false, true, false }));

    assertFalse(
            "false, true, true",
            BooleanUtils.isOneTrue(new boolean[] { false, true, true }));

    assertTrue(
            "true, false, false",
            BooleanUtils.isOneTrue(new boolean[] { true, false, false }));

    assertFalse(
            "true, false, true",
            BooleanUtils.isOneTrue(new boolean[] { true, false, true }));

    assertFalse(
            "true, true, false",
            BooleanUtils.isOneTrue(new boolean[] { true, true, false }));

    assertFalse(
            "true, true, true",
            BooleanUtils.isOneTrue(new boolean[] { true, true, true }));
}

@Test(expected = IllegalArgumentException.class)
public void testIsOneTrue_object_nullInput() {
    BooleanUtils.isOneTrue((Boolean[]) null);
}

@Test(expected = IllegalArgumentException.class)
public void testIsOneTrue_object_emptyInput() {
    BooleanUtils.isOneTrue(new Boolean[] {});
}

@Test(expected = IllegalArgumentException.class)
public void testIsOneTrue_object_nullElementInput() {
    BooleanUtils.isOneTrue(new Boolean[] {null});
}

@Test
public void testIsOneTrue_object_validInput_2items() {
    assertFalse(
            "false, false",
            BooleanUtils
                    .isOneTrue(new Boolean[] { Boolean.FALSE, Boolean.FALSE })
                    .booleanValue());

    assertTrue(
            "false, true",
            BooleanUtils
                    .isOneTrue(new Boolean[] { Boolean.FALSE, Boolean.TRUE })
                    .booleanValue());

    assertTrue(
            "true, false",
            BooleanUtils
                    .isOneTrue(new Boolean[] { Boolean.TRUE, Boolean.FALSE })
                    .booleanValue());

    assertFalse(
            "true, true",
            BooleanUtils
                    .isOneTrue(new Boolean[] { Boolean.TRUE, Boolean.TRUE })
                    .booleanValue());
}

@Test
public void testIsOneTrue_object_validInput_3items() {
    assertFalse(
            "false, false, false",
            BooleanUtils.isOneTrue(
                    new Boolean[] {
                            Boolean.FALSE,
                            Boolean.FALSE,
                            Boolean.FALSE })
                    .booleanValue());

    assertTrue(
            "false, false, true",
            BooleanUtils
                    .isOneTrue(
                            new Boolean[] {
                                    Boolean.FALSE,
                                    Boolean.FALSE,
                                    Boolean.TRUE })
                    .booleanValue());

    assertTrue(
            "false, true, false",
            BooleanUtils
                    .isOneTrue(
                            new Boolean[] {
                                    Boolean.FALSE,
                                    Boolean.TRUE,
                                    Boolean.FALSE })
                    .booleanValue());

    assertTrue(
            "true, false, false",
            BooleanUtils
                    .isOneTrue(
                            new Boolean[] {
                                    Boolean.TRUE,
                                    Boolean.FALSE,
                                    Boolean.FALSE })
                    .booleanValue());

    assertFalse(
            "true, false, true",
            BooleanUtils.isOneTrue(
                    new Boolean[] {
                            Boolean.TRUE,
                            Boolean.FALSE,
                            Boolean.TRUE })
                    .booleanValue());

    assertFalse(
            "true, true, false",
            BooleanUtils.isOneTrue(
                    new Boolean[] {
                            Boolean.TRUE,
                            Boolean.TRUE,
                            Boolean.FALSE })
                    .booleanValue());

    assertFalse(
            "false, true, true",
            BooleanUtils.isOneTrue(
                    new Boolean[] {
                            Boolean.FALSE,
                            Boolean.TRUE,
                            Boolean.TRUE })
                    .booleanValue());

    assertFalse(
            "true, true, true",
            BooleanUtils
                    .isOneTrue(new Boolean[] { Boolean.TRUE, Boolean.TRUE, Boolean.TRUE })
                    .booleanValue());
}
```