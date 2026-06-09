# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `bed6b1128d2cd89651aec0ba7e41e2625df38e23`
- B: `d704c0dc70a2f861c043785822854b4a0605ac6b`
- test: `src/test/java/org/apache/commons/lang3/text/translate/NumericEntityUnescaperTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/translate/NumericEntityUnescaper.java']`
- old_test_mode: `methods`
- user_chars: `4037`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1426, 'completion_tokens': 305, 'total_tokens': 1731}`

---

- 修改 `testUnfinishedEntity`：对应生产代码文档中 “semi-colon” 改为 “semicolon”，同步更新断言失败消息；无需调整 import。

```java
@Test
public void testUnfinishedEntity() {
    // parse it
    NumericEntityUnescaper neu = new NumericEntityUnescaper(NumericEntityUnescaper.OPTION.semiColonOptional);
    String input = "Test &#x30 not test";
    String expected = "Test \u0030 not test";

    String result = neu.translate(input);
    assertEquals(expected, result, "Failed to support unfinished entities (i.e. missing semicolon)");

    // ignore it
    neu = new NumericEntityUnescaper();
    input = "Test &#x30 not test";
    expected = input;

    result = neu.translate(input);
    assertEquals(expected, result, "Failed to ignore unfinished entities (i.e. missing semicolon)");

    // fail it
    final NumericEntityUnescaper failingNeu =
            new NumericEntityUnescaper(NumericEntityUnescaper.OPTION.errorIfNoSemiColon);
    final String failingInput = "Test &#x30 not test";
    assertThrows(IllegalArgumentException.class, () -> failingNeu.translate(failingInput));
}
```