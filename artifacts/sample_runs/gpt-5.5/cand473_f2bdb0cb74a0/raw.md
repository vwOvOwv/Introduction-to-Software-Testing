# 模型输出

- repo: `/home/lpy/workspace/misc/course/commons-lang`
- A: `d68bf970beb14fa569e7e629c625ba48c01c2ddc`
- B: `f2bdb0cb74a08b15439abf18df6ac2b52549394a`
- test: `src/test/java/org/apache/commons/lang3/BitFieldTest.java`
- prod: `['src/main/java/org/apache/commons/lang3/BitField.java']`
- old_test_mode: `methods`
- user_chars: `30546`
- input_truncated: `{'prod_diff': False, 'prod_methods_b': False, 'test_diff': False, 'old_test': False}`
- api_base: `https://yunwu.ai`
- model: `gpt-5.5`
- max_output_tokens: `8192`
- finish_reason: `stop`
- usage: `{'prompt_tokens': 9534, 'completion_tokens': 1264, 'total_tokens': 10798}`

---

- 修改 `testByte` 为 `testByteBoolean`，仅对照测试 diff 中方法重命名，生产代码行为未变。
- 修改 `testClear` 为 `testClearInt`，继续断言 `clear(int)` 在 `mask` 改为 `long` 后仍返回正确的 `int` 结果。
- 新增 `testClearLong`，对照生产代码新增的 `clear(long)` 重载方法补充 long 入参断言。
- import 无需调整。

```java
// DELETE_TESTS_START
testByte
testClear
// DELETE_TESTS_END

@Test
void testByteBoolean() {
    assertEquals(0, new BitField(0).setByteBoolean((byte) 0, true));
    assertEquals(1, new BitField(1).setByteBoolean((byte) 0, true));
    assertEquals(2, new BitField(2).setByteBoolean((byte) 0, true));
    assertEquals(4, new BitField(4).setByteBoolean((byte) 0, true));
    assertEquals(8, new BitField(8).setByteBoolean((byte) 0, true));
    assertEquals(16, new BitField(16).setByteBoolean((byte) 0, true));
    assertEquals(32, new BitField(32).setByteBoolean((byte) 0, true));
    assertEquals(64, new BitField(64).setByteBoolean((byte) 0, true));
    assertEquals(-128, new BitField(128).setByteBoolean((byte) 0, true));
    assertEquals(1, new BitField(0).setByteBoolean((byte) 1, false));
    assertEquals(0, new BitField(1).setByteBoolean((byte) 1, false));
    assertEquals(0, new BitField(2).setByteBoolean((byte) 2, false));
    assertEquals(0, new BitField(4).setByteBoolean((byte) 4, false));
    assertEquals(0, new BitField(8).setByteBoolean((byte) 8, false));
    assertEquals(0, new BitField(16).setByteBoolean((byte) 16, false));
    assertEquals(0, new BitField(32).setByteBoolean((byte) 32, false));
    assertEquals(0, new BitField(64).setByteBoolean((byte) 64, false));
    assertEquals(0, new BitField(128).setByteBoolean((byte) 128, false));
    assertEquals(-2, new BitField(1).setByteBoolean((byte) 255, false));
    final byte clearedBit = new BitField(0x40).setByteBoolean((byte) - 63, false);
    assertFalse(new BitField(0x40).isSet(clearedBit));
}

@Test
void testClearInt() {
    assertEquals(bf_multi.clear(-1), 0xFFFFC07F);
    assertEquals(bf_single.clear(-1), 0xFFFFBFFF);
    assertEquals(bf_zero.clear(-1), 0xFFFFFFFF);
}

@Test
void testClearLong() {
    assertEquals(bf_multi.clear(-1L), 0xFFFFC07FL);
    assertEquals(bf_single.clear(-1L), 0xFFFFBFFFL);
    assertEquals(bf_zero.clear(-1L), 0xFFFFFFFFL);
}
```