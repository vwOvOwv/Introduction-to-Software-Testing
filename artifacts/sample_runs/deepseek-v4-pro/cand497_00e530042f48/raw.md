# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `892c9703496079e0b65eccea0252cf52a44c4512`
- B: `00e530042f481d1000be27584cf05be939a42bb0`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `methods`
- user_chars: `5987`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1906, 'completion_tokens': 1839, 'total_tokens': 3745, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1148}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1522}`

---

- 删除旧测试方法 `testExceptions`，因为该方法已被拆分为多个单一职责的测试方法，并且缺少对 start/end 为负数的新异常校验的断言。
- 新增 `testExceptionsRandom` 方法，合并原 `testExceptions` 中所有 `random()` 相关异常断言，并新增对 `start` 或 `end` 负数的校验断言。
- 新增 `testExceptionsRandomAlphabetic`、`testExceptionsRandomAscii`、`testExceptionsRandomGraph`、`testExceptionsRandomNumeric`、`testExceptionsRandomPrint` 方法，分别单独测试对应快捷方法的负数计数异常。
- 无需调整 import，现有导入已覆盖 `assertThrows`、`Random` 等。

```java
// DELETE_TESTS_START
testExceptions
// DELETE_TESTS_END

@Test
public void testExceptionsRandom() {
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1));
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, true, true));
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, new char[] { 'a' }));
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(1, new char[0]));
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, ""));
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, (String) null));
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, 'a', 'z', false, false));
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, 'a', 'z', false, false, new char[] { 'a' }));
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(-1, 'a', 'z', false, false, new char[] { 'a' }, new Random()));
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(8, 32, 48, false, true));
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(8, 32, 65, true, false));
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.random(1, Integer.MIN_VALUE, -10, false, false, null));
}

@Test
public void testExceptionsRandomAlphabetic() {
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.randomAlphabetic(-1));
}

@Test
public void testExceptionsRandomAscii() {
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.randomAscii(-1));
}

@Test
public void testExceptionsRandomGraph() {
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.randomGraph(-1));
}

@Test
public void testExceptionsRandomNumeric() {
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.randomNumeric(-1));
}

@Test
public void testExceptionsRandomPrint() {
    assertThrows(IllegalArgumentException.class, () -> RandomStringUtils.randomPrint(-1));
}
```