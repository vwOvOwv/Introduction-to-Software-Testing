# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `b35b6c576211b96abecb05655d448be3441c117c`
- B: `96235eaae06c8b74ac24dc5814b4f4c6b6541ead`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `125029`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 30834, 'completion_tokens': 1107, 'total_tokens': 31941}`

---

- 新增 `testisEmpty`，用于覆盖新增批量 empty 方法附近的既有 `isEmpty` 基础语义，无需调整 import。
- 新增 `testisNotEmpty`，用于覆盖新增批量 empty 方法附近的既有 `isNotEmpty` 基础语义，无需调整 import。
- 新增 `testisAnyEmpty`，对应生产代码新增 `StringUtils.isAnyEmpty(CharSequence...)`，断言 null、空串以及非空场景，无需调整 import。
- 新增 `testisNoneEmpty`，对应生产代码新增 `StringUtils.isNoneEmpty(CharSequence...)`，断言其为 `isAnyEmpty` 的取反语义，无需调整 import。
- 新增 `testisBlank`，用于覆盖新增批量 blank 方法附近的既有 `isBlank` 基础语义，无需调整 import。
- 新增 `testisNotBlank`，用于覆盖新增批量 blank 方法附近的既有 `isNotBlank` 基础语义，无需调整 import。
- 新增 `testisAnyBlank`，对应生产代码新增 `StringUtils.isAnyBlank(CharSequence...)`，断言 null、空串、空白串以及非空场景，无需调整 import。
- 新增 `testisNoneBlank`，对应生产代码新增 `StringUtils.isNoneBlank(CharSequence...)`，断言其为 `isAnyBlank` 的取反语义，无需调整 import。

```java
@Test
public void testisEmpty(){
  assertTrue(StringUtils.isEmpty(null));
  assertTrue(StringUtils.isEmpty(""));
  assertFalse(StringUtils.isEmpty(" "));
  assertFalse(StringUtils.isEmpty("bob"));
  assertFalse(StringUtils.isEmpty("  bob  "));
}

@Test
public void testisNotEmpty(){
  assertFalse(StringUtils.isNotEmpty(null));
  assertFalse(StringUtils.isNotEmpty(""));
  assertTrue(StringUtils.isNotEmpty(" "));
  assertTrue(StringUtils.isNotEmpty("bob"));
  assertTrue(StringUtils.isNotEmpty("  bob  "));
}

@Test
public void testisAnyEmpty(){
  assertTrue(StringUtils.isAnyEmpty(null));
  assertTrue(StringUtils.isAnyEmpty(null, "foo"));
  assertTrue(StringUtils.isAnyEmpty("", "bar"));
  assertTrue(StringUtils.isAnyEmpty("bob", ""));
  assertTrue(StringUtils.isAnyEmpty("  bob  ", null));
  assertFalse(StringUtils.isAnyEmpty(" ","bar"));
  assertFalse(StringUtils.isAnyEmpty("foo","bar"));
}

@Test
public void testisNoneEmpty(){
  assertFalse(StringUtils.isNoneEmpty(null));
  assertFalse(StringUtils.isNoneEmpty(null, "foo"));
  assertFalse(StringUtils.isNoneEmpty("", "bar"));
  assertFalse(StringUtils.isNoneEmpty("bob", ""));
  assertFalse(StringUtils.isNoneEmpty("  bob  ", null));
  assertTrue(StringUtils.isNoneEmpty(" ", "bar"));
  assertTrue(StringUtils.isNoneEmpty("foo", "bar"));
}

@Test
public void testisBlank(){
  assertTrue(StringUtils.isBlank(null));
  assertTrue(StringUtils.isBlank(""));
  assertTrue(StringUtils.isBlank(" "));
  assertFalse(StringUtils.isBlank("bob"));
  assertFalse(StringUtils.isBlank("  bob  "));
}

@Test
public void testisNotBlank(){
  assertFalse(StringUtils.isNotBlank(null));
  assertFalse(StringUtils.isNotBlank(""));
  assertFalse(StringUtils.isNotBlank(" "));
  assertTrue(StringUtils.isNotBlank("bob"));
  assertTrue(StringUtils.isNotBlank("  bob  "));
}

@Test
public void testisAnyBlank(){
  assertTrue(StringUtils.isAnyBlank(null));
  assertTrue(StringUtils.isAnyBlank(null, "foo"));
  assertTrue(StringUtils.isAnyBlank(null, null));
  assertTrue(StringUtils.isAnyBlank("", "bar"));
  assertTrue(StringUtils.isAnyBlank("bob", ""));
  assertTrue(StringUtils.isAnyBlank("  bob  ", null));
  assertTrue(StringUtils.isAnyBlank(" ","bar"));
  assertFalse(StringUtils.isAnyBlank("foo","bar"));
}

@Test
public void testisNoneBlank(){
  assertFalse(StringUtils.isNoneBlank(null));
  assertFalse(StringUtils.isNoneBlank(null, "foo"));
  assertFalse(StringUtils.isNoneBlank(null, null));
  assertFalse(StringUtils.isNoneBlank("", "bar"));
  assertFalse(StringUtils.isNoneBlank("bob", ""));
  assertFalse(StringUtils.isNoneBlank("  bob  ", null));
  assertFalse(StringUtils.isNoneBlank(" ", "bar"));
  assertTrue(StringUtils.isNoneBlank("foo", "bar"));
}
```