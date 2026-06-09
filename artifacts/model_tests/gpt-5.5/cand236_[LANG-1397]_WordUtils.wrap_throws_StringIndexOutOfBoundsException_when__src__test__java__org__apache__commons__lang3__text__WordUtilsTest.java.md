# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `bd4066eba88a772c06394d818d87aedca8bea53c`
- B: `09ef69c5b51115300da6df43690cd455d83c8027`
- test: `src/test/java/org/apache/commons/lang3/text/WordUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/WordUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `23962`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6294, 'completion_tokens': 207, 'total_tokens': 6501}`

---

- 新增 `testLANG1397`：生产代码修复 `wrapLength == Integer.MAX_VALUE` 时 `offset + wrapLength + 1` 整型溢出导致的 `StringIndexOutOfBoundsException`，因此补充回归测试覆盖该场景；无需调整 import。

```java
    @Test
    public void testLANG1397() throws Exception {
        // Prior to fix, this was throwing StringIndexOutOfBoundsException
        WordUtils.wrap("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa "
            + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa "
            + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", Integer.MAX_VALUE);
    }
```