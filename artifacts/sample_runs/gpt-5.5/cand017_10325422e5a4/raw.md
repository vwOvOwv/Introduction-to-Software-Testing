# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e2dbe55d56bd6c1209276050f527d36717e33e1d`
- B: `10325422e5a4735aa87a4d47bdb377e09fe963d2`
- test: `src/test/java/org/apache/commons/lang3/text/StrBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/StrBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `73519`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 18059, 'completion_tokens': 521, 'total_tokens': 18580}`

---

- 修改 `testReplaceAll_StrMatcher_String`：生产代码在 `replaceImpl` 循环内重新读取 `buffer`，因此新增覆盖“匹配替换后缓冲区扩容/重分配仍能继续匹配后续位置”的断言；import 无需调整。

```java
@Test
public void testReplaceAll_StrMatcher_String() {
    StrBuilder sb = new StrBuilder("abcbccba");
    sb.replaceAll((StrMatcher) null, null);
    assertEquals("abcbccba", sb.toString());
    sb.replaceAll((StrMatcher) null, "anything");
    assertEquals("abcbccba", sb.toString());
    sb.replaceAll(StrMatcher.noneMatcher(), null);
    assertEquals("abcbccba", sb.toString());
    sb.replaceAll(StrMatcher.noneMatcher(), "anything");
    assertEquals("abcbccba", sb.toString());

    sb.replaceAll(StrMatcher.charMatcher('x'), "y");
    assertEquals("abcbccba", sb.toString());
    sb.replaceAll(StrMatcher.charMatcher('a'), "d");
    assertEquals("dbcbccbd", sb.toString());
    sb.replaceAll(StrMatcher.charMatcher('d'), null);
    assertEquals("bcbccb", sb.toString());
    sb.replaceAll(StrMatcher.stringMatcher("cb"), "-");
    assertEquals("b-c-", sb.toString());

    sb = new StrBuilder("abcba");
    sb.replaceAll(StrMatcher.charMatcher('b'), "xbx");
    assertEquals("axbxcxbxa", sb.toString());

    sb = new StrBuilder("bb");
    sb.replaceAll(StrMatcher.charMatcher('b'), "xbx");
    assertEquals("xbxxbx", sb.toString());

    sb = new StrBuilder("A1-A2A3-A4");
    sb.replaceAll(A_NUMBER_MATCHER, "***");
    assertEquals("***-******-***", sb.toString());

    sb = new StrBuilder("Dear X, hello X.");
    sb.replaceAll(StrMatcher.stringMatcher("X"), "012345678901234567");
    assertEquals("Dear 012345678901234567, hello 012345678901234567.", sb.toString());
}
```