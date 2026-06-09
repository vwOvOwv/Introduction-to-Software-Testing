# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `cc5ecf5db64abf0d2a2f59be16f9dc49a520dca9`
- B: `f24c027ff83b90beab2ec28696721200abb4f9e9`
- test: `src/test/java/org/apache/commons/lang3/SystemUtilsTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/SystemUtils.java']`
- old_test_mode: `full_class_fallback`
- user_chars: `162721`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 37252, 'completion_tokens': 3524, 'total_tokens': 40776}`

---

- 修改 `test_IS_JAVA`：生产代码新增 `SystemUtils.IS_JAVA_26`，测试需在 Java 版本为 `null` 和 `1.8` 分支断言该常量为 `false`，其余现代版本继续通过反射循环覆盖到最新支持版本；无需调整 import。
- 修改 `testIsJavaVersionAtLeast`：生产/测试 diff 增加 `JavaVersion.JAVA_26` 的 atLeast 覆盖，改为用当前 Java 主版本与目标版本数组统一断言，包含 `JAVA_26`；无需调整 import。
- 修改 `testIsJavaVersionAtMost`：生产/测试 diff 增加 `JavaVersion.JAVA_26` 的 atMost 覆盖，改为用当前 Java 主版本与目标版本数组统一断言，包含 `JAVA_26`；无需调整 import。

```java
@Test
@SuppressWarnings("deprecation")
void test_IS_JAVA() throws Exception {
    final String javaVersion = SystemUtils.JAVA_VERSION;
    final int lastSupportedVersion = getLastSupportedJavaVersion();
    if (javaVersion == null) {
        assertFalse(SystemUtils.IS_JAVA_1_1);
        assertFalse(SystemUtils.IS_JAVA_1_2);
        assertFalse(SystemUtils.IS_JAVA_1_3);
        assertFalse(SystemUtils.IS_JAVA_1_4);
        assertFalse(SystemUtils.IS_JAVA_1_5);
        assertFalse(SystemUtils.IS_JAVA_1_6);
        assertFalse(SystemUtils.IS_JAVA_1_7);
        assertFalse(SystemUtils.IS_JAVA_1_8);
        assertFalse(SystemUtils.IS_JAVA_1_9);
        assertFalse(SystemUtils.IS_JAVA_10);
        assertFalse(SystemUtils.IS_JAVA_11);
        assertFalse(SystemUtils.IS_JAVA_12);
        assertFalse(SystemUtils.IS_JAVA_13);
        assertFalse(SystemUtils.IS_JAVA_14);
        assertFalse(SystemUtils.IS_JAVA_15);
        assertFalse(SystemUtils.IS_JAVA_16);
        assertFalse(SystemUtils.IS_JAVA_17);
        assertFalse(SystemUtils.IS_JAVA_18);
        assertFalse(SystemUtils.IS_JAVA_19);
        assertFalse(SystemUtils.IS_JAVA_20);
        assertFalse(SystemUtils.IS_JAVA_21);
        assertFalse(SystemUtils.IS_JAVA_22);
        assertFalse(SystemUtils.IS_JAVA_23);
        assertFalse(SystemUtils.IS_JAVA_24);
        assertFalse(SystemUtils.IS_JAVA_25);
        assertFalse(SystemUtils.IS_JAVA_26);
        for (int version = 9; version <= lastSupportedVersion; version++) {
            assertFalse(getIS_JAVA(version));
        }
    } else if (javaVersion.startsWith("1.8")) {
        assertFalse(SystemUtils.IS_JAVA_1_1);
        assertFalse(SystemUtils.IS_JAVA_1_2);
        assertFalse(SystemUtils.IS_JAVA_1_3);
        assertFalse(SystemUtils.IS_JAVA_1_4);
        assertFalse(SystemUtils.IS_JAVA_1_5);
        assertFalse(SystemUtils.IS_JAVA_1_6);
        assertFalse(SystemUtils.IS_JAVA_1_7);
        assertTrue(SystemUtils.IS_JAVA_1_8);
        assertFalse(SystemUtils.IS_JAVA_1_9);
        assertFalse(SystemUtils.IS_JAVA_10);
        assertFalse(SystemUtils.IS_JAVA_11);
        assertFalse(SystemUtils.IS_JAVA_12);
        assertFalse(SystemUtils.IS_JAVA_13);
        assertFalse(SystemUtils.IS_JAVA_14);
        assertFalse(SystemUtils.IS_JAVA_15);
        assertFalse(SystemUtils.IS_JAVA_16);
        assertFalse(SystemUtils.IS_JAVA_17);
        assertFalse(SystemUtils.IS_JAVA_18);
        assertFalse(SystemUtils.IS_JAVA_19);
        assertFalse(SystemUtils.IS_JAVA_20);
        assertFalse(SystemUtils.IS_JAVA_21);
        assertFalse(SystemUtils.IS_JAVA_22);
        assertFalse(SystemUtils.IS_JAVA_23);
        assertFalse(SystemUtils.IS_JAVA_24);
        assertFalse(SystemUtils.IS_JAVA_25);
        assertFalse(SystemUtils.IS_JAVA_26);
        for (int version = 9; version <= lastSupportedVersion; version++) {
            assertFalse(getIS_JAVA(version));
        }
    } else if (!javaVersion.startsWith("1.")) {
        assertFalse(SystemUtils.IS_JAVA_1_1);
        assertFalse(SystemUtils.IS_JAVA_1_2);
        assertFalse(SystemUtils.IS_JAVA_1_3);
        assertFalse(SystemUtils.IS_JAVA_1_4);
        assertFalse(SystemUtils.IS_JAVA_1_5);
        assertFalse(SystemUtils.IS_JAVA_1_6);
        assertFalse(SystemUtils.IS_JAVA_1_7);
        assertFalse(SystemUtils.IS_JAVA_1_8);
        assertEquals(javaVersion.startsWith("9"), SystemUtils.IS_JAVA_1_9);
        for (int version = 9; version <= lastSupportedVersion; version++) {
            assertEquals(javaVersion.startsWith("" + version), getIS_JAVA(version));
        }
    } else {
        System.out.println("Can't test IS_JAVA value: " + javaVersion);
    }
}

