# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # Model Validation
# MAGIC Evaluate the trained model against quality thresholds and promote or reject accordingly.

# COMMAND ----------

import mlflow
import mlflow.tracking

# COMMAND ----------

dbutils.widgets.text('catalog', '', 'Catalog')
dbutils.widgets.text('schema', '', 'Schema')
dbutils.widgets.text('model_name', '', 'Model Name')

catalog = dbutils.widgets.get('catalog')
schema = dbutils.widgets.get('schema')
model_name = dbutils.widgets.get('model_name')

# COMMAND ----------

model_uri = dbutils.jobs.taskValues.get(taskKey='train_model', key='model_uri')
model_version = dbutils.jobs.taskValues.get(taskKey='train_model', key='model_version')

print(f'Model URI: {model_uri}')
print(f'Model Version: {model_version}')

# COMMAND ----------

mlflow.set_registry_uri('databricks-uc')

# COMMAND ----------

test_df = spark.table(f'{catalog}.{schema}.chewy_churn_test').toPandas()
eval_df = test_df.drop(columns=['customer_id'])

print(f'Eval DataFrame shape: {eval_df.shape}')

# COMMAND ----------

result = mlflow.evaluate(
  model=model_uri,
  data=eval_df,
  model_type='classifier',
  targets='churned',
)

# COMMAND ----------

f1_score = result.metrics['f1_score']
roc_auc = result.metrics['roc_auc']

print(f'F1 Score: {f1_score:.4f}')
print(f'ROC AUC: {roc_auc:.4f}')

# COMMAND ----------

f1_threshold = 0.7
roc_auc_threshold = 0.7

full_model_name = f'{catalog}.{schema}.{model_name}'
client = mlflow.tracking.MlflowClient()

if f1_score >= f1_threshold and roc_auc >= roc_auc_threshold:
  client.set_registered_model_alias(
    name=full_model_name,
    alias='challenger',
    version=int(model_version),
  )
  client.set_model_version_tag(
    full_model_name,
    model_version,
    'validation_status',
    'PASSED',
  )
  print(f'Model {full_model_name} version {model_version} PASSED validation (f1={f1_score:.3f}, roc_auc={roc_auc:.3f}). Alias set to challenger.')
else:
  client.set_model_version_tag(
    full_model_name,
    model_version,
    'validation_status',
    'FAILED',
  )
  raise Exception(f'Model validation failed: f1={f1_score:.3f}, roc_auc={roc_auc:.3f}')
