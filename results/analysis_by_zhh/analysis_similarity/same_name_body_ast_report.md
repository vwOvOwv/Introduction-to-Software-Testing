# Same-Name Method Body AST Similarity Report

For `@Test` methods with **identical names** in LLM and human tests, compares normalized AST token sequences of method bodies.

## Method

1. Take `Common = methods(generated) ∩ methods(human)`.
2. Normalize each method body:
   - strip comments/whitespace via AST walk
   - rename parameters (`p0..`) and locals (`v0..`)
   - normalize literal categories (`LIT:number`, `LIT:string`, ...)
3. Compute Ratcliff/Obershelp similarity per common method.
4. Aggregate:
   - `same_name_body_ast_similarity`: mean over all common methods
   - `same_name_body_ast_similarity_modified`: mean only where LLM or human changed vs `old_test`, or LLM≠human

- Scope: Maven-pass samples only
- Comparable rows: 1101
- Errors: 20
- Skipped: 107

## Summary

| model | comparable_rows | mean_all | mean_modified | mean_min | mean_p10 | mean_mismatched_methods | median_modified |
|---|---:|---:|---:|---:|---:|---:|---:|
| deepseek-v4-pro | 559 | 1.0 | 1.0 | 1.0 | 1.0 | 0.0 | 1.0 |
| gpt-5.5 | 542 | 1.0 | 1.0 | 1.0 | 1.0 | 0.0 | 1.0 |

## Lowest Modified Same-Name Body Similarity

| model | cand | same_name_modified | same_name_all | min | p10 | mismatched | common | modified_common | subject |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| deepseek-v4-pro | 5 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 90 | 1 | clarify behavior of #isNumber() with blanks |
| deepseek-v4-pro | 6 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 27 | 1 | incorporated feedback from Fabian, formatting adjusted, count ... |
| deepseek-v4-pro | 7 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 266 | 1 | tabs replaced by spaces new tests added |
| deepseek-v4-pro | 8 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 147 | 2 | LANG-1475 Fix unwrap StringIndexOutOfBoundsException |
| deepseek-v4-pro | 9 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 174 | 2 | [LANG-1784] Add Failable methods for null-safe mapping and cha... |
| deepseek-v4-pro | 11 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 104 | 1 | LANG-1408: add toDouble(BigDecimal), toDouble(BigDecimal, double) |
| deepseek-v4-pro | 17 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 91 | 1 | LANG-1276: StrBuilder#replaceAll ArrayIndexOutOfBoundsExceptio... |
| deepseek-v4-pro | 21 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 125 | 1 | NumberUtils.isCreatable(String) should match NumberUtils.creat... |
| deepseek-v4-pro | 23 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 344 | 1 | Instead of throwing a NullPointerException, ArrayUtils.toStrin... |
| deepseek-v4-pro | 25 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 46 | 1 | Use Java 8 API to manage thread local |

## Notes

- High `same_name_body_ast_similarity` with low mutation score may indicate weakened assertions.
- Prefer `same_name_body_ast_similarity_modified` over the all-common mean to avoid unchanged methods inflating scores.
- Renamed tests are out of scope; see alignment-based metric (metric 4) for those cases.
