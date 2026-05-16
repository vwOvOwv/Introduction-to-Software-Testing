import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import org.apache.commons.lang3.ClassUtils.Interfaces;
import org.apache.commons.lang3.reflect.testbed.GenericConsumer;
import org.apache.commons.lang3.reflect.testbed.GenericParent;
import org.apache.commons.lang3.reflect.testbed.StringParameterizedChild;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
@Test
public void test_getShortCanonicalName_String() {
    assertEquals("", ClassUtils.getShortCanonicalName((String) null));
    assertEquals("Map.Entry", ClassUtils.getShortCanonicalName(java.util.Map.Entry.class.getName()));
    assertEquals("Entry", ClassUtils.getShortCanonicalName(java.util.Map.Entry.class.getCanonicalName()));
    assertEquals("ClassUtils", ClassUtils.getShortCanonicalName("org.apache.commons.lang3.ClassUtils"));
    assertEquals("ClassUtils[]", ClassUtils.getShortCanonicalName("[Lorg.apache.commons.lang3.ClassUtils;"));
    assertEquals("ClassUtils[][]", ClassUtils.getShortCanonicalName("[[Lorg.apache.commons.lang3.ClassUtils;"));
    assertEquals("ClassUtils[]", ClassUtils.getShortCanonicalName("org.apache.commons.lang3.ClassUtils[]"));
    assertEquals("ClassUtils[][]", ClassUtils.getShortCanonicalName("org.apache.commons.lang3.ClassUtils[][]"));
    assertEquals("int[]", ClassUtils.getShortCanonicalName("[I"));
    assertEquals("int[]", ClassUtils.getShortCanonicalName(int[].class.getCanonicalName()));
    assertEquals("int[]", ClassUtils.getShortCanonicalName(int[].class.getName()));
    assertEquals("int[][]", ClassUtils.getShortCanonicalName("[[I"));
    assertEquals("int[]", ClassUtils.getShortCanonicalName("int[]"));
    assertEquals("int[][]", ClassUtils.getShortCanonicalName("int[][]"));

    // this is to demonstrate that the documentation and the naming of the methods
    // uses the class name and canonical name totally mixed up, which cannot be
    // fixed without backward compatibility break
    assertEquals("int[]", int[].class.getCanonicalName());
    assertEquals("[I", int[].class.getName());
    assertThrows(IllegalArgumentException.class, () -> ClassUtils.getShortCanonicalName(StringUtils.repeat("[", 256) + "I"));
    assertEquals("int" + StringUtils.repeat("[]", 255), ClassUtils.getShortCanonicalName(StringUtils.repeat("[", 255) + "I"));

    // Inner types... the problem is that these are not canonical names, classes with this name do not even have canonical
    // name
    // WARNING: this is fragile, implementation may change, naming is not guaranteed
    assertEquals("ClassUtilsTest.6", ClassUtils.getShortCanonicalName("org.apache.commons.lang3.ClassUtilsTest$6"));
    // WARNING: this is fragile, implementation may change, naming is not guaranteed
    assertEquals("ClassUtilsTest.5Named", ClassUtils.getShortCanonicalName("org.apache.commons.lang3.ClassUtilsTest$5Named"));
    assertEquals("ClassUtilsTest.Inner", ClassUtils.getShortCanonicalName("org.apache.commons.lang3.ClassUtilsTest$Inner"));
    // demonstrating what a canonical name is... it is a bigger issue to clean this up
    assertEquals("org.apache.commons.lang3.ClassUtilsTest$10", new org.apache.commons.lang3.ClassUtilsTest() {
    }.getClass().getName());
    assertNull(new org.apache.commons.lang3.ClassUtilsTest() {
    }.getClass().getCanonicalName());
}
