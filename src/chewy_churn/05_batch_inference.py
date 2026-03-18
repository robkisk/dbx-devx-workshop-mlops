# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # Batch Inference
# MAGIC Load the champion model from Unity Catalog and score the feature table.

# COMMAND ----------

import mlflow
import pandas as pd
from datetime import datetime, timezone

# COMMAND ----------

dbutils.widgets.text('catalog', '', 'Catalog')
dbutils.widgets.text('schema', '', 'Schema')
dbutils.widgets.text('model_name', '', 'Model Name')

catalog = dbutils.widgets.get('catalog')
schema = dbutils.widgets.get('schema')
model_name = dbutils.widgets.get('model_name')

# COMMAND ----------

mlflow.set_registry_uri('databricks-uc')

full_model_name = f'{catalog}.{schema}.{model_name}'
print(f'Loading champion model: {full_model_name}')

# COMMAND ----------

model = mlflow.sklearn.load_model(f'models:/{full_model_name}@champion')

client = mlflow.tracking.MlflowClient()
champion_ver = client.get_model_version_by_alias(full_model_name, 'champion')
print(f'Champion version: {champion_ver.version}')

# COMMAND ----------

features_df = spark.table(f'{catalog}.{schema}.chewy_churn_features').toPandas()

customer_ids = features_df['customer_id']
X = features_df.drop(columns=['customer_id', 'churned'])

# COMMAND ----------

predictions = model.predict(X)
probabilities = model.predict_proba(X)[:, 1]

# COMMAND ----------

result_df = pd.DataFrame({
  'customer_id': customer_ids,
  'prediction': predictions.astype(int),
  'prediction_proba': probabilities.astype(float),
  'model_version': str(champion_ver.version),
  'timestamp': datetime.now(timezone.utc),
})

# COMMAND ----------

result_spark_df = spark.createDataFrame(result_df)
result_spark_df.write.mode('append').saveAsTable(
  f'{catalog}.{schema}.chewy_churn_predictions'
)

# COMMAND ----------

count = result_spark_df.count()
print(f'Wrote {count} new predictions to {catalog}.{schema}.chewy_churn_predictions')
