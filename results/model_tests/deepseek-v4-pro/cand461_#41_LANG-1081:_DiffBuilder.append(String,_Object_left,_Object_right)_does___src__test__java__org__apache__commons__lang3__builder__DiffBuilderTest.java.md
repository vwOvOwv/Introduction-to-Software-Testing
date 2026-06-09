# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `3181b407668fa09b83ff80126b5abdfc4074ab9a`
- B: `ffc38b1f3b35ddfadb942240b9d2f933ec83d1be`
- test: `src/test/java/org/apache/commons/lang3/builder/DiffBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/DiffBuilder.java']`
- old_test_mode: `methods`
- user_chars: `5233`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1689, 'completion_tokens': 1610, 'total_tokens': 3299, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1044}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 1305}`

---

- 新增 @Test 方法：`testObjectsSameAndEqual`、`testObjectsNotSameButEqual`、`testObjectsNotSameNorEqual`，覆盖 equals 相等（同一实例/不同实例）与不相等三种情况，对应生产代码中 `DiffBuilder.append(Object)` 新增的 `equals` 短路逻辑。
- 删除 @Test 方法：`testObjectsEqual`，已被上述三个方法替代。
- 调整 import：新增 `assertFalse` 与 `assertTrue` 静态导入，供新测试使用。

```java
// IMPORTS_START
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
// IMPORTS_END

// DELETE_TESTS_START
testObjectsEqual
// DELETE_TESTS_END

    /** 
     * Test that "left" and "right" are the same instance and are equal. 
     */
    @Test
    public void testObjectsSameAndEqual() throws Exception {
        final Integer sameObject = 1;
        final TypeTestClass left = new TypeTestClass();
        left.objectField = sameObject;
        final TypeTestClass right = new TypeTestClass();
        right.objectField = sameObject;
        assertTrue(left.objectField == right.objectField);
        assertTrue(left.objectField.equals(right.objectField));

        final DiffResult list = left.diff(right);
        assertEquals(0, list.getNumberOfDiffs());
    }

    /** 
     * Test that "left" and "right" are the same instance but are equal. 
     */
    @Test
    public void testObjectsNotSameButEqual() throws Exception {
        final TypeTestClass left = new TypeTestClass();
        left.objectField = new Integer(1);
        final TypeTestClass right = new TypeTestClass();
        right.objectField = new Integer(1);
        assertFalse(left.objectField == right.objectField);
        assertTrue(left.objectField.equals(right.objectField));

        final DiffResult list = left.diff(right);
        assertEquals(0, list.getNumberOfDiffs());
    }

    /** 
     * Test that "left" and "right" are not the same instance and are not equal. 
     */
    @Test
    public void testObjectsNotSameNorEqual() throws Exception {
        final TypeTestClass left = new TypeTestClass();
        left.objectField = 4;
        final TypeTestClass right = new TypeTestClass();
        right.objectField = 100;
        assertFalse(left.objectField == right.objectField);
        assertFalse(left.objectField.equals(right.objectField));

        final DiffResult list = left.diff(right);
        assertEquals(1, list.getNumberOfDiffs());
    }
```