# Chewy Customer Churn MLOps Demo — Design Spec

## Overview

A customer churn prediction demo for Chewy, showcasing end-to-end MLOps on Databricks using the deploy code pattern. Built with Databricks Asset Bundles, GitHub Actions CI/CD, MLflow, Unity Catalog, Model Serving, and Data Profiling.

**Use case:** Predict whether a Chewy customer will churn based on behavioral and transactional features (subscription status, order frequency, pet type, days since last order, etc.).

**Model:** scikit-learn RandomForestClassifier with `mlflow.sklearn.autolog(log_models=False)` for param/metric tracking, plus explicit `mlflow.sklearn.log_model()` for controlled model registration.

**Compute:** ML Runtime 17.3 LTS (Spark 4.0, provides MLflow, scikit-learn, pandas pre-installed).

**Environments:** Dev (`bu1_dev`) and Prod (`bu1_prod`) — two Unity Catalog catalogs, two DAB targets.

## Decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Deployment pattern | Deploy code | Recommended by Big Book of MLOps v2; all pipelines tested before prod |
| Data | Synthetic generation | Self-contained demo, no external dependencies |
| Feature engineering | Lightweight | Focus on MLOps lifecycle, not data engineering |
| Model | Single scikit-learn classifier | Workshop is about ops, not model selection |
| Inference | Batch + Model Serving endpoint | Full story; serving produces inference tables for monitoring |
| Pipeline structure | Notebook-based (Approach A) | Clear demo flow, good Databricks UI rendering |
| Environments | 2 (dev + prod) | Simplified for workshop; dev doubles as staging |
| Wheel packaging | Side demo only | Show capability without complicating main flow |

## Bundle Structure

```
dbx-devx-workshop-mlops/
├── databricks.yml                               # Updated with ML variables
├── resources/
│   ├── devx_lakeflow_project_etl.pipeline.yml   # Existing SDP pipeline (unchanged)
│   ├── sample_job.job.yml                        # Existing ETL job (unchanged)
│   ├── chewy_churn_training.job.yml              # Train -> Validate -> Deploy workflow
│   ├── chewy_churn_inference.job.yml             # Batch inference job
│   ├── chewy_churn_monitoring.job.yml            # Data Profiling refresh
│   ├── chewy_churn_artifacts.yml                 # MLflow experiment + registered model in UC
│   └── chewy_churn_wheel_demo.job.yml            # Wheel packaging demo job
├── src/
│   ├── transformations/                          # Existing SDP code (unchanged)
│   ├── chewy_churn/                              # ML notebooks
│   │   ├── 00_setup_data.py                      # Synthetic data generation
│   │   ├── 01_feature_engineering.py             # Feature table assembly
│   │   ├── 02_train_model.py                     # Train + MLflow + register to UC
│   │   ├── 03_validate_model.py                  # Validation + assign @challenger
│   │   ├── 04_deploy_model.py                    # Champion vs Challenger + serving
│   │   ├── 05_batch_inference.py                 # Score with @champion
│   │   └── 06_monitor.py                         # Data Profiling setup + refresh
│   └── chewy_churn_wheel/                        # Python wheel demo
│       ├── pyproject.toml
│       └── chewy_churn_pkg/
│           ├── __init__.py
│           └── predict.py
├── .github/workflows/                            # Existing (no changes)
│   ├── validate_dev.yml
│   ├── deploy_dev.yml
│   └── deploy_prod.yml
└── tests/
    └── unit/
        └── test_features.py
```

## Bundle Variables (additions to databricks.yml)

```yaml
variables:
  # existing
  catalog:
    description: Unity Catalog name
    default: main
  schema:
    description: Schema name for tables
    default: default
  service_principal_id:
    description: Application ID of the service principal for CI/CD

  # new ML variables
  model_name:
    description: Registered model name in UC
    default: chewy_churn_model
  experiment_name:
    description: MLflow experiment path
    default: /chewy-churn-experiment
  endpoint_name:
    description: Model Serving endpoint name
    default: chewy-churn-serving
```

Target overrides remain as-is: dev uses `bu1_dev`/`devx_workshop`, prod uses `bu1_prod`/`devx_workshop`.

## Resource Definitions

### chewy_churn_artifacts.yml

Declares the MLflow experiment and registered model as UC-managed resources:

```yaml
resources:
  experiments:
    chewy_churn_experiment:
      name: ${var.experiment_name}
      permissions:
        - level: CAN_MANAGE
          user_name: robby.kiskanyan@databricks.com

  registered_models:
    chewy_churn_model:
      name: ${var.catalog}.${var.schema}.${var.model_name}
      catalog_name: ${var.catalog}
      schema_name: ${var.schema}
      grants:
        - privileges:
            - EXECUTE
          principal: account users
```

### chewy_churn_training.job.yml

Three-task sequential workflow:

