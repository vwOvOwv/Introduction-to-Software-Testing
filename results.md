# commons-lang 样本测试结果（135 条）

执行时间：2026-05-20 23:01:21（批量实验完成）

说明：

- 样本池：`artifacts/lang_sample_candidates_filtered.json`，共 **135** 条。
- 流水线：`run_sample_experiment.py` → `update_tests_deepseek.py`（DeepSeek）→ 合并进 A 底本并 **从 B 同步 import / 嵌套类** → `run_single_maven_test.py` 在 **B** 上执行 `mvn -q -Dtest=<TestClass> test`。
- 结果来源：逐个扫描 `artifacts/sample_runs/candNNN_*/run_report.json` 和生成产物目录。
- **「通过」** 指 `maven.returncode=0`（该测试类在 B 上可编译且测试全绿），不表示与 PR 金标准 diff 完全一致。

## 总体统计

| 指标 | 数量 | 占比 |
| --- | ---: | ---: |
| 样本总数 | 135 | 100% |
| DeepSeek 有输出（`raw.md` / `deepseek_output.md`） | 135 | 100.0% |
| **Maven 通过**（`returncode=0`） | **132** | **97.8%** |
| 编译失败（`COMPILATION ERROR`） | 3 | 2.2% |
| 测试失败（已编译，`Tests run` 失败） | 0 | 0.0% |
| 合并失败（无 `@Test` 可合并） | 0 | 0.0% |
| 其它 Maven 非 0 | 0 | 0.0% |

## 结论摘要

- 在「A 底本 + 模型只改 `@Test` + 从 B 补 import/一层嵌套类」设定下，**约 98%** 样本能在 B 上跑通聚焦测试类。
- 主要失败形态：**编译失败**（缺符号/import/深层嵌套类，约 3 条）> **测试失败**（逻辑/断言未对齐，约 0 条）> **合并失败**（模型未输出可解析 `@Test`，0 条：cand124、cand128）。
- 与早期仅 8 条、未做 B 同步时相比，前 8 条在 `--resync-generated` 后由 2/8 提升至 **7/8** Maven 通过（cand006 仍为深层嵌套类编译失败）。

## 全量结果表

