# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `078e512e6cc5ba49eb3c5a3a63a0ddb657324fd9`
- B: `5fef9575646f6583fd2d9ee01368b3deefe6ce82`
- test: `src/test/java/org/apache/commons/lang3/reflect/MethodUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/reflect/MethodUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `53193`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 11686, 'completion_tokens': 1484, 'total_tokens': 13170}`

---

- 新增 `testInvokeMethodForceAccessNoArgs`，覆盖生产代码新增的 `invokeMethod(object, true, methodName)` 强制访问私有无参方法能力，并验证 accessible 状态会恢复。
- 新增 `testInvokeMethodForceAccessWithArgs`，覆盖生产代码新增的 `invokeMethod(object, true, methodName, args...)` 对私有重载方法及参数匹配的支持。
- 新增 `testDistance`，通过反射覆盖生产代码新增的私有 `distance` 方法的不可赋值、精确匹配、装箱/拆箱和继承距离计算。
- 需要调整 import，新增 `java.util.Date` 与 `org.apache.commons.lang3.ClassUtils`，分别用于新增测试参数和 `wrapperToPrimitive` 断言。

```java
// IMPORTS_START
import static org.hamcrest.Matchers.hasItemInArray;
import static org.hamcrest.Matchers.hasItems;
import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNotSame;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertSame;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.lang.reflect.Method;
import java.lang.reflect.Type;
import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.apache.commons.lang3.ArrayUtils;
import org.apache.commons.lang3.ClassUtils;
import org.apache.commons.lang3.ClassUtils.Interfaces;
import org.apache.commons.lang3.math.NumberUtils;
import org.apache.commons.lang3.mutable.Mutable;
import org.apache.commons.lang3.mutable.MutableObject;
import org.apache.commons.lang3.reflect.testbed.Annotated;
import org.apache.commons.lang3.reflect.testbed.GenericConsumer;
import org.apache.commons.lang3.reflect.testbed.GenericParent;
import org.apache.commons.lang3.reflect.testbed.StringParameterizedChild;
import org.apache.commons.lang3.tuple.ImmutablePair;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
// IMPORTS_END

@SuppressWarnings("unused")
private String privateStringStuff() {
    return "privateStringStuff()";
}

@SuppressWarnings("unused")
private String privateStringStuff(final int i) {
    return "privateStringStuff(int)";
}

@SuppressWarnings("unused")
private String privateStringStuff(final Integer i) {
    return "privateStringStuff(Integer)";
}

@SuppressWarnings("unused")
private String privateStringStuff(final double d) {
    return "privateStringStuff(double)";
}

@SuppressWarnings("unused")
private String privateStringStuff(final String s) {
    return "privateStringStuff(String)";
}

@SuppressWarnings("unused")
private String privateStringStuff(final Object s) {
    return "privateStringStuff(Object)";
}

@Test
public void testInvokeMethodForceAccessNoArgs() throws Exception {
    Method privateStringStuffMethod = MethodUtils.getMatchingMethod(TestBean.class, "privateStringStuff");
    Assert.assertFalse(privateStringStuffMethod.isAccessible());
    Assert.assertEquals("privateStringStuff()", MethodUtils.invokeMethod(testBean, true, "privateStringStuff"));
    Assert.assertFalse(privateStringStuffMethod.isAccessible());
}

@Test
public void testInvokeMethodForceAccessWithArgs() throws Exception {
    Assert.assertEquals("privateStringStuff(Integer)", MethodUtils.invokeMethod(testBean, true, "privateStringStuff", 5));
    Assert.assertEquals("privateStringStuff(double)", MethodUtils.invokeMethod(testBean, true, "privateStringStuff", 5.0d));
    Assert.assertEquals("privateStringStuff(String)", MethodUtils.invokeMethod(testBean, true, "privateStringStuff", "Hi There"));
    Assert.assertEquals("privateStringStuff(Object)", MethodUtils.invokeMethod(testBean, true, "privateStringStuff", new Date()));
}

@Test
public void testDistance() throws Exception {
    Method distanceMethod = MethodUtils.getMatchingMethod(MethodUtils.class, "distance", Class[].class, Class[].class);
    distanceMethod.setAccessible(true);

    Assert.assertEquals(-1, distanceMethod.invoke(null, new Class[]{String.class}, new Class[]{Date.class}));
    Assert.assertEquals(0, distanceMethod.invoke(null, new Class[]{Date.class}, new Class[]{Date.class}));
    Assert.assertEquals(1, distanceMethod.invoke(null, new Class[]{Integer.class}, new Class[]{ClassUtils.wrapperToPrimitive(Integer.class)}));
    Assert.assertEquals(2, distanceMethod.invoke(null, new Class[]{Integer.class}, new Class[]{Object.class}));

    distanceMethod.setAccessible(false);
}
```