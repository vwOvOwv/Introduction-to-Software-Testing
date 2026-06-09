# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `c4ea2b0113b28b9d861acefc296f277e2eddaf9f`
- B: `b6224451728562b0a4b33b63e8589753b1e2a57c`
- test: `src/test/java/org/apache/commons/lang3/ClassUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ClassUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `93913`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 20375, 'completion_tokens': 402, 'total_tokens': 20777}`

---

- 修改辅助方法 `assertGetClassThrowsException`：生产代码现在抛出 `new ClassNotFoundException(className)`，因此测试需捕获异常并断言非 null 输入时异常消息等于原始 `className`。
- 修改 `@Test` 方法 `testGetClassClassNotFound`：新增包含内部类风格名称的找不到类场景，以覆盖生产代码不再返回转换后的 `$` 名称作为异常消息。
- import 无需调整：`assertEquals` 与 `assertThrows` 已存在静态导入。

```java
    private void assertGetClassThrowsException(final String className, final Class<? extends Exception> exceptionType) {
        final Exception exception = assertThrows(exceptionType, () -> ClassUtils.getClass(className),
            "ClassUtils.getClass() should fail with an exception of type " + exceptionType.getName() + " when given class name \"" + className + "\".");
        if (className != null) {
            assertEquals(className, exception.getMessage());
        }
    }

    @Test
    void testGetClassClassNotFound() throws Exception {
        assertGetClassThrowsClassNotFound("bool");
        assertGetClassThrowsClassNotFound("bool[]");
        assertGetClassThrowsClassNotFound("integer[]");
        assertGetClassThrowsClassNotFound("org.apache.commons.lang3.ClassUtilsTest.AClassThatCannotBeFound");
    }
```