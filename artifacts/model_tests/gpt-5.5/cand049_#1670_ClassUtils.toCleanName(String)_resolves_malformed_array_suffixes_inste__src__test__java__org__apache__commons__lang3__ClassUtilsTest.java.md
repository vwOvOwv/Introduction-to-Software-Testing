# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `465c6a980aa783bd0fa82ab2742568c3f34c0d55`
- B: `28f46460d63b4c7806a2b9cce382b2b79ba6fd50`
- test: `src/test/java/org/apache/commons/lang3/ClassUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ClassUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `98458`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 21380, 'completion_tokens': 462, 'total_tokens': 21842}`

---

- 新增 `testGetClassStringMalformedMiddleJunkRejected`，对应生产代码在 `toCleanName` 中拒绝 `[]` 数组后缀中夹杂非成对数组标记的畸形输入。
- 新增 `testGetClassStringMalformedUnpairedBracketsRejected`，对应生产代码使用 `(?:\\[\\])+` 校验数组后缀必须由完整 `[]` 对组成。
- 新增 `testGetClassStringWellFormedArrayStillResolves`，对应生产代码修复后仍应接受合法的一维和二维普通数组类名。
- 不需要调整 import，旧测试文件已包含 `assertNotNull`、`assertThrows` 和 `@Test` 所需 import。

```java
    /**
     * Pre-patch: getClass("java.lang.String[]junk[]") silently returns String[][][][]. Post-patch: must throw
     * IllegalArgumentException.
     */
    @Test
    public void testGetClassStringMalformedMiddleJunkRejected() {
        assertThrows(IllegalArgumentException.class, () -> ClassUtils.getClass("java.lang.String[]junk[]"));
    }

    /**
     * Mutation control: suffix ends with "[]" so the array-branch is entered, and the suffix from arrIdx contains only '['
     * and ']' chars but NOT as well-formed pairs ("[]][]").
     */
    @Test
    public void testGetClassStringMalformedUnpairedBracketsRejected() {
        assertThrows(IllegalArgumentException.class, () -> ClassUtils.getClass("java.lang.String[]][]"));
    }

    /**
     * Negative control: well-formed multi-dim array still resolves.
     */
    @Test
    public void testGetClassStringWellFormedArrayStillResolves() throws Exception {
        assertNotNull(ClassUtils.getClass("java.lang.String[]"));
        assertNotNull(ClassUtils.getClass("java.lang.String[][]"));
    }
```