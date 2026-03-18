---
name: deploy-cicd
description: "Trigger and monitor GitHub Actions CI/CD workflows for dev and/or prod Databricks Asset Bundle deployments. Use when the user says 'deploy', 'run cicd', 'trigger workflows', or 'test the pipeline'."
user_invocable: true
---

# Deploy CI/CD Workflows

Trigger and monitor the GitHub Actions CI/CD deployment workflows for this project.

## Arguments

The user may specify a target: `dev`, `prod`, or `all` (default: `all`).
Examples: `/deploy-cicd`, `/deploy-cicd dev`, `/deploy-cicd prod`, `/deploy-cicd all`

## Workflow Files

- **DEV**: `.github/workflows/deploy_dev.yml` — validate → deploy → run pipeline on dev workspace
- **PROD**: `.github/workflows/deploy_prod.yml` — validate → deploy → run pipeline on prod workspace
- **Validate only**: `.github/workflows/validate_dev.yml` — PR validation (validate + summary)

## Execution Steps

1. **Parse target** from user arguments (default to `all` if not specified)

2. **Trigger workflow(s)** using `gh workflow run`:
   - If `dev` or `all`: `gh workflow run deploy_dev.yml`
   - If `prod` or `all`: trigger prod AFTER dev passes (sequential)

3. **Monitor each run** by polling with `gh run view <run-id>`:
   - Check every 30 seconds
   - Report status of each job (validate, deploy, pipeline run)
   - Stop polling once the run reaches a terminal state (completed/failed)

4. **On failure**, automatically fetch logs:
   ```bash
   gh run view <run-id> --log-failed
   ```
   Then pull pipeline-level errors if the failure is in the "Run pipeline refresh job" step:
   ```bash
   databricks pipelines list-pipeline-events <pipeline-id> --profile <target> --output json | jq '[.[] | select(.level == "ERROR")] | .[0].error.exceptions[0].message'
   ```

5. **Report final status** with a summary table:
   ```
   | Workflow | Validate | Deploy | Pipeline Run | Status |
   |----------|:--------:|:------:|:------------:|:------:|
   | DEV      | Xs       | Xs     | Xs           | Pass/Fail |
   | PROD     | Xs       | Xs     | Xs           | Pass/Fail |
   ```

## Profile Mapping

- `dev` workflow → `--profile dev` for Databricks CLI
- `prod` workflow → `--profile prod` for Databricks CLI

## Notes

- Dev and prod run sequentially (prod only triggers after dev passes) unless the user explicitly requests only prod
- If a workflow is already running, inform the user and ask whether to wait or cancel
- The pipeline run step takes the longest (~30-60s) — a run lasting over 30s in the deploy job is normal
