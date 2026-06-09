# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `8c1a0d2ee1433681958809b4a0fede65f62936e6`
- B: `a08ec31dbf212a033953dc6916a743dccbb93e37`
- test: `src/test/java/org/apache/commons/lang3/text/WordUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/WordUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `24161`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6588, 'completion_tokens': 289, 'total_tokens': 6877, 'prompt_tokens_details': {'cached_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 143}}`

---

- 新增 `testLANG1292`：覆盖 `WordUtils.wrap` 在多段长字符串换行时不再因 `spaceToWrapAt` 偏移量错误抛出 `StringIndexOutOfBoundsException`。
- 不需要调整 import：新增测试仅使用已有的 `org.junit.Test` 和 `WordUtils`。

```java
@Test
public void testLANG1292() throws Exception {
    // Prior to fix, this was throwing StringIndexOutOfBoundsException
    WordUtils.wrap("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa "
            + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa "
            + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 70);
}
```