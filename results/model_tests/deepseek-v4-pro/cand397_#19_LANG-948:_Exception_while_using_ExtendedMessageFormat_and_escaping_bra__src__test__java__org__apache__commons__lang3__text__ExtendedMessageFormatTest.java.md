# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cbeb45b243897dd974978ac339c40c2915b638d1`
- B: `bf6ee5c56eb32bb572c240d765d542c048ec9565`
- test: `src/test/java/org/apache/commons/lang3/text/ExtendedMessageFormatTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/ExtendedMessageFormat.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `33228`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7904, 'completion_tokens': 3562, 'total_tokens': 11466, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 3304}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 7520}`

---

- 新增 @Test 方法 `testEscapedBraces_LANG_948`，对应生产代码中引号解析逻辑变更后对大括号转义的支持。
- 无需删除或修改已有的 @Test 方法；原测试方法在变更后均可通过编译并断言。
- 无需调整 import 语句，现有 import 已满足新测试所需类型。

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