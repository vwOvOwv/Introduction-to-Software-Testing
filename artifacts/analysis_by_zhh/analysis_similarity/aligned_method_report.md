# Aligned Method Similarity Report

Aligns LLM and human `@Test` methods by fingerprint (SUT calls + assert semantics + control flow),
then compares normalized body AST similarity on aligned pairs.

## Method

1. Fingerprint per method: SUT call signatures, assert semantic tags, control-flow counts.
2. Pairwise fingerprint similarity: `0.5*SUT + 0.35*assert + 0.15*control_flow`.
3. Greedy alignment: same-name pairs first, then best remaining pairs with similarity >= 0.3.
4. Metrics:
   - `aligned_method_similarity`: mean body AST similarity on aligned pairs
   - `alignment_coverage_human`: matched human methods / all human methods
   - `unmatched_human_method_count`: human methods with no LLM match

- Scope: Maven-pass samples only
- Comparable rows: 1101
- Errors: 20
- Skipped: 107

## Summary

| model | comparable_rows | mean_name_jaccard | mean_aligned_body | mean_aligned_fp | mean_coverage_human | mean_unmatched_human | median_coverage |
|---|---:|---:|---:|---:|---:|---:|---:|
| deepseek-v4-pro | 559 | 0.9935 | 0.9982 | 0.9982 | 0.9953 | 0.1699 | 1.0 |
| gpt-5.5 | 542 | 0.9946 | 0.9982 | 0.9982 | 0.9965 | 0.3413 | 1.0 |

## Lowest Human Alignment Coverage

| model | cand | coverage_human | aligned_body | name_jaccard | unmatched_human | llm/human methods | subject |
|---|---:|---:|---:|---:|---:|---:|---|
| gpt-5.5 | 122 | 0.2885 | 1.0 | 0.2885 | 74 | 30/104 | [LANG-1568] More failable functional interfaces to m... |
| deepseek-v4-pro | 215 | 0.3684 | 1.0 | 0.3684 | 24 | 14/38 | Sort by method name. |
| gpt-5.5 | 327 | 0.6495 | 1.0 | 0.6495 | 34 | 63/97 | LANG-1134: New methods for lang3.Validate This close... |
| deepseek-v4-pro | 417 | 0.7727 | 1.0 | 0.7727 | 5 | 17/22 | [LANG-1568] FailableBooleanSupplier, FailableIntSupp... |
| deepseek-v4-pro | 127 | 0.7812 | 1.0 | 0.7812 | 7 | 25/32 | Syntax for optional tokens in DurationFormatUtils (#... |
| gpt-5.5 | 148 | 0.7887 | 1.0 | 0.7887 | 56 | 209/265 | swap and shift for arrays |
| deepseek-v4-pro | 14 | 0.8 | 1.0 | 0.8 | 8 | 32/40 | LANG-1352: EnumUtils.getEnumIgnoreCase and isValidEn... |
| gpt-5.5 | 14 | 0.8 | 1.0 | 0.8 | 8 | 32/40 | LANG-1352: EnumUtils.getEnumIgnoreCase and isValidEn... |
| deepseek-v4-pro | 503 | 0.8333 | 1.0 | 0.8333 | 1 | 5/6 | Add Processor.Type.getLabel() and Processor.toString() |
| deepseek-v4-pro | 508 | 0.8462 | 1.0 | 0.8462 | 2 | 11/13 | Add ReflectionDiffBuilder.Builder |

## Low Method-Name Jaccard but Large Human Unmatched Count

| model | cand | name_jaccard | coverage_human | aligned_body | cross_name_pairs | unmatched_human | subject |
|---|---:|---:|---:|---:|---:|---:|---|
| gpt-5.5 | 122 | 0.2885 | 0.2885 | 1.0 | 0 | 74 | [LANG-1568] More failable functional interfaces to m... |
| gpt-5.5 | 148 | 0.7887 | 0.7887 | 1.0 | 0 | 56 | swap and shift for arrays |
| gpt-5.5 | 327 | 0.6495 | 0.6495 | 1.0 | 0 | 34 | LANG-1134: New methods for lang3.Validate This close... |
| deepseek-v4-pro | 215 | 0.3684 | 0.3684 | 1.0 | 0 | 24 | Sort by method name. |
| deepseek-v4-pro | 14 | 0.8 | 0.8 | 1.0 | 0 | 8 | LANG-1352: EnumUtils.getEnumIgnoreCase and isValidEn... |
| deepseek-v4-pro | 580 | 0.875 | 0.875 | 1.0 | 0 | 8 | LANG-1021: Provide methods to retrieve all fields/me... |
| gpt-5.5 | 14 | 0.8 | 0.8 | 1.0 | 0 | 8 | LANG-1352: EnumUtils.getEnumIgnoreCase and isValidEn... |
| deepseek-v4-pro | 127 | 0.7812 | 0.7812 | 1.0 | 0 | 7 | Syntax for optional tokens in DurationFormatUtils (#... |
| deepseek-v4-pro | 417 | 0.7727 | 0.7727 | 1.0 | 0 | 5 | [LANG-1568] FailableBooleanSupplier, FailableIntSupp... |
| deepseek-v4-pro | 147 | 0.8824 | 0.8824 | 1.0 | 0 | 2 | Code refactor to simplify Functions and new tests (#... |

## Notes

- Useful when method names diverge (rename/refactor) but testing intent may still overlap.
- Low coverage with high aligned body similarity indicates partial but accurate updates.
- Fingerprint collision can mis-align; combine with mutation testing for behavioral validation.
