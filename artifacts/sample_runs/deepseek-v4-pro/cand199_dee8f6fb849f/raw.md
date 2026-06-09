# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `68cb8af7e402041e33e931f33bc60a32d7b9ce95`
- B: `dee8f6fb849fd3b7d928f13e273f8160f0a45f5b`
- test: `src/test/java/org/apache/commons/lang3/CharSequenceUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/CharSequenceUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `16850`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 4418, 'completion_tokens': 3066, 'total_tokens': 7484, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2064}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 4034}`

---

- 新增 `@Test` 方法 `testNewLastIndexOf`，用于覆盖 `CharSequenceUtils.lastIndexOf` 重构后的行为，包括随机长字符串场景。
- 新增三个私有辅助方法：`testNewLastIndexOfSingle(CharSequence, CharSequence)`、`testNewLastIndexOfSingle(CharSequence, CharSequence, int)` 和 `testNewLastIndexOfSingleSingle(CharSequence, CharSequence, int)`，封装多起始位置的预期验证。
- 新增内部类 `WrapperString`（实现 `CharSequence`），作为非 `String`/`StringBuilder`/`StringBuffer` 的 `CharSequence` 测试桩。
- 调整 `import` 区块：新增 `import static java.nio.CharBuffer.wrap;`、`import java.nio.CharBuffer;`、`import java.util.Random;`、`import java.util.stream.IntStream;`、`import org.apache.commons.lang3.text.StrBuilder;`，以支撑新增测试代码。

```java
// IMPORTS_START
import static java.nio.CharBuffer.wrap;
import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.nio.CharBuffer;
import java.util.Random;
import java.util.stream.IntStream;

import org.apache.commons.lang3.text.StrBuilder;
import org.junit.jupiter.api.Test;
// IMPORTS_END

    static class WrapperString implements CharSequence {
        CharSequence inner;

        public WrapperString(CharSequence inner) {
            this.inner = inner;
        }

        @Override
        public int length() {
            return inner.length();
        }

        @Override
        public char charAt(int index) {
            return inner.charAt(index);
        }

        @Override
        public CharSequence subSequence(int start, int end) {
            return inner.subSequence(start, end);
        }

        @Override
        public String toString() {
            return inner.toString();
        }

        @Override
        public IntStream chars() {
            return inner.chars();
        }

        @Override
        public IntStream codePoints() {
            return inner.codePoints();
        }
    }

    @Test
    public void testNewLastIndexOf() {
        testNewLastIndexOfSingle("808087847-1321060740-635567660180086727-925755305", "-1321060740-635567660", 21);
        testNewLastIndexOfSingle("", "");
        testNewLastIndexOfSingle("1", "");
        testNewLastIndexOfSingle("", "1");
        testNewLastIndexOfSingle("1", "1");
        testNewLastIndexOfSingle("11", "1");
        testNewLastIndexOfSingle("1", "11");

        Random random = new Random();
        StringBuilder seg = new StringBuilder();
        while (seg.length() <= CharSequenceUtils.TO_STRING_LIMIT) {
            seg.append(random.nextInt());
        }
        StringBuilder original = new StringBuilder(seg);
        testNewLastIndexOfSingle(original, seg);
        for (int i = 0; i < 100; i++) {
            if (random.nextDouble() < 0.5) {
                original.append(random.nextInt() % 10);
            } else {
                original = new StringBuilder().append(String.valueOf(random.nextInt() % 100)).append(original);
            }
            testNewLastIndexOfSingle(original, seg);
        }
    }

    private void testNewLastIndexOfSingle(CharSequence a, CharSequence b) {
        int maxa = Math.max(a.length(), b.length());
        for (int i = -maxa-10; i <= maxa+10; i++) {
            testNewLastIndexOfSingle(a, b, i);
        }
    }

    private void testNewLastIndexOfSingle(CharSequence a, CharSequence b, int start) {
        testNewLastIndexOfSingleSingle(a, b, start);
        testNewLastIndexOfSingleSingle(b, a, start);
    }

    private void testNewLastIndexOfSingleSingle(CharSequence a, CharSequence b, int start) {
        int expected = a.toString().lastIndexOf(b.toString(), start);
        assertEquals(
                expected,
                CharSequenceUtils.lastIndexOf(new WrapperString(a.toString()), b.toString(), start),
                "testNewLastIndexOf fails! original : " + a + " seg : " + b + " start : " + start
        );
    }
```