# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `8e7ea70a33ecb8db5207849ea6371b4a5a8ffd26`
- B: `aeb6f86bcdec061ee9c6be96066fa19c56523490`
- test: `src/test/java/org/apache/commons/lang3/builder/EqualsBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/EqualsBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `48132`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 13178, 'completion_tokens': 2075, 'total_tokens': 15253, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1740}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 12794}`

---

- 新增 @Test 方法 `testToEqualsExclude`，验证反射比较时 `@EqualsExclude` 注解能正确排除字段。
- 新增静态内部类 `TestObjectEqualsExclude`，用于上述测试方法。
- 需要新增 import `org.apache.commons.lang3.builder.EqualsExclude`。

```java
// IMPORTS_START
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;

import java.util.Arrays;

import org.apache.commons.lang3.builder.EqualsExclude;
import org.junit.Test;
// IMPORTS_END

    static class TestObjectEqualsExclude {
        @EqualsExclude
        private int a;
        private int b;

        public TestObjectEqualsExclude(int a, int b) {
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