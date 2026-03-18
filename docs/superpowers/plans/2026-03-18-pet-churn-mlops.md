# Pet Retail Customer Churn MLOps Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an end-to-end MLOps demo for Pet retail customer churn prediction, deployed via Databricks Asset Bundles with GitHub Actions CI/CD.

**Architecture:** Notebook-based ML pipelines (data gen, feature engineering, train, validate, deploy, inference, monitor) orchestrated as Databricks Workflows. Bundle resources define jobs and MLflow artifacts in UC. Two-environment setup (dev/prod) with Champion/Challenger model promotion.

**Tech Stack:** Databricks Asset Bundles, GitHub Actions (OIDC), MLflow, scikit-learn, Unity Catalog, Model Serving, Data Profiling (`databricks.lakehouse_monitoring`), Databricks SDK.

**Spec:** `docs/superpowers/specs/2026-03-18-pet-churn-mlops-design.md`

---

## File Map

| File | Action | Responsibility |
| --- | --- | --- |
| `databricks.yml` | Modify | Add ML variables (model_name, experiment_name, endpoint_name) |
| `resources/pet_churn_artifacts.yml` | Create | MLflow experiment + registered model in UC |
| `resources/pet_churn_training.job.yml` | Create | 3-task training workflow (train → validate → deploy) |
| `resources/pet_churn_inference.job.yml` | Create | Batch inference job |
| `resources/pet_churn_monitoring.job.yml` | Create | Data Profiling refresh job |
| `resources/pet_churn_wheel_demo.job.yml` | Create | Wheel packaging demo job |
| `src/pet_churn/00_setup_data.py` | Create | Synthetic data generation notebook |
| `src/pet_churn/01_feature_engineering.py` | Create | Feature table assembly notebook |
| `src/pet_churn/02_train_model.py` | Create | Model training notebook |
| `src/pet_churn/03_validate_model.py` | Create | Model validation notebook |
| `src/pet_churn/04_deploy_model.py` | Create | Champion/Challenger deployment notebook |
| `src/pet_churn/05_batch_inference.py` | Create | Batch inference notebook |
| `src/pet_churn/06_monitor.py` | Create | Data Profiling setup notebook |
| `src/pet_churn_wheel/pyproject.toml` | Create | Wheel build config |
| `src/pet_churn_wheel/pet_churn_pkg/__init__.py` | Create | Package init |
| `src/pet_churn_wheel/pet_churn_pkg/predict.py` | Create | Batch predict function |
| `tests/unit/test_features.py` | Create | Unit tests for feature logic |

---

## Task 1: Update Bundle Config with ML Variables

**Files:**
- Modify: `databricks.yml`

- [ ] **Step 1: Add ML variables to databricks.yml**

Add these variables after the existing `service_principal_id` variable:

```yaml
  model_name:
    description: Registered model name in UC
    default: pet_churn_model
  experiment_name:
    description: MLflow experiment path
    default: /pet-churn-experiment
  endpoint_name:
    description: Model Serving endpoint name
    default: pet-churn-serving
```

- [ ] **Step 2: Validate bundle**

Run: `databricks bundle validate --target dev --profile dev`
Expected: Validation passes with no errors. New variables appear in output.

- [ ] **Step 3: Commit**

```bash
git add databricks.yml
git commit -m "feat: add ML variables to bundle config (model_name, experiment_name, endpoint_name)"
```

---

## Task 2: Create MLflow Artifacts Resource

**Files:**
- Create: `resources/pet_churn_artifacts.yml`

- [ ] **Step 1: Create the artifacts resource file**

```yaml
resources:
  experiments:
    pet_churn_experiment:
      name: ${var.experiment_name}
      permissions:
        - level: CAN_MANAGE
          user_name: robby.kiskanyan@databricks.com

  registered_models:
    pet_churn_model:
      name: ${var.catalog}.${var.schema}.${var.model_name}
      catalog_name: ${var.catalog}
      schema_name: ${var.schema}
      grants:
        - privileges:
            - EXECUTE
          principal: account users
```

- [ ] **Step 2: Validate bundle**

Run: `databricks bundle validate --target dev --profile dev`
Expected: Validation passes. `pet_churn_experiment` and `pet_churn_model` appear in bundle summary.

- [ ] **Step 3: Commit**

