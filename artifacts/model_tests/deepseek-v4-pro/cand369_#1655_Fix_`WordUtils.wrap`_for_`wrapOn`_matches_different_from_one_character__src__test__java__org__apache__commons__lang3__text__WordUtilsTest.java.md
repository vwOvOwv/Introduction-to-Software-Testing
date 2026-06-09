# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `4069652c9bdaba5724bd4e27939935aab6eb96e9`
- B: `9f7d3b5ec3aab40ee404a652495848213a608f01`
- test: `src/test/java/org/apache/commons/lang3/text/WordUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/WordUtils.java']`
- old_test_mode: `methods`
- user_chars: `10183`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2990, 'completion_tokens': 2271, 'total_tokens': 5261, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1205}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2606}`

---

- 新增 `@ParameterizedTest` 方法 `testWrapStringIntStringBooleanString`，用于替换旧的手动测试 `testWrap_StringIntStringBooleanString` 和零宽环绕测试 `testZeroWidthWrapOnRegex`，并整合了超时控制与系统换行符断言。  
- 新增静态工厂方法 `testWrapStringIntStringBooleanString`，提供参数化数据，覆盖原有测试用例及更多边界场景。  
- 删除旧测试方法 `testWrap_StringIntStringBooleanString` 和 `testZeroWidthWrapOnRegex`。  
- 需要调整 import：移除 `assertTimeout` 和 `Duration`，新增 `arguments`、`Stream`、`Timeout`、`ParameterizedTest`、`Arguments`、`MethodSource`。

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