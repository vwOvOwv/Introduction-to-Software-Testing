# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `2e3fa5c2532c95a95b4f52aeb5b7520282dd4691`
- B: `77d187eefc8596ef8203eb827486099cc8b27835`
- test: `src/test/java/org/apache/commons/lang3/ValidateTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Validate.java']`
- old_test_mode: `methods`
- user_chars: `98409`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 24119, 'completion_tokens': 2686, 'total_tokens': 26805}`

---

- 新增 `testNotNaNValidation`，覆盖新增的 `Validate.notNaN(double, ...)` 默认消息与自定义消息行为；无需调整 import。
- 新增 `testFiniteValidation`，覆盖新增的 `Validate.finite(double, ...)` 对 `Infinity`、`-Infinity`、`NaN` 的校验；无需调整 import。
- 新增 `testGreaterValidation`，覆盖新增的 `greaterObj`、`greater(long/double, ...)` 边界与异常消息；无需调整 import。
- 新增 `testGreaterOrEqualValidation`，覆盖新增的 `greaterOrEqualObj`、`greaterOrEqual(long/double, ...)` 边界与异常消息；无需调整 import。
- 新增 `testSmallerValidation`，覆盖新增的 `smallerObj`、`smaller(long/double, ...)` 边界与异常消息；无需调整 import。
- 新增 `testSmallerOrEqualValidation`，覆盖新增的 `smallerOrEqualObj`、`smallerOrEqual(long/double, ...)` 边界与异常消息；无需调整 import。
- 新增 `testDifferentValidation`，覆盖新增的 `differentObj`、`different(long/double, ...)` 相等值异常与 `NaN` 特殊行为；无需调整 import。

```java
    @Test
    public void testNotNaNValidation() {
        Validate.notNaN(0.0);
        Validate.notNaN(Double.POSITIVE_INFINITY);
        Validate.notNaN(Double.NEGATIVE_INFINITY);

        try {
            Validate.notNaN(Double.NaN);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The validated value is not a number", ex.getMessage());
        }

        try {
            Validate.notNaN(Double.NaN, "MSG");
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("MSG", ex.getMessage());
        }
    }

    @Test
    public void testFiniteValidation() {
        Validate.finite(0.0);

        try {
            Validate.finite(Double.POSITIVE_INFINITY);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value is invalid: Infinity", ex.getMessage());
        }

        try {
            Validate.finite(Double.NEGATIVE_INFINITY);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value is invalid: -Infinity", ex.getMessage());
        }

        try {
            Validate.finite(Double.NaN);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value is invalid: NaN", ex.getMessage());
        }

        try {
            Validate.finite(Double.NaN, "MSG");
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("MSG", ex.getMessage());
        }
    }

    @Test
    public void testGreaterValidation() {
        Validate.greaterObj("c", "b");
        Validate.greater(1, 0);
        Validate.greater(1.0, 0.0);
        Validate.greater(Double.POSITIVE_INFINITY, 0.0);

        try {
            Validate.greaterObj("b", "b");
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value b is not greater than b", ex.getMessage());
        }

        try {
            Validate.greater(0, 0);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value 0 is not greater than 0", ex.getMessage());
        }

        try {
            Validate.greater(Double.NaN, 0.0);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value NaN is not greater than 0.0", ex.getMessage());
        }

        try {
            Validate.greater(0.0, Double.NaN, "MSG");
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("MSG", ex.getMessage());
        }
    }

    @Test
    public void testGreaterOrEqualValidation() {
        Validate.greaterOrEqualObj("c", "b");
        Validate.greaterOrEqualObj("b", "b");
        Validate.greaterOrEqual(1, 0);
        Validate.greaterOrEqual(0, 0);
        Validate.greaterOrEqual(1.0, 0.0);
        Validate.greaterOrEqual(0.0, 0.0);

        try {
            Validate.greaterOrEqualObj("a", "b");
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value a is not greater than or equal to b", ex.getMessage());
        }

        try {
            Validate.greaterOrEqual(-1, 0);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value -1 is not greater than or equal to 0", ex.getMessage());
        }

        try {
            Validate.greaterOrEqual(Double.NaN, Double.NaN);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value NaN is not greater than or equal to NaN", ex.getMessage());
        }

        try {
            Validate.greaterOrEqual(-1.0, 0.0, "MSG");
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("MSG", ex.getMessage());
        }
    }

    @Test
    public void testSmallerValidation() {
        Validate.smallerObj("a", "b");
        Validate.smaller(-1, 0);
        Validate.smaller(-1.0, 0.0);
        Validate.smaller(Double.NEGATIVE_INFINITY, 0.0);

        try {
            Validate.smallerObj("b", "b");
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value b is not smaller than b", ex.getMessage());
        }

        try {
            Validate.smaller(0, 0);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value 0 is not smaller than 0", ex.getMessage());
        }

        try {
            Validate.smaller(Double.NaN, 0.0);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value NaN is not smaller than 0.0", ex.getMessage());
        }

        try {
            Validate.smaller(0.0, Double.NaN, "MSG");
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("MSG", ex.getMessage());
        }
    }

    @Test
    public void testSmallerOrEqualValidation() {
        Validate.smallerOrEqualObj("a", "b");
        Validate.smallerOrEqualObj("b", "b");
        Validate.smallerOrEqual(-1, 0);
        Validate.smallerOrEqual(0, 0);
        Validate.smallerOrEqual(-1.0, 0.0);
        Validate.smallerOrEqual(0.0, 0.0);

        try {
            Validate.smallerOrEqualObj("c", "b");
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value c is not smaller than or equal to b", ex.getMessage());
        }

        try {
            Validate.smallerOrEqual(1, 0);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value 1 is not smaller than or equal to 0", ex.getMessage());
        }

        try {
            Validate.smallerOrEqual(Double.NaN, 0.0);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value NaN is not smaller than or equal to 0.0", ex.getMessage());
        }

        try {
            Validate.smallerOrEqual(1.0, 0.0, "MSG");
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("MSG", ex.getMessage());
        }
    }

    @Test
    public void testDifferentValidation() {
        Validate.differentObj("b", "a");
        Validate.different(1, 0);
        Validate.different(1.0, 0.0);
        Validate.different(Double.NaN, 0.0);
        Validate.different(1.0, Double.NaN);
        Validate.different(Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY);

        try {
            Validate.differentObj("a", "a");
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value a is invalid", ex.getMessage());
        }

        try {
            Validate.different(0, 0);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value 0 is invalid", ex.getMessage());
        }

        try {
            Validate.different(Double.POSITIVE_INFINITY, Double.POSITIVE_INFINITY);
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("The value Infinity is invalid", ex.getMessage());
        }

        try {
            Validate.different(0, 0, "MSG");
            fail("Expecting IllegalArgumentException");
        } catch (final IllegalArgumentException ex) {
            assertEquals("MSG", ex.getMessage());
        }
    }
```