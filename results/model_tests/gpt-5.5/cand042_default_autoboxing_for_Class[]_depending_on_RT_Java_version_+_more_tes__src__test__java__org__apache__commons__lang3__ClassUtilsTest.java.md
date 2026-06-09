# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `485dd97b184fe42bf9b1434633be84cb6acc75f2`
- B: `240b7a92f63bec0a81ec8707e6b08115da368590`
- test: `src/test/java/org/apache/commons/lang3/ClassUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ClassUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `62169`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 13711, 'completion_tokens': 3764, 'total_tokens': 17475}`

---

- 修改 `test_isAssignable_ClassArray_ClassArray`：生产代码默认 `isAssignable(Class<?>[], Class<?>[])` 改为按当前 Java 版本启用 autoboxing，因此补充 primitive/wrapper 数组断言。
- 新增 `test_isAssignable_ClassArray_ClassArray_Autoboxing`：覆盖显式 `autoboxing=true` 的数组赋值行为，避免默认行为变化影响断言语义。
- 新增 `test_isAssignable_ClassArray_ClassArray_NoAutoboxing`：覆盖显式 `autoboxing=false` 的数组赋值行为，保留旧语义验证。
- 修改 `test_isAssignable`：默认单类赋值现在随 Java 版本启用 autoboxing，因此补充 primitive/wrapper 到 `Object` 的默认行为断言。
- 修改 `test_isAssignable_Autoboxing`：补充显式 autoboxing 下 primitive/wrapper 到 `Object` 的断言。
- 新增 `test_isAssignable_NoAutoboxing`：覆盖显式禁用 autoboxing 的单类赋值旧行为。
- 新增 `test_isAssignable_DefaultUnboxing_Widening`：覆盖默认方法在 wrapper unboxing 后 primitive widening 的 Java 版本相关行为。
- import 无需调整，仅原文件中多余空行可删除但不影响编译。

