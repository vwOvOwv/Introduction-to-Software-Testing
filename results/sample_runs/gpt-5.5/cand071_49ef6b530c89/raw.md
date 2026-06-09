# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ce40e5bdf29138c17b934b84206b31ece5ebd3e3`
- B: `49ef6b530c89c5f7181aa3fbdb957155a6802b05`
- test: `src/test/java/org/apache/commons/lang3/builder/HashCodeBuilderTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/builder/HashCodeBuilder.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `27732`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 8401, 'completion_tokens': 371, 'total_tokens': 8772}`

---

- 新增 `testEquals`：覆盖生产代码新增的 `HashCodeBuilder.equals(Object)`，验证同一实例、相同累计值实例以及不同累计值实例的相等/不相等行为。
- 需要调整 import：新增静态导入 `assertNotEquals` 以断言不同 `HashCodeBuilder` 实例不相等。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.apache.commons.lang3.AbstractLangTest;
import org.junit.jupiter.api.Test;
// IMPORTS_END

@Test
public void testEquals() {
    final HashCodeBuilder hcb1 = new HashCodeBuilder(17, 37).append(1).append('a');
    final HashCodeBuilder hcb2 = new HashCodeBuilder(17, 37).append(1).append('a');
    final HashCodeBuilder hcb3 = new HashCodeBuilder(17, 37).append(2).append('c');
    assertEquals(hcb1, hcb1);
    assertEquals(hcb1, hcb2);
    assertEquals(hcb2, hcb1);
    assertNotEquals(hcb1, hcb3);
    assertNotEquals(hcb2, hcb3);
}
```