# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `4069652c9bdaba5724bd4e27939935aab6eb96e9`
- B: `9f7d3b5ec3aab40ee404a652495848213a608f01`
- test: `src/test/java/org/apache/commons/lang3/text/WordUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/WordUtils.java']`
- old_test_mode: `methods`
- user_chars: `10183`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2941, 'completion_tokens': 1251, 'total_tokens': 4192}`

---

- 修改 `testWrap_StringIntStringBooleanString`：生产代码现在按匹配结束位置推进并支持多字符/变宽 wrap regex，旧的单一 `@Test` 改为覆盖更多场景的参数化测试 `testWrapStringIntStringBooleanString`。
- 删除 `testZeroWidthWrapOnRegex`：零宽正则防无限循环场景已合并到新的参数化测试中，并用 `@Timeout(2)` 替代 `assertTimeout(Duration...)`。
- 需要调整 import：移除 `assertTimeout` 与 `java.time.Duration`，新增 JUnit 5 参数化测试、`@Timeout`、`Stream`、`Arguments` 与 `arguments` 静态导入。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.params.provider.Arguments.arguments;

import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.util.stream.Stream;

import org.apache.commons.lang3.AbstractLangTest;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
// IMPORTS_END

// DELETE_TESTS_START
testWrap_StringIntStringBooleanString
testZeroWidthWrapOnRegex
// DELETE_TESTS_END

static Stream<Arguments> testWrapStringIntStringBooleanString() {
    return Stream.of(
            // null passthrough
            arguments(null, -1, false, "/", null),
            // no changes test
            arguments("flammable/inflammable", 30, false, "/", "flammable/inflammable"),
            // wrap on / and small width
            arguments("flammable/inflammable", 2, false, "/", "flammable\ninflammable"),
            // wrap long words on / 1
            arguments("flammable/inflammable", 9, true, "/", "flammable\ninflammab\nle"),
            // wrap long words on / 2
            arguments("flammable/inflammable", 15, true, "/", "flammable\ninflammable"),
            // wrap long words on / 3
            arguments("flammableinflammable", 15, true, "/", "flammableinflam\nmable"),
            // default values
            arguments("a/a/a/a", -1, false, "/", "a\na\na\na"),
            arguments("a a a a", 1, false, null, "a\na\na\na"),
            // strip leading / keep trailing
            arguments("///abc///def///ghi", 3, false, "/", "abc\ndef\nghi"),
            arguments("///abc///def///ghi", 4, false, "/", "abc/\ndef/\nghi"),
            arguments("///abc///def///ghi", 5, false, "/", "abc//\ndef//\nghi"),
            // keep only two trailing, wrap on third
            arguments("///abc///def///ghi", 6, false, "/", "abc//\ndef//\nghi"),
            // zero-width regex match must advance to avoid an infinite loop
            arguments("abcabc", 3, false, "(?=a)", "abc\nabc"),
            arguments("abcdefabcdef", 4, false, "(?=a)", "abcdef\nabcdef"),
            arguments("abcdefabcdef", 4, true, "(?=a)", "abcd\nef\nabcd\nef"),
            // width two regex
            arguments("abc\\/abc", 3, false, "\\\\/", "abc\nabc"),
            arguments("abcdef\\/abcdef", 4, false, "\\\\/", "abcdef\nabcdef"),
            arguments("abcdef\\/abcdef", 4, true, "\\\\/", "abcd\nef\nabcd\nef"),
            // variable-width regex
            arguments(".abc.-def.--ghi", 5, false, "[.]-*", "abc\ndef\nghi")
            );
}

@ParameterizedTest
@MethodSource
@Timeout(2)
void testWrapStringIntStringBooleanString(final String str, final int wrapLength, final boolean wrapLongWords, final String wrapOn, final String expected) {
    assertEquals(expected, WordUtils.wrap(str, wrapLength, "\n", wrapLongWords, wrapOn));
    final String sep = System.lineSeparator();
    if (!sep.equals("\n")) {
        assertEquals(expected != null ? expected.replace("\n", sep) : null, WordUtils.wrap(str, wrapLength, null, wrapLongWords, wrapOn));
    }
}
```