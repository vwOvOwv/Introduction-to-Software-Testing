# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `8e8e78d849825696237b9f540f3e082a44b1e838`
- B: `6f03c0ce11db4a270124b9bf93338d3db9fccf5c`
- test: `src/test/java/org/apache/commons/lang3/ClassUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ClassUtils.java']`
- old_test_mode: `methods`
- user_chars: `25710`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6235, 'completion_tokens': 2921, 'total_tokens': 9156}`

---

- 新增 `test_getCanonicalName_Class`，覆盖生产代码中 `ClassUtils.getCanonicalName(Class<?>)` 改为返回 `Class#getCanonicalName()` 且匿名/局部类返回空字符串的行为。
- 新增 `test_getName_Class`，替代旧的 `test_getClassName_Class`，保持 `ClassUtils.getName(Class<?>)` 断言并调整匿名/局部类编号。
- 新增 `test_getName_Object`，补充 `ClassUtils.getName(Object, String)` 的对象场景断言。
- 删除旧测试方法 `test_getClassName_Class`，对应测试 diff 中该方法被移除并由 `test_getName_Class` 覆盖。
- 修改 `test_getShortCanonicalName_Class`、`test_getShortCanonicalName_Object`、`test_getShortClassName_Class`、`test_getShortClassName_Object`，对应新增测试导致匿名/局部类编译编号变化。
- 不需要调整 import。

```java
// DELETE_TESTS_START
test_getClassName_Class
// DELETE_TESTS_END

    @Test
    public void test_getCanonicalName_Class() {
        assertEquals("org.apache.commons.lang3.ClassUtils", ClassUtils.getCanonicalName(ClassUtils.class));
        assertEquals("java.util.Map.Entry", ClassUtils.getCanonicalName(Map.Entry.class));
        assertEquals("", ClassUtils.getCanonicalName((Class<?>) null));

        assertEquals("java.lang.String[]", ClassUtils.getCanonicalName(String[].class));
        assertEquals("java.util.Map.Entry[]", ClassUtils.getCanonicalName(Map.Entry[].class));

        // Primitives
        assertEquals("boolean", ClassUtils.getCanonicalName(boolean.class));
        assertEquals("byte", ClassUtils.getCanonicalName(byte.class));
        assertEquals("char", ClassUtils.getCanonicalName(char.class));
        assertEquals("short", ClassUtils.getCanonicalName(short.class));
        assertEquals("int", ClassUtils.getCanonicalName(int.class));
        assertEquals("long", ClassUtils.getCanonicalName(long.class));
        assertEquals("float", ClassUtils.getCanonicalName(float.class));
        assertEquals("double", ClassUtils.getCanonicalName(double.class));

        // Primitive Arrays
        assertEquals("boolean[]", ClassUtils.getCanonicalName(boolean[].class));
        assertEquals("byte[]", ClassUtils.getCanonicalName(byte[].class));
        assertEquals("char[]", ClassUtils.getCanonicalName(char[].class));
        assertEquals("short[]", ClassUtils.getCanonicalName(short[].class));
        assertEquals("int[]", ClassUtils.getCanonicalName(int[].class));
        assertEquals("long[]", ClassUtils.getCanonicalName(long[].class));
        assertEquals("float[]", ClassUtils.getCanonicalName(float[].class));
        assertEquals("double[]", ClassUtils.getCanonicalName(double[].class));

        // Arrays of arrays of ...
        assertEquals("java.lang.String[][]", ClassUtils.getCanonicalName(String[][].class));
        assertEquals("java.lang.String[][][]", ClassUtils.getCanonicalName(String[][][].class));
        assertEquals("java.lang.String[][][][]", ClassUtils.getCanonicalName(String[][][][].class));

        // Inner types
        class Named {
            // empty
        }
        assertEquals(StringUtils.EMPTY, ClassUtils.getCanonicalName(new Object() {
            // empty
        }.getClass()));
        assertEquals(StringUtils.EMPTY, ClassUtils.getCanonicalName(Named.class));
        assertEquals("org.apache.commons.lang3.ClassUtilsTest.Inner", ClassUtils.getCanonicalName(Inner.class));
    }

    @Test
    public void test_getName_Class() {
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
        assertEquals("org.apache.commons.lang3.ClassUtilsTest$2", ClassUtils.getName(new Object() {
            // empty
        }.getClass()));
        assertEquals("org.apache.commons.lang3.ClassUtilsTest$2Named", ClassUtils.getName(Named.class));
        assertEquals("org.apache.commons.lang3.ClassUtilsTest$Inner", ClassUtils.getName(Inner.class));
    }

    @Test
    public void test_getName_Object() {
        assertEquals("org.apache.commons.lang3.ClassUtils", ClassUtils.getName(new ClassUtils(), "<null>"));
        assertEquals("org.apache.commons.lang3.ClassUtilsTest$Inner", ClassUtils.getName(new Inner(), "<null>"));
        assertEquals("java.lang.String", ClassUtils.getName("hello", "<null>"));
        assertEquals("<null>", ClassUtils.getName(null, "<null>"));

        // Inner types
        class Named {
            // empty
        }
        assertEquals("org.apache.commons.lang3.ClassUtilsTest$3", ClassUtils.getName(new Object() {
            // empty
        }, "<null>"));
        assertEquals("org.apache.commons.lang3.ClassUtilsTest$3Named", ClassUtils.getName(new Named(), "<null>"));
        assertEquals("org.apache.commons.lang3.ClassUtilsTest$Inner", ClassUtils.getName(new Inner(), "<null>"));
    }

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
        assertEquals("ClassUtilsTest.7", ClassUtils.getShortCanonicalName(new Object() {
            // empty
        }.getClass()));
        assertEquals("ClassUtilsTest.7Named", ClassUtils.getShortCanonicalName(Named.class));
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
        assertEquals("ClassUtilsTest.8", ClassUtils.getShortCanonicalName(new Object() {
            // empty
        }, "<null>"));
        assertEquals("ClassUtilsTest.8Named", ClassUtils.getShortCanonicalName(new Named(), "<null>"));
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
        assertEquals("ClassUtilsTest.9", ClassUtils.getShortClassName(new Object() {
            // empty
        }.getClass()));
        assertEquals("ClassUtilsTest.9Named", ClassUtils.getShortClassName(Named.class));
        assertEquals("ClassUtilsTest.Inner", ClassUtils.getShortClassName(Inner.class));
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
        assertEquals("ClassUtilsTest.10", ClassUtils.getShortClassName(new Object() {
            // empty
        }, "<null>"));
        assertEquals("ClassUtilsTest.10Named", ClassUtils.getShortClassName(new Named(), "<null>"));
        assertEquals("ClassUtilsTest.Inner", ClassUtils.getShortClassName(new Inner(), "<null>"));
    }
```