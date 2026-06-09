# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `724c00f0e86926e758b56bea03cdc517c475ad6a`
- B: `8fcefb4f98856998d857e90f73bb88af043ef3b8`
- test: `src/test/java/org/apache/commons/lang3/StreamsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/Streams.java']`
- old_test_mode: `methods`
- user_chars: `10987`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2954, 'completion_tokens': 1820, 'total_tokens': 4774}`

---

- 修改 `testSimpleStreamMap`：对照测试 diff，将 JUnit 测试方法可见性改为 `public`。
- 修改 `testSimpleStreamMapFailing`：对照测试 diff，将 JUnit 测试方法可见性改为 `public`。
- 修改 `testSimpleStreamForEach`：对照测试 diff，将 JUnit 测试方法可见性改为 `public`。
- 修改 `testToArray`：对照测试 diff，将 JUnit 测试方法可见性改为 `public`。
- 修改 `simpleStreamForEachFailing`：对照测试 diff，将 `@TestFactory` 方法可见性改为 `public`。
- 修改 `testSimpleStreamFilter`：对照测试 diff，将 JUnit 测试方法可见性改为 `public`。
- 修改 `simpleStreamFilterFailing`：对照测试 diff，将 `@TestFactory` 方法可见性改为 `public`。
- 不需要调整 import。

```java
@Test
public void testSimpleStreamMap() {
    final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");
    final List<Integer> output = Functions.stream(input).map(Integer::valueOf).collect(Collectors.toList());
    assertEquals(6, output.size());
    for (int i = 0; i < 6; i++) {
        assertEquals(i + 1, output.get(i).intValue());
    }
}

@Test
public void testSimpleStreamMapFailing() {
    final List<String> input = Arrays.asList("1", "2", "3", "4 ", "5", "6");
    final Executable testMethod = () -> Functions.stream(input).map(Integer::valueOf).collect(Collectors.toList());
    final NumberFormatException thrown = assertThrows(NumberFormatException.class, testMethod);
    assertEquals("For input string: \"4 \"", thrown.getMessage());
}

@Test
public void testSimpleStreamForEach() {
    final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");
    final List<Integer> output = new ArrayList<>();
    Functions.stream(input).forEach(s -> output.add(Integer.valueOf(s)));
    assertEquals(6, output.size());
    for (int i = 0; i < 6; i++) {
        assertEquals(i + 1, output.get(i).intValue());
    }
}

@Test
public void testToArray() {
    final String[] array = Arrays.asList("2", "3", "1").stream().collect(Streams.toArray(String.class));
    assertNotNull(array);
    assertEquals(3, array.length);
    assertEquals("2", array[0]);
    assertEquals("3", array[1]);
    assertEquals("1", array[2]);
}

@TestFactory
public Stream<DynamicTest> simpleStreamForEachFailing() {
    final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");

    return Stream.of(

            dynamicTest("IllegalArgumentException", () -> {
                final IllegalArgumentException ise = new IllegalArgumentException();
                final Executable testMethod = () -> Functions.stream(input)
                        .forEach(asIntConsumer(ise));
                final IllegalArgumentException thrown = assertThrows(IllegalArgumentException.class, testMethod);
                assertThat(thrown.getMessage(), is(nullValue()));
            }),

            dynamicTest("OutOfMemoryError", () -> {
                final OutOfMemoryError oome = new OutOfMemoryError();
                final Executable oomeTestMethod = () -> Functions.stream(input)
                        .forEach(asIntConsumer(oome));
                final OutOfMemoryError oomeThrown = assertThrows(OutOfMemoryError.class, oomeTestMethod);
                assertThat(oomeThrown.getMessage(), is(nullValue()));
            }),

            dynamicTest("SAXException", () -> {
                final SAXException se = new SAXException();
                final Executable seTestMethod = () -> Functions.stream(input)
                        .forEach(asIntConsumer(se));
                final UndeclaredThrowableException seThrown = assertThrows(UndeclaredThrowableException.class, seTestMethod);
                assertAll(
                        () -> assertThat(seThrown.getMessage(), is(nullValue())),
                        () -> assertThat(seThrown.getCause(), is(equalTo(se)))
                );
            })
    );
}

@Test
public void testSimpleStreamFilter() {
    final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");
    final List<Integer> output = Functions.stream(input)
            .map(Integer::valueOf)
            .filter(i -> (i.intValue() % 2 == 0))
            .collect(Collectors.toList());
    assertEvenNumbers(output);
}

@TestFactory
public Stream<DynamicTest> simpleStreamFilterFailing() {
    final List<String> input = Arrays.asList("1", "2", "3", "4", "5", "6");
    final List<Integer> output = Functions.stream(input)
            .map(Integer::valueOf)
            .filter(asIntPredicate(null))
            .collect(Collectors.toList());
    assertEvenNumbers(output);

    return Stream.of(

            dynamicTest("IllegalArgumentException", () -> {
                final IllegalArgumentException iae = new IllegalArgumentException("Invalid argument: " + 5);
                final Executable testMethod = () -> Functions.stream(input)
                        .map(Integer::valueOf)
                        .filter(asIntPredicate(iae))
                        .collect(Collectors.toList());
                final IllegalArgumentException thrown = assertThrows(IllegalArgumentException.class, testMethod);
                assertThat(thrown.getMessage(), is(equalTo("Invalid argument: " + 5)));
            }),

            dynamicTest("OutOfMemoryError", () -> {
                final OutOfMemoryError oome = new OutOfMemoryError();
                final Executable testMethod = () -> Functions.stream(input)
                        .map(Integer::valueOf)
                        .filter(asIntPredicate(oome))
                        .collect(Collectors.toList());
                final OutOfMemoryError thrown = assertThrows(OutOfMemoryError.class, testMethod);
                assertThat(thrown.getMessage(), is(nullValue()));
            }),

            dynamicTest("SAXException", () -> {
                final SAXException se = new SAXException();
                final Executable testMethod = () -> Functions.stream(input)
                        .map(Integer::valueOf)
                        .filter(asIntPredicate(se))
                        .collect(Collectors.toList());
                final UndeclaredThrowableException thrown = assertThrows(UndeclaredThrowableException.class, testMethod);
                assertAll(
                        () -> assertThat(thrown.getMessage(), is(nullValue())),
                        () -> assertThat(thrown.getCause(), is(equalTo(se)))
                );
            })
    );
}
```