**Task 1: train_model**
- Notebook: `src/chewy_churn/02_train_model.py`
- Reads `{catalog}.{schema}.chewy_churn_features`
- Train/test split (80/20, stratified)
- Fits `RandomForestClassifier`
- `mlflow.sklearn.autolog(log_models=False)` logs params, metrics, confusion matrix
- Explicit `mlflow.sklearn.log_model()` registers model to `{catalog}.{schema}.chewy_churn_model`
- Sets `model_uri` as task value via `dbutils.jobs.taskValues.set()`

**Task 2: validate_model** (depends on Task 1)
- Notebook: `src/chewy_churn/03_validate_model.py`
- Reads `model_uri` from task values
- Loads model from UC
- Runs `mlflow.evaluate()` with classification metrics
- Validation thresholds: F1 >= 0.7, AUC >= 0.7
- On pass: `client.set_registered_model_alias(..., alias="challenger")`
- On fail: tags model version with `validation_status: FAILED`, raises exception

**Task 3: deploy_model** (depends on Task 2)
- Notebook: `src/chewy_churn/04_deploy_model.py`
- Loads `@challenger` model version
- If `@champion` alias exists: loads champion, compares both on held-out evaluation data, winner gets `champion` alias
- If no champion: challenger auto-promotes to `champion`
- Creates or updates Model Serving endpoint named `{endpoint_name}` targeting the `champion` model version
- Enables inference table logging

### chewy_churn_inference.job.yml

Single-task batch inference job:
- Notebook: `src/chewy_churn/05_batch_inference.py`
- Loads model via `models:/{catalog}.{schema}.{model_name}@champion`
- Reads new/unscored customer data from feature table
- Writes predictions to `{catalog}.{schema}.chewy_churn_predictions`
- Scheduled daily in prod, paused in dev

### chewy_churn_monitoring.job.yml

Single-task monitoring job:
- Notebook: `src/chewy_churn/06_monitor.py`
- Creates or refreshes an `InferenceLog` Data Profile on the predictions table
- Baseline table: the training data used to fit the champion model
- Produces `chewy_churn_predictions_profile_metrics` and `chewy_churn_predictions_drift_metrics`
- Scheduled daily in prod (after inference job), paused in dev

## Notebook Details

### 00_setup_data.py

Generates synthetic Chewy customer data using the databricks-data-generation skill pattern. Writes to `{catalog}.{schema}.chewy_churn_customers`.

Target columns (synthetic):
- `customer_id` (string, primary key)
- `subscription_active` (boolean — Autoship subscription)
- `pet_type` (categorical — dog, cat, bird, fish, reptile)
- `days_since_last_order` (int)
- `total_orders_12m` (int — orders in last 12 months)
- `avg_order_value` (float)
- `total_spend_12m` (float)
- `customer_tenure_days` (int)
- `support_tickets_6m` (int)
- `website_visits_30d` (int)
- `churned` (boolean — target label)

Approximately 10,000 rows. Churn rate ~20% with realistic correlations (high support tickets + low recent orders = more likely to churn).

### 01_feature_engineering.py

Lightweight assembly:
- Reads `chewy_churn_customers`
- Selects/renames feature columns
- Writes to `{catalog}.{schema}.chewy_churn_features` as a Delta table, then sets primary key via `ALTER TABLE ADD CONSTRAINT pk PRIMARY KEY (customer_id)` (making it a UC feature table)
- Splits a held-out evaluation set to `{catalog}.{schema}.chewy_churn_eval` for Champion/Challenger comparison

### 02_train_model.py

- Parameterized via job parameters: `catalog`, `schema`, `model_name`, `experiment_name`
- Sets MLflow experiment and registry URI (`databricks-uc`)
- Reads feature table, splits train/test (80/20 stratified on `churned`)
- Writes test split to `{catalog}.{schema}.chewy_churn_test` for downstream validation
- `mlflow.sklearn.autolog(log_models=False)` for param/metric tracking
- Fits `RandomForestClassifier(n_estimators=100, random_state=42)`
- Explicit `mlflow.sklearn.log_model()` with `registered_model_name` to register to UC
- Sets task value: `dbutils.jobs.taskValues.set("train_model", "model_uri", model_uri)`
- Sets task value: `dbutils.jobs.taskValues.set("train_model", "model_version", model_version)`

### 03_validate_model.py

- Reads `model_uri` and `model_version` from task values
- Loads model from UC
- Reads test split from `{catalog}.{schema}.chewy_churn_test` (written by train task)
- Runs `mlflow.evaluate()` on test data with `model_type="classifier"`, `targets="churned"`
- Checks thresholds:
  - `f1_score >= 0.7`
  - `roc_auc >= 0.7`
- On pass: `client.set_registered_model_alias(name=full_model_name, alias="challenger", version=model_version)`
- On fail: `client.set_model_version_tag(name, version, "validation_status", "FAILED")` then `raise Exception`

### 04_deploy_model.py

- Loads challenger version (from `@challenger` alias)
- Checks if `@champion` alias exists:
  - **Yes:** loads both, evaluates on `chewy_churn_eval` table, compares F1 scores. If challenger >= champion, promote challenger to `champion`. Otherwise keep existing champion and delete `challenger` alias.
  - **No (first deployment):** promote challenger directly to `champion`.
