# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ce7f4ed073b5a7b326871bd2339e355dbe9468fa`
- B: `d38919fcbda835f0ad82d65f25349bd7105b67cc`
- test: `src/test/java/org/apache/commons/lang3/ClassUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ClassUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `77513`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 16990, 'completion_tokens': 599, 'total_tokens': 17589}`

---

- 新增 `test_getAbbreviatedName_Class`：覆盖新增的 `ClassUtils.getAbbreviatedName(Class<?>, int)` 对 `null`、短长度和足够长度的缩写行为。
- 新增 `test_getAbbreviatedName_Class_Exceptions`：覆盖新增缩写 API 在 `len <= 0` 时抛出 `IllegalArgumentException` 的生产逻辑。
- 新增 `test_getAbbreviatedName_String`：覆盖新增的 `ClassUtils.getAbbreviatedName(String, int)` 对 `null`、无包名类名和全限定类名的行为。
- 不需要调整 import：旧测试已包含 `assertEquals`、`assertTrue`、`fail` 和 `@Test` 所需导入。

```java
@Test
public void test_getAbbreviatedName_Class() {
    assertEquals("", ClassUtils.getAbbreviatedName((Class<?>)null, 1));
    assertEquals("j.l.String", ClassUtils.getAbbreviatedName(String.class, 1));
    assertEquals("j.l.String", ClassUtils.getAbbreviatedName(String.class, 5));
    assertEquals("j.lang.String", ClassUtils.getAbbreviatedName(String.class, 13));
    assertEquals("j.lang.String", ClassUtils.getAbbreviatedName(String.class, 15));
    assertEquals("java.lang.String", ClassUtils.getAbbreviatedName(String.class, 20));
}

@Test
public void test_getAbbreviatedName_Class_Exceptions() {
    try {
        ClassUtils.getAbbreviatedName(String.class, 0);
        fail("ClassUtils.getAbbreviatedName() should fail with an "
            + "IllegalArgumentException for a len value of 0.");
    } catch (final Exception e) {
        assertTrue(e instanceof IllegalArgumentException);
    }
    try {
        ClassUtils.getAbbreviatedName(String.class, -10);
        fail("ClassUtils.getAbbreviatedName() should fail with an "
            + "IllegalArgumentException for negative values of len.");
    } catch (final Exception e) {
        assertTrue(e instanceof IllegalArgumentException);
    }
}

@Test
public void test_getAbbreviatedName_String() {
    assertEquals("", ClassUtils.getAbbreviatedName((String)null, 1));
    assertEquals("WithoutPackage", ClassUtils.getAbbreviatedName("WithoutPackage", 1));
    assertEquals("j.l.String", ClassUtils.getAbbreviatedName("java.lang.String", 1));
}
```