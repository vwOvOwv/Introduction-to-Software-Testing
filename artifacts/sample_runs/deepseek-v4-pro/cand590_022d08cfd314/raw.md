# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `4d7a616ccaf6c4a2aef171999f04c71d3749313d`
- B: `022d08cfd31475073c664da109ad50bfe9539d82`
- test: `src/test/java/org/apache/commons/lang3/exception/ContextedExceptionTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/exception/ContextedException.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `14181`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3607, 'completion_tokens': 3030, 'total_tokens': 6637, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2231}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 3223}`

---

- 删除老测试方法 `testGetMessage`，因为生产代码变更删除了它（测试 diff 中已移除）。
- 修改 `testAddValue` 方法以匹配新的 `addValue` 行为：不再添加 faulty object，改为仅添加 4 个普通值；并验证重复 label 的索引机制；以及上下文消息的尾部合并。
- 新增 `testReplaceValue` 方法，验证新增的 `replaceValue` 方法：替换已有 label 的值，label 集合大小保持不变，且不破坏上下文消息的结构。
- 无需修改 import，现有导包已足够。

```java
// DELETE_TESTS_START
testGetMessage
// DELETE_TESTS_END

    public void testAddValue() {
        contextedException = new ContextedException(new Exception(TEST_MESSAGE))
        .addValue("test1", null)
        .addValue("test2", "some value")
        .addValue("test Date", new Date())
        .addValue("test Nbr", new Integer(5));
        
        String message = contextedException.getMessage();
        assertTrue(message.indexOf(TEST_MESSAGE)>=0);
        assertTrue(message.indexOf("test1")>=0);
        assertTrue(message.indexOf("test2")>=0);
        assertTrue(message.indexOf("test Date")>=0);
        assertTrue(message.indexOf("test Nbr")>=0);
        assertTrue(message.indexOf("some value")>=0);
        assertTrue(message.indexOf("5")>=0);
        
        assertTrue(contextedException.getValue("test1") == null);
        assertTrue(contextedException.getValue("test2").equals("some value"));
        
        assertTrue(contextedException.getLabelSet().size() == 4);
        assertTrue(contextedException.getLabelSet().contains("test1"));
        assertTrue(contextedException.getLabelSet().contains("test2"));
        assertTrue(contextedException.getLabelSet().contains("test Date"));
        assertTrue(contextedException.getLabelSet().contains("test Nbr"));

        contextedException.addValue("test2", "different value");
        assertTrue(contextedException.getLabelSet().size() == 5);
        assertTrue(contextedException.getLabelSet().contains("test2"));
        assertTrue(contextedException.getLabelSet().contains("test2[1]"));
        
        String contextMessage = contextedException.getFormattedExceptionMessage(null);
        assertTrue(contextMessage.indexOf(TEST_MESSAGE) == -1);
        assertTrue(contextedException.getMessage().endsWith(contextMessage));
    }

    public void testReplaceValue() {
        contextedException = new ContextedException(new Exception(TEST_MESSAGE))
        .addValue("test Poorly written obj", new ObjectWithFaultyToString());
        
        String message = contextedException.getMessage();
        assertTrue(message.indexOf(TEST_MESSAGE)>=0);
        assertTrue(message.indexOf("test Poorly written obj")>=0);
        assertTrue(message.indexOf("Crap")>=0);
        
        assertTrue(contextedException.getValue("crap") == null);
        assertTrue(contextedException.getValue("test Poorly written obj") instanceof ObjectWithFaultyToString);
        
        assertTrue(contextedException.getLabelSet().size() == 1);
        assertTrue(contextedException.getLabelSet().contains("test Poorly written obj"));
        
        assertTrue(!contextedException.getLabelSet().contains("crap"));

        contextedException.replaceValue("test Poorly written obj", "replacement");

        assertTrue(contextedException.getLabelSet().size() == 1);

        String contextMessage = contextedException.getFormattedExceptionMessage(null);
        assertTrue(contextMessage.indexOf(TEST_MESSAGE) == -1);
        assertTrue(contextedException.getMessage().endsWith(contextMessage));
    }
```