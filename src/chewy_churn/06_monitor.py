# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # Data Profiling Monitor
# MAGIC Create or retrieve a Lakehouse Monitor for the predictions table.

# COMMAND ----------

import databricks.lakehouse_monitoring as lm

# COMMAND ----------

dbutils.widgets.text('catalog', '', 'Catalog')
dbutils.widgets.text('schema', '', 'Schema')

catalog = dbutils.widgets.get('catalog')
schema = dbutils.widgets.get('schema')

# COMMAND ----------

table_name = f'{catalog}.{schema}.chewy_churn_predictions'
baseline_table = f'{catalog}.{schema}.chewy_churn_features'

print(f'Predictions table: {table_name}')
print(f'Baseline table:    {baseline_table}')

# COMMAND ----------

try:
  monitor = lm.get_monitor(table_name=table_name)
  print(f'Monitor already exists for {table_name}')
except Exception:
  monitor = lm.create_monitor(
    table_name=table_name,
    profile_type=lm.InferenceLog(
      timestamp_col='timestamp',
      granularities=['1 day'],
      model_id_col='model_version',
      problem_type='classification',
      prediction_col='prediction',
    ),
    output_schema_name=f'{catalog}.{schema}',
    baseline_table_name=baseline_table,
  )
  print(f'Created monitor for {table_name}')

# COMMAND ----------

lm.run_refresh(table_name=table_name)
print('Monitor refresh triggered')

# COMMAND ----------

print(f'Profile metrics table: {table_name}_profile_metrics')
print(f'Drift metrics table:   {table_name}_drift_metrics')
