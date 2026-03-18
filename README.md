# MLOps on Databricks Workshop

End-to-end MLOps demo using **Databricks Asset Bundles (DABs)**, **GitHub Actions CI/CD**, **MLflow**, **Unity Catalog**, **Model Serving**, and **Data Profiling**. Built around a customer churn prediction use case.

## What This Project Demonstrates

### MLOps Lifecycle (Deploy Code Pattern)

All ML pipelines — training, validation, deployment, inference, and monitoring — are version-controlled and promoted through environments as code. Models are trained in each environment using that environment's data, not promoted as artifacts between environments.

```
[Setup Data] -> [Feature Engineering] -> [Train Model] -> [Validate Model] -> [Deploy Model]
                                              |                                      |
                                              v                                      v
                                         MLflow Experiment                   Model Serving Endpoint
                                         UC Registered Model                 Champion/Challenger Aliases
                                              |
                                              v
                                      [Batch Inference] -> [Data Profiling Monitor]
                                              |                      |
                                              v                      v
                                      Predictions Table       Drift Metrics + Dashboard
```

### Key Concepts Showcased

- **Databricks Asset Bundles** — declarative YAML project structure with environment-specific targets, variable interpolation, and `uv build --wheel` artifact packaging
- **GitHub Actions CI/CD** — three-workflow pattern (validate on PR, deploy on push) with OAuth token federation (OIDC) — no long-lived secrets
- **MLflow Tracking + Unity Catalog Model Registry** — experiment tracking, model registration with three-level names, Champion/Challenger aliases
- **Multi-Task Databricks Workflows** — sequential job orchestration (train -> validate -> deploy) with task value passing between steps
- **Model Serving** — serverless REST endpoint with zero-downtime model updates
- **Data Profiling** — inference table monitoring for drift detection with auto-generated dashboards
- **Python Wheel Packaging** — demonstrates DABs `python_wheel_task` with `uv build --wheel` as an alternative deployment pattern

## Project Structure

```
.
├── databricks.yml                          # Bundle root: targets, variables, artifacts
├── resources/
│   ├── pet_churn_artifacts.yml           # MLflow experiment + UC registered model
│   ├── pet_churn_setup.job.yml           # Data generation + feature engineering job
│   ├── pet_churn_training.job.yml        # Train -> Validate -> Deploy workflow
│   ├── pet_churn_inference.job.yml       # Batch inference (daily, scheduled)
│   ├── pet_churn_monitoring.job.yml      # Data Profiling refresh (daily, scheduled)
│   ├── pet_churn_wheel_demo.job.yml      # Python wheel packaging demo
│   ├── devx_lakeflow_project_etl.pipeline.yml  # SDP ETL pipeline (data engineering demo)
│   └── sample_job.job.yml                      # ETL pipeline refresh job
├── src/
│   ├── pet_churn/                        # ML notebooks
│   │   ├── 00_setup_data.py                #   Synthetic customer data generation
│   │   ├── 01_feature_engineering.py       #   Feature table with UC primary key
│   │   ├── 02_train_model.py              #   RandomForest training + MLflow logging
│   │   ├── 03_validate_model.py           #   Threshold checks + challenger alias
│   │   ├── 04_deploy_model.py             #   Champion/Challenger + serving endpoint
│   │   ├── 05_batch_inference.py          #   Score with champion model
│   │   └── 06_monitor.py                  #   Data Profiling setup + refresh
│   ├── pet_churn_wheel/                  # Python wheel demo package
│   │   ├── pyproject.toml
│   │   └── pet_churn_pkg/
│   │       ├── __init__.py
│   │       └── predict.py                  #   CLI entry point for python_wheel_task
│   └── transformations/                    # SDP ETL source code
├── tests/
│   └── unit/
│       └── test_features.py                # Feature schema validation tests
├── .github/workflows/
│   ├── validate_dev.yml                    # PR gate: bundle validate + summary
│   ├── deploy_dev.yml                      # Feature branch: validate -> deploy -> run
│   └── deploy_prod.yml                     # Main merge: validate -> deploy -> run
├── docs/
│   └── superpowers/
│       ├── specs/                           # Design specification
│       └── plans/                           # Implementation plan
└── pyproject.toml                          # Python tooling (uv, ruff, pytest)
```

## Prerequisites

- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html) v0.279+ (for Direct Deployment Engine)
- [uv](https://docs.astral.sh/uv/) (for Python dependency management and wheel builds)
- Two Databricks workspaces (dev and prod) with Unity Catalog enabled
- A Databricks service principal with OIDC federation policies for GitHub Actions
- GitHub repository with environments (`dev` and `prod`) configured

## Getting Started

### 1. Install Tools

```bash
# Databricks CLI
brew tap databricks/tap && brew install databricks
databricks --version  # must be v0.279+

# uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify
uv --version
```

### 2. Configure Authentication

```bash
# Authenticate to workspaces
databricks auth login --host https://your-dev-workspace.azuredatabricks.net --profile dev
databricks auth login --host https://your-prod-workspace.azuredatabricks.net --profile prod

# Verify
databricks current-user me --profile dev
databricks current-user me --profile prod
```

### 3. Validate and Deploy to Dev

```bash
databricks bundle validate --target dev --profile dev
databricks bundle deploy --target dev --profile dev
```

### 4. Run the MLOps Pipeline

Run jobs in this order for the initial setup:

```bash
# Step 1: Generate synthetic data + build feature table
databricks bundle run pet_churn_setup --target dev --profile dev

# Step 2: Train model, validate, deploy (creates serving endpoint)
databricks bundle run pet_churn_training --target dev --profile dev

# Step 3: Run batch inference with the champion model
databricks bundle run pet_churn_inference --target dev --profile dev

# Step 4: Set up Data Profiling monitor on predictions table
databricks bundle run pet_churn_monitoring --target dev --profile dev
```

### 5. Verify Results

```bash
# Show all deployed resources with URLs
databricks bundle summary --target dev --profile dev
```

After running, explore in the Databricks UI:

- **MLflow Experiment** — metrics, parameters, model artifacts, lineage
- **Unity Catalog** — registered model with Champion/Challenger aliases
- **Model Serving** — live REST endpoint (make test API calls)
- **Data Profiling** — auto-generated dashboard with drift metrics

## CI/CD Flow

```
Push to feature branch  -> deploy_dev.yml    (validate -> deploy -> run in dev)
                                |
PR opened to main       -> validate_dev.yml  (validate + summary against dev)
                                |
PR merged (push to main)-> deploy_prod.yml   (validate -> deploy -> run in prod)
```

All workflows use **GitHub OIDC tokens** to authenticate to Databricks — no long-lived secrets or tokens.

### GitHub Actions Setup

**Repository Secret:**

| Secret                 | Description                      |
| ---------------------- | -------------------------------- |
| `DATABRICKS_CLIENT_ID` | Service principal Application ID |

**Environment Secrets** (set per environment: `dev` and `prod`):

| Secret            | Description                        |
| ----------------- | ---------------------------------- |
| `DATABRICKS_HOST` | Workspace URL for that environment |

**Environment Variables** (set per environment: `dev` and `prod`):

| Variable             | dev             | prod            |
| -------------------- | --------------- | --------------- |
| `DATABRICKS_CATALOG` | `bu1_dev`       | `bu1_prod`      |
| `DATABRICKS_SCHEMA`  | `devx_workshop` | `devx_workshop` |

### OIDC Federation Policies

The service principal needs federation policies for each GitHub trigger context:

```
repo:<owner>/<repo>:environment:dev
repo:<owner>/<repo>:environment:prod
repo:<owner>/<repo>:ref:refs/heads/*
repo:<owner>/<repo>:pull_request
```

## Bundle Configuration

### Variables

| Variable               | Description                   | Default                                       |
| ---------------------- | ----------------------------- | --------------------------------------------- |
| `catalog`              | Unity Catalog name            | `main`                                        |
| `schema`               | Schema for tables and models  | `default`                                     |
| `service_principal_id` | SP Application ID (prod only) | _(required)_                                  |
| `model_name`           | Registered model name in UC   | `pet_churn_model`                             |
| `experiment_name`      | MLflow experiment path        | `/Users/{user}/{target}-pet-churn-experiment` |
| `endpoint_name`        | Model Serving endpoint name   | `pet-churn-serving`                           |

Override via CLI: `databricks bundle deploy --var="catalog=my_catalog"`

Override via env: `export BUNDLE_VAR_catalog=my_catalog`

### Targets

| Target          | Mode        | Catalog    | Behavior                                        |
| --------------- | ----------- | ---------- | ----------------------------------------------- |
| `dev` (default) | development | `bu1_dev`  | Resource names prefixed, schedules paused       |
| `prod`          | production  | `bu1_prod` | Single deployment, schedules active, runs as SP |

### Artifacts

The wheel package is built automatically during `databricks bundle deploy` using `uv build --wheel`. No manual build step required.

## Jobs Reference

| Job                    | Tasks                                         | Description                                               |
| ---------------------- | --------------------------------------------- | --------------------------------------------------------- |
| `pet_churn_setup`      | setup_data -> feature_engineering             | One-time data generation + feature table creation         |
| `pet_churn_training`   | train_model -> validate_model -> deploy_model | Full training pipeline with Champion/Challenger promotion |
| `pet_churn_inference`  | batch_inference                               | Score feature table with champion model (daily)           |
| `pet_churn_monitoring` | refresh_monitor                               | Refresh Data Profiling metrics (daily)                    |
| `pet_churn_wheel_demo` | wheel_predict                                 | Demonstrates `python_wheel_task` packaging                |
| `sample_job`           | refresh_pipeline                              | SDP ETL pipeline refresh (data engineering demo)          |

## Task Dependencies and Execution Order

The MLOps pipeline is composed of four independent Databricks Workflows, each containing sequential tasks. The workflows themselves must be run in order for the initial setup, but after that, training, inference, and monitoring can run independently on their own schedules.

### Cross-Job Execution Order

```
 pet_churn_setup                pet_churn_training
 ┌─────────────────┐              ┌──────────────────────────────────────────────┐
 │                 │              │                                              │
 │  setup_data     │              │  train_model                                 │
 │       │         │              │       │                                      │
 │       ▼         │              │       │ passes model_uri, model_version      │
 │  feature_       │   creates    │       ▼                                      │
 │  engineering ───┼──────────►   │  validate_model                              │
 │                 │  feature     │       │                                      │
 └─────────────────┘  tables     │       │ assigns @challenger alias             │
                                  │       ▼                                      │
                                  │  deploy_model                                │
                                  │       │                                      │
                                  │       │ promotes @champion, creates endpoint  │
                                  └───────┼──────────────────────────────────────┘
                                          │
                          ┌───────────────┼───────────────┐
                          │               │               │
                          ▼               ▼               ▼
              ┌─────────────────┐  ┌────────────┐  ┌──────────────────┐
              │ pet_churn_    │  │ Model      │  │ pet_churn_     │
              │ inference       │  │ Serving    │  │ monitoring       │
              │                 │  │ Endpoint   │  │                  │
              │ batch_inference │  │ (REST API) │  │ refresh_monitor  │
              │      │          │  └────────────┘  │      │           │
              │      ▼          │                   │      ▼           │
              │ predictions     │                   │ profile_metrics  │
              │ table           │                   │ drift_metrics    │
              └─────────────────┘                   └──────────────────┘
```

### Intra-Job Task Dependencies

Each job's tasks run sequentially within the workflow. Dependencies are enforced by `depends_on` in the job YAML.

**pet_churn_setup** (run once):

```
setup_data ──► feature_engineering
```

- `setup_data` generates synthetic customer data into `pet_churn_customers`
- `feature_engineering` reads that table, encodes features, writes `pet_churn_features` + `pet_churn_eval`

**pet_churn_training** (run on demand or scheduled):

```
train_model ──► validate_model ──► deploy_model
     │                │                  │
     │                │                  ├─► updates @champion alias
     │                │                  └─► creates/updates serving endpoint
     │                └─► assigns @challenger alias (or fails pipeline)
     └─► writes pet_churn_test table
         passes model_uri + model_version via taskValues
```

**pet_churn_inference** (daily schedule):

```
batch_inference
     │
     └─► loads @champion model, scores features, appends to pet_churn_predictions
```

**pet_churn_monitoring** (daily schedule):

```
refresh_monitor
     │
     └─► creates/refreshes Data Profile on pet_churn_predictions
         produces _profile_metrics and _drift_metrics tables
```

### Data Dependencies Across Jobs

| Table                                   | Written By          | Read By                                             |
| --------------------------------------- | ------------------- | --------------------------------------------------- |
| `pet_churn_customers`                   | setup_data          | feature_engineering                                 |
| `pet_churn_features`                    | feature_engineering | train_model, batch_inference, monitoring (baseline) |
| `pet_churn_eval`                        | feature_engineering | deploy_model (Champion vs Challenger comparison)    |
| `pet_churn_test`                        | train_model         | validate_model                                      |
| `pet_churn_predictions`                 | batch_inference     | refresh_monitor                                     |
| `pet_churn_predictions_profile_metrics` | refresh_monitor     | Dashboards, SQL alerts                              |
| `pet_churn_predictions_drift_metrics`   | refresh_monitor     | Dashboards, SQL alerts                              |

### After Initial Setup

Once the setup and first training run complete, the steady-state operation is:

1. **Retraining** — `pet_churn_training` runs on demand (or triggered by monitoring alerts)
2. **Inference** — `pet_churn_inference` runs daily on a schedule
3. **Monitoring** — `pet_churn_monitoring` runs daily after inference

If monitoring detects drift, a data scientist can trigger retraining, which produces a new model version that goes through the validate -> deploy pipeline automatically.

## MLOps Pipeline Details

### Training Workflow (pet_churn_training)

**Task 1: train_model**

- Reads feature table from Unity Catalog
- Trains `RandomForestClassifier` with `class_weight='balanced'`
- `mlflow.sklearn.autolog(log_models=False)` for param/metric tracking
- Explicit `mlflow.sklearn.log_model()` for controlled registration to UC
- Passes `model_uri` and `model_version` to downstream tasks via `dbutils.jobs.taskValues`

**Task 2: validate_model**

- Loads model and test data, computes F1 and ROC AUC with sklearn
- Checks thresholds: F1 >= 0.2, ROC AUC >= 0.6
- On pass: assigns `@challenger` alias to the model version
- On fail: tags model as `FAILED`, raises exception (blocks deployment)

**Task 3: deploy_model**

- Compares `@challenger` vs `@champion` on held-out evaluation data
- Promotes winner to `@champion` alias
- Creates or updates Model Serving endpoint with the champion version

### Champion/Challenger Pattern

Model aliases in Unity Catalog are mutable named references to specific model versions:

- `@champion` — the model currently serving production traffic
- `@challenger` — a newly validated candidate being compared against the champion

Inference workloads always target `@champion`. When a new model wins the comparison, the alias pointer moves but inference code stays unchanged — zero-downtime model updates.

### Data Profiling (Monitoring)

Uses `databricks.lakehouse_monitoring` SDK to create an `InferenceLog` profile on the predictions table:

- Tracks prediction distribution drift over time
- Compares against the training data baseline
- Auto-generates a dashboard with drift metrics

## DABs Command Reference

```bash
# Validate configuration
databricks bundle validate --target dev --profile dev

# Deploy all resources
databricks bundle deploy --target dev --profile dev

# Run a specific job
databricks bundle run pet_churn_training --target dev --profile dev

# Show deployed resources and URLs
databricks bundle summary --target dev --profile dev

# Tear down all deployed resources
databricks bundle destroy --target dev --profile dev
```

## Tech Stack

- **Databricks Asset Bundles** — declarative infrastructure-as-code for Databricks
- **GitHub Actions** — CI/CD with OIDC workload identity federation
- **MLflow** — experiment tracking, model registry, model evaluation
- **Unity Catalog** — governance for data, models, and features
- **scikit-learn** — model training (RandomForestClassifier)
- **Model Serving** — serverless REST endpoint for real-time predictions
- **Data Profiling** — inference table monitoring and drift detection
- **uv** — Python package management and wheel builds
- **ruff** — Python linting and formatting

## Documentation

- [Design Spec](docs/superpowers/specs/2026-03-18-pet-churn-mlops-design.md) — architecture decisions and data flow
- [Implementation Plan](docs/superpowers/plans/2026-03-18-pet-churn-mlops.md) — step-by-step build plan
- [Databricks Asset Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/)
- [GitHub Actions for Databricks](https://docs.databricks.com/aws/en/dev-tools/ci-cd/github)
- [OAuth Token Federation](https://docs.databricks.com/aws/en/dev-tools/auth/oauth-federation)
- [The Big Book of MLOps (2nd Edition)](https://www.databricks.com/resources/ebook/the-big-book-of-mlops)

# new line
