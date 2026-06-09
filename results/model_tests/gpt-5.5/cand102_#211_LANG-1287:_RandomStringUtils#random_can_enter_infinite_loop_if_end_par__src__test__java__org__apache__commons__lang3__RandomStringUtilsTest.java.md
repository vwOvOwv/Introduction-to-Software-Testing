# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `b0bcf4f60a1e92480d78e44e3fda6e42cfc1b207`
- B: `695342cb1cef42f30fd1a8496f181c92b21ae82d`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `25566`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6533, 'completion_tokens': 518, 'total_tokens': 7051}`

---

- 修改 `testExceptions`：生产代码在 `chars == null` 且请求数字/字母但 `end` 不足以覆盖 `'0'`/`'A'` 时新增 `IllegalArgumentException`，因此在旧异常测试中补充两个对应断言。
- import 无需调整：新增断言仍使用已有的 `fail`、`RandomStringUtils` 和 `IllegalArgumentException`。

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