# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `aadbea734d78e8d535d3a5837643336ca1384bd2`
- B: `0de9354f505f415c7ad35fe735cebab4900a698a`
- test: `src/test/java/org/apache/commons/lang3/BooleanUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/BooleanUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `49706`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 10977, 'completion_tokens': 2057, 'total_tokens': 13034, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 757}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 10593}`

---

- 新增 `testIsOneTrue_primitive_nullInput`、`testIsOneTrue_primitive_emptyInput`、`testIsOneTrue_primitive_validInput_2items`、`testIsOneTrue_primitive_validInput_3items`、`testIsOneTrue_object_nullInput`、`testIsOneTrue_object_emptyInput`、`testIsOneTrue_object_nullElementInput`、`testIsOneTrue_object_validInput_2items`、`testIsOneTrue_object_validInput_3items` 共 9 个测试方法，用于覆盖生产代码新增的 `isOneTrue(boolean...)` 和 `isOneTrue(Boolean...)` 方法。
- 无需调整 import，所需的 `assertTrue`、`assertFalse` 已在旧测试类中静态导入。

```java
    //  test isOneTrue
    //  -----------------------------------------------------------------------
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