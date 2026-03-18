# Databricks notebook source

# COMMAND ----------

import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# COMMAND ----------

dbutils.widgets.text('catalog', '')
dbutils.widgets.text('schema', '')
dbutils.widgets.text('model_name', '')
dbutils.widgets.text('experiment_name', '')

catalog = dbutils.widgets.get('catalog')
schema = dbutils.widgets.get('schema')
model_name = dbutils.widgets.get('model_name')
experiment_name = dbutils.widgets.get('experiment_name')

# COMMAND ----------

mlflow.set_registry_uri('databricks-uc')
mlflow.set_experiment(experiment_name)

# COMMAND ----------

df = spark.read.table(f'{catalog}.{schema}.chewy_churn_features').toPandas()

# COMMAND ----------

X = df.drop(columns=['customer_id', 'churned'])
y = df['churned']

# COMMAND ----------

X_train, X_test, y_train, y_test = train_test_split(
  X, y, test_size=0.2, stratify=y, random_state=42
)

# COMMAND ----------

test_df = df.loc[X_test.index]
spark.createDataFrame(test_df).write.mode('overwrite').saveAsTable(
  f'{catalog}.{schema}.chewy_churn_test'
)

# COMMAND ----------

with mlflow.start_run() as run:
  mlflow.sklearn.autolog(log_models=False)

  model = RandomForestClassifier(n_estimators=100, random_state=42)
  model.fit(X_train, y_train)

  signature = mlflow.models.infer_signature(X_train, y_train)

  result = mlflow.sklearn.log_model(
    model,
    artifact_path='model',
    registered_model_name=f'{catalog}.{schema}.{model_name}',
    input_example=X_train[:1],
    signature=signature,
  )

  model_version = result.registered_model_version
  model_uri = f'models:/{catalog}.{schema}.{model_name}/{model_version}'

  dbutils.jobs.taskValues.set(key='model_uri', value=model_uri)
  dbutils.jobs.taskValues.set(key='model_version', value=str(model_version))

# COMMAND ----------

print(f'model_uri: {model_uri}')
print(f'model_version: {model_version}')
