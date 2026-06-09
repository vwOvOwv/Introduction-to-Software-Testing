# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `f13d18cff3f0932e727dda04bf80008fc2fbbc70`
- B: `f643b4fa939e89348618ddffae20a804f4461363`
- test: `src/test/java/org/apache/commons/lang3/RandomStringUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RandomStringUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `28976`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 7255, 'completion_tokens': 355, 'total_tokens': 7610}`

---

- 新增 `testCharOverflow`：生产代码将无字符集随机生成从 `char` 扩展为合法 Unicode code point，并修复高起点范围下的 char 溢出问题，因此增加 LANG-1286 回归测试。
- import 无需调整：旧测试已包含 `java.util.Random`、`org.junit.Test` 和 `assertTrue` 静态导入。

```java
    /**
     * Test for LANG-1286. Creates situation where old code would
     * overflow a char and result in a code point outside the specified
     * range.
     * 
     * @throws Exception
     */
    @Test
    public void testCharOverflow() throws Exception {
        int start = Character.MAX_VALUE;
        int end = Integer.MAX_VALUE;
        
        @SuppressWarnings("serial")
        Random fixedRandom = new Random() {
            @Override
            public int nextInt(int n) {
                // Prevents selection of 'start' as the character
                return super.nextInt(n - 1) + 1;
            }
        };
        
        String result = RandomStringUtils.random(2, start, end, false, false, null, fixedRandom);
        int c = result.codePointAt(0);
        assertTrue(String.format("Character '%d' not in range [%d,%d).", c, start, end), c >= start && c < end);
    }
```