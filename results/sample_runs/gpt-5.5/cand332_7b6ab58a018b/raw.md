# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `7a304cfc7b405af7fea9e9d9c25ccae283c8d708`
- B: `7b6ab58a018b5f6608ea07bc414d3f34a576c6a2`
- test: `src/test/java/org/apache/commons/lang3/ObjectUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/ObjectUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `17855`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 4505, 'completion_tokens': 1074, 'total_tokens': 5579}`

---

- 新增 `testCloneOfCloneable`，覆盖新增的 `ObjectUtils.clone(Object)` 对可克隆对象返回克隆实例的行为。
- 新增 `testCloneOfNotCloneable`，覆盖新增的 `ObjectUtils.clone(Object)` 对非 `Cloneable` 对象返回 `null` 的行为。
- 新增 `testCloneOfUncloneable`，覆盖新增的 `ObjectUtils.clone(Object)` 对声明 `Cloneable` 但无公开 `clone` 方法时抛出 `CloneFailedException` 的行为。
- 新增 `testPossibleCloneOfCloneable`，覆盖新增的 `ObjectUtils.cloneIfPossible(Object)` 对可克隆对象返回克隆实例的行为。
- 新增 `testPossibleCloneOfNotCloneable`，覆盖新增的 `ObjectUtils.cloneIfPossible(Object)` 对非 `Cloneable` 对象返回原对象的行为。
- 新增 `testPossibleCloneOfUncloneable`，覆盖新增的 `ObjectUtils.cloneIfPossible(Object)` 传播克隆失败异常的行为。
- 需要调整 import，新增 `CloneFailedException` 与 `MutableObject`，其余旧 import 保持不变。

```java
// IMPORTS_START
import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.util.Calendar;
import java.util.Date;

import org.apache.commons.lang3.exception.CloneFailedException;
import org.apache.commons.lang3.mutable.MutableObject;

import junit.framework.TestCase;
// IMPORTS_END

    /**
     * Tests {@link ObjectUtils#clone(Object)} with a cloneable object.
     */
    public void testCloneOfCloneable() {
        final CloneableString string = new CloneableString("apache");
        final CloneableString stringClone = ObjectUtils.clone(string);
        assertEquals("apache", stringClone.getValue());
    }

    /**
     * Tests {@link ObjectUtils#clone(Object)} with a not cloneable object.
     */
    public void testCloneOfNotCloneable() {
        final String string = new String("apache");
        assertNull(ObjectUtils.clone(string));
    }

    /**
     * Tests {@link ObjectUtils#clone(Object)} with an uncloneable object.
     */
    public void testCloneOfUncloneable() {
        final UncloneableString string = new UncloneableString("apache");
        try {
            ObjectUtils.clone(string);
            fail("Thrown " + CloneFailedException.class.getName() + " expected");
        } catch (final CloneFailedException e) {
            assertEquals(NoSuchMethodException.class, e.getCause().getClass());
        }
    }

    /**
     * Tests {@link ObjectUtils#cloneIfPossible(Object)} with a cloneable object.
     */
    public void testPossibleCloneOfCloneable() {
        final CloneableString string = new CloneableString("apache");
        final CloneableString stringClone = ObjectUtils.cloneIfPossible(string);
        assertEquals("apache", stringClone.getValue());
    }

    /**
     * Tests {@link ObjectUtils#cloneIfPossible(Object)} with a not cloneable object.
     */
    public void testPossibleCloneOfNotCloneable() {
        final String string = new String("apache");
        assertSame(string, ObjectUtils.cloneIfPossible(string));
    }

    /**
     * Tests {@link ObjectUtils#cloneIfPossible(Object)} with an uncloneable object.
     */
    public void testPossibleCloneOfUncloneable() {
        final UncloneableString string = new UncloneableString("apache");
        try {
            ObjectUtils.cloneIfPossible(string);
            fail("Thrown " + CloneFailedException.class.getName() + " expected");
        } catch (final CloneFailedException e) {
            assertEquals(NoSuchMethodException.class, e.getCause().getClass());
        }
    }

    /**
     * String that is cloneable.
     */
    static final class CloneableString extends MutableObject<String> implements Cloneable {
        private static final long serialVersionUID = 1L;

        CloneableString(final String s) {
            super(s);
        }

        @Override
        public CloneableString clone() throws CloneNotSupportedException {
            return (CloneableString) super.clone();
        }
    }

    /**
     * String that is not cloneable.
     */
    static final class UncloneableString extends MutableObject<String> implements Cloneable {
        private static final long serialVersionUID = 1L;

        UncloneableString(final String s) {
            super(s);
        }
    }
```