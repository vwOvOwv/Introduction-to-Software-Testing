# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `d7e927deffc5c687c1fb8c7f10bed571a91e420f`
- B: `6f2c93ceeecc48f4eca2c52345a7bf33329211c1`
- test: `src/test/java/org/apache/commons/lang3/math/NumberUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/math/NumberUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `100482`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 26603, 'completion_tokens': 117, 'total_tokens': 26720}`

---

- 新增 `testInvalidNumber`：覆盖 `createNumber` 中指数位置等于或早于小数点时应抛出 `NumberFormatException` 的新校验逻辑；无需调整 import。

```java
    @Test
    public void testInvalidNumber() {
        assertThrows(NumberFormatException.class, () -> NumberUtils.createNumber("E123e.3"));
    }
```