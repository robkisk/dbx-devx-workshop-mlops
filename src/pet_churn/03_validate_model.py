# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # Model Validation
# MAGIC Evaluate the trained model against quality thresholds and promote or reject accordingly.

# COMMAND ----------

import mlflow
import mlflow.sklearn
from sklearn.metrics import f1_score as sklearn_f1, roc_auc_score

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

test_df = spark.table(f'{catalog}.{schema}.pet_churn_test').toPandas()

y_true = test_df['churned']
X_test = test_df.drop(columns=['customer_id', 'churned'])

print(f'Test set shape: {X_test.shape}')
print(f'Churn distribution:\n{y_true.value_counts()}')

# COMMAND ----------

# Load the model and generate predictions
model = mlflow.sklearn.load_model(model_uri)
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print(f'Prediction distribution:\n  0: {(y_pred == 0).sum()}\n  1: {(y_pred == 1).sum()}')

# COMMAND ----------

# Compute metrics with sklearn for full control
f1 = sklearn_f1(y_true, y_pred)
roc_auc = roc_auc_score(y_true, y_proba)

print(f'F1 Score (positive class): {f1:.4f}')
print(f'ROC AUC: {roc_auc:.4f}')

# Log metrics to the training run for tracking
with mlflow.start_run(run_id=mlflow.search_runs(filter_string=f"tags.mlflow.runName LIKE '%'", max_results=1).iloc[0].run_id) if False else mlflow.start_run():
  mlflow.log_metric('val_f1_score', f1)
  mlflow.log_metric('val_roc_auc', roc_auc)

# COMMAND ----------

f1_threshold = 0.2
roc_auc_threshold = 0.6

full_model_name = f'{catalog}.{schema}.{model_name}'
client = mlflow.tracking.MlflowClient()

if f1 >= f1_threshold and roc_auc >= roc_auc_threshold:
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
  print(f'PASSED: Model {full_model_name} v{model_version} (f1={f1:.3f}, roc_auc={roc_auc:.3f}). Alias set to challenger.')
else:
  client.set_model_version_tag(
    full_model_name,
    model_version,
    'validation_status',
    'FAILED',
  )
  raise Exception(f'Model validation failed: f1={f1:.3f}, roc_auc={roc_auc:.3f}')
