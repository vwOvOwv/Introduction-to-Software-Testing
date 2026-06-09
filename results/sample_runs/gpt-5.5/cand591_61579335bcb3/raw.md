# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `03fe88ab71cf2eadaa39654786c3fba713742768`
- B: `61579335bcb3da854fc8be82b5e61dc52b5018d3`
- test: `src/test/java/org/apache/commons/lang3/time/FastDateFormatTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/FastDateFormat.java']`
- old_test_mode: `methods`
- user_chars: `12702`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3365, 'completion_tokens': 1869, 'total_tokens': 5234}`

---

- 修改 `testParseSync`：生产代码 `FastDateFormat.format(Object, StringBuffer, FieldPosition)` 改为通过 `printer.format(obj)` 追加结果，测试同步解析性能时需同时覆盖格式化与解析路径，并改用线程安全包装的 `Format`。
- 不修改 `testLANG_1152`：该断言与本次生产代码变更无关，在 B 上仍应保持原行为。
- 需要调整 import：新增 `FieldPosition`、`ParsePosition`、`AtomicLongArray`，移除不再使用的 `ParseException`、`AtomicLong`。

```java
// IMPORTS_START
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertNotSame;
import static org.junit.Assert.assertSame;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.text.FieldPosition;
import java.text.Format;
import java.text.ParsePosition;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;
import java.util.TimeZone;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLongArray;

import org.apache.commons.lang3.test.SystemDefaults;
import org.apache.commons.lang3.test.SystemDefaultsSwitch;
import org.junit.Assert;
import org.junit.Rule;
import org.junit.Test;
// IMPORTS_END

@Test
public void testParseSync() throws InterruptedException {
    final String pattern = "yyyy-MM-dd'T'HH:mm:ss.SSS";
    final SimpleDateFormat inner = new SimpleDateFormat(pattern);
    final Format sdf = new Format() {
        private static final long serialVersionUID = 1L;

        @Override
        public StringBuffer format(final Object obj, final StringBuffer toAppendTo, final FieldPosition fieldPosition) {
            synchronized (this) {
                return inner.format(obj, toAppendTo, fieldPosition);
            }
        }

        @Override
        public Object parseObject(final String source, final ParsePosition pos) {
            synchronized (this) {
                return inner.parseObject(source, pos);
            }
        }
    };

    final AtomicLongArray sdfTime = measureTime(sdf, sdf);

    final Format fdf = FastDateFormat.getInstance(pattern);
    final AtomicLongArray fdfTime = measureTime(fdf, fdf);

    System.out.println(">>FastDateFormatTest: FastDatePrinter:" + fdfTime.get(0) + "  SimpleDateFormat:" + sdfTime.get(0));
    System.out.println(">>FastDateFormatTest: FastDateParser:" + fdfTime.get(1) + "  SimpleDateFormat:" + sdfTime.get(1));
}

private AtomicLongArray measureTime(final Format printer, final Format parser) throws InterruptedException {
    final ExecutorService pool = Executors.newFixedThreadPool(NTHREADS);
    final AtomicInteger failures = new AtomicInteger(0);
    final AtomicLongArray totalElapsed = new AtomicLongArray(2);

    for (int i = 0; i < NTHREADS; ++i) {
        pool.submit(new Runnable() {
            @Override
            public void run() {
                for (int j = 0; j < NROUNDS; ++j) {
                    try {
                        final Date date = new Date();

                        final long t0 = System.currentTimeMillis();
                        final String formattedDate = printer.format(date);
                        totalElapsed.addAndGet(0, System.currentTimeMillis() - t0);

                        final long t1 = System.currentTimeMillis();
                        final Object pd = parser.parseObject(formattedDate);
                        totalElapsed.addAndGet(1, System.currentTimeMillis() - t1);

                        if (!date.equals(pd)) {
                            failures.incrementAndGet();
                        }
                    } catch (final Exception e) {
                        failures.incrementAndGet();
                    }
                }
            }
        });
    }

    pool.shutdown();
    if (!pool.awaitTermination(20, TimeUnit.SECONDS)) {
        fail("did not complete tasks");
    }
    assertEquals(0, failures.get());
    return totalElapsed;
}
```