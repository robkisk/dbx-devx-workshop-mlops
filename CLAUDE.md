# MLOps Workshop — Chewy

Databricks MLOps workshop showcasing the **deploy code** pattern with Databricks Asset Bundles, GitHub Actions CI/CD, MLflow, and Unity Catalog. Two-environment setup (dev + prod) for demo simplicity.

## Workshop Scope

### What We're Showcasing

1. **Deploy Code Pattern** — all ML pipelines (training, validation, deployment, inference) are version-controlled and promoted through environments. Models are trained in production using production data, not promoted as artifacts from dev.

2. **Databricks Asset Bundles (DABs)** — YAML-defined project structure with environment-specific target overrides. Bundle variables for catalog, schema, and service principal. `mode: development` for dev, `mode: production` for prod.

3. **GitHub Actions CI/CD** — three-workflow pattern:
   - `validate_dev.yml`: PR to main → bundle validate + summary (gate)
   - `deploy_dev.yml`: push to feature branch → validate → deploy → run
   - `deploy_prod.yml`: merge to main → validate → deploy → run
   - OAuth token federation (`github-oidc`) for authentication
   - GitHub environments (`dev`, `prod`) with separate secrets/variables

4. **MLflow Experiment Tracking & Model Registry in Unity Catalog** — log params, metrics, and model artifacts during training. Register models to Unity Catalog with three-level names (`catalog.schema.model_name`). Use model aliases (`champion`, `challenger`) for deployment management.

5. **Multi-Task Databricks Workflow** — production orchestration:
   - **Task 1: Model Training** — train on prod data, log to MLflow, register model to `prod` catalog
   - **Task 2: Model Validation** — load model from UC, run validation checks (format, metadata, performance thresholds), assign `challenger` alias if passed
   - **Task 3: Model Deployment** — compare challenger vs champion on held-out data, promote winner to `champion` alias, optionally update Model Serving endpoint

6. **Feature Engineering in Unity Catalog** — Delta tables with primary keys as feature tables. Parallel feature computation tasks. Lineage tracked from features to models.

7. **Model Serving** — serverless REST endpoints from UC-registered models. Inference tables for monitoring. Zero-downtime updates when champion model changes.

8. **Data Profiling** (formerly "Lakehouse Monitoring") — attach profiles to inference tables to track data drift and model quality over time. Three profile types: TimeSeries, InferenceLog, Snapshot. Auto-generated dashboards and alerting on metric thresholds. Custom metrics via Jinja-templated SQL expressions.

### What We're NOT Covering

- LLMOps, RAG, vector databases, fine-tuning, or generative AI patterns
- Three-environment setup (staging is collapsed into dev for demo purposes)
- Pre-training or custom LLM deployment

### Environment Architecture

Two environments, each mapping to a Unity Catalog catalog:

| Environment | Catalog    | Mode          | Auth Identity      | Schedule  |
| ----------- | ---------- | ------------- | ------------------ | --------- |
| **Dev**     | `bu1_dev`  | `development` | User (interactive) | Paused    |
| **Prod**    | `bu1_prod` | `production`  | Service Principal  | Scheduled |

### Key MLOps Concepts to Demonstrate

- **Data-centric AI**: ML pipelines are data pipelines — feature engineering, training, inference, and monitoring all operate on Delta tables governed by Unity Catalog
- **Unified governance**: Models, features, inference tables, and profile metric tables all live under the same UC namespace with consistent permissions
- **Champion/Challenger aliases**: Mutable named references to model versions — inference workloads target `@champion`, validation assigns `@challenger` to new candidates
- **Reproducibility**: MLflow tracks params, metrics, artifacts, and git info for every run. Model lineage traces back to training data and code.
- **Automated retraining**: Scheduled or triggered by Data Profiling alerts when drift/degradation is detected

## Official Documentation & Examples

### Databricks Asset Bundles

- **DABs overview**: https://docs.databricks.com/aws/en/dev-tools/bundles/
- **DABs configuration settings**: https://docs.databricks.com/aws/en/dev-tools/bundles/settings
- **Bundle configuration examples**: https://docs.databricks.com/aws/en/dev-tools/bundles/examples
- **Bundle lifecycle**: https://docs.databricks.com/aws/en/dev-tools/bundles/work-tasks#lifecycle
- **Direct Deployment Engine**: https://docs.databricks.com/aws/en/dev-tools/bundles/direct
- **Authentication for DABs**: https://docs.databricks.com/aws/en/dev-tools/bundles/authentication
- **Custom bundle templates**: https://docs.databricks.com/aws/en/dev-tools/bundles/template-tutorial
- **Example bundles repo**: https://github.com/databricks/bundle-examples/tree/main

