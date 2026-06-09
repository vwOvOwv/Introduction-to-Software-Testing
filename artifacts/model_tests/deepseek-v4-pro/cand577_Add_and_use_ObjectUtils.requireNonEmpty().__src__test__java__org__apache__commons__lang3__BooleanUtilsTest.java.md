# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `43f0424827dfcbc3a301007b5d5ca0e412473948`
- B: `ea344865514a8b75eb4e9d1a159fc8434e5bb7fa`
- test: `src/test/java/org/apache/commons/lang3/BooleanUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/BooleanUtils.java']`
- old_test_mode: `methods`
- user_chars: `11617`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3248, 'completion_tokens': 924, 'total_tokens': 4172, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 503}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2864}`

---

- 修改 `testAnd_object_nullInput`：将预期的异常类型从 `IllegalArgumentException` 改为 `NullPointerException`，以匹配生产代码变更。
- 修改 `testAnd_primitive_nullInput`：将预期的异常类型从 `IllegalArgumentException` 改为 `NullPointerException`。
- 修改 `testOr_object_nullInput`：将预期的异常类型从 `IllegalArgumentException` 改为 `NullPointerException`。
- 修改 `testOr_primitive_nullInput`：将预期的异常类型从 `IllegalArgumentException` 改为 `NullPointerException`。
- 修改 `testXor_object_nullInput`：将预期的异常类型从 `IllegalArgumentException` 改为 `NullPointerException`。
- 修改 `testXor_primitive_nullInput`：将预期的异常类型从 `IllegalArgumentException` 改为 `NullPointerException`。

```java
    @Test
    public void testAnd_object_nullInput() {
        assertThrows(NullPointerException.class, () -> BooleanUtils.and((Boolean[]) null));
    }

    @Test
    public void testAnd_primitive_nullInput() {
        assertThrows(NullPointerException.class, () -> BooleanUtils.and((boolean[]) null));
    }

    @Test
    public void testOr_object_nullInput() {
        assertThrows(NullPointerException.class, () -> BooleanUtils.or((Boolean[]) null));
    }

    @Test
    public void testOr_primitive_nullInput() {
        assertThrows(NullPointerException.class, () -> BooleanUtils.or((boolean[]) null));
    }

    @Test
    public void testXor_object_nullInput() {
        assertThrows(NullPointerException.class, () -> BooleanUtils.xor((Boolean[]) null));
    }

    @Test
    public void testXor_primitive_nullInput() {
        assertThrows(NullPointerException.class, () -> BooleanUtils.xor((boolean[]) null));
    }
```