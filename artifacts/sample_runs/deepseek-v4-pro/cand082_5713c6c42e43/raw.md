# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `f8a6bf9500f655c0f772313e8d0098984420299b`
- B: `5713c6c42e43977df17a7a6c0d39a8ff4f4540b6`
- test: `src/test/java/org/apache/commons/lang3/ClassUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ClassUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `106290`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 25112, 'completion_tokens': 2994, 'total_tokens': 28106, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2242}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 24728}`

---

- 新增测试方法 `testGetClassLengthIllegal`：对应生产代码新增的类名长度超限检查（>65535），使用参数化测试验证抛出 `IllegalArgumentException`。
- 新增测试方法 `testGetClassLongestCheck`：验证最大允许类名长度（65535）与最大数组维度（255）边界情况，包括正确解析和超限抛出异常。
- 修改测试方法 `testGetClassByNormalNameArrays`：增加一行断言，验证 `getClass` 能正确解析二维数组的 JNI 风格类名 `"[[Ljava.util.Map$Entry;"`。
- 新增类常量 `MAX_ARRAY_DIMENSIONS`：在测试类中添加 `private static final int MAX_ARRAY_DIMENSIONS = 255;`，供新增测试方法使用。
- 无需调整导入或删除已有测试方法。

```java
private static final int MAX_ARRAY_DIMENSIONS = 255;

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
    assertThrows(IllegalArgumentException.class, () -> assertEquals(classNameLength, ClassUtils.getClass(StringUtils.repeat("a.", classNameLength / 2))));
}

@Test
void testGetClassLongestCheck() throws ClassNotFoundException {
    final String maxClassName = StringUtils.repeat("a", 65535);
    final String maxDimensions = StringUtils.repeat("[]", MAX_ARRAY_DIMENSIONS);
    final String maxOpens = StringUtils.repeat("[", MAX_ARRAY_DIMENSIONS);
    assertThrows(ClassNotFoundException.class, () -> ClassUtils.getClass(maxClassName));
    assertNotNull(ClassUtils.getClass("java.lang.String" + maxDimensions));
    assertThrows(ClassNotFoundException.class, () -> ClassUtils.getClass(maxClassName + maxDimensions));
    assertThrows(ClassNotFoundException.class, () -> ClassUtils.getClass(maxOpens + "L" + maxClassName + ";"));
    // maxOpens + 1
    assertThrows(IllegalArgumentException.class, () -> ClassUtils.getClass(maxOpens + "[L" + maxClassName + ";"));
}
```