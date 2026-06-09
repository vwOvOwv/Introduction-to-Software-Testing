# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e53ac03299baba72a2cb875efb4a8c1c7d374353`
- B: `7e0d6dbd2a65d8b36a4c9042565d06af34d489a0`
- test: `src/test/java/org/apache/commons/lang3/RuntimeEnvironmentTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RuntimeEnvironment.java']`
- old_test_mode: `methods`
- user_chars: `10737`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://api.deepseek.com`
- model: `deepseek-v4-pro`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3091, 'completion_tokens': 2064, 'total_tokens': 5155, 'prompt_tokens_details': {'cached_tokens': 384}, 'completion_tokens_details': {'reasoning_tokens': 1097}, 'prompt_cache_hit_tokens': 384, 'prompt_cache_miss_tokens': 2707}`

---

- 删除旧 `testIsContainer` @Test 方法，因为生产代码删除了 `inDocker`、`inPodman`、`inWsl` 并更改了 `inContainer` 的签名与逻辑。
- 新增参数化测试 `testIsContainer` 及辅助方法 `doTestInContainer`，以验证新的 `inContainer(String)` 在不同环境变量与文件存在性下的行为。
- 新增静态参数工厂方法 `testIsContainer`（作为 `@MethodSource`）和三个环境变量字符串常量。
- 新增 `@TempDir` 字段，用于创建临时文件模拟容器环境。
- 调整 import：移除 `assertDoesNotThrow`、`Test`，添加 `assertEquals`、`IOException`、`StandardCharsets`、`Files`、`Path`、`UUID`、`TempDir`、`ParameterizedTest`、`Arguments`、`MethodSource`。

```java
// IMPORTS_START
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.UUID;

import org.junit.jupiter.api.io.TempDir;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
// IMPORTS_END

// DELETE_TESTS_START
testIsContainer
// DELETE_TESTS_END

    private static final String simpleEnviron = "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\u0000" +
            "HOSTNAME=d62718b69f37\u0000TERM=xterm\u0000HOME=/root\u0000";

    private static final String podmanEnviron = "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\u0000" +
            "HOSTNAME=d62718b69f37\u0000TERM=xterm\u0000container=podman\u0000HOME=/root\u0000";

    private static final String emptyContainer = "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\u0000" +
            "HOSTNAME=d62718b69f37\u0000TERM=xterm\u0000container=\u0000HOME=/root\u0000";

    @TempDir
    private Path tempDir;

    private static Arguments[] testIsContainer() {
        return new Arguments[]{
                Arguments.of("in docker no file", simpleEnviron, null, false),
                Arguments.of("in docker with file", simpleEnviron, ".dockerenv", true),
                Arguments.of("in podman no file", podmanEnviron, "run/.containerenv", true),
                Arguments.of("in podman with file", simpleEnviron, "run/.containerenv", true),
                Arguments.of("in podman empty env var no file", emptyContainer, null, false),
                Arguments.of("in podman empty env var with file", emptyContainer, "run/.containerenv", false),
                Arguments.of("not in container", simpleEnviron, null, false),
                Arguments.of("pid1 error no file", null, null, false),
                Arguments.of("pid1 error docker file", null, ".dockerenv", true),
                Arguments.of("pid1 error podman file", null, ".dockerenv", true),
        };
    }

    @ParameterizedTest
    @MethodSource
    public void testIsContainer(String label, String environ, String fileToCreate, boolean expected) throws IOException {
        assertEquals(expected, doTestInContainer(environ, fileToCreate), label);
    }

    private boolean doTestInContainer(String environ, String fileToCreate) throws IOException {
        Path testDir = tempDir.resolve(UUID.randomUUID().toString());
        Path pid1EnvironFile = testDir.resolve("proc/1/environ");
        Files.createDirectories(pid1EnvironFile.getParent());

        if (fileToCreate != null) {
            Path file = testDir.resolve(fileToCreate);
            Files.createDirectories(file.getParent());
            Files.createFile(file);
        }

        if (environ != null) {
            Files.write(pid1EnvironFile, environ.getBytes(StandardCharsets.UTF_8));
        }

        return RuntimeEnvironment.inContainer(testDir.toString());
    }
```