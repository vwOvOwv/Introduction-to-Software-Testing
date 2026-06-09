# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `2e3fa5c2532c95a95b4f52aeb5b7520282dd4691`
- B: `77d187eefc8596ef8203eb827486099cc8b27835`
- test: `src/test/java/org/apache/commons/lang3/ValidateTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Validate.java']`
- old_test_mode: `methods`
- user_chars: `98409`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 23897, 'completion_tokens': 8109, 'total_tokens': 32006, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2346}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 23513}`

---

- 新增 `testNotNaN1`、`testNotNaN2`、`testFinite1`、`testFinite2`、`testGreaterObject1`、`testGreaterObject2`、`testGreaterLong1`、`testGreaterLong2`、`testGreaterDouble1`、`testGreaterDouble2`、`testGreaterOrEqualObject1`、`testGreaterOrEqualObject2`、`testGreaterOrEqualLong1`、`testGreaterOrEqualLong2`、`testGreaterOrEqualDouble1`、`testGreaterOrEqualDouble2`、`testSmallerObject1`、`testSmallerObject2`、`testSmallerLong1`、`testSmallerLong2`、`testSmallerDouble1`、`testSmallerDouble2`、`testSmallerOrEqualObject1`、`testSmallerOrEqualObject2`、`testSmallerOrEqualLong1`、`testSmallerOrEqualLong2`、`testSmallerOrEqualDouble1`、`testSmallerOrEqualDouble2`、`testDifferentObject1`、`testDifferentObject2`、`testDifferentLong1`、`testDifferentLong2`、`testDifferentDouble1`、`testDifferentDouble2` 测试方法，以覆盖生产代码新增的 `notNaN`、`finite`、`greater`/`greaterObj`、`greaterOrEqual`/`greaterOrEqualObj`、`smaller`/`smallerObj`、`smallerOrEqual`/`smallerOrEqualObj`、`different`/`differentObj` 各方法及其重载。
- 不需要删除旧测试方法，也不需要调整 `import` 语句。

```java
//-----------------------------------------------------------------------
//-----------------------------------------------------------------------

@Test
public void testNotNaN1() {
    Validate.notNaN(0.0);
    Validate.notNaN(Double.POSITIVE_INFINITY);
    Validate.notNaN(Double.NEGATIVE_INFINITY);
    try {
        Validate.notNaN(Double.NaN);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The validated value is not a number", ex.getMessage());
    }
}

