# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `0799f01df18c8f2d5695390cfc6db807fe019b18`
- B: `02a98515a337991f0ce05271ac90121fa204d9db`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `129007`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 31818, 'completion_tokens': 361, 'total_tokens': 32179, 'prompt_tokens_details': {'cached_tokens': 31744}}`

---

- 新增 `testRotate_StringInt`：生产代码新增 `StringUtils.rotate(String, int)`，测试需覆盖 null、空串、零位移、正/负位移以及超过长度的循环位移。
- import 无需调整：旧测试文件已有 `org.junit.Test` 与 `assertEquals` 静态导入，可直接编译新增测试。

```java
//-----------------------------------------------------------------------
@Test
public void testRotate_StringInt() {
    assertEquals(null, StringUtils.rotate(null, 1));
    assertEquals("", StringUtils.rotate("", 1));
    assertEquals("abcdefg", StringUtils.rotate("abcdefg", 0));
    assertEquals("fgabcde", StringUtils.rotate("abcdefg", 2));
    assertEquals("cdefgab", StringUtils.rotate("abcdefg", -2));
    assertEquals("abcdefg", StringUtils.rotate("abcdefg", 7));
    assertEquals("abcdefg", StringUtils.rotate("abcdefg", -7));
    assertEquals("fgabcde", StringUtils.rotate("abcdefg", 9));
    assertEquals("cdefgab", StringUtils.rotate("abcdefg", -9));
    assertEquals("efgabcd", StringUtils.rotate("abcdefg", 17));
    assertEquals("defgabc", StringUtils.rotate("abcdefg", -17));
}
```