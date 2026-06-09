# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `b900dce2001366a56f139514b781864ddc20e158`
- B: `e6ae7561a05b1356625563cd868dce8a0fa4ddae`
- test: `src/test/java/org/apache/commons/lang3/stream/StreamsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/stream/Streams.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `19834`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 5181, 'completion_tokens': 251, 'total_tokens': 5432}`

---

- 新增 `testInstanceOfStream`：生产代码新增 `Streams.instancesOf(Class, Collection)`，测试需覆盖普通集合、含 `null` 集合、全 `null` 集合以及 `List<Object>` 入参场景；无需调整 import。

```java
    @Test
    public void testInstanceOfStream() {
        assertEquals(2, Streams.instancesOf(String.class, Arrays.asList("A", "B")).collect(Collectors.toList()).size());
        assertEquals(2, Streams.instancesOf(String.class, Arrays.asList(null, "A", null, "B", null)).collect(Collectors.toList()).size());
        assertEquals(0, Streams.instancesOf(String.class, Arrays.asList(null, null)).collect(Collectors.toList()).size());
        //
        List<Object> objects = Arrays.asList("A", "B");
        assertEquals(2, Streams.instancesOf(String.class, objects).collect(Collectors.toList()).size());
    }
```