| 编号 | 结果 | DeepSeek | 聚焦测试执行结果 | 备注 |
| --- | --- | --- | --- | --- |
| cand001 | 通过 | 成功 | `FailableTest` 通过 | PR#1435 [LANG-1784] Add Failable methods for null-safe mapping and c。`artifacts/sample_runs/cand001_07914b39281e/` |
| cand002 | 通过 | 成功 | `NumberUtilsTest` 通过 | PR#1626 NumberUtils.isCreatable(String) should match NumberUtils.cre。`artifacts/sample_runs/cand002_127050d2b54b/` |
| cand003 | 通过 | 成功 | `RecursiveToStringStyleTest` 通过 | PR#1584 [LANG-1452] RecursiveToStringStyle and MultilineRecursiveToS。`artifacts/sample_runs/cand003_1418a770ba43/` |
| cand004 | 通过 | 成功 | `ArrayUtilsTest` 通过 | Instead of throwing a NullPointerException, ArrayUtils.toStr。`artifacts/sample_runs/cand004_1521bf3e9f3e/` |
| cand005 | 通过 | 成功 | `FunctionsTest` 通过 | PR#1435 [LANG-1784] Add Functions methods for null-safe mapping and。`artifacts/sample_runs/cand005_1a3a12dc7388/` |
| cand006 | 通过 | 成功 | `MethodUtilsTest` 通过 | PR#1414 LANG-1778 fix by reversing order (#1414)。`artifacts/sample_runs/cand006_1e455838963a/` |
| cand007 | 通过 | 成功 | `ArrayUtilsTest` 通过 | PR#1585 [LANG-1814] ArrayUtils.subarray(..) may overflow index arith。`artifacts/sample_runs/cand007_26ead6134ad5/` |
| cand008 | 通过 | 成功 | `RandomStringUtilsTest` 通过 | PR#1638 Two fixes in RandomStringUtils.random(int, int, int, boolean。`artifacts/sample_runs/cand008_313d877d57ab/` |
| cand009 | 通过 | 成功 | `LocaleUtilsTest` 通过 | PR#1630 [LANG-1823] LocaleUtils.toLocale cannot parse valid JDK Loca。`artifacts/sample_runs/cand009_3df7f4440e74/` |
| cand010 | 通过 | 成功 | `ArrayUtilsTest` 通过 | PR#1589 fix LANG-1816 (#1589)。`artifacts/sample_runs/cand010_52c06bea2f2b/` |
| cand011 | 通过 | 成功 | `ClassUtilsTest` 通过 | PR#1495 Bugfix/class utils to canonical name length check (#1495)。`artifacts/sample_runs/cand011_5713c6c42e43/` |
| cand012 | 通过 | 成功 | `NumberUtilsTest` 通过 | PR#1635 NumberUtils.createNumber(String): Float shortcut can bypass。`artifacts/sample_runs/cand012_5904c573ffac/` |
| cand013 | 通过 | 成功 | `TimedSemaphoreTest` 通过 | PR#1639 TimedSemaphore.shutdown() must wake threads blocked in acqui。`artifacts/sample_runs/cand013_5914a8e80a54/` |
| cand014 | 通过 | 成功 | `ClassUtilsTest` 通过 | PR#1437 [LANG-1774] Improve handling of ClassUtils.getShortCanonical。`artifacts/sample_runs/cand014_61c2d8f84931/` |
| cand015 | 通过 | 成功 | `MethodUtilsTest` 通过 | PR#1289 [LANG-1754] Use getAllSuperclassesAndInterfaces() in getMatc。`artifacts/sample_runs/cand015_65970408668e/` |
| cand016 | 通过 | 成功 | `StringsTest` 通过 | Avoid JDK-8015417 in Strings.equals()。`artifacts/sample_runs/cand016_6e78b38f0555/` |
| cand017 | 通过 | 成功 | `RegExUtilsTest` 通过 | Add RegExUtils methods typed to CharSequence input and depre。`artifacts/sample_runs/cand017_744a8c30c6e4/` |
| cand018 | 通过 | 成功 | `ClassUtilsTest` 通过 | PR#1494 ClassUtils now throws `IllegalArgumentException` when array。`artifacts/sample_runs/cand018_7cc1ac1c30d9/` |
| cand019 | 通过 | 成功 | `RuntimeEnvironmentTest` 通过 | PR#1323 Improve container detection by mimicing systemd (#1323)。`artifacts/sample_runs/cand019_7e0d6dbd2a65/` |
| cand020 | 通过 | 成功 | `NumberUtilsTest` 通过 | PR#1560 [LANG-1806] NumberUtils.isParsable("1.f") should return true。`artifacts/sample_runs/cand020_8089a0c2d320/` |
| cand021 | 通过 | 成功 | `TypeUtilsTest` 通过 | PR#1549 [LANG-1700] Improve handling of parameterized types and vari。`artifacts/sample_runs/cand021_8f8cc04e6550/` |
| cand022 | 通过 | 成功 | `ConversionTest` 通过 | Conversion.hexTo*() methods now throw IllegalArgumentExcepti。`artifacts/sample_runs/cand022_929df5d5c00a/` |
| cand023 | 通过 | 成功 | `StringUtilsTest` 通过 | PR#1297 fix: default ttl in recursive replacement (#1297)。`artifacts/sample_runs/cand023_972aa7b29a7c/` |
| cand024 | 通过 | 成功 | `NumberUtilsTest` 通过 | PR#1531 LANG-1695: Allow trailing decimal point in NumberUtils.isPar。`artifacts/sample_runs/cand024_9828dc73d4f2/` |
| cand025 | 通过 | 成功 | `ArrayFillTest` 通过 | PR#1386 Add fill method for boolean arrays in ArrayFill utility clas。`artifacts/sample_runs/cand025_9d5ad944277b/` |
| cand026 | 通过 | 成功 | `DateUtilsTest` 通过 | PR#1609 LANG-771 Fix DateUtils.ceiling increment on exact boundary (。`artifacts/sample_runs/cand026_a9a0dd8a72c5/` |
| cand027 | 通过 | 成功 | `StopWatchTest` 通过 | PR#1610 fix: Make stopInstant be in sync with stopTimeNanos for spli。`artifacts/sample_runs/cand027_aa47951bd022/` |
| cand028 | 通过 | 成功 | `ClassUtilsTest` 通过 | PR#1577 Fix ClassNotFoundException message variable (#1577)。`artifacts/sample_runs/cand028_b62244517285/` |
| cand029 | 通过 | 成功 | `CharSetTest` 通过 | PR#1530 [LANG-1804] Fix CharSet#getInstance returns null instead of。`artifacts/sample_runs/cand029_b8d382039a85/` |
| cand030 | 通过 | 成功 | `ArchUtilsTest` 通过 | PR#1625 Add "ppc64le" to ArchUtils (#1625)。`artifacts/sample_runs/cand030_bb675e1127ad/` |
| cand031 | 通过 | 成功 | `TypeUtilsTest` 通过 | PR#1548 [LANG-1749] Add stricter type checks for  parameterized type。`artifacts/sample_runs/cand031_bcad40a502cd/` |
| cand032 | 通过 | 成功 | `ConversionTest` 通过 | Conversion.hexTo*() methods now throw IllegalArgumentExcepti。`artifacts/sample_runs/cand032_be8b654fc02d/` |
| cand033 | 通过 | 成功 | `StopWatchTest` 通过 | PR#1473 LANG-1504 - Adding labels to split StopWatch feature (#1473)。`artifacts/sample_runs/cand033_ce2ba7b28260/` |
| cand034 | 通过 | 成功 | `ArrayUtilsTest` 通过 | PR#1559 [LANG-1810] Deprecate SOFT_MAX_ARRAY_LENGTH in favor of MAX_。`artifacts/sample_runs/cand034_d9de2fd5b8c6/` |
| cand035 | 通过 | 成功 | `NumberUtilsTest` 通过 | Let existing catch clause handle the NPE edge case。`artifacts/sample_runs/cand035_ee2041464e60/` |
| cand036 | 通过 | 成功 | `StringsTest` 通过 | PR#1299 [LANG-1682] Javadoc and test: Use Strings.CI.startsWithAny m。`artifacts/sample_runs/cand036_f51f015e3deb/` |
| cand037 | 通过 | 成功 | `NumberUtilsTest` 通过 | PR#1629 [LANG-1821] NumberUtils.isCreatable fails for hexadecimal nu。`artifacts/sample_runs/cand037_fa59a31596ce/` |
| cand038 | 通过 | 成功 | `PairTest` 通过 | Add tests。`artifacts/sample_runs/cand038_fc3638e0fc8d/` |
| cand039 | 通过 | 成功 | `RandomStringUtilsTest` 通过 | PR#1273 Fix handling of non-ASCII letters & numbers in RandomStringU。`artifacts/sample_runs/cand039_fd866a9c2d6c/` |
| cand040 | 通过 | 成功 | `SystemUtilsTest` 通过 | Add SystemUtils.IS_OS_MAC_OSX_SEQUOIA。`artifacts/sample_runs/cand040_010c5d26330c/` |
| cand041 | 通过 | 成功 | `LocaleUtilsTest` 通过 | `LocaleUtils.toLocale(String)` for a 2 letter country code n。`artifacts/sample_runs/cand041_03e7c36d2daf/` |
| cand042 | 通过 | 成功 | `DateUtilsTest` 通过 | PR#1385 Add org.apache.commons.lang3.time.DateUtils.toLocalDateTime(。`artifacts/sample_runs/cand042_0c6a5c10a7a0/` |
| cand043 | 通过 | 成功 | `SystemPropertiesTest` 通过 | Add SystemProperties.JAVA_SECURITY_KERBEROS_CONF。`artifacts/sample_runs/cand043_0dffedc822ce/` |
| cand044 | 通过 | 成功 | `LocaleUtilsTest` 通过 | LocaleUtils.toLocale(String) cannot parse four segments。`artifacts/sample_runs/cand044_0f4dee8451df/` |
| cand045 | 通过 | 成功 | `SystemPropertiesTest` 通过 | Add SystemProperties.JAVA_SECURITY_DEBUG。`artifacts/sample_runs/cand045_106b61a5be74/` |
| cand046 | 通过 | 成功 | `LangCollectorsTest` 通过 | Add LangCollectors.collect(Collector, T...)。`artifacts/sample_runs/cand046_118652d768eb/` |
| cand047 | 通过 | 成功 | `LangCollectorsTest` 通过 | Make LangCollectors.collect(...) null-safe。`artifacts/sample_runs/cand047_17ba8b9da6a8/` |
| cand048 | 通过 | 成功 | `StopWatchTest` 通过 | Add StopWatch.getDuration() and deprecate getTime()。`artifacts/sample_runs/cand048_263026823515/` |
| cand049 | 通过 | 成功 | `StopWatchTest` 通过 | Add StopWatch.getSplitDuration() and deprecate getSplitTime(。`artifacts/sample_runs/cand049_2875a65756da/` |
| cand050 | 通过 | 成功 | `CalendarUtilsTest` 通过 | Add CalendarUtils.toLocalDateTime(Calendar)。`artifacts/sample_runs/cand050_328f2aedfb86/` |
| cand051 | 通过 | 成功 | `DurationUtilsTest` 通过 | Add DurationUtils.get(String, TemporalUnit, long)。`artifacts/sample_runs/cand051_35f35e9e1cee/` |
| cand052 | 通过 | 成功 | `BasicThreadFactoryTest` 通过 | Add BasicThreadFactory.builder() and deprecate BasicThreadFa。`artifacts/sample_runs/cand052_35fee6998b8d/` |
| cand053 | 通过 | 成功 | `NumberUtilsTest` 通过 | [LANG-1729] NumberUtils.isParsable() returns true for full w。`artifacts/sample_runs/cand053_3bd162585900/` |
| cand054 | 通过 | 成功 | `StopWatchTest` 通过 | Add StopWatch.getStopInstant() and deprecate getStopTime()。`artifacts/sample_runs/cand054_3ebd20002ef3/` |
| cand055 | 通过 | 成功 | `SystemUtilsTest` 通过 | Add SystemUtils.getUserDirPath()。`artifacts/sample_runs/cand055_421229b42f79/` |
| cand056 | 通过 | 成功 | `SystemUtilsTest` 通过 | Add org.apache.commons.lang3.SystemUtils.IS_OS_NETWARE。`artifacts/sample_runs/cand056_4c39aa2ca612/` |
| cand057 | 通过 | 成功 | `TypeUtilsTest` 通过 | Fix StackOverflowError in TypeUtils.typeVariableToString(Typ。`artifacts/sample_runs/cand057_4e228a53509b/` |
| cand058 | 通过 | 成功 | `SystemUtilsTest` 通过 | Add SystemUtils.getJavaHomePath()。`artifacts/sample_runs/cand058_5035fdd788bc/` |
| cand059 | 通过 | 成功 | `ReflectionDiffBuilderTest` 通过 | Fix NullPointerException in ReflectionDiffBuilder.getExclude。`artifacts/sample_runs/cand059_5bcedccec3ed/` |
| cand060 | 通过 | 成功 | `RandomStringUtilsTest` 通过 | RandomStringUtils.random() methods may not return when asked。`artifacts/sample_runs/cand060_5d46a39e450f/` |
| cand061 | 通过 | 成功 | `MethodUtilsTest` 通过 | MethodUtils cannot find or invoke vararg methods of interfac。`artifacts/sample_runs/cand061_5dd8e33cf68b/` |
| cand062 | 失败 | 成功 | `ArrayUtilsTest` 编译失败 | [LANG-1811] ArrayUtils.shuffle() throws NullPointerException；合并后 testCompile 失败。`artifacts/sample_runs/cand062_623235ebca46/` |
| cand063 | 通过 | 成功 | `StreamsTest` 通过 | Fix generics in org.apache.commons.lang3.stream.Streams.toAr。`artifacts/sample_runs/cand063_6622a4685750/` |
| cand064 | 通过 | 成功 | `CalendarUtilsTest` 通过 | Add CalendarUtils.toZonedDateTime(Calendar)。`artifacts/sample_runs/cand064_666ad13656c6/` |
| cand065 | 通过 | 成功 | `StopWatchTest` 通过 | Fix NullPointerException in StopWatch.getStopTime()。`artifacts/sample_runs/cand065_677e57f56bfa/` |
| cand066 | 通过 | 成功 | `RegExUtilsTest` 通过 | Add RegExUtils.replacePattern(CharSequence, String, String)。`artifacts/sample_runs/cand066_6b81f9e6cf42/` |
| cand067 | 通过 | 成功 | `EventListenerSupportTest` 通过 | [LANG-1727] EventListenerSupport doesn't document ordering o。`artifacts/sample_runs/cand067_6e2741da4d1e/` |
| cand068 | 通过 | 成功 | `DiffBuilderTest` 通过 | PR#786 [LANG-1657] DiffBuilder: Type constraint for method append(.。`artifacts/sample_runs/cand068_739d62630092/` |
| cand069 | 通过 | 成功 | `CharSetTest` 通过 | CharSet now maintains iteration order。`artifacts/sample_runs/cand069_7489d6e21334/` |
| cand070 | 通过 | 成功 | `EnumUtilsTest` 通过 | Fix edge-case NullPointerException in org.apache.commons.lan。`artifacts/sample_runs/cand070_76ec155eea3b/` |
| cand071 | 通过 | 成功 | `ConversionTest` 通过 | Conversion.hexTo*() methods now throw IllegalArgumentExcepti。`artifacts/sample_runs/cand071_7833161882d5/` |
| cand072 | 通过 | 成功 | `LongRangeTest` 通过 | Add LongRange.toLongStream()。`artifacts/sample_runs/cand072_798caa4e5174/` |
| cand073 | 通过 | 成功 | `ReflectionDiffBuilderTest` 通过 | Fail-fast for a null DiffBuilder in ReflectionDiffBuilder.Re。`artifacts/sample_runs/cand073_7c8d26daac0c/` |
| cand074 | 通过 | 成功 | `CalendarUtilsTest` 通过 | PR#725 Add CalendarUtils.toLocalDate() #725。`artifacts/sample_runs/cand074_80e6a67649ec/` |
| cand075 | 通过 | 成功 | `MethodUtilsTest` 通过 | org.apache.commons.lang3.reflect.MethodUtils.getMethodObject。`artifacts/sample_runs/cand075_8a7b0da6fc78/` |
| cand076 | 通过 | 成功 | `ComparableUtilsTest` 通过 | Fix NullPointerExceptions in org.apache.commons.lang3.compar。`artifacts/sample_runs/cand076_8cc6363673bb/` |
| cand077 | 通过 | 成功 | `EnumUtilsTest` 通过 | Add EnumSet.stream(Class)。`artifacts/sample_runs/cand077_8e1f5a9aca4a/` |
| cand078 | 通过 | 成功 | `FractionTest` 通过 | [LANG-1764] Several hash collisions in Fraction class。`artifacts/sample_runs/cand078_94f612b31fd9/` |
| cand079 | 通过 | 成功 | `CharRangeTest` 通过 | [LANG-1802] Fix collision in CharRange.hashCode()。`artifacts/sample_runs/cand079_97e572cb7e10/` |
| cand080 | 通过 | 成功 | `SystemUtilsTest` 通过 | Add SystemUtils.getJavaIoTmpDirPath()。`artifacts/sample_runs/cand080_97fb6a23e02d/` |
| cand081 | 通过 | 成功 | `RegExUtilsTest` 通过 | Add RegExUtils.dotAllMatcher(String, CharSequence) and depre。`artifacts/sample_runs/cand081_9bc57f7fed72/` |
| cand082 | 通过 | 成功 | `LocaleUtilsTest` 通过 | LocaleUtils.availableLocaleSet() uses predictable iteration。`artifacts/sample_runs/cand082_9d6a4be2f1ff/` |
| cand083 | 通过 | 成功 | `SerializationUtilsTest` 通过 | [LANG-1759] SerializationUtils.clone(Object) throws ClassCas。`artifacts/sample_runs/cand083_a01471c196db/` |
| cand084 | 通过 | 成功 | `EnumUtilsTest` 通过 | org.apache.commons.lang3.EnumUtils.getFirstEnumIgnoreCase(Cl。`artifacts/sample_runs/cand084_a4ba12e80c1b/` |
| cand085 | 通过 | 成功 | `ClassUtilsTest` 通过 | org.apache.commons.lang3.ClassUtils.getCanonicalName(String)。`artifacts/sample_runs/cand085_a5f9a0cc22e4/` |
| cand086 | 通过 | 成功 | `LockingVisitorsTest` 通过 | Add org.apache.commons.lang3.concurrent.locks.LockingVisitor。`artifacts/sample_runs/cand086_ae28edfbddde/` |
| cand087 | 通过 | 成功 | `MethodUtilsTest` 通过 | [LANG-1757] NullPointerException in MethodUtils.getMatchingA。`artifacts/sample_runs/cand087_af1598229fca/` |
| cand088 | 通过 | 成功 | `EnumUtilsTest` 通过 | Add EnumUtils.getFirstEnum(Class<E>, int, ToIntFunction<E>,。`artifacts/sample_runs/cand088_b2e66fe50ba8/` |
| cand089 | 通过 | 成功 | `LockingVisitorsTest` 通过 | Add builders for LockingVisitors implementations。`artifacts/sample_runs/cand089_b6f72e73ee96/` |
| cand090 | 通过 | 成功 | `CalendarUtilsTest` 通过 | Add CalendarUtils.toOffsetDateTime(Calendar)。`artifacts/sample_runs/cand090_bfa3c06361fa/` |
| cand091 | 通过 | 成功 | `MutablePairTest` 通过 | Add MutablePair.ofNonNull(Map.Entry)。`artifacts/sample_runs/cand091_c140fc8154e8/` |
| cand092 | 通过 | 成功 | `IntegerRangeTest` 通过 | Add IntegerRange.toIntStream()。`artifacts/sample_runs/cand092_c64cf945161e/` |
| cand093 | 通过 | 成功 | `MethodUtilsTest` 通过 | [LANG-1789] NullPointerException when generating NoSuchMetho。`artifacts/sample_runs/cand093_cd87ec61b8d0/` |
| cand094 | 通过 | 成功 | `SystemUtilsTest` 通过 | Add SystemUtils.IS_OS_ANDROID。`artifacts/sample_runs/cand094_d0bb31bc10ac/` |
| cand095 | 通过 | 成功 | `DoubleRangeTest` 通过 | Add DoubleRange.fit(double)。`artifacts/sample_runs/cand095_d8f7c3843231/` |
| cand096 | 通过 | 成功 | `SystemPropertiesTest` 通过 | Add SystemProperties.getPath(String, Supplier<Path>)。`artifacts/sample_runs/cand096_da0583008020/` |
| cand097 | 通过 | 成功 | `TimedSemaphoreTest` 通过 | Add TimedSemaphore.builder() and Builder。`artifacts/sample_runs/cand097_df3e2715f412/` |
| cand098 | 通过 | 成功 | `ThreadUtilsTest` 通过 | ThreadUtils.sleepQuietly(Duration) now restores the current。`artifacts/sample_runs/cand098_e1ffb6ea0b9e/` |
| cand099 | 通过 | 成功 | `RegExUtilsTest` 通过 | Add RegExUtils.removePattern(CharSequence, String) and depre。`artifacts/sample_runs/cand099_e7d001f1b77c/` |
| cand100 | 通过 | 成功 | `MethodUtilsTest` 通过 | PR#1427 MethodUtils cannot find or invoke a vararg method without pr。`artifacts/sample_runs/cand100_ee09f69951c0/` |
| cand101 | 通过 | 成功 | `ArrayUtilsTest` 通过 | Add ArrayUtils.startsWith()。`artifacts/sample_runs/cand101_ef3d5d93a30b/` |
| cand102 | 通过 | 成功 | `StopWatchTest` 通过 | Add StopWatch.getStartInstant() and deprecate getStartTime()。`artifacts/sample_runs/cand102_f1aed3eacb50/` |
| cand103 | 通过 | 成功 | `ArrayFillTest` 通过 | PR#1386 Add ArrayFill.fill(boolean[], boolean) #1386。`artifacts/sample_runs/cand103_f431d2eeb71c/` |
| cand104 | 通过 | 成功 | `RegExUtilsTest` 通过 | Add RegExUtils methods typed to CharSequence input and depre。`artifacts/sample_runs/cand104_f43534ec04d4/` |
| cand105 | 通过 | 成功 | `SystemUtilsTest` 通过 | Add SystemUtils.getUserHomePath()。`artifacts/sample_runs/cand105_fb42e80e9293/` |
| cand106 | 通过 | 成功 | `LongRangeTest` 通过 | Add LongRange.fit(long)。`artifacts/sample_runs/cand106_fe43aa478db7/` |
| cand107 | 通过 | 成功 | `SystemUtilsTest` 通过 | Add SystemUtils.IS_OS_MAC_OSX_SONOMA。`artifacts/sample_runs/cand107_ff66cce0ca10/` |
| cand108 | 通过 | 成功 | `ObjectToStringComparatorTest` 通过 | Optimize ObjectToStringComparator.compare() method。`artifacts/sample_runs/cand108_71c905200de7/` |
| cand109 | 通过 | 成功 | `StopWatchTest` 通过 | Add StopWatch.run([Failable]Runnable) and get([Failable]Supp。`artifacts/sample_runs/cand109_da246244aebf/` |
| cand110 | 通过 | 成功 | `MethodUtilsTest` 通过 | MethodUtils cannot find or invoke a public method on a publi。`artifacts/sample_runs/cand110_1d5ba7a1109b/` |
| cand111 | 通过 | 成功 | `BitFieldTest` 通过 | PR#1561 Add long support to `BitField` (#1561)。`artifacts/sample_runs/cand111_f2bdb0cb74a0/` |
| cand112 | 通过 | 成功 | `RandomStringUtilsTest` 通过 | PR#1235 Reimplement RandomStringUtils on top of SecureRandom#getInst。`artifacts/sample_runs/cand112_f382d61a0377/` |
| cand113 | 通过 | 成功 | `ThreadUtilsTest` 通过 | Add Predicates。`artifacts/sample_runs/cand113_b046e22faf9c/` |
| cand114 | 通过 | 成功 | `RandomStringUtilsTest` 通过 | PR#1247 [LANG-1745] RandomStringUtils.random() with a negative chara。`artifacts/sample_runs/cand114_00e530042f48/` |
| cand115 | 通过 | 成功 | `AtomicSafeInitializerTest` 通过 | org.apache.commons.lang3.concurrent.AtomicSafeInitializer.ge。`artifacts/sample_runs/cand115_0f211efaf122/` |
| cand116 | 通过 | 成功 | `ValidateTest` 通过 | Add Validate.isTrue(boolean, Supplier<String>)。`artifacts/sample_runs/cand116_2188eb0e2e15/` |
| cand117 | 通过 | 成功 | `NumberUtilsTest` 通过 | Comment: Remove unnecessary Latin acronym。`artifacts/sample_runs/cand117_64d6a28a12d9/` |
| cand118 | 失败 | 成功 | `SystemUtilsTest` 编译失败 | Add JavaVersion.JAVA_27；合并后 testCompile 失败。`artifacts/sample_runs/cand118_7e3571e7e2c6/` |
| cand119 | 通过 | 成功 | `SystemPropertiesTest` 通过 | Add SystemProperties.getBoolean(Class, String, BooleanSuppli。`artifacts/sample_runs/cand119_8b27dec0340e/` |
| cand120 | 通过 | 成功 | `SystemPropertiesTest` 通过 | Add org.apache.commons.lang3.SystemProperties.isPropertySet(。`artifacts/sample_runs/cand120_9b383f3fadcc/` |
| cand121 | 通过 | 成功 | `RandomStringUtilsTest` 通过 | PR#1379 [LANG-1772] Restrict size of cache to prevent overflow error。`artifacts/sample_runs/cand121_c2260f094d78/` |
| cand122 | 通过 | 成功 | `ArrayFillTest` 通过 | Add ArrayFill.fill(T[], FailableIntFunction))。`artifacts/sample_runs/cand122_dc6ff345793c/` |
| cand123 | 失败 | 成功 | `SystemUtilsTest` 编译失败 | Add JavaVersion.JAVA_26；合并后 testCompile 失败。`artifacts/sample_runs/cand123_f24c027ff83b/` |
| cand124 | 通过 | 成功 | `FastDateParserTest` 通过 | Clean caches between tests。`artifacts/sample_runs/cand124_ef5de64ed438/` |
| cand125 | 通过 | 成功 | `MethodUtilsTest` 通过 | MethodUtils cannot find or invoke vararg methods when wideni。`artifacts/sample_runs/cand125_14d34506c993/` |
| cand126 | 通过 | 成功 | `ReflectionDiffBuilderTest` 通过 | Add some tests that use reflection。`artifacts/sample_runs/cand126_b62fc004d1a6/` |
| cand127 | 通过 | 成功 | `ObjectUtilsTest` 通过 | Add ObjectUtils.getIfNull(Object, Object) and deprecate defa。`artifacts/sample_runs/cand127_177911e47146/` |
| cand128 | 通过 | 成功 | `StreamsTest` 通过 | Normalize parameter names。`artifacts/sample_runs/cand128_a511a163b579/` |
| cand129 | 通过 | 成功 | `ConsumersTest` 通过 | Flip args on new API。`artifacts/sample_runs/cand129_4c1cbdbb8002/` |
| cand130 | 通过 | 成功 | `FailableTest` 通过 | PR#1435 [LANG-1784] Add Functions|Failable methods for null-safe map。`artifacts/sample_runs/cand130_c49ed131f71d/` |
| cand131 | 通过 | 成功 | `RandomStringUtilsTest` 通过 | PR#1250 Feature/randomutils secure() and insecure() (#1250)。`artifacts/sample_runs/cand131_c95ee37dffd4/` |
| cand132 | 通过 | 成功 | `JavaVersionTest` 通过 | Add JavaVersion.JAVA_25。`artifacts/sample_runs/cand132_70fa706916dc/` |
| cand133 | 通过 | 成功 | `ArrayUtilsTest` 通过 | Add ArrayUtils.containsAny(int[], int...)。`artifacts/sample_runs/cand133_85f91f420890/` |
| cand134 | 通过 | 成功 | `JavaVersionTest` 通过 | Add SystemUtils.IS_JAVA_23。`artifacts/sample_runs/cand134_e7437aa445b3/` |
| cand135 | 通过 | 成功 | `JavaVersionTest` 通过 | Add JavaVersion.JAVA_24。`artifacts/sample_runs/cand135_f664abb5e255/` |

## 失败样本索引（便于查阅）

### 合并失败（0）

- 无

### Maven 通过但测试失败（0）

无（详见上表 `测试失败` 行）。

### 编译失败（3）

cand062、cand118、cand123（详见上表）。

## 主要产物路径

- 单条：`artifacts/sample_runs/candNNN_<B前12位>/`（`deepseek_output.md`、`generated.java`、`run_report.json`）
- 候选列表：`artifacts/lang_sample_candidates_filtered.json`
