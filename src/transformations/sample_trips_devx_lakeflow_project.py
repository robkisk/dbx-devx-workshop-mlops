from pyspark import pipelines as dp
from pyspark.sql.functions import col

# This file defines a sample transformation.
# Test deployment: 2026-01-22 - Feature branch CICD validation
# Edit the sample below or add new transformations
# using "+ Add" in the file browser.


@dp.table
def sample_trips_devx_lakeflow_project():
  """my new function"""
  return spark.read.table('samples.nyctaxi.trips')
