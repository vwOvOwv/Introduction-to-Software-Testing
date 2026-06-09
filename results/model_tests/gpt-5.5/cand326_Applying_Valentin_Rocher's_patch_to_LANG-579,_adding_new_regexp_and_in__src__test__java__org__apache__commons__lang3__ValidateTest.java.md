# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `76660f4a9879509176bb0a146ca45ba6616d854c`
- B: `779828c9a2bb5c38c2cd99c2596ff8ba6b755dd8`
- test: `src/test/java/org/apache/commons/lang3/ValidateTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Validate.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `39669`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 8589, 'completion_tokens': 963, 'total_tokens': 9552}`

---

- 新增 `testMatchesPattern`，覆盖新增 `Validate.matchesPattern(CharSequence, String)` 的成功匹配与默认异常消息。
- 新增 `testMatchesPattern_withMessage`，覆盖新增 `Validate.matchesPattern(CharSequence, String, String, Object...)` 的自定义异常消息。
- 新增 `testInclusiveBetween`，覆盖新增 `Validate.inclusiveBetween` 的边界包含行为与默认异常消息。
- 新增 `testInclusiveBetween_withMessage`，覆盖新增 `Validate.inclusiveBetween` 自定义消息重载。
- 新增 `testExclusiveBetween`，覆盖新增 `Validate.exclusiveBetween` 的边界排除行为与默认异常消息。
- 新增 `testExclusiveBetween_withMessage`，覆盖新增 `Validate.exclusiveBetween` 自定义消息重载。
- 不需要调整 import。

```java
public void testMatchesPattern()
{
    CharSequence str = "hi";
    Validate.matchesPattern(str, "[a-z]*");
    try
    {
        Validate.matchesPattern(str, "[0-9]*");
        fail("Expecting IllegalArgumentException");
    }
    catch (IllegalArgumentException e)
    {
        assertEquals("The string hi does not match the pattern [0-9]*", e.getMessage());
    }
}

public void testMatchesPattern_withMessage()
{
    CharSequence str = "hi";
    Validate.matchesPattern(str, "[a-z]*", "Does not match");
    try
    {
        Validate.matchesPattern(str, "[0-9]*", "Does not match");
        fail("Expecting IllegalArgumentException");
    }
    catch (IllegalArgumentException e)
    {
        assertEquals("Does not match", e.getMessage());
    }
}

public void testInclusiveBetween()
{
    Validate.inclusiveBetween("a", "c", "b");
    Validate.inclusiveBetween(0, 2, 1);
    Validate.inclusiveBetween(0, 2, 2);
    try {
        Validate.inclusiveBetween(0, 5, 6);
        fail("Expecting IllegalArgumentException");
    } catch (IllegalArgumentException e) {
        assertEquals("The value 6 is not in the specified inclusive range of 0 to 5", e.getMessage());
    }
}

public void testInclusiveBetween_withMessage()
{
    Validate.inclusiveBetween("a", "c", "b", "Error");
    Validate.inclusiveBetween(0, 2, 1, "Error");
    Validate.inclusiveBetween(0, 2, 2, "Error");
    try {
        Validate.inclusiveBetween(0, 5, 6, "Error");
        fail("Expecting IllegalArgumentException");
    } catch (IllegalArgumentException e) {
        assertEquals("Error", e.getMessage());
    }
}

public void testExclusiveBetween()
{
    Validate.exclusiveBetween("a", "c", "b");
    Validate.exclusiveBetween(0, 2, 1);
    try {
        Validate.exclusiveBetween(0, 5, 6);
        fail("Expecting IllegalArgumentException");
    } catch (IllegalArgumentException e) {
        assertEquals("The value 6 is not in the specified exclusive range of 0 to 5", e.getMessage());
    }
    try {
        Validate.exclusiveBetween(0, 5, 5);
        fail("Expecting IllegalArgumentException");
    } catch (IllegalArgumentException e) {
        assertEquals("The value 5 is not in the specified exclusive range of 0 to 5", e.getMessage());
    }
}

public void testExclusiveBetween_withMessage()
{
    Validate.exclusiveBetween("a", "c", "b", "Error");
    Validate.exclusiveBetween(0, 2, 1, "Error");
    try {
        Validate.exclusiveBetween(0, 5, 6, "Error");
        fail("Expecting IllegalArgumentException");
    } catch (IllegalArgumentException e) {
        assertEquals("Error", e.getMessage());
    }
    try {
        Validate.exclusiveBetween(0, 5, 5, "Error");
        fail("Expecting IllegalArgumentException");
    } catch (IllegalArgumentException e) {
        assertEquals("Error", e.getMessage());
    }
}
```