# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `6681a34d25b63a47c2d619ae0466825304ea9b1f`
- B: `4e228a53509bd8cb01220939906a538dcd1baa40`
- test: `src/test/java/org/apache/commons/lang3/reflect/TypeUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/reflect/TypeUtils.java']`
- old_test_mode: `methods`
- user_chars: `11128`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2966, 'completion_tokens': 1485, 'total_tokens': 4451}`

---

- 修改 `test_LANG_1698`：生产代码已在 `typeVariableToString` 中规避 Java 17+ 的递归栈溢出，因此删除 Java 版本假设，直接断言类型名。
- 新增 `testTypeToString(Type type)` 参数化测试：覆盖生产代码 `TypeUtils.toString(Type)` 对 JDK 泛型反射类型不再栈溢出的行为。
- 新增 `testTypeToString()` 方法源：为新增参数化测试提供 `Comparator`、`Comparable`、`ArrayList`、`HashMap` 的泛型类型样本。
- 需要调整 import：新增 `assertNotNull`、`Stream`、`ParameterizedTest`、`MethodSource`，删除 `assumeTrue`、`JavaVersion`、`SystemUtils`。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.awt.Insets;
import java.io.Serializable;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.GenericArrayType;
import java.lang.reflect.Method;
import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.lang.reflect.TypeVariable;
import java.lang.reflect.WildcardType;
import java.net.URI;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.TreeSet;
import java.util.stream.Stream;

import org.apache.commons.lang3.AbstractLangTest;
import org.apache.commons.lang3.reflect.testbed.Foo;
import org.apache.commons.lang3.reflect.testbed.GenericParent;
import org.apache.commons.lang3.reflect.testbed.GenericTypeHolder;
import org.apache.commons.lang3.reflect.testbed.StringParameterizedChild;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
// IMPORTS_END

static Stream<Type> testTypeToString() {
    // @formatter:off
    return Stream.of(Comparator.class, Comparable.class, ArrayList.class, HashMap.class)
            .flatMap(cls -> Stream.of(cls.getDeclaredMethods()))
            .flatMap(m ->
                Stream.concat(Stream.of(m.getGenericExceptionTypes()),
                Stream.concat(Stream.of(m.getGenericParameterTypes()),
                Stream.concat(Stream.of(m.getGenericReturnType()), Stream.of(m.getTypeParameters())))));
    // @formatter:on
}

/**
 * Tests https://issues.apache.org/jira/projects/LANG/issues/LANG-1698
 *
 * <pre>{@code
 * java.lang.StackOverflowError
    at org.apache.commons.lang3.reflect.TypeUtils.typeVariableToString(TypeUtils.java:1785)
    at org.apache.commons.lang3.reflect.TypeUtils.toString(TypeUtils.java:1869)
    at org.apache.commons.lang3.reflect.TypeUtils.lambda$static$0(TypeUtils.java:319)
    at org.apache.commons.lang3.stream.Streams$FailableStream.collect(Streams.java:142)
    at org.apache.commons.lang3.reflect.TypeUtils.parameterizedTypeToString(TypeUtils.java:1609)
    at org.apache.commons.lang3.reflect.TypeUtils.toString(TypeUtils.java:1863)
    at org.apache.commons.lang3.reflect.TypeUtils.lambda$static$0(TypeUtils.java:319)
    at org.apache.commons.lang3.stream.Streams$FailableStream.collect(Streams.java:142)
    at org.apache.commons.lang3.reflect.TypeUtils.typeVariableToString(TypeUtils.java:1785)
 * }</pre>
 */
@Test
public void test_LANG_1698() {
    final ParameterizedType comparing = (ParameterizedType) Arrays.stream(Comparator.class.getDeclaredMethods())
            .filter(k -> k.getName().equals("comparing")).findFirst()
            .orElse(Comparator.class.getDeclaredMethods()[0]).getGenericParameterTypes()[0];
    final String typeName = TypeUtils
            .parameterize((Class<?>) comparing.getRawType(), comparing.getActualTypeArguments()).getTypeName();
    assertEquals("java.util.function.Function<? super T, ? extends U>", typeName);
}

@ParameterizedTest
@MethodSource
public void testTypeToString(Type type) {
    // No stack overflow
    assertNotNull(TypeUtils.toString(type));
}
```