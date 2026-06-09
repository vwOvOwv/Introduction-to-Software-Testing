# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9f89fd4626bbb4e34a905835e397bcffbad59307`
- B: `0095d8adf26b9469115b1be0358cb09d1fcb5fd4`
- test: `src/test/java/org/apache/commons/lang3/builder/EqualsBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/EqualsBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `68464`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 17743, 'completion_tokens': 1476, 'total_tokens': 19219, 'prompt_tokens_details': {'cached_tokens': 17408}}`

---

- 新增辅助内部类 `TestRecursiveObject`、`TestRecursiveInnerObject`、`TestRecursiveCycleObject`，用于覆盖生产代码新增的递归反射比较路径。
- 新增 `@Test` 方法 `testObjectRecursive`，验证 `EqualsBuilder#setTestRecursive(true)` 后 `append(Object,Object)` 会递归比较非基本类型字段。
- 新增 `@Test` 方法 `testObjectRecursiveCycleSelfreference`，验证递归比较能处理自引用对象且不会栈溢出。
- 新增 `@Test` 方法 `testObjectRecursiveCycle`，验证递归比较能处理对象环，并覆盖新增的 `reflectionEquals(..., testRecursive, ...)` 重载。
- import 无需调整，现有 `assertTrue`、`assertFalse` 和 `@Test` 已满足新增测试需要。

```java
static class TestRecursiveObject {
    private TestRecursiveInnerObject a;
    private TestRecursiveInnerObject b;
    private int z;

    public TestRecursiveObject(final TestRecursiveInnerObject a,
            final TestRecursiveInnerObject b, final int z) {
        this.a = a;
        this.b = b;
    }

    public TestRecursiveInnerObject getA() {
        return a;
    }

    public TestRecursiveInnerObject getB() {
        return b;
    }

    public int getZ() {
        return z;
    }
}

static class TestRecursiveInnerObject {
    private int n;

    public TestRecursiveInnerObject(final int n) {
        this.n = n;
    }

    public int getN() {
        return n;
    }
}

static class TestRecursiveCycleObject {
    private TestRecursiveCycleObject cycle;
    private int n;

    public TestRecursiveCycleObject(final int n) {
        this.n = n;
        this.cycle = this;
    }

    public TestRecursiveCycleObject(final TestRecursiveCycleObject cycle, final int n) {
        this.n = n;
        this.cycle = cycle;
    }

    public int getN() {
        return n;
    }

    public TestRecursiveCycleObject getCycle() {
        return cycle;
    }

    public void setCycle(final TestRecursiveCycleObject cycle) {
        this.cycle = cycle;
    }
}

@Test
public void testObjectRecursive() {
    final TestRecursiveInnerObject i1_1 = new TestRecursiveInnerObject(1);
    final TestRecursiveInnerObject i1_2 = new TestRecursiveInnerObject(1);
    final TestRecursiveInnerObject i2_1 = new TestRecursiveInnerObject(2);
    final TestRecursiveInnerObject i2_2 = new TestRecursiveInnerObject(2);
    final TestRecursiveInnerObject i3 = new TestRecursiveInnerObject(3);
    final TestRecursiveInnerObject i4 = new TestRecursiveInnerObject(4);

    final TestRecursiveObject o1_a = new TestRecursiveObject(i1_1, i2_1, 1);
    final TestRecursiveObject o1_b = new TestRecursiveObject(i1_2, i2_2, 1);
    final TestRecursiveObject o2 = new TestRecursiveObject(i3, i4, 2);
    final TestRecursiveObject oNull = new TestRecursiveObject(null, null, 2);

    assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_a, o1_a).isEquals());
    assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_a, o1_b).isEquals());

    assertFalse(new EqualsBuilder().setTestRecursive(true).append(o1_a, o2).isEquals());

    assertTrue(new EqualsBuilder().setTestRecursive(true).append(oNull, oNull).isEquals());
    assertFalse(new EqualsBuilder().setTestRecursive(true).append(o1_a, oNull).isEquals());
}

@Test
public void testObjectRecursiveCycleSelfreference() {
    final TestRecursiveCycleObject o1_a = new TestRecursiveCycleObject(1);
    final TestRecursiveCycleObject o1_b = new TestRecursiveCycleObject(1);
    final TestRecursiveCycleObject o2 = new TestRecursiveCycleObject(2);

    assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_a, o1_a).isEquals());
    assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_a, o1_b).isEquals());
    assertFalse(new EqualsBuilder().setTestRecursive(true).append(o1_a, o2).isEquals());
}

@Test
public void testObjectRecursiveCycle() {
    final TestRecursiveCycleObject o1_a = new TestRecursiveCycleObject(1);
    final TestRecursiveCycleObject i1_a = new TestRecursiveCycleObject(o1_a, 100);
    o1_a.setCycle(i1_a);

    final TestRecursiveCycleObject o1_b = new TestRecursiveCycleObject(1);
    final TestRecursiveCycleObject i1_b = new TestRecursiveCycleObject(o1_b, 100);
    o1_b.setCycle(i1_b);

    final TestRecursiveCycleObject o2 = new TestRecursiveCycleObject(2);
    final TestRecursiveCycleObject i2 = new TestRecursiveCycleObject(o1_b, 200);
    o2.setCycle(i2);

    assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_a, o1_a).isEquals());
    assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_a, o1_b).isEquals());
    assertFalse(new EqualsBuilder().setTestRecursive(true).append(o1_a, o2).isEquals());

    assertTrue(EqualsBuilder.reflectionEquals(o1_a, o1_b, false, null, true));
    assertFalse(EqualsBuilder.reflectionEquals(o1_a, o2, false, null, true));
}
```