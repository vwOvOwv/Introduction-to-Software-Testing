# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `3c0ac0e87c03ae63a782e48bb31878ec9f114c39`
- B: `dad064eebbde450cb500a0e0d72200c655ac47c6`
- test: `src/test/java/org/apache/commons/lang3/BooleanUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/BooleanUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `48618`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 10580, 'completion_tokens': 1486, 'total_tokens': 12066}`

---

- 新增 @Test 方法 `testOneHot_object_emptyInput`，覆盖新增 `BooleanUtils.oneHot(Boolean...)` 对空数组抛出 `IllegalArgumentException`。
- 新增 @Test 方法 `testOneHot_object_nullElementInput`，覆盖对象数组中 `null` 元素按 `false` 处理。
- 新增 @Test 方法 `testOneHot_object_nullInput`，覆盖新增 `BooleanUtils.oneHot(Boolean...)` 对 `null` 数组抛出 `NullPointerException`。
- 新增 @Test 方法 `testOneHot_object_validInput_1item`，覆盖对象数组单元素 one-hot 行为。
- 新增 @Test 方法 `testOneHot_object_validInput_2items`，覆盖对象数组两个元素 one-hot 行为。
- 新增 @Test 方法 `testOneHot_object_validInput_2ItemsNullsTreatedAsFalse`，覆盖对象 varargs 中 `null` 按 `false` 参与 one-hot。
- 新增 @Test 方法 `testOneHot_object_validInput_3items`，覆盖对象数组三个元素 one-hot 行为。
- 新增 @Test 方法 `testOneHot_primitive_emptyInput`，覆盖新增 `BooleanUtils.oneHot(boolean...)` 对空数组抛出 `IllegalArgumentException`。
- 新增 @Test 方法 `testOneHot_primitive_nullInput`，覆盖新增 `BooleanUtils.oneHot(boolean...)` 对 `null` 数组抛出 `NullPointerException`。
- 新增 @Test 方法 `testOneHot_primitive_validInput_1item`，覆盖 primitive 数组单元素 one-hot 行为。
- 新增 @Test 方法 `testOneHot_primitive_validInput_2items`，覆盖 primitive 数组两个元素 one-hot 行为。
- 新增 @Test 方法 `testOneHot_primitive_validInput_3items`，覆盖 primitive 数组三个元素 one-hot 行为。
- import 无需调整，旧测试已有 `assertEquals`、`assertFalse`、`assertThrows`、`assertTrue` 和 `@Test` 所需 import。

```java
    @Test
    public void testOneHot_object_emptyInput() {
        assertThrows(IllegalArgumentException.class, () -> BooleanUtils.oneHot(new Boolean[] {}));
    }

    @Test
    public void testOneHot_object_nullElementInput() {
        assertEquals(Boolean.FALSE, BooleanUtils.oneHot(new Boolean[] {null}));
    }

    @Test
    public void testOneHot_object_nullInput() {
        assertThrows(NullPointerException.class, () -> BooleanUtils.oneHot((Boolean[]) null));
    }

    @Test
    public void testOneHot_object_validInput_1item() {
        assertTrue(BooleanUtils.oneHot(new Boolean[]{Boolean.TRUE}), "true");

        assertFalse(BooleanUtils.oneHot(new Boolean[]{Boolean.FALSE}), "false");

        assertFalse(BooleanUtils.oneHot(new Boolean[]{null}), "false");
    }

    @Test
    public void testOneHot_object_validInput_2items() {
        assertFalse(BooleanUtils.oneHot(new Boolean[]{true, true}), "both true");

        assertFalse(BooleanUtils.oneHot(new Boolean[]{false, false}), "both false");

        assertTrue(BooleanUtils.oneHot(new Boolean[]{true, false}), "first true");

        assertTrue(BooleanUtils.oneHot(new Boolean[]{false, true}), "last true");
    }

    @Test
    public void testOneHot_object_validInput_2ItemsNullsTreatedAsFalse() {
        assertFalse(BooleanUtils.oneHot(null, null), "both null");

        assertTrue(BooleanUtils.oneHot(true, null), "first true");

        assertTrue(BooleanUtils.oneHot(null, true), "last true");
    }

    @Test
    public void testOneHot_object_validInput_3items() {
        // none true
        assertFalse(BooleanUtils.oneHot(new Boolean[]{false, false, false}), "all false");

        // one true
        assertTrue(BooleanUtils.oneHot(new Boolean[]{true, false, false}), "first true");

        assertTrue(BooleanUtils.oneHot(new Boolean[]{false, true, false}), "middle true");

        assertTrue(BooleanUtils.oneHot(new Boolean[]{false, false, true}), "last true");

        // two true
        assertFalse(BooleanUtils.oneHot(new Boolean[]{false, true, true}), "first false");

        assertFalse(BooleanUtils.oneHot(new Boolean[]{true, false, true}), "middle false");

        assertFalse(BooleanUtils.oneHot(new Boolean[]{true, true, false}), "last false");

        // three true
        assertFalse(BooleanUtils.oneHot(new Boolean[]{true, true, true}), "all true");
    }

    @Test
    public void testOneHot_primitive_emptyInput() {
        assertThrows(IllegalArgumentException.class, () -> BooleanUtils.oneHot(new boolean[] {}));
    }

    @Test
    public void testOneHot_primitive_nullInput() {
        assertThrows(NullPointerException.class, () -> BooleanUtils.oneHot((boolean[]) null));
    }

    @Test
    public void testOneHot_primitive_validInput_1item() {
        assertTrue(BooleanUtils.oneHot(new boolean[]{true}), "true");

        assertFalse(BooleanUtils.oneHot(new boolean[]{false}), "false");
    }

    @Test
    public void testOneHot_primitive_validInput_2items() {
        assertFalse(BooleanUtils.oneHot(new boolean[]{true, true}), "both true");

        assertFalse(BooleanUtils.oneHot(new boolean[]{false, false}), "both false");

        assertTrue(BooleanUtils.oneHot(new boolean[]{true, false}), "first true");

        assertTrue(BooleanUtils.oneHot(new boolean[]{false, true}), "last true");
    }

    @Test
    public void testOneHot_primitive_validInput_3items() {
        // none true
        assertFalse(BooleanUtils.oneHot(new boolean[]{false, false, false}), "all false");

        // one true
        assertTrue(BooleanUtils.oneHot(new boolean[]{true, false, false}), "first true");

        assertTrue(BooleanUtils.oneHot(new boolean[]{false, true, false}), "middle true");

        assertTrue(BooleanUtils.oneHot(new boolean[]{false, false, true}), "last true");

        // two true
        assertFalse(BooleanUtils.oneHot(new boolean[]{false, true, true}), "first false");

        assertFalse(BooleanUtils.oneHot(new boolean[]{true, false, true}), "middle false");

        assertFalse(BooleanUtils.oneHot(new boolean[]{true, true, false}), "last false");

        // three true
        assertFalse(BooleanUtils.oneHot(new boolean[]{true, true, true}), "all true");
    }
```