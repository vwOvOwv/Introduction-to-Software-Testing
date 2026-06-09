# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `e53ac03299baba72a2cb875efb4a8c1c7d374353`
- B: `7e0d6dbd2a65d8b36a4c9042565d06af34d489a0`
- test: `src/test/java/org/apache/commons/lang3/RuntimeEnvironmentTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/RuntimeEnvironment.java']`
- old_test_mode: `methods`
- user_chars: `10737`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 3021, 'completion_tokens': 1109, 'total_tokens': 4130}`

---

- 修改 `testIsContainer`：生产代码删除了 `inDocker`、`inPodman`、`inWsl`，并新增包级 `inContainer(String dirPrefix)`，因此将旧的“不抛异常”测试改为基于临时目录的参数化断言测试。
- 新增 `testIsContainer` 的 `@MethodSource` 数据源方法 `testIsContainer()`：覆盖 `container` 环境变量、`.dockerenv`、`run/.containerenv` 以及 `/proc/1/environ` 缺失等分支。
- 需要调整 import：移除 `assertDoesNotThrow` 和 `Test`，新增 `assertEquals`、文件/路径/UUID、`TempDir` 以及 JUnit Params 相关 import。

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