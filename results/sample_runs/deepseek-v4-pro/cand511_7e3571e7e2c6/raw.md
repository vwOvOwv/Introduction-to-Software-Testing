# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `53dc633eb330bea4335b015a273346553446bb8a`
- B: `7e3571e7e2c6d96f8c491b75b876162687d800c9`
- test: `src/test/java/org/apache/commons/lang3/SystemUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/SystemUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `169892`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `length`
- usage: `{'prompt_tokens': 46949, 'completion_tokens': 8192, 'total_tokens': 55141, 'prompt_tokens_details': {'cached_tokens': 41088}, 'completion_tokens_details': {'reasoning_tokens': 8192}, 'prompt_cache_hit_tokens': 41088, 'prompt_cache_miss_tokens': 5861}`
  （length 表示输出可能被截断，已尝试自动续写一轮）

---

- 修改 `testIsJavaVersionAtLeast` 方法：在所有现有分支（IS_JAVA_1_8 至 IS_JAVA_26）末尾增加对 `JAVA_27` 的 `assertFalse` 断言，并新增 `IS_JAVA_27` 分支覆盖所有更小版本的 `assertTrue` 与自身的 `assertTrue`。
- 修改 `testIsJavaVersionAtMost` 方法：在所有分支（IS_JAVA_1_8 至 IS_JAVA_26）末尾增加对 `JAVA_27` 的 `assertTrue` 断言（其中 `IS_JAVA_9` 分支按 diff 出现两次 `assertTrue`），并新增 `IS_JAVA_27` 分支覆盖所有更小版本的 `assertFalse` 与自身的 `assertTrue`。
- 无需新增或删除 import，也不需要删除任何测试方法。

```java
@Test
void testIsJavaVersionAtLeast() {
    if (SystemUtils.IS_JAVA_1_8) {
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_1));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_2));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_3));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_4));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_5));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_6));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_7));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_8));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_9));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_10));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_11));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_12));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_13));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_14));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_15));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_16));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_17));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_18));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_19));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_20));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_21));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_22));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_23));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_24));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_25));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_26));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_27));
    } else if (SystemUtils.IS_JAVA_9) {
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_1));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_2));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_3));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_4));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_5));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_6));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_7));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_8));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_9));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_10));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_11));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_12));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_13));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_14));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_15));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_16));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_17));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_18));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_19));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_20));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_21));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_22));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_23));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_24));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_25));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_26));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_27));
    } else if (SystemUtils.IS_JAVA_10) {
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_1));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_2));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_3));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_4));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_5));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_6));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_7));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_8));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_9));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_10));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_11));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_12));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_13));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_14));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_15));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_16));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_17));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_18));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_19));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_20));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_21));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_22));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_23));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_24));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_25));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_26));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_27));
    } else if (SystemUtils.IS_JAVA_11) {
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_1));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_2));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_3));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_4));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_5));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_6));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_7));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_8));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_9));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_10));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_11));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_12));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_13));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_14));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_15));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_16));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_17));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_18));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_19));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_20));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_21));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_22));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_23));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_24));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_25));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_26));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_27));
    } else if (SystemUtils.IS_JAVA_12) {
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_1));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_2));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_3));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_4));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_5));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_6));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_7));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_8));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_9));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_10));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_11));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_12));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_13));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_14));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_15));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_16));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_17));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_18));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_19));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_20));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_21));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_22));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_23));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_24));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_25));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_26));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_27));
    } else if (SystemUtils.IS_JAVA_13) {
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_1));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_2));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_3));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_4));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_5));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_6));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_7));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_8));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_9));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_10));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_11));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_12));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_13));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_14));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_15));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_16));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_17));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_18));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_19));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_20));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_21));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_22));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_23));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_24));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_25));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_26));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_27));
    } else if (SystemUtils.IS_JAVA_14) {
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_1));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_2));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_3));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_4));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_5));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_6));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_7));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_8));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_9));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_10));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_11));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_12));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_13));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_14));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_15));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_16));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_17));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_18));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_19));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_20));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_21));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_22));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_23));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_24));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_25));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_26));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_27));
    } else if (SystemUtils.IS_JAVA_15) {
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_1));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_2));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_3));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_4));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_5));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_6));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_7));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_8));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_9));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_10));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_11));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_12));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_13));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_14));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_15));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_16));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_17));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_18));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_19));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_20));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_21));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_22));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_23));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_24));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_25));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_26));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_27));
    } else if (SystemUtils.IS_JAVA_16) {
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_1));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_2));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_3));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_4));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_5));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_6));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_7));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_8));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_9));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_10));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_11));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_12));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_13));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_14));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_15));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_16));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_17));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_18));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_19));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_20));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_21));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_22));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_23));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_24));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_25));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_26));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_27));
    } else if (SystemUtils.IS_JAVA_17) {
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_1));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_2));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_3));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_4));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_5));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_6));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_7));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_8));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_9));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_10));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_11));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_12));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_13));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_14));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_15));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_16));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_17));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_18));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_19));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_20));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_21));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_22));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_23));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_24));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_25));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_26));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_27));
    } else if (SystemUtils.IS_JAVA_18) {
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_1));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_2));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_3));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_4));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_5));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_6));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_7));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_1_8));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_9));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_10));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_11));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_12));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_13));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_14));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_15));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_16));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_17));
        assertTrue(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_18));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_19));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_20));
        assertFalse(SystemUtils.isJavaVersionAtLeast(JavaVersion.JAVA_21));
        assertFalse(SystemUtils.isJavaVersion