# LLM vs Human Test Similarity

This report compares each LLM-generated `generated.java` against the human-written test file in commit B. Only samples whose generated tests pass Maven (`maven_returncode == 0`) are included in the similarity averages.

## Metrics

- `method_name_jaccard`: Jaccard similarity between LLM and human test method names.
- `added_test_name_jaccard`: Jaccard similarity between test method names added relative to `old_test.java`; summary averages exclude samples where neither side added tests.
- `deleted_test_name_jaccard`: Jaccard similarity between test method names deleted relative to `old_test.java`; summary averages exclude samples where neither side deleted tests.
- `modified_test_name_jaccard`: Jaccard similarity between same-named tests whose normalized method bodies changed relative to `old_test.java`; summary averages exclude samples where neither side modified tests.
- `assert_count_ratio`: total LLM assertion count divided by human assertion count.
- `assert_type_jaccard`: Jaccard similarity between assertion API types, such as `assertEquals` and `assertThrows`.

## Summary

| model | comparable_rows | added_applicable_rows | deleted_applicable_rows | modified_applicable_rows | method_name_jaccard | added_test_name_jaccard | deleted_test_name_jaccard | modified_test_name_jaccard | assert_count_ratio | assert_type_jaccard |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek-v4-pro | 561 | 319 | 41 | 242 | 0.9953 | 0.9210 | 0.9512 | 1.0000 | 0.9958 | 0.9994 |
| gpt-5.5 | 560 | 323 | 43 | 254 | 0.9965 | 0.9538 | 0.9767 | 1.0000 | 0.9977 | 1.0000 |

## Perfect-Match Rates

| model | method_name_jaccard = 1.0 | added_test_name_jaccard = 1.0 | deleted_test_name_jaccard = 1.0 | modified_test_name_jaccard = 1.0 | assert_type_jaccard = 1.0 |
|---|---:|---:|---:|---:|---:|
| deepseek-v4-pro | 0.9501 | 0.9185 | 0.9512 | 1.0000 | 0.9964 |
| gpt-5.5 | 0.9714 | 0.9536 | 0.9767 | 1.0000 | 1.0000 |

## Lowest Method-Name Similarity Samples

Each model contributes up to 10 non-perfect Maven-pass samples; if fewer rows are shown, the remaining samples are perfect matches for this metric.

