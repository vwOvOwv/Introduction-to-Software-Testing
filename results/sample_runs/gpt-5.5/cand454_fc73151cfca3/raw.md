# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e2ec4f2fdb2bb8d97f64a33e9ac288d52854a530`
- B: `fc73151cfca36ea2641f340700dbe339b9e1f103`
- test: `src/test/java/org/apache/commons/lang3/text/StrBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/StrBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `73764`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 18116, 'completion_tokens': 169, 'total_tokens': 18285}`

---

- 新增 `test_LANG_1131_EqualsWithNullStrBuilder`：生产代码 `StrBuilder.equals(StrBuilder)` 新增了 `other == null` 返回 `false` 的分支，需要覆盖传入 `null` 的行为。
- 不需要调整 import：新增测试仅使用已有的 `@Test` 和 `assertFalse`。

```java
    @Test
    public void test_LANG_1131_EqualsWithNullStrBuilder() throws Exception {
        final StrBuilder sb = new StrBuilder();
        final StrBuilder other = null;
        assertFalse(sb.equals(other));
    }
```