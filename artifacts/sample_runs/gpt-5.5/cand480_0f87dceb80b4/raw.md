# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `f015fb2b31a5621689a57ce9d2d300e5f32357e1`
- B: `0f87dceb80b432b434dbd81ed4f1ab97c740efc1`
- test: `src/test/java/org/apache/commons/lang3/builder/EqualsBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/EqualsBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `55707`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 14654, 'completion_tokens': 581, 'total_tokens': 15235}`

---

- 不新增、修改或删除任何 `@Test` / `@ParameterizedTest` 方法；生产代码 diff 仅为参数添加 `final`，对应测试 diff 也只需同步递归测试辅助类构造器和 setter 的参数 `final` 以满足代码风格检查。
- 不需要调整 import；现有 JUnit 4 import 与测试断言未受生产代码签名兼容性影响。

```java
public TestRecursiveObject(final TestRecursiveInnerObject a,
        final TestRecursiveInnerObject b, final int z) {
    this.a = a;
    this.b = b;
}

public TestRecursiveInnerObject(final int n) {
    this.n = n;
}

public TestRecursiveCycleObject(final int n) {
    this.n = n;
    this.cycle = this;
}

public TestRecursiveCycleObject(final TestRecursiveCycleObject cycle, final int n) {
    this.n = n;
    this.cycle = cycle;
}

public void setCycle(final TestRecursiveCycleObject cycle) {
    this.cycle = cycle;
}
```