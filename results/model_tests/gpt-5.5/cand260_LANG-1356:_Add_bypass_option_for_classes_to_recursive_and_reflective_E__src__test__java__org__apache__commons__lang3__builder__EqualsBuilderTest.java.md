# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `2ce40494073aa4e9bdcba4c39d24727b7141d227`
- B: `2e9f3a80146262511ca7bcdd3411f095dff4951d`
- test: `src/test/java/org/apache/commons/lang3/builder/EqualsBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/EqualsBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `61308`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 15749, 'completion_tokens': 700, 'total_tokens': 16449}`

---

- 新增辅助内部类 `TestRecursiveGenericObject`，对应生产代码新增递归模式下 `bypassReflectionClasses` 对泛型字段比较路径的覆盖。
- 新增 `testObjectRecursiveGenericInteger`，验证递归比较泛型对象中 `Integer` 字段时仍按值递归比较。
- 新增 `testObjectRecursiveGenericString`，验证默认绕过 `String.class` 反射比较后，`String` 的延迟 `hashCode` 缓存字段不会导致递归比较误判。
- 不需要调整 import，新增测试仅使用现有 `@Test`、`assertTrue`、`assertFalse`。

```java
    static class TestRecursiveGenericObject<T> {

        private final T a;

        TestRecursiveGenericObject(final T a) {
            this.a = a;
        }

        public T getA() {
            return a;
        }
    }

    @Test
    public void testObjectRecursiveGenericInteger() {
        final TestRecursiveGenericObject<Integer> o1_a = new TestRecursiveGenericObject<Integer>(1);
        final TestRecursiveGenericObject<Integer> o1_b = new TestRecursiveGenericObject<Integer>(1);
        final TestRecursiveGenericObject<Integer> o2 = new TestRecursiveGenericObject<Integer>(2);

        assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_a, o1_b).isEquals());
        assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_b, o1_a).isEquals());

        assertFalse(new EqualsBuilder().setTestRecursive(true).append(o1_b, o2).isEquals());
    }

    @Test
    public void testObjectRecursiveGenericString() {
        // Note: Do not use literals, because string literals are always mapped by same object (internal() of String))!
        String s1_a = String.valueOf(1);
        final TestRecursiveGenericObject<String> o1_a = new TestRecursiveGenericObject<String>(s1_a);
        final TestRecursiveGenericObject<String> o1_b = new TestRecursiveGenericObject<String>(String.valueOf(1));
        final TestRecursiveGenericObject<String> o2 = new TestRecursiveGenericObject<String>(String.valueOf(2));

        // To trigger bug reported in LANG-1356, call hashCode only on string in instance o1_a
        s1_a.hashCode();

        assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_a, o1_b).isEquals());
        assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_b, o1_a).isEquals());

        assertFalse(new EqualsBuilder().setTestRecursive(true).append(o1_b, o2).isEquals());
    }
```