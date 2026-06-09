# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cbeb45b243897dd974978ac339c40c2915b638d1`
- B: `bf6ee5c56eb32bb572c240d765d542c048ec9565`
- test: `src/test/java/org/apache/commons/lang3/text/ExtendedMessageFormatTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/ExtendedMessageFormat.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `33228`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7570, 'completion_tokens': 369, 'total_tokens': 7939}`

---

- 新增 `testEscapedBraces_LANG_948`：覆盖 `ExtendedMessageFormat` 在 B 中调整引号解析后，对被单引号转义的大括号和双单引号转义场景的格式化行为。
- import 无需调整：现有 `org.junit.Test` 与 `assertEquals` 静态导入已满足新增测试。

```java
    /**
     * Test Bug LANG-948 - Exception while using ExtendedMessageFormat and escaping braces
     */
    @Test
    public void testEscapedBraces_LANG_948() {
        // message without placeholder because braces are escaped by quotes 
        final String pattern = "Message without placeholders '{}'";
        final ExtendedMessageFormat emf = new ExtendedMessageFormat(pattern, registry);
        assertEquals("Message without placeholders {}", emf.format(new Object[] {"DUMMY"}));

        // message with placeholder because quotes are escaped by quotes 
        final String pattern2 = "Message with placeholder ''{0}''";
        final ExtendedMessageFormat emf2 = new ExtendedMessageFormat(pattern2, registry);
        assertEquals("Message with placeholder 'DUMMY'", emf2.format(new Object[] {"DUMMY"}));
    }
```