# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `4796a0a79259bbaf4fdab61dd158cb658e6a8d44`
- B: `b5749b4f54b30c0c2050e456c12cfcf516434f13`
- test: `src/test/java/org/apache/commons/lang3/builder/HashCodeBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/HashCodeBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `28954`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 8491, 'completion_tokens': 1078, 'total_tokens': 9569}`

---

- 新增 `testNonreflectionObjectCycle`：覆盖 `HashCodeBuilder.append(Object)` 对非反射 `hashCode()` 中对象循环引用的注册/反注册逻辑，验证不会递归溢出且 registry 被清理；无需调整 import。
- 不修改或删除现有 `@Test` 方法；生产 diff 对包装类型和循环检测的变更不影响现有 import。

```java
    /**
     * Test Objects pointing to each other when <code>append()</code> methods are used on <code>HashCodeBuilder</code> instance.
     */
    @Test
    public void testNonreflectionObjectCycle() {
        class NonreflectionTestCycleA {
            int index = 20;
            String name = "NonreflectionTestCycleA";
            Object b;

            @Override
            public int hashCode() {
                final HashCodeBuilder builder = new HashCodeBuilder();
                builder.append(index);
                builder.append(name);
                builder.append(b);
                return builder.toHashCode();
            }
        }

        class NonreflectionTestCycleB {
            int index = 21;
            String name = "NonreflectionTestCycleB";
            Object a;

            @Override
            public int hashCode() {
                final HashCodeBuilder builder = new HashCodeBuilder();
                builder.append(index);
                builder.append(name);
                builder.append(a);
                return builder.toHashCode();
            }
        }

        final NonreflectionTestCycleA a = new NonreflectionTestCycleA();
        final NonreflectionTestCycleB b = new NonreflectionTestCycleB();
        a.b = b;
        b.a = a;

        a.hashCode();
        assertNull(HashCodeBuilder.getRegistry());
        b.hashCode();
        assertNull(HashCodeBuilder.getRegistry());
    }
```