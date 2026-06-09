# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `4d7a616ccaf6c4a2aef171999f04c71d3749313d`
- B: `022d08cfd31475073c664da109ad50bfe9539d82`
- test: `src/test/java/org/apache/commons/lang3/exception/ContextedExceptionTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/exception/ContextedException.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `14181`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3604, 'completion_tokens': 1059, 'total_tokens': 4663}`

---

- 修改 `testAddValue`：对应生产代码中 `addValue` 对重复 label 改为追加索引的行为，将“故障 toString 对象替换”场景拆出，并新增对 `test2[1]` 的断言。
- 新增 `testReplaceValue`：对应新增的 `ContextedException.replaceValue(String, Object)` 方法，验证已有 label 被替换且 label 数量不增加。
- 删除 `testGetMessage`：该测试仅委托 `testAddValue`，与更新后的行为覆盖重复。
- import 无需调整。

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