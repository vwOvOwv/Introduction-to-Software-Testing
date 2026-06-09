# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `88654b79c92386b7c411f064cc373e7698a49449`
- B: `6ea2fc8d38e035bafaa92c7d3b007be38c2e9000`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `31258`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7754, 'completion_tokens': 565, 'total_tokens': 8319, 'prompt_tokens_details': {'cached_tokens': 7424}, 'completion_tokens_details': {'reasoning_tokens': 174}}`

---

- 新增 `testGetClassName`，覆盖新增的 `ObjectUtils.getClassName(Object)` 对 `null`、JDK 类和内部类实例的返回值。
- 新增 `testGetSimpleName`，覆盖新增的 `ObjectUtils.getClassSimpleName(Object)` 对 `null`、JDK 类和内部类实例的返回值。
- 新增 `testGetCanonicalName`，覆盖新增的 `ObjectUtils.getClassCanonicalName(Object)` 对 `null`、JDK 类和内部类实例的返回值。
- 不需要调整 import，因为旧测试已静态导入 `assertNull` 和 `assertEquals`。

```java
    /**
     * @since 3.7
     */
    @Test
    public void testGetClassName() {
        assertNull(ObjectUtils.getClassName(null));
        assertEquals("java.lang.String", ObjectUtils.getClassName(new String()));
        assertEquals("org.apache.commons.lang3.ObjectUtilsTest$CloneableString",
                ObjectUtils.getClassName(new CloneableString("test")));
    }

    /**
     * @since 3.7
     */
    @Test
    public void testGetSimpleName() {
        assertNull(ObjectUtils.getClassSimpleName(null));
        assertEquals("String", ObjectUtils.getClassSimpleName(new String()));
        assertEquals("CloneableString", ObjectUtils.getClassSimpleName(new CloneableString("test")));
    }

    /**
     * @since 3.7
     */
    @Test
    public void testGetCanonicalName() {
        assertNull(ObjectUtils.getClassCanonicalName(null));
        assertEquals("java.lang.String", ObjectUtils.getClassCanonicalName(new String()));
        assertEquals("org.apache.commons.lang3.ObjectUtilsTest.CloneableString",
                ObjectUtils.getClassCanonicalName(new CloneableString("test")));
    }
```