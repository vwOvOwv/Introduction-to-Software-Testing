# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `ae6a24dd439a7b778e35b484a3a6eae1a8eb64d7`
- B: `f56931c176fef5e164b681c740746aebdccccec3`
- test: `src/test/java/org/apache/commons/lang3/time/FastDateParserTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/time/FastDateParser.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `52418`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 13328, 'completion_tokens': 2265, 'total_tokens': 15593, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 2093}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 12944}`

---

- 新增 `testLang1380` 测试方法，验证法语月份缩写中可选尾部句点（`.`）的解析；无需调整任何 import，现有 import 已包含所需依赖。

```java
@Test
public void testLang1380() throws ParseException {
    final Calendar expected = Calendar.getInstance(GMT, Locale.FRANCE);
    expected.clear();
    expected.set(2014, Calendar.APRIL, 14);

    final DateParser fdp = getInstance("dd MMM yyyy", GMT, Locale.FRANCE);
    assertEquals(expected.getTime(), fdp.parse("14 avril 2014"));
    assertEquals(expected.getTime(), fdp.parse("14 avr. 2014"));
    assertEquals(expected.getTime(), fdp.parse("14 avr 2014"));
}
```