# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `68acbc803e416a38616bc25505cb88dde81af5ca`
- B: `e8a2c29721d145c52c970049e5469cfb0dcefd87`
- test: `src/test/java/org/apache/commons/lang3/CharSequenceUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/CharSequenceUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `9294`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2532, 'completion_tokens': 1203, 'total_tokens': 3735}`

---

- 新增 `testRegionMatches`：覆盖 `CharSequenceUtils.regionMatches` 新增的负偏移、长度越界与空指针行为，并与 `String.regionMatches` 对齐。
- 不删除现有 `@Test` 方法；无需调整 import，现有 `org.junit.Assert` 与 `org.junit.Test` 已满足新增测试。

```java
    static class TestData {
        final String source;
        final boolean ignoreCase;
        final int toffset;
        final String other;
        final int ooffset;
        final int len;
        final boolean expected;
        final Class<?> throwable;

        TestData(final String source, final boolean ignoreCase, final int toffset,
                final String other, final int ooffset, final int len, final boolean expected) {
            this.source = source;
            this.ignoreCase = ignoreCase;
            this.toffset = toffset;
            this.other = other;
            this.ooffset = ooffset;
            this.len = len;
            this.expected = expected;
            this.throwable = null;
        }

        TestData(final String source, final boolean ignoreCase, final int toffset,
                final String other, final int ooffset, final int len, final Class<?> throwable) {
            this.source = source;
            this.ignoreCase = ignoreCase;
            this.toffset = toffset;
            this.other = other;
            this.ooffset = ooffset;
            this.len = len;
            this.expected = false;
            this.throwable = throwable;
        }

        @Override
        public String toString() {
            final StringBuilder sb = new StringBuilder();
            sb.append(source).append("[").append(toffset).append("]");
            sb.append(ignoreCase ? " caseblind " : " samecase ");
            sb.append(other).append("[").append(ooffset).append("]");
            sb.append(" ").append(len).append(" => ");
            if (throwable != null) {
                sb.append(throwable);
            } else {
                sb.append(expected);
            }
            return sb.toString();
        }
    }

    private static final TestData[] TEST_DATA = {
            new TestData("", true, -1, "", -1, -1, false),
            new TestData("", true, 0, "", 0, 1, false),
            new TestData("a", true, 0, "abc", 0, 0, true),
            new TestData("a", true, 0, "abc", 0, 1, true),
            new TestData("a", true, 0, null, 0, 0, NullPointerException.class),
            new TestData(null, true, 0, null, 0, 0, NullPointerException.class),
            new TestData(null, true, 0, "", 0, 0, NullPointerException.class),
    };

    private static abstract class RunTest {

        abstract boolean invoke();

        void run(final TestData data, final String id) {
            if (data.throwable != null) {
                try {
                    invoke();
                    Assert.fail(id + " Expected " + data.throwable);
                } catch (final Exception e) {
                    if (!e.getClass().equals(data.throwable)) {
                        Assert.fail(id + " Expected " + data.throwable + " got " + e.getClass());
                    }
                }
            } else {
                final boolean stringCheck = invoke();
                Assert.assertEquals(id + " Failed test " + data, data.expected, stringCheck);
            }
        }
    }

    @Test
    public void testRegionMatches() {
        for (final TestData data : TEST_DATA) {
            new RunTest() {
                @Override
                boolean invoke() {
                    return data.source.regionMatches(data.ignoreCase, data.toffset, data.other, data.ooffset, data.len);
                }
            }.run(data, "String");

            new RunTest() {
                @Override
                boolean invoke() {
                    return CharSequenceUtils.regionMatches(data.source, data.ignoreCase, data.toffset, data.other, data.ooffset, data.len);
                }
            }.run(data, "CSString");

            new RunTest() {
                @Override
                boolean invoke() {
                    return CharSequenceUtils.regionMatches(new StringBuilder(data.source), data.ignoreCase, data.toffset, data.other, data.ooffset, data.len);
                }
            }.run(data, "CSNonString");
        }
    }
```