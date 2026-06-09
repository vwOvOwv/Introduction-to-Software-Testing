# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `91ccf53c7d358f8cdc906a023e306d675e3c30d8`
- B: `95a0e2b09bc4a3a363e5ab1c853d002fb74ad7af`
- test: `src/test/java/org/apache/commons/lang3/text/StrLookupTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/StrLookup.java']`
- old_test_mode: `methods`
- user_chars: `2853`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 1084, 'completion_tokens': 396, 'total_tokens': 1480}`

---

- 修改 `testSystemPropertiesLookup`：生产代码改为通过 `SystemProperties.getProperty(key)` 查询，`null` key 不再抛出 `NullPointerException`，旧断言需改为 `assertNull`。
- 调整 import：删除不再使用的 `assertThrows` 静态导入，保留 `assertEquals` 与 `assertNull`。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

import java.util.HashMap;
import java.util.Map;

import org.junit.jupiter.api.Test;
// IMPORTS_END

@Test
public void testSystemPropertiesLookup() {
    assertEquals(System.getProperty("os.name"), StrLookup.systemPropertiesLookup().lookup("os.name"));
    assertNull(StrLookup.systemPropertiesLookup().lookup(""));
    assertNull(StrLookup.systemPropertiesLookup().lookup("other"));
    assertNull(StrLookup.systemPropertiesLookup().lookup(null));
}
```