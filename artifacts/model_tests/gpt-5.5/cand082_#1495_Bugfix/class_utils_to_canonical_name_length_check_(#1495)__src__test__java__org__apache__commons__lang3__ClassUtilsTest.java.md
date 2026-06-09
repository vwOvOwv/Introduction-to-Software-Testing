# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `f8a6bf9500f655c0f772313e8d0098984420299b`
- B: `5713c6c42e43977df17a7a6c0d39a8ff4f4540b6`
- test: `src/test/java/org/apache/commons/lang3/ClassUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ClassUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `106290`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 23399, 'completion_tokens': 1157, 'total_tokens': 24556}`

---

- 修改 `testGetClassByNormalNameArrays`：生产代码改为 `toCleanName` 后支持已编码的多维内部类数组名，因此新增 `[[Ljava.util.Map$Entry;` 的断言。
- 新增 `testGetClassLengthIllegal`：对应新增的最大类名长度 65,535 校验，覆盖超长普通类名和点分形式类名会抛出 `IllegalArgumentException`。
- 新增 `testGetClassLongestCheck`：覆盖 65,535 长度边界、255 维数组边界以及 256 维已编码数组非法场景。
- import 无需调整：旧测试已包含 `ParameterizedTest`、`IntRangeSource`、`assertNotNull`、`assertThrows` 等所需 import。

```java
    @Test
    void testGetClassByNormalNameArrays() throws ClassNotFoundException {
        assertEquals(int[].class, ClassUtils.getClass("int[]"));
        assertEquals(long[].class, ClassUtils.getClass("long[]"));
        assertEquals(short[].class, ClassUtils.getClass("short[]"));
        assertEquals(byte[].class, ClassUtils.getClass("byte[]"));
        assertEquals(char[].class, ClassUtils.getClass("char[]"));
        assertEquals(float[].class, ClassUtils.getClass("float[]"));
        assertEquals(double[].class, ClassUtils.getClass("double[]"));
        assertEquals(boolean[].class, ClassUtils.getClass("boolean[]"));
        assertEquals(String[].class, ClassUtils.getClass("java.lang.String[]"));
        assertEquals(java.util.Map.Entry[].class, ClassUtils.getClass("java.util.Map.Entry[]"));
        assertEquals(java.util.Map.Entry[].class, ClassUtils.getClass("java.util.Map$Entry[]"));
        assertEquals(java.util.Map.Entry[].class, ClassUtils.getClass("[Ljava.util.Map.Entry;"));
        assertEquals(java.util.Map.Entry[].class, ClassUtils.getClass("[Ljava.util.Map$Entry;"));
        assertEquals(java.util.Map.Entry[][].class, ClassUtils.getClass("[[Ljava.util.Map$Entry;"));
    }

    @ParameterizedTest
    @IntRangeSource(from = 65536, to = 65555)
    void testGetClassLengthIllegal(final int classNameLength) throws ClassNotFoundException {
        assertThrows(IllegalArgumentException.class, () -> ClassUtils.getClass(StringUtils.repeat("a", classNameLength)));
        assertThrows(IllegalArgumentException.class,
                () -> assertEquals(classNameLength, ClassUtils.getClass(StringUtils.repeat("a.", classNameLength / 2))));
    }

    @Test
    void testGetClassLongestCheck() throws ClassNotFoundException {
        final String maxClassName = StringUtils.repeat("a", 65535);
        final String maxDimensions = StringUtils.repeat("[]", 255);
        final String maxOpens = StringUtils.repeat("[", 255);
        assertThrows(ClassNotFoundException.class, () -> ClassUtils.getClass(maxClassName));
        assertNotNull(ClassUtils.getClass("java.lang.String" + maxDimensions));
        assertThrows(ClassNotFoundException.class, () -> ClassUtils.getClass(maxClassName + maxDimensions));
        assertThrows(ClassNotFoundException.class, () -> ClassUtils.getClass(maxOpens + "L" + maxClassName + ";"));
        assertThrows(IllegalArgumentException.class, () -> ClassUtils.getClass(maxOpens + "[L" + maxClassName + ";"));
    }
```