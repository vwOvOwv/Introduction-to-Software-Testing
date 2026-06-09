# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `51ad9f989dda1e5c7f9487d1477c82ea003a864a`
- B: `ff415c8f8f213d40a19f8dc9ac037050ef497bf8`
- test: `src/test/java/org/apache/commons/lang3/stream/StreamsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/stream/Streams.java']`
- old_test_mode: `methods`
- user_chars: `13310`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3593, 'completion_tokens': 4104, 'total_tokens': 7697, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2873}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 3209}`

---

- 新增测试方法：`testNullSafeStreamNotNull`、`testNullSafeStreamNull`、`testToStreamNotNull`、`testToStreamNull`，因为生产代码新增了公共方法 `Streams.nullSafeStream` 和 `Streams.toStream`，需要覆盖非空与空集合场景。
- 修改测试方法：`simpleStreamFilterFailing` 将所有流式调用从多行合并为单行（与生产代码变更无关，仅为代码风格调整）；`simpleStreamForEachFailing` 将 `SAXException` 部分的多行断言合并为单行；`testSimpleStreamFilter` 将 `filter` 与 `collect` 调用合并为单行。
- 无需删除测试方法，无需调整 import。

```java
    @Test
    public void testNullSafeStreamNotNull() {
        assertEquals(2, Streams.nullSafeStream(Arrays.asList("A", "B")).collect(Collectors.toList()).size());
        assertEquals(2, Streams.nullSafeStream(Arrays.asList(null, "A", null, "B", null)).collect(Collectors.toList()).size());
        assertEquals(0, Streams.nullSafeStream(Arrays.asList(null, null)).collect(Collectors.toList()).size());
    }

    @Test
    public void testNullSafeStreamNull() {
        final List<String> input = null;
        assertEquals(0, Streams.nullSafeStream(input).collect(Collectors.toList()).size());
    }

    @Test
    public void testToStreamNotNull() {
        assertEquals(2, Streams.toStream(Arrays.asList("A", "B")).collect(Collectors.toList()).size());
    }

    @Test
    public void testToStreamNull() {
        final List<String> input = null;
        assertEquals(0, Streams.toStream(input).collect(Collectors.toList()).size());
    }

    @TestFactory
    public Stream<DynamicTest> simpleStreamFilterFailing() {
        final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");
        final List<Integer> output = Failable.stream(input).map(Integer::valueOf).filter(asIntPredicate(null)).collect(Collectors.toList());
        assertEvenNumbers(output);

        return Stream.of(

            dynamicTest("IllegalArgumentException", () -> {
                final IllegalArgumentException iae = new IllegalArgumentException("Invalid argument: " + 5);
                final Executable testMethod = () -> Failable.stream(input).map(Integer::valueOf).filter(asIntPredicate(iae)).collect(Collectors.toList());
                final IllegalArgumentException thrown = assertThrows(IllegalArgumentException.class, testMethod);
                assertThat(thrown.getMessage(), is(equalTo("Invalid argument: " + 5)));
            }),

            dynamicTest("OutOfMemoryError", () -> {
                final OutOfMemoryError oome = new OutOfMemoryError();
                final Executable testMethod = () -> Failable.stream(input).map(Integer::valueOf).filter(asIntPredicate(oome)).collect(Collectors.toList());
                final OutOfMemoryError thrown = assertThrows(OutOfMemoryError.class, testMethod);
                assertThat(thrown.getMessage(), is(nullValue()));
            }),

            dynamicTest("SAXException", () -> {
                final SAXException se = new SAXException();
                final Executable testMethod = () -> Failable.stream(input).map(Integer::valueOf).filter(asIntPredicate(se)).collect(Collectors.toList());
                final UndeclaredThrowableException thrown = assertThrows(UndeclaredThrowableException.class, testMethod);
                assertAll(() -> assertThat(thrown.getMessage(), is(nullValue())), () -> assertThat(thrown.getCause(), is(equalTo(se))));
            }));
    }

    @TestFactory
    public Stream<DynamicTest> simpleStreamForEachFailing() {
        final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");

        return Stream.of(

            dynamicTest("IllegalArgumentException", () -> {
                final IllegalArgumentException ise = new IllegalArgumentException();
                final Executable testMethod = () -> Failable.stream(input).forEach(asIntConsumer(ise));
                final IllegalArgumentException thrown = assertThrows(IllegalArgumentException.class, testMethod);
                assertThat(thrown.getMessage(), is(nullValue()));
            }),

            dynamicTest("OutOfMemoryError", () -> {
                final OutOfMemoryError oome = new OutOfMemoryError();
                final Executable oomeTestMethod = () -> Failable.stream(input).forEach(asIntConsumer(oome));
                final OutOfMemoryError oomeThrown = assertThrows(OutOfMemoryError.class, oomeTestMethod);
                assertThat(oomeThrown.getMessage(), is(nullValue()));
            }),

            dynamicTest("SAXException", () -> {
                final SAXException se = new SAXException();
                final Executable seTestMethod = () -> Failable.stream(input).forEach(asIntConsumer(se));
                final UndeclaredThrowableException seThrown = assertThrows(UndeclaredThrowableException.class, seTestMethod);
                assertAll(() -> assertThat(seThrown.getMessage(), is(nullValue())), () -> assertThat(seThrown.getCause(), is(equalTo(se))));
            }));
    }

    @Test
    public void testSimpleStreamFilter() {
        final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");
        final List<Integer> output = Failable.stream(input).map(Integer::valueOf).filter(i -> (i.intValue() % 2 == 0)).collect(Collectors.toList());
        assertEvenNumbers(output);
    }
```