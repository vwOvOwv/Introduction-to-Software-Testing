# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `26e41e01993211c6c121099c37416dad20b25e3d`
- B: `6a65b76f2ab90cad2c297ff0d9f747ebb982e515`
- test: `src/test/java/org/apache/commons/lang3/math/NumberUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/math/NumberUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `94052`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 25251, 'completion_tokens': 164, 'total_tokens': 25415}`

---

- 修改 `testInvalidNumber`：生产代码 `getMantissa` 现在会在仅有符号、无法取得 mantissa 时抛出 `NumberFormatException`，因此为 `NumberUtils.createNumber("-")` 增加异常断言。
- import 无需调整：现有测试已静态导入 `assertThrows`。

```java
    @Test
    public void testInvalidNumber() {
        assertThrows(NumberFormatException.class, () -> NumberUtils.createNumber("E123e.3"));
        assertThrows(NumberFormatException.class, () -> NumberUtils.createNumber("-"));
    }
```