# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ce7f4ed073b5a7b326871bd2339e355dbe9468fa`
- B: `d38919fcbda835f0ad82d65f25349bd7105b67cc`
- test: `src/test/java/org/apache/commons/lang3/ClassUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ClassUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `77513`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 17949, 'completion_tokens': 1135, 'total_tokens': 19084, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 643}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 17565}`

---

- 新增 `test_getAbbreviatedName_Class` 测试方法，对应生产代码新增的 `getAbbreviatedName(Class<?>, int)` 方法。
- 新增 `test_getAbbreviatedName_Class_Exceptions` 测试方法，覆盖 `getAbbreviatedName(Class<?>, int)` 对非法长度参数的异常场景。
- 新增 `test_getAbbreviatedName_String` 测试方法，对应生产代码新增的 `getAbbreviatedName(String, int)` 方法。
- 无需调整 import，现有静态导入已包含所需断言方法。

```java
// -------------------------------------------------------------------------
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