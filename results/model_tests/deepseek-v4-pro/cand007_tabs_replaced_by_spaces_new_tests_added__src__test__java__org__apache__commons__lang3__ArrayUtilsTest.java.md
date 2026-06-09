# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `a3995141bf1b8a478e86fdbecc95f2b98f892647`
- B: `06506aecf9e46441d08edab311e19e599d273fab`
- test: `src/test/java/org/apache/commons/lang3/ArrayUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ArrayUtils.java']`
- old_test_mode: `methods`
- user_chars: `23404`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6997, 'completion_tokens': 1277, 'total_tokens': 8274, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 939}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 6613}`

---

- 修改 `testSwapChar` 方法：增加正向交换、相同索引交换、逆序交换三种场景，并使用 `assertArrayEquals` 替代逐个元素的 `assertEquals` 断言。
- 新增 `testSwapCharOutOfBounds` 方法：测试数组越界时抛出 `ArrayIndexOutOfBoundsException`。
- 需在测试类中新增 `import static org.junit.Assert.assertArrayEquals;` 导入，以支持数组断言。

```java
import static org.junit.Assert.assertArrayEquals;

// 修改后的 testSwapChar 方法
@Test
public void testSwapChar() {
    char[] array = new char[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 2);
    assertArrayEquals(new char[] {3, 2, 1}, array);
    
    array = new char[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 0);
    assertArrayEquals(new char[] {1, 2, 3}, array);
    
    array = new char[] {1, 2, 3};
    ArrayUtils.swap(array, 1, 0);
    assertArrayEquals(new char[] {2, 1, 3}, array);
}

// 新增的 testSwapCharOutOfBounds 方法
@Test(expected = ArrayIndexOutOfBoundsException.class)
public void testSwapCharOutOfBounds() {
    char[] array = new char[] {1, 2, 3};
    ArrayUtils.swap(array, 0, 5);
}
```