```java
public void test_isAssignable_ClassArray_ClassArray() throws Exception {
    Class<?>[] array2 = new Class[] {Object.class, Object.class};
    Class<?>[] array1 = new Class[] {Object.class};
    Class<?>[] array1s = new Class[] {String.class};
    Class<?>[] array0 = new Class[] {};
    Class<?>[] arrayPrimitives = { Integer.TYPE, Boolean.TYPE };
    Class<?>[] arrayWrappers = { Integer.class, Boolean.class };

    assertFalse(ClassUtils.isAssignable(array1, array2));
    assertFalse(ClassUtils.isAssignable(null, array2));
    assertTrue(ClassUtils.isAssignable(null, array0));
    assertTrue(ClassUtils.isAssignable(array0, array0));
    assertTrue(ClassUtils.isAssignable(array0, null));
    assertTrue(ClassUtils.isAssignable((Class[]) null, (Class[]) null));

    assertFalse(ClassUtils.isAssignable(array1, array1s));
    assertTrue(ClassUtils.isAssignable(array1s, array1s));
    assertTrue(ClassUtils.isAssignable(array1s, array1));

    boolean autoboxing = SystemUtils.isJavaVersionAtLeast(1.5f);

    assertEquals(autoboxing, ClassUtils.isAssignable(arrayPrimitives, arrayWrappers));
    assertEquals(autoboxing, ClassUtils.isAssignable(arrayWrappers, arrayPrimitives));
    assertFalse(ClassUtils.isAssignable(arrayPrimitives, array1));
    assertFalse(ClassUtils.isAssignable(arrayWrappers, array1));
    assertEquals(autoboxing, ClassUtils.isAssignable(arrayPrimitives, array2));
    assertTrue(ClassUtils.isAssignable(arrayWrappers, array2));
}

public void test_isAssignable_ClassArray_ClassArray_Autoboxing() throws Exception {
    Class<?>[] array2 = new Class[] {Object.class, Object.class};
    Class<?>[] array1 = new Class[] {Object.class};
    Class<?>[] array1s = new Class[] {String.class};
    Class<?>[] array0 = new Class[] {};
    Class<?>[] arrayPrimitives = { Integer.TYPE, Boolean.TYPE };
    Class<?>[] arrayWrappers = { Integer.class, Boolean.class };

    assertFalse(ClassUtils.isAssignable(array1, array2, true));
    assertFalse(ClassUtils.isAssignable(null, array2, true));
    assertTrue(ClassUtils.isAssignable(null, array0, true));
    assertTrue(ClassUtils.isAssignable(array0, array0, true));
    assertTrue(ClassUtils.isAssignable(array0, null, true));
    assertTrue(ClassUtils.isAssignable((Class[]) null, (Class[]) null, true));

    assertFalse(ClassUtils.isAssignable(array1, array1s, true));
    assertTrue(ClassUtils.isAssignable(array1s, array1s, true));
    assertTrue(ClassUtils.isAssignable(array1s, array1, true));

    assertTrue(ClassUtils.isAssignable(arrayPrimitives, arrayWrappers, true));
    assertTrue(ClassUtils.isAssignable(arrayWrappers, arrayPrimitives, true));
    assertFalse(ClassUtils.isAssignable(arrayPrimitives, array1, true));
    assertFalse(ClassUtils.isAssignable(arrayWrappers, array1, true));
    assertTrue(ClassUtils.isAssignable(arrayPrimitives, array2, true));
    assertTrue(ClassUtils.isAssignable(arrayWrappers, array2, true));
}

public void test_isAssignable_ClassArray_ClassArray_NoAutoboxing() throws Exception {
    Class<?>[] array2 = new Class[] {Object.class, Object.class};
    Class<?>[] array1 = new Class[] {Object.class};
    Class<?>[] array1s = new Class[] {String.class};
    Class<?>[] array0 = new Class[] {};
    Class<?>[] arrayPrimitives = { Integer.TYPE, Boolean.TYPE };
    Class<?>[] arrayWrappers = { Integer.class, Boolean.class };

    assertFalse(ClassUtils.isAssignable(array1, array2, false));
    assertFalse(ClassUtils.isAssignable(null, array2, false));
    assertTrue(ClassUtils.isAssignable(null, array0, false));
    assertTrue(ClassUtils.isAssignable(array0, array0, false));
    assertTrue(ClassUtils.isAssignable(array0, null, false));
    assertTrue(ClassUtils.isAssignable((Class[]) null, (Class[]) null, false));

    assertFalse(ClassUtils.isAssignable(array1, array1s, false));
    assertTrue(ClassUtils.isAssignable(array1s, array1s, false));
    assertTrue(ClassUtils.isAssignable(array1s, array1, false));

    assertFalse(ClassUtils.isAssignable(arrayPrimitives, arrayWrappers, false));
    assertFalse(ClassUtils.isAssignable(arrayWrappers, arrayPrimitives, false));
    assertFalse(ClassUtils.isAssignable(arrayPrimitives, array1, false));
    assertFalse(ClassUtils.isAssignable(arrayWrappers, array1, false));
    assertTrue(ClassUtils.isAssignable(arrayWrappers, array2, false));
    assertFalse(ClassUtils.isAssignable(arrayPrimitives, array2, false));
}

public void test_isAssignable() throws Exception {
    assertFalse(ClassUtils.isAssignable((Class<?>) null, null));
    assertFalse(ClassUtils.isAssignable(String.class, null));

    assertTrue(ClassUtils.isAssignable(null, Object.class));
    assertTrue(ClassUtils.isAssignable(null, Integer.class));
    assertFalse(ClassUtils.isAssignable(null, Integer.TYPE));
    assertTrue(ClassUtils.isAssignable(String.class, Object.class));
    assertTrue(ClassUtils.isAssignable(String.class, String.class));
    assertFalse(ClassUtils.isAssignable(Object.class, String.class));

    boolean autoboxing = SystemUtils.isJavaVersionAtLeast(1.5f);

    assertEquals(autoboxing, ClassUtils.isAssignable(Integer.TYPE, Integer.class));
    assertEquals(autoboxing, ClassUtils.isAssignable(Integer.TYPE, Object.class));
    assertEquals(autoboxing, ClassUtils.isAssignable(Integer.class, Integer.TYPE));
    assertEquals(autoboxing, ClassUtils.isAssignable(Integer.class, Object.class));
    assertTrue(ClassUtils.isAssignable(Integer.TYPE, Integer.TYPE));
    assertTrue(ClassUtils.isAssignable(Integer.class, Integer.class));
    assertEquals(autoboxing, ClassUtils.isAssignable(Boolean.TYPE, Boolean.class));
    assertEquals(autoboxing, ClassUtils.isAssignable(Boolean.TYPE, Object.class));
    assertEquals(autoboxing, ClassUtils.isAssignable(Boolean.class, Boolean.TYPE));
    assertEquals(autoboxing, ClassUtils.isAssignable(Boolean.class, Object.class));
    assertTrue(ClassUtils.isAssignable(Boolean.TYPE, Boolean.TYPE));
    assertTrue(ClassUtils.isAssignable(Boolean.class, Boolean.class));
}

public void test_isAssignable_Autoboxing() throws Exception {
    assertFalse(ClassUtils.isAssignable((Class<?>) null, null, true));
    assertFalse(ClassUtils.isAssignable(String.class, null, true));

    assertTrue(ClassUtils.isAssignable(null, Object.class, true));
    assertTrue(ClassUtils.isAssignable(null, Integer.class, true));
    assertFalse(ClassUtils.isAssignable(null, Integer.TYPE, true));
    assertTrue(ClassUtils.isAssignable(String.class, Object.class, true));
    assertTrue(ClassUtils.isAssignable(String.class, String.class, true));
    assertFalse(ClassUtils.isAssignable(Object.class, String.class, true));
    assertTrue(ClassUtils.isAssignable(Integer.TYPE, Integer.class, true));
    assertTrue(ClassUtils.isAssignable(Integer.TYPE, Object.class, true));
    assertTrue(ClassUtils.isAssignable(Integer.class, Integer.TYPE, true));
    assertTrue(ClassUtils.isAssignable(Integer.class, Object.class, true));
    assertTrue(ClassUtils.isAssignable(Integer.TYPE, Integer.TYPE, true));
    assertTrue(ClassUtils.isAssignable(Integer.class, Integer.class, true));
    assertTrue(ClassUtils.isAssignable(Boolean.TYPE, Boolean.class, true));
    assertTrue(ClassUtils.isAssignable(Boolean.class, Boolean.TYPE, true));
    assertTrue(ClassUtils.isAssignable(Boolean.class, Object.class, true));
    assertTrue(ClassUtils.isAssignable(Boolean.TYPE, Boolean.TYPE, true));
    assertTrue(ClassUtils.isAssignable(Boolean.class, Boolean.class, true));
}

public void test_isAssignable_NoAutoboxing() throws Exception {
    assertFalse(ClassUtils.isAssignable((Class<?>) null, null, false));
    assertFalse(ClassUtils.isAssignable(String.class, null, false));

    assertTrue(ClassUtils.isAssignable(null, Object.class, false));
    assertTrue(ClassUtils.isAssignable(null, Integer.class, false));
    assertFalse(ClassUtils.isAssignable(null, Integer.TYPE, false));
    assertTrue(ClassUtils.isAssignable(String.class, Object.class, false));
    assertTrue(ClassUtils.isAssignable(String.class, String.class, false));
    assertFalse(ClassUtils.isAssignable(Object.class, String.class, false));
    assertFalse(ClassUtils.isAssignable(Integer.TYPE, Integer.class, false));
    assertFalse(ClassUtils.isAssignable(Integer.TYPE, Object.class, false));
    assertFalse(ClassUtils.isAssignable(Integer.class, Integer.TYPE, false));
    assertTrue(ClassUtils.isAssignable(Integer.TYPE, Integer.TYPE, false));
    assertTrue(ClassUtils.isAssignable(Integer.class, Integer.class, false));
    assertFalse(ClassUtils.isAssignable(Boolean.TYPE, Boolean.class, false));
    assertFalse(ClassUtils.isAssignable(Boolean.TYPE, Object.class, false));
    assertFalse(ClassUtils.isAssignable(Boolean.class, Boolean.TYPE, false));
    assertTrue(ClassUtils.isAssignable(Boolean.class, Object.class, false));
    assertTrue(ClassUtils.isAssignable(Boolean.TYPE, Boolean.TYPE, false));
    assertTrue(ClassUtils.isAssignable(Boolean.class, Boolean.class, false));
}

public void test_isAssignable_DefaultUnboxing_Widening() throws Exception {
    boolean autoboxing = SystemUtils.isJavaVersionAtLeast(1.5f);

    // test byte conversions
    assertFalse("byte -> char", ClassUtils.isAssignable(Byte.class, Character.TYPE));
    assertEquals("byte -> byte", autoboxing, ClassUtils.isAssignable(Byte.class, Byte.TYPE));
    assertEquals("byte -> short", autoboxing, ClassUtils.isAssignable(Byte.class, Short.TYPE));
    assertEquals("byte -> int", autoboxing, ClassUtils.isAssignable(Byte.class, Integer.TYPE));
    assertEquals("byte -> long", autoboxing, ClassUtils.isAssignable(Byte.class, Long.TYPE));
    assertEquals("byte -> float", autoboxing, ClassUtils.isAssignable(Byte.class, Float.TYPE));
    assertEquals("byte -> double", autoboxing, ClassUtils.isAssignable(Byte.class, Double.TYPE));
    assertFalse("byte -> boolean", ClassUtils.isAssignable(Byte.class, Boolean.TYPE));

    // test short conversions
    assertFalse("short -> char", ClassUtils.isAssignable(Short.class, Character.TYPE));
    assertFalse("short -> byte", ClassUtils.isAssignable(Short.class, Byte.TYPE));
    assertEquals("short -> short", autoboxing, ClassUtils.isAssignable(Short.class, Short.TYPE));
    assertEquals("short -> int", autoboxing, ClassUtils.isAssignable(Short.class, Integer.TYPE));
    assertEquals("short -> long", autoboxing, ClassUtils.isAssignable(Short.class, Long.TYPE));
    assertEquals("short -> float", autoboxing, ClassUtils.isAssignable(Short.class, Float.TYPE));
    assertEquals("short -> double", autoboxing, ClassUtils.isAssignable(Short.class, Double.TYPE));
    assertFalse("short -> boolean", ClassUtils.isAssignable(Short.class, Boolean.TYPE));

    // test char conversions
    assertEquals("char -> char", autoboxing, ClassUtils.isAssignable(Character.class, Character.TYPE));
    assertFalse("char -> byte", ClassUtils.isAssignable(Character.class, Byte.TYPE));
    assertFalse("char -> short", ClassUtils.isAssignable(Character.class, Short.TYPE));
    assertEquals("char -> int", autoboxing, ClassUtils.isAssignable(Character.class, Integer.TYPE));
    assertEquals("char -> long", autoboxing, ClassUtils.isAssignable(Character.class, Long.TYPE));
    assertEquals("char -> float", autoboxing, ClassUtils.isAssignable(Character.class, Float.TYPE));
    assertEquals("char -> double", autoboxing, ClassUtils.isAssignable(Character.class, Double.TYPE));
    assertFalse("char -> boolean", ClassUtils.isAssignable(Character.class, Boolean.TYPE));

    // test int conversions
    assertFalse("int -> char", ClassUtils.isAssignable(Integer.class, Character.TYPE));
    assertFalse("int -> byte", ClassUtils.isAssignable(Integer.class, Byte.TYPE));
    assertFalse("int -> short", ClassUtils.isAssignable(Integer.class, Short.TYPE));
    assertEquals("int -> int", autoboxing, ClassUtils.isAssignable(Integer.class, Integer.TYPE));
    assertEquals("int -> long", autoboxing, ClassUtils.isAssignable(Integer.class, Long.TYPE));
    assertEquals("int -> float", autoboxing, ClassUtils.isAssignable(Integer.class, Float.TYPE));
    assertEquals("int -> double", autoboxing, ClassUtils.isAssignable(Integer.class, Double.TYPE));
    assertFalse("int -> boolean", ClassUtils.isAssignable(Integer.class, Boolean.TYPE));

    // test long conversions
    assertFalse("long -> char", ClassUtils.isAssignable(Long.class, Character.TYPE));
    assertFalse("long -> byte", ClassUtils.isAssignable(Long.class, Byte.TYPE));
    assertFalse("long -> short", ClassUtils.isAssignable(Long.class, Short.TYPE));
    assertFalse("long -> int", ClassUtils.isAssignable(Long.class, Integer.TYPE));
    assertEquals("long -> long", autoboxing, ClassUtils.isAssignable(Long.class, Long.TYPE));
    assertEquals("long -> float", autoboxing, ClassUtils.isAssignable(Long.class, Float.TYPE));
    assertEquals("long -> double", autoboxing, ClassUtils.isAssignable(Long.class, Double.TYPE));
    assertFalse("long -> boolean", ClassUtils.isAssignable(Long.class, Boolean.TYPE));

    // test float conversions
    assertFalse("float -> char", ClassUtils.isAssignable(Float.class, Character.TYPE));
    assertFalse("float -> byte", ClassUtils.isAssignable(Float.class, Byte.TYPE));
    assertFalse("float -> short", ClassUtils.isAssignable(Float.class, Short.TYPE));
    assertFalse("float -> int", ClassUtils.isAssignable(Float.class, Integer.TYPE));
    assertFalse("float -> long", ClassUtils.isAssignable(Float.class, Long.TYPE));
    assertEquals("float -> float", autoboxing, ClassUtils.isAssignable(Float.class, Float.TYPE));
    assertEquals("float -> double", autoboxing, ClassUtils.isAssignable(Float.class, Double.TYPE));
    assertFalse("float -> boolean", ClassUtils.isAssignable(Float.class, Boolean.TYPE));

    // test double conversions
    assertFalse("double -> char", ClassUtils.isAssignable(Double.class, Character.TYPE));
    assertFalse("double -> byte", ClassUtils.isAssignable(Double.class, Byte.TYPE));
    assertFalse("double -> short", ClassUtils.isAssignable(Double.class, Short.TYPE));
    assertFalse("double -> int", ClassUtils.isAssignable(Double.class, Integer.TYPE));
    assertFalse("double -> long", ClassUtils.isAssignable(Double.class, Long.TYPE));
    assertFalse("double -> float", ClassUtils.isAssignable(Double.class, Float.TYPE));
    assertEquals("double -> double", autoboxing, ClassUtils.isAssignable(Double.class, Double.TYPE));
    assertFalse("double -> boolean", ClassUtils.isAssignable(Double.class, Boolean.TYPE));

    // test boolean conversions
    assertFalse("boolean -> char", ClassUtils.isAssignable(Boolean.class, Character.TYPE));
    assertFalse("boolean -> byte", ClassUtils.isAssignable(Boolean.class, Byte.TYPE));
    assertFalse("boolean -> short", ClassUtils.isAssignable(Boolean.class, Short.TYPE));
    assertFalse("boolean -> int", ClassUtils.isAssignable(Boolean.class, Integer.TYPE));
    assertFalse("boolean -> long", ClassUtils.isAssignable(Boolean.class, Long.TYPE));
    assertFalse("boolean -> float", ClassUtils.isAssignable(Boolean.class, Float.TYPE));
    assertFalse("boolean -> double", ClassUtils.isAssignable(Boolean.class, Double.TYPE));
    assertEquals("boolean -> boolean", autoboxing, ClassUtils.isAssignable(Boolean.class, Boolean.TYPE));
}
```