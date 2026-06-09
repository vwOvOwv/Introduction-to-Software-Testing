# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `8c1153d371d4498677605b847f8bfb0e0e743fd5`
- B: `36c4cc67a17b51256096f0a33427071b3cc1194e`
- test: `src/test/java/org/apache/commons/lang3/StreamsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Streams.java']`
- old_test_mode: `methods`
- user_chars: `10235`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2880, 'completion_tokens': 1018, 'total_tokens': 3898}`

---

- 修改 `testSimpleStreamMap`：对照测试 diff，将 `map((s) -> ...)` 更新为 `map(s -> ...)`；无需调整 import。
- 修改 `testSimpleStreamMapFailing`：对照测试 diff，将 `map((s) -> ...)` 更新为 `map(s -> ...)`；无需调整 import。
- 修改 `testSimpleStreamForEach`：对照测试 diff，将 `forEach((s) -> ...)` 更新为 `forEach(s -> ...)`；无需调整 import。
- 修改 `testSimpleStreamFilter`：对照测试 diff，将 `map((s) -> ...)` 和 `filter((i) -> ...)` 更新为无括号 lambda；无需调整 import。
- 修改 `testSimpleStreamFilterFailing`：对照测试 diff，将多处 `map((s) -> ...)` 更新为 `map(s -> ...)`；无需调整 import。

```java
@Test
void testSimpleStreamMap() {
    final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");
    final List<Integer> output = Functions.stream(input).map(s -> Integer.valueOf(s)).collect(Collectors.toList());
    assertEquals(6, output.size());
    for (int i = 0;  i < 6;  i++) {
        assertEquals(i+1, output.get(i).intValue());
    }
}

@Test
void testSimpleStreamMapFailing() {
    final List<String> input = Arrays.asList("1", "2", "3", "4 ", "5", "6");
    try {
        Functions.stream(input).map(s -> Integer.valueOf(s)).collect(Collectors.toList());
        fail("Expected Exception");
    } catch (final NumberFormatException nfe) {
        assertEquals("For input string: \"4 \"", nfe.getMessage());
    }
}

@Test
void testSimpleStreamForEach() {
    final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");
    final List<Integer> output = new ArrayList<>();
    Functions.stream(input).forEach(s -> output.add(Integer.valueOf(s)));
    assertEquals(6, output.size());
    for (int i = 0;  i < 6;  i++) {
        assertEquals(i+1, output.get(i).intValue());
    }
}

@Test
void testSimpleStreamFilter() {
    final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");
    final List<Integer> output = Functions.stream(input)
            .map(s -> Integer.valueOf(s))
            .filter(i -> {
                return i.intValue() %2 == 0;
            })
            .collect(Collectors.toList());
    assertEvenNumbers(output);
}

@Test
void testSimpleStreamFilterFailing() {
    final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");
    final List<Integer> output = Functions.stream(input)
            .map(s -> Integer.valueOf(s))
            .filter(asIntPredicate(null))
            .collect(Collectors.toList());
    assertEvenNumbers(output);

    output.clear();
    final IllegalArgumentException iae = new IllegalArgumentException("Invalid argument: " + 5);
    try {
        Functions.stream(input)
                .map(s -> Integer.valueOf(s))
                .filter(asIntPredicate(iae))
                .collect(Collectors.toList());
        fail("Expected Exception");
    } catch (final IllegalArgumentException e) {
        assertSame(iae, e);
    }

    output.clear();
    final OutOfMemoryError oome = new OutOfMemoryError();
    try {
        Functions.stream(input)
                .map(s -> Integer.valueOf(s))
                .filter(asIntPredicate(oome))
                .collect(Collectors.toList());
        fail("Expected Exception");
    } catch (final Throwable t) {
        assertSame(oome, t);
    }

    output.clear();
    final SAXException se = new SAXException();
    try {
        Functions.stream(input)
                .map(s -> Integer.valueOf(s))
                .filter(asIntPredicate(se))
                .collect(Collectors.toList());
        fail("Expected Exception");
    } catch (final UndeclaredThrowableException t) {
        assertSame(se, t.getCause());
    }
}
```