# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `8e7ea70a33ecb8db5207849ea6371b4a5a8ffd26`
- B: `aeb6f86bcdec061ee9c6be96066fa19c56523490`
- test: `src/test/java/org/apache/commons/lang3/builder/EqualsBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/EqualsBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `48132`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 12864, 'completion_tokens': 382, 'total_tokens': 13246}`

---

- 新增 `testToEqualsExclude`，对应生产代码 `reflectionAppend` 新增跳过 `@EqualsExclude` 注解字段的逻辑，验证被注解字段差异不影响反射相等、未注解字段差异仍不相等。
- 新增测试辅助内部类 `TestObjectEqualsExclude`，用于提供一个带 `@EqualsExclude` 字段和一个普通字段的对象；无需调整 import，因为 `EqualsExclude` 与测试类在同一 package 下。

```java
    static class TestObjectEqualsExclude {
        @EqualsExclude
        private int a;
        private int b;

        public TestObjectEqualsExclude(final int a, final int b) {
            this.a = a;
            this.b = b;
        }

        public int getA() {
            return a;
        }

        public int getB() {
            return b;
        }
    }

    @Test
    public void testToEqualsExclude() {
        TestObjectEqualsExclude one = new TestObjectEqualsExclude(1, 2);
        TestObjectEqualsExclude two = new TestObjectEqualsExclude(1, 3);

        assertFalse(EqualsBuilder.reflectionEquals(one, two));

        one = new TestObjectEqualsExclude(1, 2);
        two = new TestObjectEqualsExclude(2, 2);

        assertTrue(EqualsBuilder.reflectionEquals(one, two));
    }
```