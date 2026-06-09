# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `8c1a0d2ee1433681958809b4a0fede65f62936e6`
- B: `a08ec31dbf212a033953dc6916a743dccbb93e37`
- test: `src/test/java/org/apache/commons/lang3/text/WordUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/WordUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `24161`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 6378, 'completion_tokens': 1559, 'total_tokens': 7937, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1350}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 5994}`

---

- 修改 import：将 `import static org.junit.Assert.assertEquals;` 等四行分立静态导入替换为 `import static org.junit.Assert.*;`，以匹配生产/测试 diff 的导入变更。
- 新增 @Test 方法 `testLANG1292`：根据测试 diff 添加此方法，验证 LANG-1292 修复后不再抛出 StringIndexOutOfBoundsException。

```java
// IMPORTS_START
import static org.junit.Assert.*;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;

import org.apache.commons.lang3.SystemUtils;
import org.junit.Test;
// IMPORTS_END

    @Test
    public void testLANG1292() throws Exception {
        // Prior to fix, this was throwing StringIndexOutOfBoundsException
        WordUtils.wrap("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa "
                + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa "
                + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",70);
    }
```