import static org.apache.commons.lang3.LangAssertions.assertIllegalArgumentException;
import static org.apache.commons.lang3.LangAssertions.assertNullPointerException;
import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
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
import java.util.Collections;
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
@Test
void testIsAssignable_ClassWithParameterizedType() {
    final ParameterizedType topre1 = TypeUtils.parameterize(TestIF.class, TypeUtils.wildcardType().build());
    final Type to1 = TypeUtils.parameterize(Class.class, TypeUtils.wildcardType().withUpperBounds(topre1).build());
    final Type from1 = TypeUtils.parameterize(Class.class, TestIF.class);
    assertFalse(TypeUtils.isAssignable(from1, to1), "Class<TestIF> should not be assignable to Class<? extends TestIF<?>>");

    final ParameterizedType topre2 = TypeUtils.parameterize(TestIF.class, TypeUtils.wildcardType().build());
    final Type to2 = TypeUtils.parameterize(Class.class, TypeUtils.wildcardType().withUpperBounds(topre2).build());
    final Type from2 = TypeUtils.parameterize(Class.class, TestImpl.class);
    assertFalse(TypeUtils.isAssignable(from2, to2), "Class<TestImpl> should not be assignable to Class<? extends TestIF<?>>");

    final ParameterizedType topre3 = TypeUtils.parameterize(TestIF.class, Number.class);
    final Type to3 = TypeUtils.parameterize(Class.class, TypeUtils.wildcardType().withUpperBounds(topre3).build());
    final Type from3 = TypeUtils.parameterize(Class.class, TestImpl2.class);
    assertFalse(TypeUtils.isAssignable(from3, to3), "Class<TestImpl2> should not be assignable to Class<? extends TestIF<Number>>");
}

private interface TestIF<T> {
}

private static class TestImpl<T> implements TestIF<T> {
}

private static class TestImpl2<R> implements TestIF<Number> {


    private static class TestImpl<T> implements TestIF<T> {
    }


    private static class TestImpl2<R> implements TestIF<Number> {
    }
}