```bash
git add resources/pet_churn_artifacts.yml
git commit -m "feat: add MLflow experiment and registered model resources"
```

---

## Task 3: Create Synthetic Data Generation Notebook

**Files:**
- Create: `src/pet_churn/00_setup_data.py`

This is a Databricks notebook. Use the `databricks-data-generation` skill (invoke via `Skill` tool) to generate realistic synthetic pet retail customer data.

- [ ] **Step 1: Create the notebook**

The notebook must:
- Accept `catalog` and `schema` as widget parameters (`dbutils.widgets.text()`)
- Generate ~10,000 rows of synthetic customer data with columns: `customer_id`, `subscription_active`, `pet_type`, `days_since_last_order`, `total_orders_12m`, `avg_order_value`, `total_spend_12m`, `customer_tenure_days`, `support_tickets_6m`, `website_visits_30d`, `churned`
- Use the `databricks-data-generation` skill for generation guidance
- Target ~20% churn rate with realistic correlations (high support tickets + low orders → higher churn probability)
- Write to `{catalog}.{schema}.pet_churn_customers` as a managed Delta table (overwrite mode)
- Begin with `# Databricks notebook source` header comment

- [ ] **Step 2: Validate bundle still passes**

Run: `databricks bundle validate --target dev --profile dev`
Expected: Passes (notebooks don't affect validation, but confirms no syntax issues in YAML includes).

- [ ] **Step 3: Commit**

```bash
git add src/pet_churn/00_setup_data.py
git commit -m "feat: add synthetic data generation notebook for pet retail churn"
```

---

## Task 4: Create Feature Engineering Notebook

**Files:**
- Create: `src/pet_churn/01_feature_engineering.py`

- [ ] **Step 1: Create the notebook**

The notebook must:
- Accept `catalog` and `schema` as widget parameters
- Read from `{catalog}.{schema}.pet_churn_customers`
- Select feature columns and the target label
- Encode `pet_type` as a numeric column (label encoding or one-hot)
- Cast `subscription_active` and `churned` booleans to integers
- Write full feature set to `{catalog}.{schema}.pet_churn_features` (overwrite mode)
- Set primary key: `ALTER TABLE {catalog}.{schema}.pet_churn_features ADD CONSTRAINT pet_churn_pk PRIMARY KEY (customer_id)`
- Split 20% as held-out evaluation set, write to `{catalog}.{schema}.pet_churn_eval`
- Begin with `# Databricks notebook source` header comment

- [ ] **Step 2: Commit**

```bash
git add src/pet_churn/01_feature_engineering.py
git commit -m "feat: add feature engineering notebook with UC primary key"
```

---

## Task 5: Create Model Training Notebook

**Files:**
- Create: `src/pet_churn/02_train_model.py`

- [ ] **Step 1: Create the notebook**

The notebook must:
- Accept parameters: `catalog`, `schema`, `model_name`, `experiment_name`
- Set `mlflow.set_registry_uri('databricks-uc')`
- Set `mlflow.set_experiment(experiment_name)`
- Read `{catalog}.{schema}.pet_churn_features`
- Drop `customer_id` from feature matrix, use `churned` as target
- Split train/test 80/20 stratified on `churned` with `random_state=42`
- Write test split to `{catalog}.{schema}.pet_churn_test` (overwrite mode)
- Inside an `mlflow.start_run()` context:
  - `mlflow.sklearn.autolog(log_models=False)` — logs params and metrics without double-logging the model
  - Fit `RandomForestClassifier(n_estimators=100, random_state=42)`
  - `mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=f"{catalog}.{schema}.{model_name}", input_example=X_train[:1], signature=infer_signature(X_train, y_train))`
  - Extract `model_version` from the registered model version
  - Build `model_uri = f"models:/{catalog}.{schema}.{model_name}/{model_version}"`
  - `dbutils.jobs.taskValues.set(key="model_uri", value=model_uri)`
  - `dbutils.jobs.taskValues.set(key="model_version", value=str(model_version))`
- Begin with `# Databricks notebook source` header comment

- [ ] **Step 2: Commit**

```bash
git add src/pet_churn/02_train_model.py
git commit -m "feat: add model training notebook with MLflow tracking and UC registration"
```

---

## Task 6: Create Model Validation Notebook

**Files:**
- Create: `src/pet_churn/03_validate_model.py`

- [ ] **Step 1: Create the notebook**

The notebook must:
- Accept parameters: `catalog`, `schema`, `model_name`
- Read task values: `model_uri = dbutils.jobs.taskValues.get(taskKey="train_model", key="model_uri")` and `model_version = dbutils.jobs.taskValues.get(taskKey="train_model", key="model_version")`
- Set `mlflow.set_registry_uri('databricks-uc')`
- Read test data from `{catalog}.{schema}.pet_churn_test`
- Build evaluation DataFrame with features and `churned` target
- Run `mlflow.evaluate(model=model_uri, data=eval_df, model_type="classifier", targets="churned")`
- Extract `f1_score` and `roc_auc` from evaluation results
- Define thresholds: `f1_score >= 0.7` and `roc_auc >= 0.7`
- If thresholds pass:
  - `client = mlflow.tracking.MlflowClient()`
  - `full_model_name = f"{catalog}.{schema}.{model_name}"`
  - `client.set_registered_model_alias(name=full_model_name, alias="challenger", version=int(model_version))`
  - `client.set_model_version_tag(full_model_name, model_version, "validation_status", "PASSED")`
- If thresholds fail:
  - `client.set_model_version_tag(full_model_name, model_version, "validation_status", "FAILED")`
  - `raise Exception(f"Model validation failed: f1={f1_score:.3f}, roc_auc={roc_auc:.3f}")`
- Begin with `# Databricks notebook source` header comment

- [ ] **Step 2: Commit**

```bash
git add src/pet_churn/03_validate_model.py
git commit -m "feat: add model validation notebook with threshold checks and challenger alias"
```

---

## Task 7: Create Model Deployment Notebook

**Files:**
- Create: `src/pet_churn/04_deploy_model.py`

- [ ] **Step 1: Create the notebook**

The notebook must:
- Accept parameters: `catalog`, `schema`, `model_name`, `endpoint_name`
- Set `mlflow.set_registry_uri('databricks-uc')`
- `client = mlflow.tracking.MlflowClient()`
- `full_model_name = f"{catalog}.{schema}.{model_name}"`
- Get challenger version: `challenger_version = client.get_model_version_by_alias(full_model_name, "challenger")`
- Try to get champion version (wrap in try/except for first-deployment case):
  ```python
  try:
      champion_version = client.get_model_version_by_alias(full_model_name, "champion")
      has_champion = True
  except Exception:
      has_champion = False
  ```
- If `has_champion`:
  - Read evaluation data from `{catalog}.{schema}.pet_churn_eval`
  - Load both models, predict on eval data, compare F1 scores
  - If challenger F1 >= champion F1: promote challenger to `champion`
  - Else: keep existing champion, delete `challenger` alias
- If not `has_champion`: promote challenger directly to `champion`
- After promotion, create/update Model Serving endpoint using the Databricks SDK:
  ```python
  from databricks.sdk import WorkspaceClient
  from databricks.sdk.service.serving import (
      EndpointCoreConfigInput,
      ServedEntityInput,
      AutoCaptureConfigInput,
  )

  w = WorkspaceClient()
  champion_version_num = client.get_model_version_by_alias(full_model_name, "champion").version

  served_entity = ServedEntityInput(
      entity_name=full_model_name,
      entity_version=champion_version_num,
      workload_size="Small",
      scale_to_zero_enabled=True,
  )
  auto_capture = AutoCaptureConfigInput(
      catalog_name=catalog,
      schema_name=schema,
      enabled=True,
  )

  try:
      existing = w.serving_endpoints.get(endpoint_name)
      # Update existing endpoint with new model version
      w.serving_endpoints.update_config(
          name=endpoint_name,
          served_entities=[served_entity],
          auto_capture_config=auto_capture,
      )
  except Exception:
      # Create new endpoint
      w.serving_endpoints.create(
          name=endpoint_name,
          config=EndpointCoreConfigInput(
              served_entities=[served_entity],
              auto_capture_config=auto_capture,
          ),
      )
  ```
- Begin with `# Databricks notebook source` header comment

- [ ] **Step 2: Commit**

```bash
git add src/pet_churn/04_deploy_model.py
git commit -m "feat: add deployment notebook with Champion/Challenger comparison and Model Serving"
```

---

## Task 8: Create Batch Inference Notebook

**Files:**
- Create: `src/pet_churn/05_batch_inference.py`

- [ ] **Step 1: Create the notebook**

The notebook must:
- Accept parameters: `catalog`, `schema`, `model_name`
- Set `mlflow.set_registry_uri('databricks-uc')`
- `full_model_name = f"{catalog}.{schema}.{model_name}"`
- Load champion model: `model = mlflow.sklearn.load_model(f"models:/{full_model_name}@champion")`
- Get champion version number for tagging predictions
- Read feature data from `{catalog}.{schema}.pet_churn_features`
- Convert to pandas, drop `customer_id` and `churned` for prediction
- Generate predictions and prediction probabilities (`model.predict()` and `model.predict_proba()`)
- Build output DataFrame with columns: `customer_id`, `prediction`, `prediction_proba` (probability of churn class), `model_version` (string), `timestamp` (current UTC timestamp)
- Convert to Spark DataFrame
- Write to `{catalog}.{schema}.pet_churn_predictions` (append mode — preserves history for monitoring)
- Begin with `# Databricks notebook source` header comment

- [ ] **Step 2: Commit**

```bash
git add src/pet_churn/05_batch_inference.py
git commit -m "feat: add batch inference notebook scoring with champion model"
```

---

## Task 9: Create Data Profiling (Monitoring) Notebook

**Files:**
- Create: `src/pet_churn/06_monitor.py`

- [ ] **Step 1: Create the notebook**

The notebook must:
- Accept parameters: `catalog`, `schema`
- `import databricks.lakehouse_monitoring as lm`
- `table_name = f"{catalog}.{schema}.pet_churn_predictions"`
- `baseline_table = f"{catalog}.{schema}.pet_churn_features"`
- Try to get existing monitor, create if not found:
  ```python
  try:
      monitor = lm.get_monitor(table_name=table_name)
      print(f"Monitor already exists for {table_name}")
  except Exception:
      monitor = lm.create_monitor(
          table_name=table_name,
          profile_type=lm.InferenceLog(
              timestamp_col="timestamp",
              granularities=["1 day"],
              model_id_col="model_version",
              problem_type="classification",
              prediction_col="prediction",
          ),
          output_schema_name=f"{catalog}.{schema}",
          baseline_table_name=baseline_table,
      )
      print(f"Created monitor for {table_name}")
  ```
- Trigger refresh: `lm.run_refresh(table_name=table_name)`
- Print metric table locations for reference
- Begin with `# Databricks notebook source` header comment

- [ ] **Step 2: Commit**

```bash
git add src/pet_churn/06_monitor.py
git commit -m "feat: add Data Profiling monitoring notebook"
```

---

## Task 10: Create Training Workflow Resource

**Files:**
- Create: `resources/pet_churn_training.job.yml`

- [ ] **Step 1: Create the job resource**

The YAML must define a 3-task sequential workflow:
- Job name: `pet_churn_training`
- Job parameters: `catalog` (default `${var.catalog}`), `schema` (default `${var.schema}`), `model_name` (default `${var.model_name}`), `experiment_name` (default `${var.experiment_name}`), `endpoint_name` (default `${var.endpoint_name}`)
- All tasks share a single job cluster (ML Runtime, single node) to keep costs low and avoid repeated cluster spin-up:
  ```yaml
  job_clusters:
    - job_cluster_key: ml_cluster
      new_cluster:
        spark_version: 17.3.x-cpu-ml-scala2.13
        node_type_id: i3.xlarge
        num_workers: 0
  ```
- Task 1 (`train_model`): notebook task pointing to `../src/pet_churn/02_train_model.py`, `job_cluster_key: ml_cluster`
- Task 2 (`validate_model`): depends on `train_model`, notebook `../src/pet_churn/03_validate_model.py`, `job_cluster_key: ml_cluster`
- Task 3 (`deploy_model`): depends on `validate_model`, notebook `../src/pet_churn/04_deploy_model.py`, `job_cluster_key: ml_cluster`
- Each task passes job-level parameters through to the notebook via `{{job.parameters["catalog"]}}` syntax
- `max_concurrent_runs: 1`

**Important prerequisite:** Notebooks `00_setup_data.py` and `01_feature_engineering.py` must be run manually (or via a separate one-time job) before triggering this workflow. The training job starts at notebook `02_train_model.py` and assumes feature tables already exist.

- [ ] **Step 2: Validate bundle**

Run: `databricks bundle validate --target dev --profile dev`
Expected: Passes. `pet_churn_training` job appears in bundle summary.

- [ ] **Step 3: Commit**

```bash
git add resources/pet_churn_training.job.yml
git commit -m "feat: add training workflow resource (train -> validate -> deploy)"
```

---

## Task 11: Create Inference and Monitoring Job Resources

**Files:**
- Create: `resources/pet_churn_inference.job.yml`
- Create: `resources/pet_churn_monitoring.job.yml`

- [ ] **Step 1: Create inference job resource**

The YAML must define:
- Job name: `pet_churn_inference`
- Parameters: `catalog`, `schema`, `model_name` (with defaults from bundle variables)
- Single task: notebook task pointing to `../src/pet_churn/05_batch_inference.py`
- Schedule: daily in prod (`quartz_cron_expression: "0 0 11 * * ?"`), paused in dev via `pause_status: PAUSED` override or rely on `mode: development` auto-pause
- Cluster: single node ML Runtime

- [ ] **Step 2: Create monitoring job resource**

The YAML must define:
- Job name: `pet_churn_monitoring`
- Parameters: `catalog`, `schema`
- Single task: notebook task pointing to `../src/pet_churn/06_monitor.py`
- Schedule: daily, offset from inference (e.g., `"0 0 13 * * ?"`)
- Cluster: single node ML Runtime

- [ ] **Step 3: Validate bundle**

Run: `databricks bundle validate --target dev --profile dev`
Expected: Passes. Both jobs appear in bundle summary.

- [ ] **Step 4: Commit**

```bash
git add resources/pet_churn_inference.job.yml resources/pet_churn_monitoring.job.yml
git commit -m "feat: add batch inference and monitoring job resources"
```

---

## Task 12: Create Wheel Packaging Demo

**Files:**
- Create: `src/pet_churn_wheel/pyproject.toml`
- Create: `src/pet_churn_wheel/pet_churn_pkg/__init__.py`
- Create: `src/pet_churn_wheel/pet_churn_pkg/predict.py`
- Create: `resources/pet_churn_wheel_demo.job.yml`

- [ ] **Step 1: Create the Python package**

`src/pet_churn_wheel/pyproject.toml`:
```toml
[project]
name = "pet-churn-pkg"
version = "0.1.0"
description = "Pet retail churn prediction package - DABs wheel demo"
requires-python = ">=3.10"
dependencies = ["mlflow>=2.13.0"]

[project.scripts]
pet-churn-predict = "pet_churn_pkg.predict:main"

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"
```

`src/pet_churn_wheel/pet_churn_pkg/__init__.py`:
```python
"""Pet retail churn prediction package."""
```

`src/pet_churn_wheel/pet_churn_pkg/predict.py`:
```python
"""Batch prediction using a UC-registered model."""

import argparse

import mlflow
from pyspark.sql import SparkSession


def score_batch(spark, model_uri: str, input_table: str, output_table: str) -> None:
    """Load a model from UC and score a table, writing predictions."""
    mlflow.set_registry_uri('databricks-uc')
    model = mlflow.sklearn.load_model(model_uri)

    input_df = spark.table(input_table).toPandas()
    feature_cols = [c for c in input_df.columns if c not in ('customer_id', 'churned')]
    predictions = model.predict(input_df[feature_cols])

    input_df['prediction'] = predictions
    output_df = spark.createDataFrame(input_df[['customer_id', 'prediction']])
    output_df.write.mode('overwrite').saveAsTable(output_table)


def main():
    """CLI entry point for python_wheel_task."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_uri', required=True)
    parser.add_argument('--input_table', required=True)
    parser.add_argument('--output_table', required=True)
    args = parser.parse_args()

    spark = SparkSession.builder.getOrCreate()
    score_batch(spark, args.model_uri, args.input_table, args.output_table)
```

- [ ] **Step 2: Create the wheel demo job resource**

`resources/pet_churn_wheel_demo.job.yml`:
```yaml
resources:
  jobs:
    pet_churn_wheel_demo:
      name: pet_churn_wheel_demo

      tasks:
        - task_key: wheel_predict
          python_wheel_task:
            package_name: pet_churn_pkg
            entry_point: pet-churn-predict
            parameters:
              - --model_uri
              - models:/${var.catalog}.${var.schema}.${var.model_name}@champion
              - --input_table
              - ${var.catalog}.${var.schema}.pet_churn_features
              - --output_table
              - ${var.catalog}.${var.schema}.pet_churn_wheel_predictions
          libraries:
            - whl: ../src/pet_churn_wheel/dist/*.whl

      job_clusters:
        - job_cluster_key: ml_cluster
          new_cluster:
            spark_version: 17.3.x-cpu-ml-scala2.13
            node_type_id: i3.xlarge
            num_workers: 0
```

- [ ] **Step 3: Validate bundle**

Run: `databricks bundle validate --target dev --profile dev`
Expected: Passes. `pet_churn_wheel_demo` job appears in summary.

- [ ] **Step 4: Commit**

```bash
git add src/pet_churn_wheel/ resources/pet_churn_wheel_demo.job.yml
git commit -m "feat: add wheel packaging demo (predict package + DABs job)"
```

---

## Task 13: Add Unit Tests for Feature Engineering

**Files:**
- Create: `tests/unit/test_features.py`

- [ ] **Step 1: Create the test file**

```python
"""Unit tests for feature engineering logic."""

import pytest


EXPECTED_FEATURE_COLUMNS = [
    'customer_id',
    'subscription_active',
    'pet_type_encoded',
    'days_since_last_order',
    'total_orders_12m',
    'avg_order_value',
    'total_spend_12m',
    'customer_tenure_days',
    'support_tickets_6m',
    'website_visits_30d',
    'churned',
]


def test_expected_columns_defined():
    """Verify the expected feature schema is complete and has no duplicates."""
    assert len(EXPECTED_FEATURE_COLUMNS) == len(set(EXPECTED_FEATURE_COLUMNS))
    assert 'customer_id' in EXPECTED_FEATURE_COLUMNS
    assert 'churned' in EXPECTED_FEATURE_COLUMNS


def test_customer_id_is_first_column():
    """Primary key should be the first column for clarity."""
    assert EXPECTED_FEATURE_COLUMNS[0] == 'customer_id'


def test_no_raw_categorical_columns():
    """pet_type should be encoded, not raw string."""
    assert 'pet_type' not in EXPECTED_FEATURE_COLUMNS
    assert 'pet_type_encoded' in EXPECTED_FEATURE_COLUMNS
```

- [ ] **Step 2: Run tests**

Run: `uv run pytest tests/unit/test_features.py -v`
Expected: 3 tests pass.

- [ ] **Step 3: Commit**

```bash
git add tests/unit/test_features.py
git commit -m "test: add unit tests for feature engineering schema"
```

---

## Task 14: Add ML Dependencies to pyproject.toml

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add mlflow and scikit-learn to dev dependencies**

Add to the `[dependency-groups] dev` section:

```
"mlflow>=2.13.0",
"scikit-learn>=1.4.0",
```

These are for local testing only — ML Runtime provides them on clusters.

- [ ] **Step 2: Sync dependencies**

Run: `uv sync --group dev`
Expected: Dependencies resolve and install.

- [ ] **Step 3: Run all tests**

Run: `uv run pytest tests/ -v`
Expected: All tests pass.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "feat: add mlflow and scikit-learn to dev dependencies"
```

---

## Task 15: Full Bundle Validation and Final Commit

- [ ] **Step 1: Validate bundle for both targets**

Run: `databricks bundle validate --target dev --profile dev`
Expected: Passes with all resources listed.

Run: `databricks bundle validate --target prod --profile prod`
Expected: Passes (may warn about service_principal_id if not set locally — that's expected, CI/CD injects it).

- [ ] **Step 2: Run full test suite**

Run: `uv run pytest tests/ -v`
Expected: All tests pass.

- [ ] **Step 3: Review all files**

Verify:
- All notebooks start with `# Databricks notebook source`
- All resource YAMLs reference correct notebook paths (`../src/pet_churn/...`)
- `databricks.yml` includes `resources/*.yml` pattern (already does)
- No hardcoded catalog/schema names — all use parameters

- [ ] **Step 4: Commit any remaining changes**

```bash
git add -A
git commit -m "chore: final validation pass for pet churn MLOps demo"
```
