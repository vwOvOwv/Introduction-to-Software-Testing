## 项目组织

这个仓库按实验步骤组织。根目录只放主流程脚本，工具脚本统一放在 `misc/`。

### 主流程

1. `1_scan.py`  
   扫描 `commons-lang` 历史，找出可能适合做实验的 A/B commit 对。

2. `2_filter.py`  
   清洗候选，去掉噪音提交，只保留更像 `Foo.java` / `FooTest.java` 配对的样本。

3. `3_verify.py`  
   在 B 提交上跑原始测试，确认候选本身能被 Maven 正常验证。

4. `4_run.py`  
   批量执行完整实验：生成测试、合并成 `generated.java`，再调用 Maven 验证。

### 工具脚本

- `misc/update_tests_utils.py`  
  prompt 构造、Java 测试方法抽取、模型输出合并、OpenAI 兼容接口请求。

- `misc/update_tests.py`  
  单独调用模型生成测试输出，主要用于 dry-run 和调试；正式实验由 `4_run.py` 自动调用。

- `misc/run_single_maven_test.py`  
  切换到指定 B commit，覆盖测试文件，运行 `mvn -Dtest=... test`，写 JSON 报告。

- `misc/merge_verified_pass.py`  
  合并 JDK 8 / JDK 17 等多份验证报告中的 pass 样本。

- `misc/build_results_md.py`  
  扫描实验产物，生成 `results.md`。

## 常用命令

```bash
python 1_scan.py
python 2_filter.py
python 3_verify.py --limit 5
python 4_run.py --limit 5 --skip-maven
```

模型调用需要设置：

```bash
export MODEL_API_BASE="https://..."
export MODEL_NAME="..."
export MODEL_API_KEY="..."
```

## 主要产物

- `artifacts/lang_sample_candidates*.json`：候选样本
- `artifacts/lang_sample_verify_report*.json`：候选验证结果
- `artifacts/model_tests/<model>/`：模型原始输出
- `artifacts/sample_runs/cand*/`：完整实验的单条产物

## 路径约定

默认被测仓库路径是 `../commons-lang`。如果放在其他位置，请通过对应脚本的 `--repo` 参数指定。
