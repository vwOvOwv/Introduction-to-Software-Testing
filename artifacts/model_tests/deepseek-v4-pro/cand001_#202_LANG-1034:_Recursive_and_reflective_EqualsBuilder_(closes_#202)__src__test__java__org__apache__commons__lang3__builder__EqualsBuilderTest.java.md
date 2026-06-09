# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `9f89fd4626bbb4e34a905835e397bcffbad59307`
- B: `0095d8adf26b9469115b1be0358cb09d1fcb5fd4`
- test: `src/test/java/org/apache/commons/lang3/builder/EqualsBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/EqualsBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `68464`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 18307, 'completion_tokens': 2035, 'total_tokens': 20342, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 802}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 17923}`

---

- 新增 `@Test` 方法 `testObjectRecursive`，测试递归相等性检验的基本行为。
- 新增 `@Test` 方法 `testObjectRecursiveCycleSelfreference`，测试带自引用对象的递归相等性。
- 新增 `@Test` 方法 `testObjectRecursiveCycle`，测试相互引用循环对象的递归相等性。
- 新增三个内部类 `TestRecursiveObject`、`TestRecursiveInnerObject`、`TestRecursiveCycleObject`，作为测试用的数据结构。
- 无需调整 import，现有 import 已覆盖所有必要类型。

```java
static class TestRecursiveObject {
    private TestRecursiveInnerObject a;
    private TestRecursiveInnerObject b;
    private int z;

    public TestRecursiveObject(TestRecursiveInnerObject a,
                               TestRecursiveInnerObject b, int z) {
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

    public TestRecursiveInnerObject(int n) {
        this.n = n;
    }

    public int getN() {
        return n;
    }
}

static class TestRecursiveCycleObject {
    private TestRecursiveCycleObject cycle;
    private int n;

    public TestRecursiveCycleObject(int n) {
        this.n = n;
        this.cycle = this;
    }

    public TestRecursiveCycleObject(TestRecursiveCycleObject cycle, int n) {
        this.n = n;
        this.cycle = cycle;
    }

    public int getN() {
        return n;
    }

    public TestRecursiveCycleObject getCycle() {
        return cycle;
    }

    public void setCycle(TestRecursiveCycleObject cycle) {
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