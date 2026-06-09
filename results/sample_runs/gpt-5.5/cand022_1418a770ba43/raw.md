# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `3f803b8bf78602c9464b2d01023634e32df1c388`
- B: `1418a770ba436d15693c3bb29a67e501c2008274`
- test: `src/test/java/org/apache/commons/lang3/builder/RecursiveToStringStyleTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/RecursiveToStringStyle.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `17275`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 4887, 'completion_tokens': 1239, 'total_tokens': 6126}`

---

- 新增 `testAtomicsArray`：覆盖 `RecursiveToStringStyle.accept()` 现在不递归 `AtomicBoolean`，且 `AtomicInteger` / `AtomicLong` 作为 `Number` 子类按普通值输出。
- 新增 `testBigDecimal`：覆盖 `accept()` 现在过滤 `Number` 子类，避免 `BigDecimal` 被递归反射展开。
- 新增 `testBigInteger`：覆盖 `accept()` 现在过滤 `Number` 子类，避免 `BigInteger` 被递归反射展开。
- 新增 `testMutableWrapperArray`：覆盖 `accept()` 现在过滤 `MutableBoolean`，并验证其他 mutable number wrapper 按普通值输出。
- 需要调整 import：新增 `BigDecimal`、`BigInteger`、atomic 类型以及 mutable wrapper 类型的导入。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

import org.apache.commons.lang3.AbstractLangTest;
import org.apache.commons.lang3.mutable.MutableBoolean;
import org.apache.commons.lang3.mutable.MutableByte;
import org.apache.commons.lang3.mutable.MutableDouble;
import org.apache.commons.lang3.mutable.MutableFloat;
import org.apache.commons.lang3.mutable.MutableInt;
import org.apache.commons.lang3.mutable.MutableLong;
import org.apache.commons.lang3.mutable.MutableShort;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
// IMPORTS_END

@Test
void testAtomicsArray() {
    assertEquals(baseStr + "[{<null>,5,{3,6}}]",
            new ToStringBuilder(base).append(new Object[] { null, base, new AtomicLong[] { new AtomicLong(3), new AtomicLong(6) } }).toString());
    assertEquals(baseStr + "[{<null>,5,{3,6}}]",
            new ToStringBuilder(base).append(new Object[] { null, base, new AtomicInteger[] { new AtomicInteger(3), new AtomicInteger(6) } }).toString());
    assertEquals(baseStr + "[{<null>,5,{true,false}}]",
            new ToStringBuilder(base).append(new Object[] { null, base, new AtomicBoolean[] { new AtomicBoolean(true), new AtomicBoolean(false) } }).toString());
}

@Test
void testBigDecimal() {
    assertEquals(baseStr + "[{<null>,5,{3,6}}]",
            new ToStringBuilder(base).append(new Object[] { null, base, new BigDecimal[] { BigDecimal.valueOf(3), BigDecimal.valueOf(6) } }).toString());
    assertEquals(baseStr + "[{<null>,5,{3.0,6.0}}]",
            new ToStringBuilder(base).append(new Object[] { null, base, new BigDecimal[] { BigDecimal.valueOf(3.0), BigDecimal.valueOf(6.0) } }).toString());
}

@Test
void testBigInteger() {
    assertEquals(baseStr + "[{<null>,5,{3,6}}]",
            new ToStringBuilder(base).append(new Object[] { null, base, new BigInteger[] { BigInteger.valueOf(3), BigInteger.valueOf(6) } }).toString());
}

@Test
void testMutableWrapperArray() {
    assertEquals(baseStr + "[{<null>,5,{3,6}}]",
            new ToStringBuilder(base).append(new Object[] { null, base, new MutableLong[] { new MutableLong(3), new MutableLong(6) } }).toString());
    assertEquals(baseStr + "[{<null>,5,{3,6}}]",
            new ToStringBuilder(base).append(new Object[] { null, base, new MutableInt[] { new MutableInt(3), new MutableInt(6) } }).toString());
    assertEquals(baseStr + "[{<null>,5,{3,6}}]",
            new ToStringBuilder(base).append(new Object[] { null, base, new MutableShort[] { new MutableShort(3), new MutableShort(6) } }).toString());
    assertEquals(baseStr + "[{<null>,5,{3,6}}]",
            new ToStringBuilder(base).append(new Object[] { null, base, new MutableByte[] { new MutableByte((byte) 3), new MutableByte((byte) 6) } }).toString());
    assertEquals(baseStr + "[{<null>,5,{3.0,6.0}}]",
            new ToStringBuilder(base).append(new Object[] { null, base, new MutableFloat[] { new MutableFloat(3f), new MutableFloat(6f) } }).toString());
    assertEquals(baseStr + "[{<null>,5,{3.0,6.0}}]",
            new ToStringBuilder(base).append(new Object[] { null, base, new MutableDouble[] { new MutableDouble(3d), new MutableDouble(6d) } }).toString());
    assertEquals(baseStr + "[{<null>,5,{true,false}}]",
            new ToStringBuilder(base).append(new Object[] { null, base, new MutableBoolean[] { new MutableBoolean(true), new MutableBoolean(false) } }).toString());
}
```