@Test
void testIsJavaVersionAtLeast() throws Exception {
    int currentJavaVersion = SystemUtils.IS_JAVA_1_8 ? 8 : 0;
    for (int version = 9; version <= getLastSupportedJavaVersion(); version++) {
        if (getIS_JAVA(version)) {
            currentJavaVersion = version;
            break;
        }
    }
    if (currentJavaVersion == 0) {
        return;
    }

    final JavaVersion[] javaVersions = {
        JavaVersion.JAVA_1_1,
        JavaVersion.JAVA_1_2,
        JavaVersion.JAVA_1_3,
        JavaVersion.JAVA_1_4,
        JavaVersion.JAVA_1_5,
        JavaVersion.JAVA_1_6,
        JavaVersion.JAVA_1_7,
        JavaVersion.JAVA_1_8,
        JavaVersion.JAVA_9,
        JavaVersion.JAVA_10,
        JavaVersion.JAVA_11,
        JavaVersion.JAVA_12,
        JavaVersion.JAVA_13,
        JavaVersion.JAVA_14,
        JavaVersion.JAVA_15,
        JavaVersion.JAVA_16,
        JavaVersion.JAVA_17,
        JavaVersion.JAVA_18,
        JavaVersion.JAVA_19,
        JavaVersion.JAVA_20,
        JavaVersion.JAVA_21,
        JavaVersion.JAVA_22,
        JavaVersion.JAVA_23,
        JavaVersion.JAVA_24,
        JavaVersion.JAVA_25,
        JavaVersion.JAVA_26
    };
    final int[] versionNumbers = {
        1, 2, 3, 4, 5, 6, 7, 8,
        9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
    };

    for (int i = 0; i < javaVersions.length; i++) {
        assertEquals(currentJavaVersion >= versionNumbers[i], SystemUtils.isJavaVersionAtLeast(javaVersions[i]));
    }
}

@Test
void testIsJavaVersionAtMost() throws Exception {
    int currentJavaVersion = SystemUtils.IS_JAVA_1_8 ? 8 : 0;
    for (int version = 9; version <= getLastSupportedJavaVersion(); version++) {
        if (getIS_JAVA(version)) {
            currentJavaVersion = version;
            break;
        }
    }
    if (currentJavaVersion == 0) {
        return;
    }

    final JavaVersion[] javaVersions = {
        JavaVersion.JAVA_1_1,
        JavaVersion.JAVA_1_2,
        JavaVersion.JAVA_1_3,
        JavaVersion.JAVA_1_4,
        JavaVersion.JAVA_1_5,
        JavaVersion.JAVA_1_6,
        JavaVersion.JAVA_1_7,
        JavaVersion.JAVA_1_8,
        JavaVersion.JAVA_9,
        JavaVersion.JAVA_10,
        JavaVersion.JAVA_11,
        JavaVersion.JAVA_12,
        JavaVersion.JAVA_13,
        JavaVersion.JAVA_14,
        JavaVersion.JAVA_15,
        JavaVersion.JAVA_16,
        JavaVersion.JAVA_17,
        JavaVersion.JAVA_18,
        JavaVersion.JAVA_19,
        JavaVersion.JAVA_20,
        JavaVersion.JAVA_21,
        JavaVersion.JAVA_22,
        JavaVersion.JAVA_23,
        JavaVersion.JAVA_24,
        JavaVersion.JAVA_25,
        JavaVersion.JAVA_26
    };
    final int[] versionNumbers = {
        1, 2, 3, 4, 5, 6, 7, 8,
        9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26
    };

    for (int i = 0; i < javaVersions.length; i++) {
        assertEquals(currentJavaVersion <= versionNumbers[i], SystemUtils.isJavaVersionAtMost(javaVersions[i]));
    }
}
```