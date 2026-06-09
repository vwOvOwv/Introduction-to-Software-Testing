# Delta-AST Similarity Report

Compares **changes relative to `old_test.java`** between LLM-generated tests and human tests (commit B).

## Method

1. Classify delta methods as added / deleted / modified using normalized AST token sequences.
2. Align LLM delta vs human delta:
   - modified methods: same name
   - added methods: same name first, then SUT-call fingerprint (Jaccard >= 0.3)
3. Compute token-sequence similarity (Ratcliff/Obershelp) per aligned pair.
4. Aggregate with denominator `max(|LLM changes|, |Human changes|)` where changes = added + modified + deleted;
   unmatched delta methods contribute 0; if both sides have no changes, score = 1.0.

- Scope: Maven-pass samples only
- Comparable rows: 1101
- Errors: 20
- Skipped: 107

## Summary

| model | comparable_rows | mean_delta_method_ast_similarity | mean_delta_added_ast_sim | mean_delta_modified_ast_sim | median |
|---|---:|---:|---:|---:|---:|
| deepseek-v4-pro | 559 | 0.9605 | 0.9567 | 1.0 | 1.0 |
| gpt-5.5 | 542 | 0.9757 | 0.978 | 1.0 | 1.0 |

## Lowest Delta-AST Samples

| model | cand | delta_method_ast_similarity | delta_added_ast_sim | llm_added | human_added | llm_modified | human_modified | subject |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| deepseek-v4-pro | 58 | 0.0 | 0.0 | 0 | 3 | 0 | 0 | [LANG-1568] More failable functional interfaces to match JRE functional inter... |
| deepseek-v4-pro | 72 | 0.0 | 0.0 | 0 | 2 | 0 | 0 | LANG-1495 Update EnumUtils.java (#475) |
| deepseek-v4-pro | 182 | 0.0 | 0.0 | 0 | 1 | 0 | 0 | LANG-1348 - StackOverflowError on TypeUtils.toString(...) for a generic retur... |
| deepseek-v4-pro | 194 | 0.0 | 0.0 | 0 | 1 | 0 | 0 | LANG-1371: Fix TypeUtils.parameterize to work correctly with narrower-typed v... |
| deepseek-v4-pro | 201 | 0.0 | 0.0 | 0 | 1 | 0 | 0 | #LAN-1114 fixes bug in TypeUtils.equals(WildcardType, Type) where it was inco... |
| deepseek-v4-pro | 215 | 0.0 | 1.0 | 0 | 0 | 0 | 0 | Sort by method name. |
| deepseek-v4-pro | 223 | 0.0 | 0.0 | 0 | 1 | 0 | 0 | LANG-1223: Add StopWatch#getTime(TimeUnit) (closes #152) |
| deepseek-v4-pro | 247 | 0.0 | 0.0 | 0 | 1 | 0 | 0 | LANG-1190: TypeUtils.isAssignable throws NullPointerException when fromType h... |
| deepseek-v4-pro | 248 | 0.0 | 0.0 | 0 | 1 | 0 | 0 | LANG-1311: TypeUtils.toString() doesn't handle primitive and Object arrays co... |
| deepseek-v4-pro | 312 | 0.0 | 0.0 | 0 | 1 | 0 | 0 | EnumUtils.getEnumSystemProperty(...). |

## Notes

- Unlike whole-file Jaccard, this metric ignores unchanged test methods.
- A low score with high `method_name_jaccard` usually means missing added tests or weak modified bodies.
- AST token similarity is structural; it does not guarantee behavioral equivalence.
