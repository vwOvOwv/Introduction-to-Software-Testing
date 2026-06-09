# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e2b349d046ec9945ece518b068ae38bc73b7f83c`
- B: `5dd8e33cf68b649b9af0bbbede58d6b5637b4c3e`
- test: `src/test/java/org/apache/commons/lang3/reflect/MethodUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/reflect/MethodUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `74775`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 16336, 'completion_tokens': 1284, 'total_tokens': 17620}`

---

- 新增 `testInvokeStaticMethodVarArgsOfInterface`，覆盖 `getMatchingAccessibleMethod` 对接口类型 varargs 组件使用 `isAssignableFrom` 接受实现类实参的静态方法场景。
- 新增 `testInvokeMethodVarArgsOfInterface`，覆盖同一生产变更在实例方法 varargs 接口参数上的行为。
- 新增测试夹具 `PublicImpl1OfPackagePrivateEmptyInterface`、`PublicImpl2OfPackagePrivateEmptyInterface` 以及 `TestBean` 中的接口 varargs 方法；无需调整 import。

```java
public static class PublicImpl1OfPackagePrivateEmptyInterface implements PackagePrivateEmptyInterface {
    // empty
}

public static class PublicImpl2OfPackagePrivateEmptyInterface implements PackagePrivateEmptyInterface {
    // empty
}

public static String staticPackagePrivateEmptyInterface(final PackagePrivateEmptyInterface... args) {
    return "static PackagePrivateEmptyInterface...";
}

public String packagePrivateEmptyInterface(final PackagePrivateEmptyInterface... args) {
    return "PackagePrivateEmptyInterface...";
}

@Test
void testInvokeStaticMethodVarArgsOfInterface() throws Exception {
    assertEquals("static PackagePrivateEmptyInterface...", MethodUtils.invokeStaticMethod(TestBean.class, "staticPackagePrivateEmptyInterface",
            new PublicImpl1OfPackagePrivateEmptyInterface(), new PublicImpl2OfPackagePrivateEmptyInterface()));
    assertEquals("static PackagePrivateEmptyInterface...",
            MethodUtils.invokeStaticMethod(TestBean.class, "staticPackagePrivateEmptyInterface", new PackagePrivateEmptyInterface() {
                // empty
            }, new PackagePrivateEmptyInterface() {
                // empty
            }));
}

@Test
void testInvokeMethodVarArgsOfInterface() throws Exception {
    assertEquals("PackagePrivateEmptyInterface...", MethodUtils.invokeMethod(testBean, "packagePrivateEmptyInterface",
            new PublicImpl1OfPackagePrivateEmptyInterface(), new PublicImpl2OfPackagePrivateEmptyInterface()));
    assertEquals("PackagePrivateEmptyInterface...", MethodUtils.invokeMethod(testBean, "packagePrivateEmptyInterface", new PackagePrivateEmptyInterface() {
        // empty
    }, new PackagePrivateEmptyInterface() {
        // empty
    }));
}
```