### CI/CD & GitHub Actions

- **GitHub Actions for Databricks**: https://docs.databricks.com/aws/en/dev-tools/ci-cd/github
- **OAuth token federation**: https://docs.databricks.com/aws/en/dev-tools/auth/oauth-federation
- **CI/CD best practices**: https://docs.databricks.com/aws/en/dev-tools/ci-cd/best-practices

### Data Profiling (formerly Lakehouse Monitoring)

- **Data Profiling overview**: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/
- **Python SDK API reference**: https://api-docs.databricks.com/python/lakehouse-monitoring/latest/databricks.lakehouse_monitoring.html
- **Custom metrics**: https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-quality-monitoring/data-profiling/custom-metrics

### Databricks CLI & SDK

- **Databricks CLI**: https://docs.databricks.com/aws/en/dev-tools/cli
- **Bundle commands**: https://docs.databricks.com/aws/en/dev-tools/cli/bundle-commands#init
- **Python SDK docs**: https://databricks-sdk-py.readthedocs.io/en/latest/index.html

## GitHub Repo for Deployment

- Repo: [dbx-devx-workshop](https://github.com/robkisk/dbx-devx-workshop)

## Reference Implementation Patterns

Patterns derived from the `mlops-demos` reference codebases (`mlops-stacks-demo`, `ml-ops-dabs-demo`, `databricks-mlops-stack-demo`).

### Bundle Structure

```
project/
├── databricks.yml              # Bundle root: name, includes, variables, targets
├── resources/
│   ├── ml_training.job.yml     # Training workflow (train → validate → deploy)
│   ├── ml_inference.job.yml    # Batch inference job
│   ├── ml_monitoring.job.yml   # Data Profiling pipeline
│   └── ml_artifacts.yml        # MLflow experiment + registered model in UC
├── src/
│   ├── training/               # Model training notebooks/scripts
│   ├── validation/             # Model validation logic + custom metrics
│   ├── deployment/             # Champion/Challenger promotion logic
│   ├── feature_engineering/    # Feature table computation
│   ├── inference/              # Batch/streaming inference pipelines
│   └── monitoring/             # Data Profiling setup + drift detection
├── tests/
│   ├── unit/                   # Local pytest (PySpark session)
│   └── integration/            # Full bundle deploy + job run tests
└── .github/workflows/
    ├── validate_dev.yml        # PR gate: bundle validate
    ├── deploy_dev.yml          # Feature branch: validate → deploy → run
    └── deploy_prod.yml         # Main merge: validate → deploy → run
```

### DAB Variables Pattern

```yaml
variables:
  catalog:
    description: Unity Catalog name
  schema:
    description: Schema for tables and models
  model_name:
    description: Registered model name in UC
  experiment_name:
    description: MLflow experiment path
  service_principal_id:
    description: SP app ID for prod run_as
```

### Training Workflow Pattern (3-Task Sequential)

```yaml
resources:
  jobs:
    ml_training_job:
      tasks:
        - task_key: train_model
          # Logs to MLflow, registers model to catalog.schema.model_name
        - task_key: validate_model
          depends_on:
            - task_key: train_model
          # Loads model from UC, runs checks, assigns "challenger" alias
        - task_key: deploy_model
          depends_on:
            - task_key: validate_model
          # Compares challenger vs champion, promotes winner
```

### Model Validation Pattern

- **Run modes**: `disabled` | `dry_run` | `enabled`
- **Baseline comparison**: Load current `@champion` model as baseline
- **MLflow evaluate**: Custom metrics + thresholds (absolute and relative)
- **On pass**: Assign `challenger` alias to new model version
- **On fail**: Exit, notify, tag model version with failure reason

### Champion/Challenger Promotion

```python
import mlflow
mlflow.set_registry_uri('databricks-uc')
client = mlflow.tracking.MlflowClient()

# After validation passes
client.set_registered_model_alias(
    name="catalog.schema.model_name",
    alias="challenger",
    version=new_version
)

# After deployment comparison passes
client.set_registered_model_alias(
    name="catalog.schema.model_name",
    alias="champion",
    version=winning_version
)
```

### GitHub Actions Auth Pattern

```yaml
env:
  DATABRICKS_BUNDLE_ENGINE: direct
  DATABRICKS_AUTH_TYPE: github-oidc
  DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
  DATABRICKS_CLIENT_ID: ${{ secrets.DATABRICKS_CLIENT_ID }}
  BUNDLE_VAR_catalog: ${{ vars.DATABRICKS_CATALOG }}
  BUNDLE_VAR_schema: ${{ vars.DATABRICKS_SCHEMA }}
```

### Data Profiling Pattern (Inference Monitoring)

The `databricks.lakehouse_monitoring` Python SDK attaches profiles to UC tables. For MLOps, the **InferenceLog** profile type monitors model serving and batch inference outputs.

```python
from databricks import lakehouse_monitoring as lm

# Create an inference profile on a predictions table
profile = lm.create_monitor(
    table_name="prod.fraud_detection.fraud_clf_inference",
    profile_type=lm.InferenceLog(
        timestamp_col="timestamp",
        granularities=["1 day"],
        model_id_col="model_version",
        problem_type="classification",  # or "regression"
        prediction_col="prediction",
        label_col="label",              # optional — enables model quality metrics
    ),
    output_schema_name="prod.fraud_detection",  # where metric tables are written
    baseline_table_name="prod.fraud_detection.training_data",  # drift reference
    slicing_exprs=["region", "customer_tier"],  # monitor subpopulations
    schedule=lm.MonitorCronSchedule(
        quartz_cron_expression="0 0 8 * * ?",  # daily at 8am
        timezone_id="UTC",
    ),
)

# Trigger an on-demand refresh
lm.run_refresh(table_name="prod.fraud_detection.fraud_clf_inference")
```

**Profile types:**

| Type           | Use Case                             | Key Fields                                                                     |
| -------------- | ------------------------------------ | ------------------------------------------------------------------------------ |
| `InferenceLog` | Model predictions (batch or serving) | `timestamp_col`, `model_id_col`, `problem_type`, `prediction_col`, `label_col` |
| `TimeSeries`   | Feature tables, time-stamped data    | `timestamp_col`, `granularities`                                               |
| `Snapshot`     | Static tables (max 4TB)              | None required                                                                  |

**Metric tables auto-created:**

- `{table_name}_profile_metrics` — summary statistics per column per time window
- `{table_name}_drift_metrics` — drift vs baseline and vs previous windows

**Custom metrics** use Jinja-templated SQL:

```python
from databricks.lakehouse_monitoring import Metric

weighted_error = Metric(
    type="aggregate",
    name="weighted_error",
    input_columns=[":table"],
    definition="""avg(CASE
        WHEN {{prediction_col}} = {{label_col}} THEN 0
        WHEN {{prediction_col}} != {{label_col}} AND critical = TRUE THEN 2
        ELSE 1 END)""",
    output_data_type='{"type":"double"}',
)
```

## DABs-First Workflow

**IMPORTANT: Databricks Asset Bundles commands are the primary interface for all deployment and execution.** Do not drop into lower-level CLI commands (`databricks jobs submit`, `databricks jobs run-now`, etc.) when a `databricks bundle` command can do the job. The bundle layer provides variable interpolation, target awareness, and resource naming that raw API calls bypass.

### Core DABs Commands

```bash
# Validate bundle configuration and resource definitions
databricks bundle validate --target dev --profile dev

# Deploy all resources (jobs, pipelines, artifacts, models) to workspace
databricks bundle deploy --target dev --profile dev

# Run a specific job by its resource key (not job ID)
databricks bundle run chewy_churn_setup --target dev --profile dev
databricks bundle run chewy_churn_training --target dev --profile dev
databricks bundle run chewy_churn_inference --target dev --profile dev

# Show deployed resource summary (names, URLs, IDs)
databricks bundle summary --target dev --profile dev

# Tear down all deployed resources
databricks bundle destroy --target dev --profile dev
```

### DABs Best Practices

- Always validate bundles before deployment: `databricks bundle validate`
- Use `mode: development` for dev (auto-prefixes resources, pauses schedules)
- Use `mode: production` with `run_as` service principal for prod
- Keep sensitive values in GitHub environment secrets, not in `databricks.yml`
- Use `BUNDLE_VAR_*` env vars for CI/CD variable injection
- Use `concurrency: 1` on prod deploy workflows to prevent race conditions
- Use `--force-lock` on prod deploys to handle stale locks
- Use `uv build --wheel` in the `artifacts` section for wheel builds
- Every runnable notebook should be part of a job resource — avoid ad-hoc `jobs submit`
