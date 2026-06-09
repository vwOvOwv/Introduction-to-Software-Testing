# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `125cfb4cab35daebe874a599877d6280b464212b`
- B: `8e8e78d849825696237b9f540f3e082a44b1e838`
- test: `src/test/java/org/apache/commons/lang3/ClassUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ClassUtils.java']`
- old_test_mode: `methods`
- user_chars: `18517`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 4958, 'completion_tokens': 1889, 'total_tokens': 6847}`

---

- 修改 `test_getShortCanonicalName_Class`：生产代码新增/调整名称相关 API 后测试类匿名/本地类序号变化，更新期望值。
- 修改 `test_getShortCanonicalName_Object`：同样因新增测试方法导致本地/匿名类序号变化，更新期望值。
- 修改 `test_getShortClassName_Class`：新增 `getName(Class<?>)` 覆盖测试插入后，更新匿名/本地类短名期望值。
- 新增 `test_getClassName_Class`：覆盖生产代码新增的 `ClassUtils.getName(Class<?>)` 方法。
- 修改 `test_getShortClassName_Object`：因新增测试方法导致匿名/本地类序号变化，更新期望值。
- import 无需调整：`Map` 已被既有测试使用。

```java
    @Test
    public void test_getShortCanonicalName_Class() {
        assertEquals("ClassUtils", ClassUtils.getShortCanonicalName(ClassUtils.class));
        assertEquals("ClassUtils[]", ClassUtils.getShortCanonicalName(ClassUtils[].class));
        assertEquals("ClassUtils[][]", ClassUtils.getShortCanonicalName(ClassUtils[][].class));
        assertEquals("int[]", ClassUtils.getShortCanonicalName(int[].class));
        assertEquals("int[][]", ClassUtils.getShortCanonicalName(int[][].class));

        // Inner types
        class Named {
            // empty
        }
        assertEquals("ClassUtilsTest.4", ClassUtils.getShortCanonicalName(new Object() {
            // empty
        }.getClass()));
        assertEquals("ClassUtilsTest.4Named", ClassUtils.getShortCanonicalName(Named.class));
        assertEquals("ClassUtilsTest.Inner", ClassUtils.getShortCanonicalName(Inner.class));
    }

    @Test
    public void test_getShortCanonicalName_Object() {
        assertEquals("<null>", ClassUtils.getShortCanonicalName(null, "<null>"));
        assertEquals("ClassUtils", ClassUtils.getShortCanonicalName(new ClassUtils(), "<null>"));
        assertEquals("ClassUtils[]", ClassUtils.getShortCanonicalName(new ClassUtils[0], "<null>"));
        assertEquals("ClassUtils[][]", ClassUtils.getShortCanonicalName(new ClassUtils[0][0], "<null>"));
        assertEquals("int[]", ClassUtils.getShortCanonicalName(new int[0], "<null>"));
        assertEquals("int[][]", ClassUtils.getShortCanonicalName(new int[0][0], "<null>"));

        // Inner types
        class Named {
            // empty
        }
        assertEquals("ClassUtilsTest.5", ClassUtils.getShortCanonicalName(new Object() {
            // empty
        }, "<null>"));
        assertEquals("ClassUtilsTest.5Named", ClassUtils.getShortCanonicalName(new Named(), "<null>"));
        assertEquals("ClassUtilsTest.Inner", ClassUtils.getShortCanonicalName(new Inner(), "<null>"));
    }

    @Test
    public void test_getShortClassName_Class() {
        assertEquals("ClassUtils", ClassUtils.getShortClassName(ClassUtils.class));
        assertEquals("Map.Entry", ClassUtils.getShortClassName(Map.Entry.class));
        assertEquals("", ClassUtils.getShortClassName((Class<?>) null));

        // LANG-535
        assertEquals("String[]", ClassUtils.getShortClassName(String[].class));
        assertEquals("Map.Entry[]", ClassUtils.getShortClassName(Map.Entry[].class));

        // Primitives
        assertEquals("boolean", ClassUtils.getShortClassName(boolean.class));
        assertEquals("byte", ClassUtils.getShortClassName(byte.class));
        assertEquals("char", ClassUtils.getShortClassName(char.class));
        assertEquals("short", ClassUtils.getShortClassName(short.class));
        assertEquals("int", ClassUtils.getShortClassName(int.class));
        assertEquals("long", ClassUtils.getShortClassName(long.class));
        assertEquals("float", ClassUtils.getShortClassName(float.class));
        assertEquals("double", ClassUtils.getShortClassName(double.class));

        // Primitive Arrays
        assertEquals("boolean[]", ClassUtils.getShortClassName(boolean[].class));
        assertEquals("byte[]", ClassUtils.getShortClassName(byte[].class));
        assertEquals("char[]", ClassUtils.getShortClassName(char[].class));
        assertEquals("short[]", ClassUtils.getShortClassName(short[].class));
        assertEquals("int[]", ClassUtils.getShortClassName(int[].class));
        assertEquals("long[]", ClassUtils.getShortClassName(long[].class));
        assertEquals("float[]", ClassUtils.getShortClassName(float[].class));
        assertEquals("double[]", ClassUtils.getShortClassName(double[].class));

        // Arrays of arrays of ...
        assertEquals("String[][]", ClassUtils.getShortClassName(String[][].class));
        assertEquals("String[][][]", ClassUtils.getShortClassName(String[][][].class));
        assertEquals("String[][][][]", ClassUtils.getShortClassName(String[][][][].class));

        // Inner types
        class Named {
            // empty
        }
        assertEquals("ClassUtilsTest.6", ClassUtils.getShortClassName(new Object() {
            // empty
        }.getClass()));
        assertEquals("ClassUtilsTest.6Named", ClassUtils.getShortClassName(Named.class));
        assertEquals("ClassUtilsTest.Inner", ClassUtils.getShortClassName(Inner.class));
    }

    @Test
    public void test_getClassName_Class() {
        assertEquals("org.apache.commons.lang3.ClassUtils", ClassUtils.getName(ClassUtils.class));
        assertEquals("java.util.Map$Entry", ClassUtils.getName(Map.Entry.class));
        assertEquals("", ClassUtils.getName((Class<?>) null));

        assertEquals("[Ljava.lang.String;", ClassUtils.getName(String[].class));
        assertEquals("[Ljava.util.Map$Entry;", ClassUtils.getName(Map.Entry[].class));

        // Primitives
        assertEquals("boolean", ClassUtils.getName(boolean.class));
        assertEquals("byte", ClassUtils.getName(byte.class));
        assertEquals("char", ClassUtils.getName(char.class));
        assertEquals("short", ClassUtils.getName(short.class));
        assertEquals("int", ClassUtils.getName(int.class));
        assertEquals("long", ClassUtils.getName(long.class));
        assertEquals("float", ClassUtils.getName(float.class));
        assertEquals("double", ClassUtils.getName(double.class));

        // Primitive Arrays
        assertEquals("[Z", ClassUtils.getName(boolean[].class));
        assertEquals("[B", ClassUtils.getName(byte[].class));
        assertEquals("[C", ClassUtils.getName(char[].class));
        assertEquals("[S", ClassUtils.getName(short[].class));
        assertEquals("[I", ClassUtils.getName(int[].class));
        assertEquals("[J", ClassUtils.getName(long[].class));
        assertEquals("[F", ClassUtils.getName(float[].class));
        assertEquals("[D", ClassUtils.getName(double[].class));

        // Arrays of arrays of ...
        assertEquals("[[Ljava.lang.String;", ClassUtils.getName(String[][].class));
        assertEquals("[[[Ljava.lang.String;", ClassUtils.getName(String[][][].class));
        assertEquals("[[[[Ljava.lang.String;", ClassUtils.getName(String[][][][].class));

        // Inner types
        class Named {
            // empty
        }
        assertEquals("org.apache.commons.lang3.ClassUtilsTest$7", ClassUtils.getName(new Object() {
            // empty
        }.getClass()));
        assertEquals("org.apache.commons.lang3.ClassUtilsTest$7Named", ClassUtils.getName(Named.class));
        assertEquals("org.apache.commons.lang3.ClassUtilsTest$Inner", ClassUtils.getName(Inner.class));
    }

    @Test
    public void test_getShortClassName_Object() {
        assertEquals("ClassUtils", ClassUtils.getShortClassName(new ClassUtils(), "<null>"));
        assertEquals("ClassUtilsTest.Inner", ClassUtils.getShortClassName(new Inner(), "<null>"));
        assertEquals("String", ClassUtils.getShortClassName("hello", "<null>"));
        assertEquals("<null>", ClassUtils.getShortClassName(null, "<null>"));

        // Inner types
        class Named {
            // empty
        }
        assertEquals("ClassUtilsTest.8", ClassUtils.getShortClassName(new Object() {
            // empty
        }, "<null>"));
        assertEquals("ClassUtilsTest.8Named", ClassUtils.getShortClassName(new Named(), "<null>"));
        assertEquals("ClassUtilsTest.Inner", ClassUtils.getShortClassName(new Inner(), "<null>"));
    }
```