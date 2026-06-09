# Human vs LLM Test Quality

This report compares Maven-pass LLM tests with the corresponding human tests at commit B.

## Summary

| model | rows | human_line | llm_line | human_branch | llm_branch | human_instruction | llm_instruction | human_method | llm_method | human_mutation | llm_mutation |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek-v4-pro | 561 | 0.8780 | 0.8763 | 0.7867 | 0.7844 | 0.8764 | 0.8745 | 0.8857 | 0.8831 | 0.8061 | 0.8061 |
| gpt-5.5 | 560 | 0.8772 | 0.8755 | 0.7829 | 0.7808 | 0.8752 | 0.8734 | 0.8838 | 0.8815 |  |  |

## Coverage Failure Breakdown

| model | side | category | count |
|---|---|---|---:|
| deepseek-v4-pro | human | test_failure | 3 |
| deepseek-v4-pro | llm | test_failure | 3 |
| gpt-5.5 | human | test_failure | 2 |
| gpt-5.5 | llm | test_failure | 2 |

## Mutation Failure Breakdown

| model | side | category | count |
|---|---|---|---:|
