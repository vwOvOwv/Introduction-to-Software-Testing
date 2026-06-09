# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `eff43864b34ab2be2eae4e9ac0e780d34fab57b3`
- B: `25e91c4242283d118ba978d4f38cd18e10c890dc`
- test: `src/test/java/org/apache/commons/lang3/time/CalendarUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/CalendarUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `7670`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2249, 'completion_tokens': 561, 'total_tokens': 2810}`

---

- 新增 `testGetStandaloneLongMonthNames`，覆盖新增的 `CalendarUtils.getInstance(Locale).getStandaloneLongMonthNames()` 德语独立长月份名行为。
- 新增 `testGetStandaloneShortMonthNames`，覆盖新增的 `CalendarUtils.getInstance(Locale).getStandaloneShortMonthNames()` 德语独立短月份名行为。
- 需要调整 import：新增 `java.util.Locale` 以支持按 Locale 获取月份显示名。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Calendar;
import java.util.Locale;

import org.junit.jupiter.api.Test;
// IMPORTS_END

@Test
public void testGetStandaloneLongMonthNames() {
    final String[] monthNames = CalendarUtils.getInstance(Locale.GERMAN).getStandaloneLongMonthNames();
    assertEquals(12, monthNames.length);
    assertEquals("Januar", monthNames[0]);
    assertEquals("Februar", monthNames[1]);
    assertEquals("M\u00e4rz", monthNames[2]);
    assertEquals("April", monthNames[3]);
    assertEquals("Mai", monthNames[4]);
    assertEquals("Juni", monthNames[5]);
    assertEquals("Juli", monthNames[6]);
    assertEquals("August", monthNames[7]);
    assertEquals("September", monthNames[8]);
    assertEquals("Oktober", monthNames[9]);
    assertEquals("November", monthNames[10]);
    assertEquals("Dezember", monthNames[11]);
}

@Test
public void testGetStandaloneShortMonthNames() {
    final String[] monthNames = CalendarUtils.getInstance(Locale.GERMAN).getStandaloneShortMonthNames();
    assertEquals(12, monthNames.length);
    assertEquals("Jan", monthNames[0]);
    assertEquals("Feb", monthNames[1]);
    assertEquals("M\u00e4r", monthNames[2]);
    assertEquals("Apr", monthNames[3]);
    assertEquals("Mai", monthNames[4]);
    assertEquals("Jun", monthNames[5]);
    assertEquals("Jul", monthNames[6]);
    assertEquals("Aug", monthNames[7]);
    assertEquals("Sep", monthNames[8]);
    assertEquals("Okt", monthNames[9]);
    assertEquals("Nov", monthNames[10]);
    assertEquals("Dez", monthNames[11]);
}
```