# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `8c1153d371d4498677605b847f8bfb0e0e743fd5`
- B: `36c4cc67a17b51256096f0a33427071b3cc1194e`
- test: `src/test/java/org/apache/commons/lang3/StreamsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Streams.java']`
- old_test_mode: `methods`
- user_chars: `10235`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2895, 'completion_tokens': 2695, 'total_tokens': 5590, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1558}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2511}`

---

- 修改 @Test 方法 `testSimpleStreamMap`：移除 map lambda 参数括号 `(s)` 为 `s`，与生产代码 diff 风格一致。
- 修改 @Test 方法 `testSimpleStreamMapFailing`：移除 map lambda 参数括号 `(s)` 为 `s`。
- 修改 @Test 方法 `testSimpleStreamForEach`：移除 forEach lambda 参数括号 `(s)` 为 `s`。
- 修改辅助方法 `asIntConsumer`：移除 lambda 参数括号 `(s)` 为 `s`。
- 修改 @Test 方法 `testSimpleStreamFilter`：移除 map lambda 参数括号 `(s)` 为 `s`，移除 filter lambda 参数括号 `(i)` 为 `i`。
- 修改辅助方法 `asIntPredicate`：移除 lambda 参数括号 `(i)` 为 `i`。
- 修改 @Test 方法 `testSimpleStreamFilterFailing`：移除所有 map lambda 参数括号 `(s)` 为 `s`。
- import 无需调整。

```java
// IMPORTS_START
// IMPORTS_END
// 无需删除任何测试方法，以下为修改后的方法

@Test
void testSimpleStreamMap() {
    final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");
    final List<Integer> output = Functions.stream(input).map(s -> Integer.valueOf(s)).collect(Collectors.toList());
    assertEquals(6, output.size());
    for (int i = 0; i < 6; i++) {
        assertEquals(i + 1, output.get(i).intValue());
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
    for (int i = 0; i < 6; i++) {
        assertEquals(i + 1, output.get(i).intValue());
    }
}

protected <T extends Throwable> FailableConsumer<String, T> asIntConsumer(final T pThrowable) {
    return s -> {
        final Integer i = Integer.valueOf(s);
        if (i.intValue() == 4) {
            throw pThrowable;
        }
    };
}

@Test
void testSimpleStreamFilter() {
    final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");
    final List<Integer> output = Functions.stream(input)
            .map(s -> Integer.valueOf(s))
            .filter(i -> {
                return i.intValue() % 2 == 0;
            })
            .collect(Collectors.toList());
    assertEvenNumbers(output);
}

protected <T extends Throwable> FailablePredicate<Integer, T> asIntPredicate(final T pThrowable) {
    return i -> {
        if (i.intValue() == 5) {
            if (pThrowable != null) {
                throw pThrowable;
            }
        }
        return i.intValue() % 2 == 0;
    };
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