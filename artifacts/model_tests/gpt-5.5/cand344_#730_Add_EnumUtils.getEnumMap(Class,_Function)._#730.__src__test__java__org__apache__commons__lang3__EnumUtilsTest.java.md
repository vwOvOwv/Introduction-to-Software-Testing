# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `70abafc95d2de789f5292c7f5df9bb4d39c2bdb9`
- B: `8a4d1b82f8d5556c866701b556d78fd3e2d4d88a`
- test: `src/test/java/org/apache/commons/lang3/EnumUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/EnumUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `35393`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9905, 'completion_tokens': 934, 'total_tokens': 10839}`

---

- 新增 `test_getEnumMap_keyFunction`，对应生产代码新增的 `EnumUtils.getEnumMap(Class<E>, Function<E,K>)` 重载，验证按自定义 key 函数生成 Map。
- 新增测试辅助枚举 `Month`，用于为 `test_getEnumMap_keyFunction` 提供稳定的整数 key。
- import 无需调整，旧测试中已有 `Map` 和 `Function` 相关 import。

```java
    @Test
    public void test_getEnumMap_keyFunction() {
        final Map<Integer, Month> test = EnumUtils.getEnumMap(Month.class, Month::getId);
        assertEquals("{1=JAN, 2=FEB, 3=MAR, 4=APR, 5=MAY, 6=JUN, 7=JUL, 8=AUG, 9=SEP, 10=OCT, 11=NOV, 12=DEC}", test.toString(),
                "getEnumMap not created correctly");
        assertEquals(12, test.size());
        assertFalse(test.containsKey(0));
        assertTrue(test.containsKey(1));
        assertEquals(Month.JAN, test.get(1));
        assertTrue(test.containsKey(2));
        assertEquals(Month.FEB, test.get(2));
        assertTrue(test.containsKey(3));
        assertEquals(Month.MAR, test.get(3));
        assertTrue(test.containsKey(4));
        assertEquals(Month.APR, test.get(4));
        assertTrue(test.containsKey(5));
        assertEquals(Month.MAY, test.get(5));
        assertTrue(test.containsKey(6));
        assertEquals(Month.JUN, test.get(6));
        assertTrue(test.containsKey(7));
        assertEquals(Month.JUL, test.get(7));
        assertTrue(test.containsKey(8));
        assertEquals(Month.AUG, test.get(8));
        assertTrue(test.containsKey(9));
        assertEquals(Month.SEP, test.get(9));
        assertTrue(test.containsKey(10));
        assertEquals(Month.OCT, test.get(10));
        assertTrue(test.containsKey(11));
        assertEquals(Month.NOV, test.get(11));
        assertTrue(test.containsKey(12));
        assertEquals(Month.DEC, test.get(12));
        assertFalse(test.containsKey(13));
    }

enum Month {
    JAN(1), FEB(2), MAR(3), APR(4), MAY(5), JUN(6), JUL(7), AUG(8), SEP(9), OCT(10), NOV(11), DEC(12);

    private final int id;

    Month(final int id) {
        this.id = id;
    }

    public int getId() {
        return this.id;
    }
}
```