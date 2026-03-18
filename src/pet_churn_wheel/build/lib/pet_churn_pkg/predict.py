"""Batch prediction using a UC-registered model."""

import argparse

import mlflow
from pyspark.sql import SparkSession


def score_batch(spark, model_uri: str, input_table: str, output_table: str) -> None:
  """Load a model from UC and score a table, writing predictions."""
  mlflow.set_registry_uri('databricks-uc')
  model = mlflow.sklearn.load_model(model_uri)

  input_df = spark.table(input_table).toPandas()
  feature_cols = [c for c in input_df.columns if c not in ('customer_id', 'churned')]
  predictions = model.predict(input_df[feature_cols])

  input_df['prediction'] = predictions
  output_df = spark.createDataFrame(input_df[['customer_id', 'prediction']])
  output_df.write.mode('overwrite').saveAsTable(output_table)


def main():
  """CLI entry point for python_wheel_task."""
  parser = argparse.ArgumentParser()
  parser.add_argument('--model_uri', required=True)
  parser.add_argument('--input_table', required=True)
  parser.add_argument('--output_table', required=True)
  args = parser.parse_args()

  spark = SparkSession.builder.getOrCreate()
  score_batch(spark, args.model_uri, args.input_table, args.output_table)
