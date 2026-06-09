# SUT Invocation Fingerprint Report

Compares **which production APIs and assertion patterns** are exercised by LLM vs human tests.

## Method

1. Parse each `@Test` method and extract:
   - **SUT calls**: static invocations on the primary production class, e.g. `ArrayUtils.shift(ref,int)`
   - **Assert semantics**: assertion kind plus coarse argument categories / exception types
2. Build multiset fingerprints (full class and delta-only methods).
3. Compute multiset Jaccard: `sum(min(a,b)) / sum(max(a,b))`.

- Scope: Maven-pass samples only
- Comparable rows: 1101
- Errors: 20
- Skipped: 107

## Summary

| model | comparable_rows | mean_sut_invocation_jaccard | mean_assert_semantic_jaccard | mean_delta_sut_jaccard | mean_delta_assert_jaccard | median_sut |
|---|---:|---:|---:|---:|---:|---:|
| deepseek-v4-pro | 559 | 0.9939 | 0.9938 | 0.9678 | 0.9633 | 1.0 |
| gpt-5.5 | 542 | 0.9959 | 0.9957 | 0.9798 | 0.98 | 1.0 |

## Lowest SUT Invocation Similarity

| model | cand | sut_invocation_jaccard | delta_sut_jaccard | assert_semantic_jaccard | sut_calls_llm | sut_calls_human | llm_added | human_added | subject |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| deepseek-v4-pro | 352 | 0.0 | 1.0 | 0.0 | 224 | 0 | 0 | 0 | Add EnumSet.stream(Class) |
| gpt-5.5 | 352 | 0.0 | 1.0 | 0.0 | 224 | 0 | 0 | 0 | Add EnumSet.stream(Class) |
| deepseek-v4-pro | 215 | 0.3682 | 1.0 | 0.3551 | 81 | 220 | 0 | 0 | Sort by method name. |
| gpt-5.5 | 327 | 0.5375 | 0.0 | 0.5398 | 165 | 307 | 0 | 34 | LANG-1134: New methods for lang3.Validate This closes #87 from github. |
| deepseek-v4-pro | 417 | 0.6491 | 0.3548 | 0.7285 | 37 | 57 | 0 | 5 | [LANG-1568] FailableBooleanSupplier, FailableIntSupplier, FailableL... |
| deepseek-v4-pro | 9 | 0.6875 | 0.0476 | 0.9034 | 88 | 128 | 0 | 3 | [LANG-1784] Add Failable methods for null-safe mapping and chaining... |
| gpt-5.5 | 9 | 0.6875 | 0.0476 | 0.9034 | 88 | 128 | 0 | 3 | [LANG-1784] Add Failable methods for null-safe mapping and chaining... |
| deepseek-v4-pro | 127 | 0.7293 | 0.0577 | 0.8068 | 132 | 181 | 0 | 7 | Syntax for optional tokens in DurationFormatUtils (#1062) |
| deepseek-v4-pro | 267 | 0.8551 | 1.0 | 0.875 | 59 | 69 | 3 | 3 | Add DurationUtils.get(String, TemporalUnit, long) |
| deepseek-v4-pro | 14 | 0.8601 | 0.0 | 0.8682 | 123 | 143 | 0 | 8 | LANG-1352: EnumUtils.getEnumIgnoreCase and isValidEnumIgnoreCase me... |

## Notes

- Low `sut_invocation_jaccard` with high `method_name_jaccard` usually means missing API coverage.
- `delta_*` metrics focus on changed/added test methods only.
- Matching call signatures do not guarantee identical test inputs or branch coverage.
