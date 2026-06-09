# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `3ff366c3db53f3687b40b0c15c14cdeb27ac8252`
- B: `40134ecdb327d1b82936f7ee3fa925b7b181c726`
- test: `src/test/java/org/apache/commons/lang3/time/FastDateParserTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/FastDateParser.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `87261`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 20502, 'completion_tokens': 907, 'total_tokens': 21409, 'prompt_tokens_details': {'cached_tokens': 20224}}`

---

- 新增 `@Test` 方法 `testJpLocales`，对应生产代码本次重写本地化文本解析策略后补充中文 locale 回归覆盖。
- 修改辅助方法 `testSdfAndFdp`，移除对已删除的 `FastDateParser#getParsePattern()` 的调用以适配生产代码 API 删除。
- 需要调整 import：新增 `org.apache.commons.lang3.LocaleUtils`，其余 import 保持不变。

```java
// IMPORTS_START
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.io.Serializable;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.TimeZone;

import org.apache.commons.lang3.LocaleUtils;
import org.apache.commons.lang3.SerializationUtils;
import org.junit.Assert;
import org.junit.Test;
// IMPORTS_END

@Test
public void testJpLocales() {

    final Calendar cal= Calendar.getInstance(GMT);
    cal.clear();
    cal.set(2003, Calendar.FEBRUARY, 10);
    cal.set(Calendar.ERA, GregorianCalendar.BC);

    final Locale locale = LocaleUtils.toLocale("zh"); {
        // ja_JP_JP cannot handle dates before 1868 properly

        final SimpleDateFormat sdf = new SimpleDateFormat(LONG_FORMAT, locale);
        final DateParser fdf = getInstance(LONG_FORMAT, locale);

        try {
            checkParse(locale, cal, sdf, fdf);
        } catch(final ParseException ex) {
            Assert.fail("Locale "+locale+ " failed with "+LONG_FORMAT+"\n" + trimMessage(ex.toString()));
        }
    }
}

private void testSdfAndFdp(final String format, final String date, final boolean shouldFail)
        throws Exception {
    Date dfdp = null;
    Date dsdf = null;
    Throwable f = null;
    Throwable s = null;

    try {
        final SimpleDateFormat sdf = new SimpleDateFormat(format, Locale.US);
        sdf.setTimeZone(NEW_YORK);
        dsdf = sdf.parse(date);
        if (shouldFail) {
            Assert.fail("Expected SDF failure, but got " + dsdf + " for ["+format+","+date+"]");
        }
    } catch (final Exception e) {
        s = e;
        if (!shouldFail) {
            throw e;
        }
    }

    try {
        final DateParser fdp = getInstance(format, NEW_YORK, Locale.US);
        dfdp = fdp.parse(date);
        if (shouldFail) {
            Assert.fail("Expected FDF failure, but got " + dfdp + " for ["+format+","+date+"]");
        }
    } catch (final Exception e) {
        f = e;
        if (!shouldFail) {
            throw e;
        }
    }
    // SDF and FDF should produce equivalent results
    assertTrue("Should both or neither throw Exceptions", (f==null)==(s==null));
    assertEquals("Parsed dates should be equal", dsdf, dfdp);
}
```