# Model Test Update Results

## Summary

| model | total | legal tests generated | maven_pass | maven_fail |  merge_incomplete | pass_rate | pass_given_generated |
|---|---:|---:|---:|---:|---:|---:|---:|
| deepseek-v4-pro | 614 | 603 | 561 | 42 | 11 | 0.9137 | 0.9303 |
| gpt-5.5 | 614 | 600 | 560 | 40 | 14 | 0.9121 | 0.9333 |

## Maven Failure Breakdown

| model | failure_category | count | rate |
|---|---|---:|---:|
| deepseek-v4-pro | compile_cannot_find_symbol | 10 | 0.0163 |
| deepseek-v4-pro | compile_error | 17 | 0.0277 |
| deepseek-v4-pro | compile_incompatible_types | 1 | 0.0016 |
| deepseek-v4-pro | compile_missing_package | 2 | 0.0033 |
| deepseek-v4-pro | maven_other_failure | 8 | 0.0130 |
| deepseek-v4-pro | rat_license_check | 2 | 0.0033 |
| deepseek-v4-pro | test_failure | 2 | 0.0033 |
| gpt-5.5 | compile_cannot_find_symbol | 12 | 0.0195 |
| gpt-5.5 | compile_error | 16 | 0.0261 |
| gpt-5.5 | compile_incompatible_types | 1 | 0.0016 |
| gpt-5.5 | maven_other_failure | 8 | 0.0130 |
| gpt-5.5 | rat_license_check | 1 | 0.0016 |
| gpt-5.5 | test_failure | 2 | 0.0033 |

## Merge Incomplete Breakdown

`merge_incomplete` means that the model returned `raw.md`, but the post-processing step failed to merge it into a valid `generated.java`.
These cases were not Maven failures; they failed before Maven validation.

| model | reason | count | candidates |
|---|---|---:|---|
| deepseek-v4-pro | output truncated (`finish_reason=length`) | 3 | 198, 511, 527 |
| deepseek-v4-pro | malformed Java block / unmatched braces | 7 | 48, 122, 148, 299, 402, 551, 564 |
| deepseek-v4-pro | delete markers but method names did not match old tests | 1 | 582 |
| gpt-5.5 | empty patch because model judged no test change was needed | 10 | 110, 139, 197, 215, 431, 445, 492, 495, 558, 606 |
| gpt-5.5 | malformed Java block / unmatched braces | 1 | 402 |
| gpt-5.5 | partial class header / annotation only, not a complete class or method | 2 | 444, 565 |
| gpt-5.5 | delete markers but method names did not match old tests | 1 | 582 |

The largest group is the `gpt-5.5` empty-patch group. These are mostly formatting, comment, or metadata-only commits where the model explicitly decided that no test method needed to be changed. They should be interpreted as post-processing limitations rather than direct model failures. A future merge rule can treat an empty Java block plus a clear "no change needed" explanation as:

```text
generated.java = old_test.java
```

and then run Maven normally.

## Takeaways

- Both models successfully produced legal tests for most samples: 603/614 for `deepseek-v4-pro` and 600/614 for `gpt-5.5`.
- Their Maven pass rates are very close: 0.9137 for `deepseek-v4-pro` and 0.9121 for `gpt-5.5`.
- Most Maven failures are compilation-related, especially unresolved symbols and general compilation errors.
- `merge_incomplete` is a separate post-processing category, not a Maven failure category.
- Several `merge_incomplete` cases can likely be recovered by improving the merge policy for empty patches, delete-only patches, and truncated model outputs.