- Creates or updates Model Serving endpoint:
  - Endpoint name: `{endpoint_name}`
  - Served model: `{catalog}.{schema}.{model_name}` at champion version
  - Workload size: `Small` (demo)
  - Scale to zero enabled
  - Inference table logging enabled
- Uses Databricks SDK `WorkspaceClient().serving_endpoints` API

### 05_batch_inference.py

- Loads model via `models:/{catalog}.{schema}.{model_name}@champion`
- Reads feature table (or new incoming data)
- Generates predictions + prediction probabilities
- Writes to `{catalog}.{schema}.chewy_churn_predictions` with columns: `customer_id`, `prediction`, `prediction_proba`, `model_version`, `timestamp`

### 06_monitor.py

- Uses `import databricks.lakehouse_monitoring as lm` (standalone package, available on ML Runtime)
- Creates (or gets existing) InferenceLog profile on `chewy_churn_predictions`:
  - `timestamp_col="timestamp"`
  - `model_id_col="model_version"`
  - `problem_type="classification"`
  - `prediction_col="prediction"`
  - `granularities=["1 day"]`
  - `output_schema_name="{catalog}.{schema}"`
- `label_col` omitted — ground truth labels are not available at inference time. Model quality metrics require a separate label join pipeline (out of scope for this demo).
- Sets baseline to training data table for drift detection
- Triggers `run_refresh()`

## Wheel Demo (chewy_churn_wheel/)

A minimal Python package to demonstrate DABs wheel task packaging:

- `chewy_churn_pkg/predict.py` contains a `score_batch(spark, model_uri, input_table)` function
- `pyproject.toml` defines the wheel build
- A small job resource (`chewy_churn_wheel_demo.job.yml`) shows a `python_wheel_task` configuration
- Not part of the main MLOps flow — a standalone showcase

## GitHub Actions

No changes to existing workflows. The three workflows already handle:
- `validate_dev.yml`: PR to main -> `databricks bundle validate --target dev`
- `deploy_dev.yml`: push to non-main branch -> validate -> deploy -> run
- `deploy_prod.yml`: push to main -> validate -> deploy -> run (with `--force-lock`)

New ML resources automatically deploy as part of the bundle. The `deploy_dev.yml` workflow continues to run `sample_job` (the ETL pipeline). The ML training workflow is run manually during the demo via `databricks bundle run chewy_churn_training --target dev` — this keeps the CI/CD pipeline fast and lets the presenter control timing during the walkthrough. The new ML variables (`model_name`, `experiment_name`, `endpoint_name`) all have defaults so no workflow changes are needed.

## Data Flow

```
[00_setup_data] -> chewy_churn_customers (raw synthetic data)
       |
[01_feature_engineering] -> chewy_churn_features (feature table, PK: customer_id)
       |                  -> chewy_churn_eval (held-out evaluation set)
       |
[02_train_model] -> MLflow experiment (metrics, params, model artifact)
       |          -> UC registered model (new version)
       |          -> chewy_churn_test (test split for validation)
       |
[03_validate_model] -> @challenger alias (if passes thresholds)
       |
[04_deploy_model] -> @champion alias (if beats existing champion)
       |            -> Model Serving endpoint (create/update)
       |
[05_batch_inference] -> chewy_churn_predictions (scored data)
       |
[06_monitor] -> chewy_churn_predictions_profile_metrics
              -> chewy_churn_predictions_drift_metrics
              -> Auto-generated dashboard
```

## Testing

### Unit Tests (tests/unit/test_features.py)

- Test feature engineering logic: correct columns, primary key present, no nulls in key columns
- Runs locally with pytest (no cluster needed)

### Integration Testing

- Via `deploy_dev.yml` GitHub Actions workflow: deploys bundle to dev, runs training job
- Manual validation during workshop: `databricks bundle run chewy_churn_training --target dev`

## Dependencies (additions to pyproject.toml)

```
mlflow>=2.13.0
scikit-learn>=1.4.0
```

These are needed for local testing only. On Databricks clusters, ML Runtime provides these pre-installed.

## Demo Walkthrough Order

1. Show `databricks.yml` — explain bundle structure, targets, variables
2. Run `00_setup_data.py` interactively — generate synthetic data, explore in UC
3. Run `01_feature_engineering.py` — show feature table in UC with primary key
4. Show `chewy_churn_training.job.yml` — explain the 3-task workflow
5. Run training workflow — watch Train -> Validate -> Deploy execute
6. Show MLflow experiment — metrics, artifacts, model lineage
7. Show UC model registry — aliases, versions, lineage to data
8. Show Model Serving endpoint — make a test API call
9. Run batch inference — show predictions table
10. Show Data Profiling — dashboard, drift metrics
11. Show GitHub Actions — push a change, watch CI/CD deploy
12. Show wheel packaging demo — explain the option for Python packages
