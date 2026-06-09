# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `2fdfb4a387951bc14a4d8d5360daa45c76fea0d6`
- B: `311dc94070b4a6fd6060d24f1b26842a225821ba`
- test: `src/test/java/org/apache/commons/lang3/CharSequenceUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/CharSequenceUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `14575`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 4241, 'completion_tokens': 1533, 'total_tokens': 5774, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 844}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 3857}`

---

- 修改 `testLength_CharBuffer`、`testLength_String`、`testLength_StringBuffer`、`testLength_StringBuilder` 和 `testSubSequence` 五个测试方法的缩进格式（从 tab 改为空格），以匹配生产代码与测试代码的 whitespace 变更；无需调整 import，因为逻辑和依赖均未发生变化。

```java
public void testLength_CharBuffer() {
    Assert.assertEquals(0, CharSequenceUtils.length(CharBuffer.wrap("")));
    Assert.assertEquals(1, CharSequenceUtils.length(CharBuffer.wrap("A")));
    Assert.assertEquals(1, CharSequenceUtils.length(CharBuffer.wrap(" ")));
    Assert.assertEquals(8, CharSequenceUtils.length(CharBuffer.wrap("ABCDEFGH")));
}

public void testLength_String() {
    Assert.assertEquals(0, CharSequenceUtils.length(null));
    Assert.assertEquals(0, CharSequenceUtils.length(""));
    Assert.assertEquals(1, CharSequenceUtils.length("A"));
    Assert.assertEquals(1, CharSequenceUtils.length(" "));
    Assert.assertEquals(8, CharSequenceUtils.length("ABCDEFGH"));
}

public void testLength_StringBuffer() {
    Assert.assertEquals(0, CharSequenceUtils.length(new StringBuffer("")));
    Assert.assertEquals(1, CharSequenceUtils.length(new StringBuffer("A")));
    Assert.assertEquals(1, CharSequenceUtils.length(new StringBuffer(" ")));
    Assert.assertEquals(8, CharSequenceUtils.length(new StringBuffer("ABCDEFGH")));
}

public void testLength_StringBuilder() {
    Assert.assertEquals(0, CharSequenceUtils.length(new StringBuilder("")));
    Assert.assertEquals(1, CharSequenceUtils.length(new StringBuilder("A")));
    Assert.assertEquals(1, CharSequenceUtils.length(new StringBuilder(" ")));
    Assert.assertEquals(8, CharSequenceUtils.length(new StringBuilder("ABCDEFGH")));
}

public void testSubSequence() {
    //
    // null input
    //
    Assert.assertEquals(null, CharSequenceUtils.subSequence(null, -1));
    Assert.assertEquals(null, CharSequenceUtils.subSequence(null, 0));
    Assert.assertEquals(null, CharSequenceUtils.subSequence(null, 1));
    //
    // non-null input
    //
    Assert.assertEquals(StringUtils.EMPTY, CharSequenceUtils.subSequence(StringUtils.EMPTY, 0));
    Assert.assertEquals("012", CharSequenceUtils.subSequence("012", 0));
    Assert.assertEquals("12", CharSequenceUtils.subSequence("012", 1));
    Assert.assertEquals("2", CharSequenceUtils.subSequence("012", 2));
    Assert.assertEquals(StringUtils.EMPTY, CharSequenceUtils.subSequence("012", 3));
    //
    // Exception expected
    //
    try {
        Assert.assertEquals(null, CharSequenceUtils.subSequence(StringUtils.EMPTY, -1));
        Assert.fail("Expected " + IndexOutOfBoundsException.class.getName());
    } catch (IndexOutOfBoundsException e) {
        // Expected
    }
    try {
        Assert.assertEquals(null, CharSequenceUtils.subSequence(StringUtils.EMPTY, 1));
        Assert.fail("Expected " + IndexOutOfBoundsException.class.getName());
    } catch (IndexOutOfBoundsException e) {
        // Expected
    }
}
```