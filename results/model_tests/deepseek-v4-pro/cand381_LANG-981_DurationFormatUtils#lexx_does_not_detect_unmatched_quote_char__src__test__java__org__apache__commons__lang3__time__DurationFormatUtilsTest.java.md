# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `8d360ae70732ae26d961f76da5a98c44ac5931c6`
- B: `aadd8e172eb22fb593fbaa454075677656fad111`
- test: `src/test/java/org/apache/commons/lang3/time/DurationFormatUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/DurationFormatUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `34861`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 10085, 'completion_tokens': 790, 'total_tokens': 10875, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 694}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 9701}`

---

- 新增 `testLANG981` 测试方法，用于验证当 lexx 方法的格式字符串中含有未闭合的单引号时，能正确抛出 `IllegalArgumentException`；无需修改 import 或删除其他测试。

```java
    @Test(expected = IllegalArgumentException.class)
    public void testLANG981() { // unmatched quote char in lexx
        DurationFormatUtils.lexx("'yMdHms''S");
    }
```