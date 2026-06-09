# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cc991feadbcee678635f7831ad8091ab8698d508`
- B: `63f1d6b83bc10a2880f5ec17a172fab284d2eff5`
- test: `src/test/java/org/apache/commons/lang3/text/StrLookupTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/text/StrLookup.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `9084`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 2441, 'completion_tokens': 425, 'total_tokens': 2866}`

---

- 新增 `testSystemPropertiesLookupNotSingleton`：对应生产代码中 `systemPropertiesLookup()` 从静态单例改为每次基于当前系统属性副本创建新 `StrLookup`，需验证旧 lookup 不受后续 `System.setProperty` 影响。
- import 无需调整：现有 `assertEquals`、`@Test` 已满足新增测试方法使用。

```java
    @Test
    public void testSystemPropertiesLookupNotSingleton() {
        final String osName = "os.name";
        final String originalOsName = System.getProperty(osName);

        final StrLookup<String> properties1 = StrLookup.systemPropertiesLookup();
        assertEquals(originalOsName, properties1.lookup(osName));

        final String differentOsName = "HAL-9000";
        try {
            System.setProperty(osName, differentOsName);
            final StrLookup<String> properties2 = StrLookup.systemPropertiesLookup();

            assertEquals(originalOsName, properties1.lookup(osName));
            assertEquals(differentOsName, properties2.lookup(osName));
        } finally {
            if (originalOsName == null) {
                System.clearProperty(osName);
            } else {
                System.setProperty(osName, originalOsName);
            }
        }
    }
```