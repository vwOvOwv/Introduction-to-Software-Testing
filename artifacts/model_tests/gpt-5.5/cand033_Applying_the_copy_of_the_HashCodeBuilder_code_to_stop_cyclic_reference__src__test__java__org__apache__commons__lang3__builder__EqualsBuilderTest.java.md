# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cfff2579f5cd4e92c46f8790b9185a45e91fd783`
- B: `1a60c21395fe7648188d1c91f62ac7baefa12742`
- test: `src/test/java/org/apache/commons/lang3/builder/EqualsBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/EqualsBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `50763`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 13640, 'completion_tokens': 579, 'total_tokens': 14219}`

---

- 新增 `testCyclicalObjectReferences`，覆盖生产代码在 `EqualsBuilder.reflectionAppend` 中新增的循环引用注册/反注册逻辑，防止递归比较导致 `StackOverflowError`。
- 新增辅助内部类 `TestObjectReference`，用于构造双向循环引用对象图并通过 `EqualsBuilder.reflectionEquals` 比较。
- 不需要调整 import，因为新增测试仅使用同包类和 `TestCase` 已有断言方法。

```java
    /**
     * Test cyclical object references which cause a StackOverflowException if
     * not handled properly. s. LANG-606
     */
    public void testCyclicalObjectReferences() {
        TestObjectReference refX1 = new TestObjectReference(1);
        TestObjectReference x1 = new TestObjectReference(1);
        x1.setObjectReference(refX1);
        refX1.setObjectReference(x1);

        TestObjectReference refX2 = new TestObjectReference(1);
        TestObjectReference x2 = new TestObjectReference(1);
        x2.setObjectReference(refX2);
        refX2.setObjectReference(x2);

        TestObjectReference refX3 = new TestObjectReference(2);
        TestObjectReference x3 = new TestObjectReference(2);
        x3.setObjectReference(refX3);
        refX3.setObjectReference(x3);

        assertTrue(x1.equals(x2));
        assertNull(EqualsBuilder.getRegistry());
        assertFalse(x1.equals(x3));
        assertNull(EqualsBuilder.getRegistry());
        assertFalse(x2.equals(x3));
        assertNull(EqualsBuilder.getRegistry());
    }

    static class TestObjectReference {
        @SuppressWarnings("unused")
        private TestObjectReference reference;
        @SuppressWarnings("unused")
        private TestObject one;

        public TestObjectReference(int one) {
            this.one = new TestObject(one);
        }

        public void setObjectReference(TestObjectReference reference) {
            this.reference = reference;
        }

        @Override
        public boolean equals(Object obj) {
            return EqualsBuilder.reflectionEquals(this, obj);
        }
    }
```