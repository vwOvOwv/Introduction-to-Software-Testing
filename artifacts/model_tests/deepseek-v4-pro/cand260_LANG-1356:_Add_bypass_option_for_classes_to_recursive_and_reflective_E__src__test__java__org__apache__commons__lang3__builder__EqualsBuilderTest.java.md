# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `2ce40494073aa4e9bdcba4c39d24727b7141d227`
- B: `2e9f3a80146262511ca7bcdd3411f095dff4951d`
- test: `src/test/java/org/apache/commons/lang3/builder/EqualsBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/EqualsBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `61308`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 16278, 'completion_tokens': 2104, 'total_tokens': 18382, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1497}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 15894}`

---

- 新增内部类 `TestRecursiveGenericObject<T>`，用于构造测试泛型递归比较所需的载体对象。
- 新增测试方法 `testObjectRecursiveGenericInteger`，验证在递归模式下对包装了相同/不同整数的泛型对象进行相等性比较，以确保新加的正则比较逻辑（对非排除类走反射）对基本包装类仍正确。
- 新增测试方法 `testObjectRecursiveGenericString`，验证在递归模式下对包装了字符串的泛型对象进行相等性比较，并显式触发 `String.hashCode` 缓存写入，以检验默认排除 String 反射后 `equals` 比较的正确性。
- 无需添加或修改任何 import 语句，现有静态导入和依赖已足够。

```java
static class TestRecursiveGenericObject<T> {

    private final T a;

    TestRecursiveGenericObject(final T a) {
        this.a = a;
    }

    public T getA() {
        return a;
    }
}

@Test
public void testObjectRecursiveGenericInteger() {
    final TestRecursiveGenericObject<Integer> o1_a = new TestRecursiveGenericObject<Integer>(1);
    final TestRecursiveGenericObject<Integer> o1_b = new TestRecursiveGenericObject<Integer>(1);
    final TestRecursiveGenericObject<Integer> o2 = new TestRecursiveGenericObject<Integer>(2);

    assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_a, o1_b).isEquals());
    assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_b, o1_a).isEquals());

    assertFalse(new EqualsBuilder().setTestRecursive(true).append(o1_b, o2).isEquals());
}

@Test
public void testObjectRecursiveGenericString() {
    // Note: Do not use literals, because string literals are always mapped by same object (internal() of String))!
    String s1_a = String.valueOf(1);
    final TestRecursiveGenericObject<String> o1_a = new TestRecursiveGenericObject<String>(s1_a);
    final TestRecursiveGenericObject<String> o1_b = new TestRecursiveGenericObject<String>(String.valueOf(1));
    final TestRecursiveGenericObject<String> o2 = new TestRecursiveGenericObject<String>(String.valueOf(2));

    // To trigger bug reported in LANG-1356, call hashCode only on string in instance o1_a
    s1_a.hashCode();

    assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_a, o1_b).isEquals());
    assertTrue(new EqualsBuilder().setTestRecursive(true).append(o1_b, o1_a).isEquals());

    assertFalse(new EqualsBuilder().setTestRecursive(true).append(o1_b, o2).isEquals());
}
```