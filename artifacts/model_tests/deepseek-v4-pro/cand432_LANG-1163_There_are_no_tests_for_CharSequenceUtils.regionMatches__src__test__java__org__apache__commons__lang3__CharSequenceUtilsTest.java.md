# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `68acbc803e416a38616bc25505cb88dde81af5ca`
- B: `e8a2c29721d145c52c970049e5469cfb0dcefd87`
- test: `src/test/java/org/apache/commons/lang3/CharSequenceUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/CharSequenceUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `9294`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2563, 'completion_tokens': 3253, 'total_tokens': 5816, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2249}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2179}`

---

- 新增 @Test 方法 `testRegionMatches` 以及辅助静态内部类 `TestData`、抽象类 `RunTest`、测试数据常量 `TEST_DATA`，用于验证更新后的 `CharSequenceUtils.regionMatches` 边界检查逻辑与原 `String.regionMatches` 行为一致；无需修改原有测试方法，也无需新增 import（所有类型均在当前包或 `java.lang` 中）。

```java
    static class TestData{
        final String source;
        final boolean ignoreCase;
        final int toffset;
        final String other;
        final int ooffset;
        final int len;
        final boolean expected;
        final Class<?> throwable;
        TestData(String source, boolean ignoreCase, int toffset,
                String other, int ooffset, int len, boolean expected){
            this.source = source;
            this.ignoreCase = ignoreCase;
            this.toffset = toffset;
            this.other = other;
            this.ooffset = ooffset;
            this.len = len;
            this.expected = expected;
            this.throwable = null;
        }
        TestData(String source, boolean ignoreCase, int toffset,
                String other, int ooffset, int len, Class<?> throwable){
            this.source = source;
            this.ignoreCase = ignoreCase;
            this.toffset = toffset;
            this.other = other;
            this.ooffset = ooffset;
            this.len = len;
            this.expected = false;
            this.throwable = throwable;
        }
        public String toString(){
            StringBuilder sb = new StringBuilder();
            sb.append(source).append("[").append(toffset).append("]");
            sb.append(ignoreCase? " caseblind ":" samecase ");
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
            //          Source  IgnoreCase Offset Other  Offset Length Result
            new TestData("",    true,      -1,    "",    -1,    -1,    false),
            new TestData("",    true,      0,     "",    0,     1,     false),
            new TestData("a",   true,      0,     "abc", 0,     0,     true),
            new TestData("a",   true,      0,     "abc", 0,     1,     true),
            new TestData("a",   true,      0,     null,  0,     0,     NullPointerException.class),
            new TestData(null,  true,      0,     null,  0,     0,     NullPointerException.class),
            new TestData(null,  true,      0,     "",    0,     0,     NullPointerException.class),
    };

    private static abstract class RunTest {
        
        abstract boolean invoke();
        
        void run(TestData data, String id) {
            if (data.throwable != null) {
                try {
                    invoke();
                    Assert.fail(id + " Expected " + data.throwable);
                } catch (Exception e) {
                    if (!e.getClass().equals(data.throwable)) {
                        Assert.fail(id + " Expected " + data.throwable + " got " + e.getClass());
                    }
                }
            } else {
                boolean stringCheck = invoke();
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