| model | cand | method_name_jaccard | added_test_name_jaccard | deleted_test_name_jaccard | assert_count_ratio | subject |
|---|---:|---:|---:|---:|---:|---|
| deepseek-v4-pro | 215 | 0.3684 | 1.0000 | 0.0000 | 0.3551 | Sort by method name. |
| deepseek-v4-pro | 417 | 0.7727 | 0.0000 | 1.0000 | 0.7285 | [LANG-1568] FailableBooleanSupplier, FailableIntSupplier, FailableLongSupplier, FailableDo |
| deepseek-v4-pro | 127 | 0.7812 | 0.0000 | 1.0000 | 0.8433 | Syntax for optional tokens in DurationFormatUtils (#1062) |
| deepseek-v4-pro | 14 | 0.8000 | 0.0000 | 1.0000 | 0.8976 | LANG-1352: EnumUtils.getEnumIgnoreCase and isValidEnumIgnoreCase methods added (closes #28 |
| deepseek-v4-pro | 503 | 0.8333 | 0.0000 | 1.0000 | 0.9857 | Add Processor.Type.getLabel() and Processor.toString() |
| deepseek-v4-pro | 508 | 0.8462 | 0.0000 | 1.0000 | 0.7368 | Add ReflectionDiffBuilder.Builder |
| deepseek-v4-pro | 580 | 0.8750 | 0.0000 | 1.0000 | 0.9812 | LANG-1021: Provide methods to retrieve all fields/methods annotated with a specific type.  |
| deepseek-v4-pro | 147 | 0.8824 | 0.0000 | 1.0000 | 0.9091 | Code refactor to simplify Functions and new tests (#463) |
| deepseek-v4-pro | 223 | 0.9000 | 0.0000 | 1.0000 | 0.9184 | LANG-1223: Add StopWatch#getTime(TimeUnit) (closes #152) |
| deepseek-v4-pro | 462 | 0.9318 | 0.0000 | 1.0000 | 0.9546 | LANG-341: Please add number to byte[] methods. Suggested by Lilianne E. Blaze. Final patch |
| gpt-5.5 | 122 | 0.2885 | 0.0750 | 1.0000 | 1.0000 | [LANG-1568] More failable functional interfaces to match JRE functional interfaces. |
| gpt-5.5 | 327 | 0.6495 | 0.0000 | 1.0000 | 0.5398 | LANG-1134: New methods for lang3.Validate This closes #87 from github. |
| gpt-5.5 | 148 | 0.7887 | 0.0000 | 1.0000 | 0.7771 | swap and shift for arrays |
| gpt-5.5 | 14 | 0.8000 | 0.0000 | 1.0000 | 0.8976 | LANG-1352: EnumUtils.getEnumIgnoreCase and isValidEnumIgnoreCase methods added (closes #28 |
| gpt-5.5 | 599 | 0.8824 | 1.0000 | 0.0000 | 0.7805 | Remove trailing spaces. |
| gpt-5.5 | 201 | 0.9500 | 0.0000 | 1.0000 | 0.9879 | #LAN-1114 fixes bug in TypeUtils.equals(WildcardType, Type) where it was incorrectly retur |
| gpt-5.5 | 247 | 0.9524 | 0.0000 | 1.0000 | 0.9940 | LANG-1190: TypeUtils.isAssignable throws NullPointerException when fromType has type varia |
| gpt-5.5 | 72 | 0.9535 | 0.0000 | 1.0000 | 0.9052 | LANG-1495 Update EnumUtils.java (#475) |
| gpt-5.5 | 248 | 0.9545 | 0.0000 | 1.0000 | 0.9822 | LANG-1311: TypeUtils.toString() doesn't handle primitive and Object arrays correctly |
| gpt-5.5 | 182 | 0.9565 | 0.0000 | 1.0000 | 0.9941 | LANG-1348 - StackOverflowError on TypeUtils.toString(...) for a generic return type of Enu |

## Lowest Added-Test Similarity Samples

Each model contributes up to 10 non-perfect Maven-pass samples; if fewer rows are shown, the remaining samples are perfect matches for this metric.

| model | cand | added_test_name_jaccard | added_test_count_llm | added_test_count_human | subject |
|---|---:|---:|---:|---:|---|
| deepseek-v4-pro | 9 | 0.0000 | 0 | 3 | [LANG-1784] Add Failable methods for null-safe mapping and chaining #1435 |
| deepseek-v4-pro | 14 | 0.0000 | 0 | 8 | LANG-1352: EnumUtils.getEnumIgnoreCase and isValidEnumIgnoreCase methods added (closes #28 |
| deepseek-v4-pro | 58 | 0.0000 | 0 | 3 | [LANG-1568] More failable functional interfaces to match JRE functional interfaces. |
| deepseek-v4-pro | 72 | 0.0000 | 0 | 2 | LANG-1495 Update EnumUtils.java (#475) |
| deepseek-v4-pro | 127 | 0.0000 | 0 | 7 | Syntax for optional tokens in DurationFormatUtils (#1062) |
| deepseek-v4-pro | 147 | 0.0000 | 0 | 2 | Code refactor to simplify Functions and new tests (#463) |
| deepseek-v4-pro | 182 | 0.0000 | 0 | 1 | LANG-1348 - StackOverflowError on TypeUtils.toString(...) for a generic return type of Enu |
| deepseek-v4-pro | 194 | 0.0000 | 0 | 1 | LANG-1371: Fix TypeUtils.parameterize to work correctly with narrower-typed varargs array  |
| deepseek-v4-pro | 201 | 0.0000 | 0 | 1 | #LAN-1114 fixes bug in TypeUtils.equals(WildcardType, Type) where it was incorrectly retur |
| deepseek-v4-pro | 223 | 0.0000 | 0 | 1 | LANG-1223: Add StopWatch#getTime(TimeUnit) (closes #152) |
| gpt-5.5 | 9 | 0.0000 | 0 | 3 | [LANG-1784] Add Failable methods for null-safe mapping and chaining #1435 |
| gpt-5.5 | 14 | 0.0000 | 0 | 8 | LANG-1352: EnumUtils.getEnumIgnoreCase and isValidEnumIgnoreCase methods added (closes #28 |
| gpt-5.5 | 72 | 0.0000 | 0 | 2 | LANG-1495 Update EnumUtils.java (#475) |
| gpt-5.5 | 148 | 0.0000 | 0 | 56 | swap and shift for arrays |
| gpt-5.5 | 182 | 0.0000 | 0 | 1 | LANG-1348 - StackOverflowError on TypeUtils.toString(...) for a generic return type of Enu |
| gpt-5.5 | 194 | 0.0000 | 0 | 1 | LANG-1371: Fix TypeUtils.parameterize to work correctly with narrower-typed varargs array  |
| gpt-5.5 | 201 | 0.0000 | 0 | 1 | #LAN-1114 fixes bug in TypeUtils.equals(WildcardType, Type) where it was incorrectly retur |
| gpt-5.5 | 247 | 0.0000 | 0 | 1 | LANG-1190: TypeUtils.isAssignable throws NullPointerException when fromType has type varia |
| gpt-5.5 | 248 | 0.0000 | 0 | 1 | LANG-1311: TypeUtils.toString() doesn't handle primitive and Object arrays correctly |
| gpt-5.5 | 312 | 0.0000 | 0 | 1 | EnumUtils.getEnumSystemProperty(...). |

## Lowest Deleted-Test Similarity Samples

Each model contributes up to 10 non-perfect Maven-pass samples; if fewer rows are shown, the remaining samples are perfect matches for this metric.

| model | cand | deleted_test_name_jaccard | deleted_test_count_llm | deleted_test_count_human | subject |
|---|---:|---:|---:|---:|---|
| deepseek-v4-pro | 215 | 0.0000 | 24 | 0 | Sort by method name. |
| deepseek-v4-pro | 267 | 0.0000 | 1 | 0 | Add DurationUtils.get(String, TemporalUnit, long) |
| gpt-5.5 | 599 | 0.0000 | 2 | 0 | Remove trailing spaces. |

## Lowest Modified-Test Similarity Samples

Each model contributes up to 10 non-perfect Maven-pass samples; if fewer rows are shown, the remaining samples are perfect matches for this metric.

| model | cand | modified_test_name_jaccard | modified_test_count_llm | modified_test_count_human | subject |
|---|---:|---:|---:|---:|---|

## Lowest Assertion-Type Similarity Samples

Each model contributes up to 10 non-perfect Maven-pass samples; if fewer rows are shown, the remaining samples are perfect matches for this metric.

| model | cand | assert_type_jaccard | assert_count_ratio | assert_count_llm | assert_count_human | subject |
|---|---:|---:|---:|---:|---:|---|
| deepseek-v4-pro | 417 | 0.8333 | 0.7285 | 110 | 151 | [LANG-1568] FailableBooleanSupplier, FailableIntSupplier, FailableLongSupplier, FailableDo |
| deepseek-v4-pro | 462 | 0.8333 | 0.9546 | 568 | 595 | LANG-341: Please add number to byte[] methods. Suggested by Lilianne E. Blaze. Final patch |

## Notes

- High structural similarity is expected for many samples because the task is test maintenance, not free-form test generation.
- `assert_count_ratio > 1` means the LLM test contains more assertion calls than the human test; `< 1` means fewer.
- These metrics are static. They do not prove behavioral equivalence; coverage-based comparison can be added later.