@Test
public void testNotNaN2() {
    Validate.notNaN(0.0, "MSG");
    Validate.notNaN(Double.POSITIVE_INFINITY, "MSG");
    Validate.notNaN(Double.NEGATIVE_INFINITY, "MSG");
    try {
        Validate.notNaN(Double.NaN, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

//-----------------------------------------------------------------------
//-----------------------------------------------------------------------

@Test
public void testFinite1() {
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
}

@Test
public void testFinite2() {
    Validate.finite(0.0, "MSG");
    try {
        Validate.finite(Double.POSITIVE_INFINITY, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.finite(Double.NEGATIVE_INFINITY, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.finite(Double.NaN, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

//-----------------------------------------------------------------------
//-----------------------------------------------------------------------

@Test
public void testGreaterObject1() {
    Validate.greaterObj("c", "b");
    try {
        Validate.greaterObj("b", "b");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value b is not greater than b", ex.getMessage());
    }
    try {
        Validate.greaterObj("a", "b");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value a is not greater than b", ex.getMessage());
    }
}

@Test
public void testGreaterObject2() {
    Validate.greaterObj("c", "b", "MSG");
    try {
        Validate.greaterObj("b", "b", "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.greaterObj("a", "b", "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

@Test
public void testGreaterLong1() {
    Validate.greater(1, 0);
    try {
        Validate.greater(0, 0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value 0 is not greater than 0", ex.getMessage());
    }
    try {
        Validate.greater(-1, 0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value -1 is not greater than 0", ex.getMessage());
    }
}

@Test
public void testGreaterLong2() {
    Validate.greater(1, 0, "MSG");
    try {
        Validate.greater(0, 0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.greater(-1, 0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

@Test
public void testGreaterDouble1() {
    Validate.greater(1.0, 0.0);
    Validate.greater(Double.POSITIVE_INFINITY, 0.0);
    try {
        Validate.greater(0.0, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value 0.0 is not greater than 0.0", ex.getMessage());
    }
    try {
        Validate.greater(-1.0, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value -1.0 is not greater than 0.0", ex.getMessage());
    }
    try {
        Validate.greater(Double.NEGATIVE_INFINITY, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value -Infinity is not greater than 0.0", ex.getMessage());
    }
    try {
        Validate.greater(Double.NaN, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value NaN is not greater than 0.0", ex.getMessage());
    }
    try {
        Validate.greater(0.0, Double.NaN);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value 0.0 is not greater than NaN", ex.getMessage());
    }
}

@Test
public void testGreaterDouble2() {
    Validate.greater(1.0, 0.0, "MSG");
    Validate.greater(Double.POSITIVE_INFINITY, 0.0, "MSG");
    try {
        Validate.greater(0.0, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.greater(-1.0, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.greater(Double.NEGATIVE_INFINITY, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.greater(Double.NaN, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.greater(0.0, Double.NaN, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

//-----------------------------------------------------------------------
//-----------------------------------------------------------------------

@Test
public void testGreaterOrEqualObject1() {
    Validate.greaterOrEqualObj("c", "b");
    Validate.greaterOrEqualObj("b", "b");
    try {
        Validate.greaterOrEqualObj("a", "b");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value a is not greater than or equal to b", ex.getMessage());
    }
}

@Test
public void testGreaterOrEqualObject2() {
    Validate.greaterOrEqualObj("c", "b", "MSG");
    Validate.greaterOrEqualObj("b", "b", "MSG");
    try {
        Validate.greaterOrEqualObj("a", "b", "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

@Test
public void testGreaterOrEqualLong1() {
    Validate.greaterOrEqual(1, 0);
    Validate.greaterOrEqual(0, 0);
    try {
        Validate.greaterOrEqual(-1, 0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value -1 is not greater than or equal to 0", ex.getMessage());
    }
}

@Test
public void testGreaterOrEqualLong2() {
    Validate.greaterOrEqual(1, 0, "MSG");
    Validate.greaterOrEqual(0, 0, "MSG");
    try {
        Validate.greaterOrEqual(-1, 0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

@Test
public void testGreaterOrEqualDouble1() {
    Validate.greaterOrEqual(1.0, 0.0);
    Validate.greaterOrEqual(Double.POSITIVE_INFINITY, 0.0);
    Validate.greaterOrEqual(0.0, 0.0);
    try {
        Validate.greaterOrEqual(-1.0, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value -1.0 is not greater than or equal to 0.0", ex.getMessage());
    }
    try {
        Validate.greaterOrEqual(Double.NEGATIVE_INFINITY, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value -Infinity is not greater than or equal to 0.0", ex.getMessage());
    }
    try {
        Validate.greaterOrEqual(Double.NaN, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value NaN is not greater than or equal to 0.0", ex.getMessage());
    }
    try {
        Validate.greaterOrEqual(0.0, Double.NaN);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value 0.0 is not greater than or equal to NaN", ex.getMessage());
    }
    try {
        Validate.greaterOrEqual(Double.NaN, Double.NaN);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value NaN is not greater than or equal to NaN", ex.getMessage());
    }
}

@Test
public void testGreaterOrEqualDouble2() {
    Validate.greaterOrEqual(1.0, 0.0, "MSG");
    Validate.greaterOrEqual(Double.POSITIVE_INFINITY, 0.0, "MSG");
    Validate.greaterOrEqual(0.0, 0.0, "MSG");

    try {
        Validate.greaterOrEqual(-1.0, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.greaterOrEqual(Double.NEGATIVE_INFINITY, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.greaterOrEqual(Double.NaN, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.greaterOrEqual(0.0, Double.NaN, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.greaterOrEqual(Double.NaN, Double.NaN, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

//-----------------------------------------------------------------------
//-----------------------------------------------------------------------

@Test
public void testSmallerObject1() {
    Validate.smallerObj("a", "b");
    try {
        Validate.smallerObj("b", "b");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value b is not smaller than b", ex.getMessage());
    }
    try {
        Validate.smallerObj("c", "b");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value c is not smaller than b", ex.getMessage());
    }
}

@Test
public void testSmallerObject2() {
    Validate.smallerObj("a", "b", "MSG");
    try {
        Validate.smallerObj("b", "b", "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.smallerObj("c", "b", "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

@Test
public void testSmallerLong1() {
    Validate.smaller(-1, 0);
    try {
        Validate.smaller(0, 0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value 0 is not smaller than 0", ex.getMessage());
    }
    try {
        Validate.smaller(1, 0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value 1 is not smaller than 0", ex.getMessage());
    }
}

@Test
public void testSmallerLong2() {
    Validate.smaller(-1, 0, "MSG");
    try {
        Validate.smaller(0, 0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.smaller(1, 0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

@Test
public void testSmallerDouble1() {
    Validate.smaller(-1.0, 0.0);
    Validate.smaller(Double.NEGATIVE_INFINITY, 0.0);
    try {
        Validate.smaller(0.0, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value 0.0 is not smaller than 0.0", ex.getMessage());
    }
    try {
        Validate.smaller(1.0, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value 1.0 is not smaller than 0.0", ex.getMessage());
    }
    try {
        Validate.smaller(Double.POSITIVE_INFINITY, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value Infinity is not smaller than 0.0", ex.getMessage());
    }
    try {
        Validate.smaller(Double.NaN, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value NaN is not smaller than 0.0", ex.getMessage());
    }
    try {
        Validate.smaller(0.0, Double.NaN);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value 0.0 is not smaller than NaN", ex.getMessage());
    }
}

@Test
public void testSmallerDouble2() {
    Validate.smaller(-1.0, 0.0, "MSG");
    Validate.smaller(Double.NEGATIVE_INFINITY, 0.0, "MSG");
    try {
        Validate.smaller(0.0, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.smaller(1.0, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.smaller(Double.POSITIVE_INFINITY, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.smaller(Double.NaN, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.smaller(0.0, Double.NaN, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

//-----------------------------------------------------------------------
//-----------------------------------------------------------------------

@Test
public void testSmallerOrEqualObject1() {
    Validate.smallerOrEqualObj("a", "b");
    Validate.smallerOrEqualObj("b", "b");
    try {
        Validate.smallerOrEqualObj("c", "b");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value c is not smaller than or equal to b", ex.getMessage());
    }
}

@Test
public void testSmallerOrEqualObject2() {
    Validate.smallerOrEqualObj("a", "b", "MSG");
    Validate.smallerOrEqualObj("b", "b", "MSG");
    try {
        Validate.smallerOrEqualObj("c", "b", "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

@Test
public void testSmallerOrEqualLong1() {
    Validate.smallerOrEqual(-1, 0);
    Validate.smallerOrEqual(0, 0);
    try {
        Validate.smallerOrEqual(1, 0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value 1 is not smaller than or equal to 0", ex.getMessage());
    }
}

@Test
public void testSmallerOrEqualLong2() {
    Validate.smallerOrEqual(-1, 0, "MSG");
    Validate.smallerOrEqual(0, 0, "MSG");
    try {
        Validate.smallerOrEqual(1, 0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

@Test
public void testSmallerOrEqualDouble1() {
    Validate.smallerOrEqual(-1.0, 0.0);
    Validate.smallerOrEqual(Double.NEGATIVE_INFINITY, 0.0);
    Validate.smallerOrEqual(0.0, 0.0);
    try {
        Validate.smallerOrEqual(1.0, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value 1.0 is not smaller than or equal to 0.0", ex.getMessage());
    }
    try {
        Validate.smallerOrEqual(Double.POSITIVE_INFINITY, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value Infinity is not smaller than or equal to 0.0", ex.getMessage());
    }
    try {
        Validate.smallerOrEqual(Double.NaN, 0.0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value NaN is not smaller than or equal to 0.0", ex.getMessage());
    }
    try {
        Validate.smallerOrEqual(0.0, Double.NaN);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value 0.0 is not smaller than or equal to NaN", ex.getMessage());
    }
}

@Test
public void testSmallerOrEqualDouble2() {
    Validate.smallerOrEqual(-1.0, 0.0, "MSG");
    Validate.smallerOrEqual(Double.NEGATIVE_INFINITY, 0.0, "MSG");
    Validate.smallerOrEqual(0.0, 0.0, "MSG");
    try {
        Validate.smallerOrEqual(1.0, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.smallerOrEqual(Double.POSITIVE_INFINITY, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.smallerOrEqual(Double.NaN, 0.0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.smallerOrEqual(0.0, Double.NaN, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

//-----------------------------------------------------------------------
//-----------------------------------------------------------------------

@Test
public void testDifferentObject1() {
    Validate.differentObj("b", "a");
    try {
        Validate.differentObj("a", "a");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value a is invalid", ex.getMessage());
    }
}

@Test
public void testDifferentObject2() {
    Validate.differentObj("b", "a", "MSG");
    try {
        Validate.differentObj("a", "a", "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

@Test
public void testDifferentLong1() {
    Validate.different(1, 0);
    try {
        Validate.different(0, 0);
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("The value 0 is invalid", ex.getMessage());
    }
}

@Test
public void testDifferentLong2() {
    Validate.different(1, 0, "MSG");
    try {
        Validate.different(0, 0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}

@Test
public void testDifferentDouble1() {
    Validate.different(1.0, 0.0);
    Validate.different(Double.NaN, 0.0);
    Validate.different(1.0, Double.NaN);
    Validate.different(Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY);
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
}

@Test
public void testDifferentDouble2() {
    Validate.different(1.0, 0.0, "MSG");
    Validate.different(Double.NaN, 0.0, "MSG");
    Validate.different(1.0, Double.NaN, "MSG");
    Validate.different(Double.NEGATIVE_INFINITY, Double.POSITIVE_INFINITY, "MSG");
    try {
        Validate.different(0, 0, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
    try {
        Validate.different(Double.POSITIVE_INFINITY, Double.POSITIVE_INFINITY, "MSG");
        fail("Expecting IllegalArgumentException");
    } catch (final IllegalArgumentException ex) {
        assertEquals("MSG", ex.getMessage());
    }
}
```