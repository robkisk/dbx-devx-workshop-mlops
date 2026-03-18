# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # Model Deployment – Champion / Challenger
# MAGIC
# MAGIC This notebook compares a newly registered **challenger** model against the
# MAGIC current **champion** (if one exists) using F1 score on the held-out eval set.
# MAGIC The winner is promoted to the `champion` alias and served via a Model Serving
# MAGIC endpoint.

# COMMAND ----------

dbutils.widgets.text('catalog', '', 'Catalog')
dbutils.widgets.text('schema', '', 'Schema')
dbutils.widgets.text('model_name', '', 'Model Name')
dbutils.widgets.text('endpoint_name', '', 'Endpoint Name')

catalog = dbutils.widgets.get('catalog')
schema = dbutils.widgets.get('schema')
model_name = dbutils.widgets.get('model_name')
endpoint_name = dbutils.widgets.get('endpoint_name')

# COMMAND ----------

import mlflow
from sklearn.metrics import f1_score

mlflow.set_registry_uri('databricks-uc')
client = mlflow.tracking.MlflowClient()

full_model_name = f'{catalog}.{schema}.{model_name}'

# COMMAND ----------

# MAGIC %md
# MAGIC ## Retrieve challenger & champion versions

# COMMAND ----------

challenger_version = client.get_model_version_by_alias(full_model_name, 'challenger')
print(f'Challenger version: {challenger_version.version}')

try:
  champion_version = client.get_model_version_by_alias(full_model_name, 'champion')
  has_champion = True
  print(f'Champion version: {champion_version.version}')
except Exception:
  has_champion = False
  print('No existing champion – first deployment')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Compare models (if champion exists)

# COMMAND ----------

if has_champion:
  eval_df = spark.table(f'{catalog}.{schema}.chewy_churn_eval').toPandas()

  feature_cols = [c for c in eval_df.columns if c not in ('customer_id', 'churned')]
  X_eval = eval_df[feature_cols]
  y_eval = eval_df['churned']

  champion_model = mlflow.sklearn.load_model(f'models:/{full_model_name}/{champion_version.version}')
  challenger_model = mlflow.sklearn.load_model(f'models:/{full_model_name}/{challenger_version.version}')

  champion_f1 = f1_score(y_eval, champion_model.predict(X_eval))
  challenger_f1 = f1_score(y_eval, challenger_model.predict(X_eval))

  print(f'Champion  F1: {champion_f1:.4f}')
  print(f'Challenger F1: {challenger_f1:.4f}')

  if challenger_f1 >= champion_f1:
    print('Challenger wins – promoting to champion')
    client.set_registered_model_alias(
      name=full_model_name,
      alias='champion',
      version=challenger_version.version,
    )
  else:
    print('Champion still better – keeping current champion')
    client.delete_registered_model_alias(
      name=full_model_name,
      alias='challenger',
    )
else:
  print('Promoting challenger to champion (first deployment)')
  client.set_registered_model_alias(
    name=full_model_name,
    alias='champion',
    version=challenger_version.version,
  )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create or update Model Serving endpoint

# COMMAND ----------

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import (
  EndpointCoreConfigInput,
  ServedEntityInput,
  AutoCaptureConfigInput,
)

w = WorkspaceClient()
champion_ver = client.get_model_version_by_alias(full_model_name, 'champion')

served_entity = ServedEntityInput(
  entity_name=full_model_name,
  entity_version=champion_ver.version,
  workload_size='Small',
  scale_to_zero_enabled=True,
)
auto_capture = AutoCaptureConfigInput(
  catalog_name=catalog,
  schema_name=schema,
  enabled=True,
)

try:
  w.serving_endpoints.get(endpoint_name)
  w.serving_endpoints.update_config(
    name=endpoint_name,
    served_entities=[served_entity],
    auto_capture_config=auto_capture,
  )
  print(f'Updated endpoint {endpoint_name}')
except Exception:
  w.serving_endpoints.create(
    name=endpoint_name,
    config=EndpointCoreConfigInput(
      served_entities=[served_entity],
      auto_capture_config=auto_capture,
    ),
  )
  print(f'Created endpoint {endpoint_name}')
