# CI/CD with Databricks Asset Bundles Workshop

Demonstrates **Databricks Asset Bundles (DABs)** with a complete CI/CD pipeline using GitHub Actions, **Workload Identity Federation (OIDC)**, and the **Direct Deployment Engine**.

## What This Project Deploys

- A **Spark Declarative Pipeline (SDP)** that reads NYC taxi trip data and aggregates fares by pickup zone
- A **scheduled job** that refreshes the pipeline daily
- All resources are parameterized across **dev** and **prod** workspaces using Unity Catalog

## Prerequisites

- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html) (v0.279+, for Direct Deployment Engine)
- Two Databricks workspaces (dev and prod) with Unity Catalog enabled
- A Databricks service principal with OIDC federation policies for GitHub Actions
- GitHub account with repository environments (`dev` and `prod`) configured

## Project Structure

```
.
├── databricks.yml                 # Bundle configuration (targets, variables, includes)
├── resources/
│   ├── devx_lakeflow_project_etl.pipeline.yml  # SDP pipeline definition
│   └── sample_job.job.yml                       # Scheduled job definition
├── src/
│   ├── transformations/           # Pipeline source code (SDP tables)
│   │   ├── sample_trips_devx_lakeflow_project.py
│   │   └── sample_zones_devx_lakeflow_project.py
│   └── explorations/              # Ad-hoc notebooks
├── .github/workflows/
│   ├── deploy_dev.yml             # Feature branch → dev workspace deployment
│   ├── validate_dev.yml           # PR validation against dev workspace
│   └── deploy_prod.yml            # Merge to main → prod workspace deployment
└── templates/                     # Custom bundle templates
```

## CI/CD Flow

```
Push to feature branch  → deploy_dev.yml    (validate → deploy → run pipeline in dev)
                              │
PR opened to main       → validate_dev.yml  (validate + summary against dev)
                              │
PR merged (push to main)→ deploy_prod.yml   (validate → deploy → run pipeline in prod)
```

## Configuration

### Bundle Variables

| Variable | Description | Dev Default | Prod Default |
|----------|-------------|-------------|--------------|
| `catalog` | Unity Catalog name | `bu1_dev` | `bu1_prod` |
| `schema` | Schema for tables | `devx_workshop` | `devx_workshop` |
| `service_principal_id` | SP Application ID (prod only) | `not-used-in-dev` | Set via CI |

**Override via CLI:**
```bash
databricks bundle deploy --var="catalog=my_catalog" --var="schema=my_schema"
```

**Override via environment:**
```bash
export BUNDLE_VAR_catalog=my_catalog
export BUNDLE_VAR_schema=my_schema
databricks bundle deploy
```

### Targets

| Target | Mode | Catalog | Description |
|--------|------|---------|-------------|
| `dev` (default) | development | `bu1_dev` | Resources prefixed with `[dev username]`, schedules paused |
| `prod` | production | `bu1_prod` | Single deployment, schedules active, runs as service principal |

## Getting Started

### 1. Install the Databricks CLI

```bash
# macOS
brew tap databricks/tap
brew install databricks

# Verify installation (must be v0.279+)
databricks --version
```

### 2. Configure Authentication

```bash
# Authenticate to your dev workspace
databricks auth login --host https://your-dev-workspace.azuredatabricks.net

# Authenticate to your prod workspace
databricks auth login --host https://your-prod-workspace.azuredatabricks.net
```

### 3. Enable the Direct Deployment Engine

```bash
# Add to your shell profile (.zshrc, .bashrc, etc.)
export DATABRICKS_BUNDLE_ENGINE=direct
```

### 4. Validate and Deploy

```bash
# Validate dev target (default)
databricks bundle validate

# Deploy to dev
databricks bundle deploy

# Run the pipeline
databricks bundle run sample_job
```

## Bundle Commands Reference

| Command | Description |
|---------|-------------|
| `databricks bundle validate` | Validate bundle configuration |
| `databricks bundle deploy` | Deploy resources to workspace |
| `databricks bundle run <resource>` | Run a job or pipeline |
| `databricks bundle destroy` | Remove deployed resources |
| `databricks bundle summary` | Show deployment summary |

### Common Flags

| Flag | Description |
|------|-------------|
| `--target <name>` | Target environment (dev, prod) |
| `-p, --profile <name>` | CLI profile to use |
| `--var="key=value"` | Override bundle variable |
| `--force-lock` | Force acquire deployment lock |

## CI/CD Setup

### Authentication: Workload Identity Federation (OIDC)

This project uses **GitHub OIDC tokens** to authenticate to Databricks, eliminating the need for long-lived secrets. The setup requires:

1. A Databricks **service principal** added to both workspaces
2. **Federation policies** on the SP matching each GitHub environment:
   ```
   repo:<org>/<repo>:environment:dev
   repo:<org>/<repo>:environment:prod
   ```
3. GitHub workflow permissions: `id-token: write` and `contents: read`

### GitHub Actions Workflows

| Workflow | Trigger | Target | Actions |
|----------|---------|--------|---------|
| `deploy_dev.yml` | Push to any branch except `main` | dev | Validate, deploy, run pipeline |
| `validate_dev.yml` | PR to `main` | dev | Validate, show summary |
| `deploy_prod.yml` | Push to `main` | prod | Validate, deploy, run pipeline |

### Required GitHub Secrets

**Repository Secrets:**
| Secret | Description |
|--------|-------------|
| `DATABRICKS_CLIENT_ID` | Service principal Application ID |

**Environment Secrets (dev and prod):**
| Secret | Environment | Description |
|--------|-------------|-------------|
| `DATABRICKS_HOST` | dev | Dev workspace URL |
| `DATABRICKS_HOST` | prod | Prod workspace URL |

> The same secret name `DATABRICKS_HOST` is used in both environments. GitHub resolves the correct value based on the job's `environment` setting.

### Required GitHub Variables

**Environment Variables (per environment):**
| Variable | Description | Example |
|----------|-------------|---------|
| `DATABRICKS_CATALOG` | Unity Catalog name | `bu1_dev` / `bu1_prod` |
| `DATABRICKS_SCHEMA` | Schema name | `devx_workshop` |

> These map to bundle variables via `BUNDLE_VAR_catalog` and `BUNDLE_VAR_schema` in the workflow.

## Resources

- [Databricks Asset Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/)
- [GitHub Actions for Databricks](https://docs.databricks.com/aws/en/dev-tools/ci-cd/github)
- [Workload Identity Federation](https://docs.databricks.com/aws/en/dev-tools/auth/oauth-federation)
- [Direct Deployment Engine](https://docs.databricks.com/aws/en/dev-tools/bundles/direct)
- [CI/CD Best Practices](https://docs.databricks.com/aws/en/dev-tools/ci-cd/best-practices)
- [Bundle Configuration Reference](https://docs.databricks.com/aws/en/dev-tools/bundles/settings)
