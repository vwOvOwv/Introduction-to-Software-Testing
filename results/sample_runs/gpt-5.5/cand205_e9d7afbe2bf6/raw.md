# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `94b3784fdec5d0e9d63e4aec6772144b68283790`
- B: `e9d7afbe2bf667167614869c7ea10e91f96ffceb`
- test: `src/test/java/org/apache/commons/lang3/StringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/StringUtils.java']`
- old_test_mode: `methods`
- user_chars: `8137`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2493, 'completion_tokens': 798, 'total_tokens': 3291}`

---

- 修改 `testWrapIfMissing_StringChar`：生产代码在字符串已被字符完整包裹时直接返回原对象，因此将对应断言改为 `assertSame` 并补充已完整包裹的非单字符用例。
- 修改 `testWrapIfMissing_StringString`：生产代码在字符串已被字符串完整包裹时直接返回原对象，因此将对应断言改为 `assertSame` 并补充多字符包裹串用例。
- 不需要调整 import。

```java
@Test
public void testWrapIfMissing_StringChar() {
    assertNull(StringUtils.wrapIfMissing(null, CharUtils.NUL));
    assertNull(StringUtils.wrapIfMissing(null, '1'));

    assertEquals("", StringUtils.wrapIfMissing("", CharUtils.NUL));
    assertEquals("xabx", StringUtils.wrapIfMissing("ab", 'x'));
    assertEquals("\"ab\"", StringUtils.wrapIfMissing("ab", '\"'));
    assertEquals("\"ab\"", StringUtils.wrapIfMissing("\"ab\"", '\"'));
    assertEquals("'ab'", StringUtils.wrapIfMissing("ab", '\''));
    assertEquals("'abcd'", StringUtils.wrapIfMissing("'abcd'", '\''));
    assertEquals("'\"abcd\"'", StringUtils.wrapIfMissing("\"abcd\"", '\''));
    assertEquals("\"'abcd'\"", StringUtils.wrapIfMissing("'abcd'", '\"'));
    assertEquals("/x/", StringUtils.wrapIfMissing("x", '/'));
    assertEquals("/x/y/z/", StringUtils.wrapIfMissing("x/y/z", '/'));
    assertEquals("/x/y/z/", StringUtils.wrapIfMissing("/x/y/z", '/'));
    assertEquals("/x/y/z/", StringUtils.wrapIfMissing("x/y/z/", '/'));

    assertSame("/", StringUtils.wrapIfMissing("/", '/'));
    assertSame("/x/", StringUtils.wrapIfMissing("/x/", '/'));
}

@Test
public void testWrapIfMissing_StringString() {
    assertNull(StringUtils.wrapIfMissing(null, "\0"));
    assertNull(StringUtils.wrapIfMissing(null, "1"));

    assertEquals("", StringUtils.wrapIfMissing("", "\0"));
    assertEquals("xabx", StringUtils.wrapIfMissing("ab", "x"));
    assertEquals("\"ab\"", StringUtils.wrapIfMissing("ab", "\""));
    assertEquals("\"ab\"", StringUtils.wrapIfMissing("\"ab\"", "\""));
    assertEquals("'ab'", StringUtils.wrapIfMissing("ab", "\'"));
    assertEquals("'abcd'", StringUtils.wrapIfMissing("'abcd'", "\'"));
    assertEquals("'\"abcd\"'", StringUtils.wrapIfMissing("\"abcd\"", "\'"));
    assertEquals("\"'abcd'\"", StringUtils.wrapIfMissing("'abcd'", "\""));
    assertEquals("/x/", StringUtils.wrapIfMissing("x", "/"));
    assertEquals("/x/y/z/", StringUtils.wrapIfMissing("x/y/z", "/"));
    assertEquals("/x/y/z/", StringUtils.wrapIfMissing("/x/y/z", "/"));
    assertEquals("/x/y/z/", StringUtils.wrapIfMissing("x/y/z/", "/"));
    assertEquals("/", StringUtils.wrapIfMissing("/", "/"));
    assertEquals("ab/ab", StringUtils.wrapIfMissing("/", "ab"));

    assertSame("ab/ab", StringUtils.wrapIfMissing("ab/ab", "ab"));
    assertSame("//x//", StringUtils.wrapIfMissing("//x//", "//"));
}
```