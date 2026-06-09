# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `a3995141bf1b8a478e86fdbecc95f2b98f892647`
- B: `06506aecf9e46441d08edab311e19e599d273fab`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `methods`
- user_chars: `23404`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6647, 'completion_tokens': 823, 'total_tokens': 7470}`

---

- 修改 `testSwapChar`：对应测试 diff，将逐元素 `assertEquals` 改为数组整体断言，并补充同下标交换、反向相邻交换场景。
- 新增 `testSwapCharOutOfBounds`：对应测试 diff，覆盖 `swap(char[], 0, 5)` 越界时抛出 `ArrayIndexOutOfBoundsException`；使用 JUnit 5 `assertThrows`，无需调整 import。

```java
    @Test
    public void testSwapChar() {
        char[] array = new char[] {1, 2, 3};
        ArrayUtils.swap(array, 0, 2);
        org.junit.jupiter.api.Assertions.assertArrayEquals(new char[] {3, 2, 1}, array);

        array = new char[] {1, 2, 3};
        ArrayUtils.swap(array, 0, 0);
        org.junit.jupiter.api.Assertions.assertArrayEquals(new char[] {1, 2, 3}, array);

        array = new char[] {1, 2, 3};
        ArrayUtils.swap(array, 1, 0);
        org.junit.jupiter.api.Assertions.assertArrayEquals(new char[] {2, 1, 3}, array);
    }

    @Test
    public void testSwapCharOutOfBounds() {
        final char[] array = new char[] {1, 2, 3};
        org.junit.jupiter.api.Assertions.assertThrows(ArrayIndexOutOfBoundsException.class,
                () -> ArrayUtils.swap(array, 0, 5));
    }
```