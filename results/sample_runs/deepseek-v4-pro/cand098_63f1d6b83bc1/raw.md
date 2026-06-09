# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cc991feadbcee678635f7831ad8091ab8698d508`
- B: `63f1d6b83bc10a2880f5ec17a172fab284d2eff5`
- test: `src/test/java/org/apache/commons/lang3/text/StrLookupTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/StrLookup.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `9084`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2575, 'completion_tokens': 1712, 'total_tokens': 4287, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1460}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2191}`

---

- 新增 `testSystemPropertiesLookupNotSingleton` 方法：验证 `systemPropertiesLookup()` 不再返回单例，每次调用返回属性快照副本，与生产代码从静态单例改为每次拷贝系统属性的变更保持一致。
- 无需修改或删除已有测试方法，原有 `testNoneLookup`、`testSystemProperiesLookup`、`testMapLookup`、`testMapLookup_nullMap` 保持不变。
- 无需调整 import ，测试类已存在所需依赖。

```java
    @Test
    public void testSystemPropertiesLookupNotSingleton() {
        final String osName = "os.name";
        final String originalOsName = System.getProperty(osName);

        StrLookup properties1 = StrLookup.systemPropertiesLookup();
        assertEquals(originalOsName, properties1.lookup(osName));

        final String differentOsName = "HAL-9000";
        System.setProperty(osName, differentOsName);
        StrLookup properties2 = StrLookup.systemPropertiesLookup();

        assertEquals(originalOsName, properties1.lookup(osName));
        assertEquals(differentOsName, properties2.lookup(osName));
    }
```