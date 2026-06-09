# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `b0bcf4f60a1e92480d78e44e3fda6e42cfc1b207`
- B: `695342cb1cef42f30fd1a8496f181c92b21ae82d`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `25566`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6661, 'completion_tokens': 2096, 'total_tokens': 8757, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1637}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 6277}`

---

- 修改 `@Test testExceptions()` 方法：在原有异常测试之后追加两个 `try-catch` 块，分别验证当 `numbers=true` 且 `end <= 48` 时以及当 `letters=true` 且 `end <= 65` 时抛出 `IllegalArgumentException`，与生产代码新增的入参校验逻辑对齐。

```java
    @Test
    public void testExceptions() {
        final char[] DUMMY = new char[]{'a'}; // valid char array
        try {
            RandomStringUtils.random(-1);
            fail();
        } catch (final IllegalArgumentException ex) {}
        try {
            RandomStringUtils.random(-1, true, true);
            fail();
        } catch (final IllegalArgumentException ex) {}
        try {
            RandomStringUtils.random(-1, DUMMY);
            fail();
        } catch (final IllegalArgumentException ex) {}
        try {
            RandomStringUtils.random(1, new char[0]); // must not provide empty array => IAE
            fail();
        } catch (final IllegalArgumentException ex) {}
        try {
            RandomStringUtils.random(-1, "");
            fail();
        } catch (final IllegalArgumentException ex) {}
        try {
            RandomStringUtils.random(-1, (String)null);
            fail();
        } catch (final IllegalArgumentException ex) {}
        try {
            RandomStringUtils.random(-1, 'a', 'z', false, false);
            fail();
        } catch (final IllegalArgumentException ex) {}
        try {
            RandomStringUtils.random(-1, 'a', 'z', false, false, DUMMY);
            fail();
        } catch (final IllegalArgumentException ex) {}
        try {
            RandomStringUtils.random(-1, 'a', 'z', false, false, DUMMY, new Random());
            fail();
        } catch (final IllegalArgumentException ex) {}
        try {
            RandomStringUtils.random(8, 32, 48, false, true);
            fail();
        } catch (final IllegalArgumentException ex) {}
        try {
            RandomStringUtils.random(8, 32, 65, true, false);
            fail();
        } catch (final IllegalArgumentException ex) {}
    }
```