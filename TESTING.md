# Testing Guide

## Prerequisites

- Terraform apply completed (`/Users/robby.kiskanyan/dev/terraform/demos/dbx-tf-deploy-simple`)
- Databricks CLI authenticated (`databricks auth profiles`)
- GitHub CLI authenticated (`gh auth status`)

---

## 1. GitHub Actions — Manual Workflow Triggers

Test CI/CD pipelines without code changes using `workflow_dispatch`.

### Dev Deploy (validate → deploy → run pipeline)

```bash
gh workflow run deploy_dev.yml
gh run watch
```

### Prod Deploy (validate → deploy → run pipeline)

```bash
gh workflow run deploy_prod.yml
gh run watch
```

### Dev Validate Only (bundle validate + summary)

```bash
gh workflow run validate_dev.yml
gh run watch
```

### Check Recent Runs

```bash
gh run list --limit 5
```

### Inspect a Failed Run

```bash
gh run view <run-id> --log-failed
```

---

## 2. GitHub Actions — Feature Branch Flow

Test the full 3-stage CI/CD promotion workflow.

### Stage 1: Push to Feature Branch → Dev Deploy

```bash
# Create and switch to feature branch
git checkout -b feature/my-change

# Make a change in src/, resources/, or databricks.yml
# ...

# Commit and push
git add -A
git commit -m "My change description"
git push -u origin feature/my-change

# deploy_dev.yml triggers automatically
gh run watch
```

### Stage 2: Open PR → Validate

```bash
gh pr create --title "My change" --body "Description of changes"

# validate_dev.yml triggers automatically
gh run watch
```

### Stage 3: Merge PR → Prod Deploy

```bash
gh pr merge --merge

# deploy_prod.yml triggers automatically
gh run watch
```

### Cleanup

```bash
git checkout main
git pull
git branch -d feature/my-change
```

---

## 3. Local Developer Loop — Asset Bundles CLI

Test code changes against the dev workspace without triggering GitHub Actions.

### Validate Bundle Configuration

```bash
databricks bundle validate --target dev --profile dev
```

### Deploy to Dev Workspace

```bash
databricks bundle deploy --target dev --profile dev
```

### Run the Job (includes pipeline refresh)

```bash
databricks bundle run sample_job --target dev --profile dev
```

### All Three in Sequence

```bash
databricks bundle validate --target dev --profile dev && \
databricks bundle deploy --target dev --profile dev && \
databricks bundle run sample_job --target dev --profile dev
```

### Check Pipeline Status

```bash
databricks pipelines list-pipelines --profile dev --output json | jq '.[] | {name, state}'
```

### Destroy Dev Bundle (cleanup)

```bash
databricks bundle destroy --target dev --profile dev
```

---

## 4. Diagnostics

### Verify GitHub Secrets Are Set

```bash
gh secret list
gh secret list --env dev
gh secret list --env prod
gh variable list --env dev
gh variable list --env prod
```

### Verify Databricks Connectivity

```bash
databricks current-user me --profile dev
databricks current-user me --profile prod
```

### Check Pipeline Events (after failure)

```bash
# Get pipeline ID from the bundle
databricks bundle summary --target dev --profile dev

# List error events
databricks pipelines list-pipeline-events <pipeline-id> --profile dev --output json \
  | jq '[.[] | select(.level == "ERROR")] | .[0].error.exceptions[0].message'
```
