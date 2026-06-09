# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `892c9703496079e0b65eccea0252cf52a44c4512`
- B: `00e530042f481d1000be27584cf05be939a42bb0`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `methods`
- user_chars: `5987`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1869, 'completion_tokens': 733, 'total_tokens': 2602}`

---

- 修改/拆分 `testExceptions`：生产代码新增 `start < 0 || end < 0` 的异常分支，因此将旧的综合异常测试拆为多个更聚焦的方法，并在 `testExceptionsRandom` 中新增负字符位置断言。
- 新增 `testExceptionsRandomAlphabetic`、`testExceptionsRandomAscii`、`testExceptionsRandomGraph`、`testExceptionsRandomNumeric`、`testExceptionsRandomPrint`：对应测试 diff 中从原 `testExceptions` 拆出的各随机字符串 API 负长度异常断言。
- 需要删除旧测试方法 `testExceptions`；不需要调整 import。

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