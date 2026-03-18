# Databricks notebook source

# COMMAND ----------

dbutils.widgets.text('catalog', '', 'Catalog')
dbutils.widgets.text('schema', '', 'Schema')

catalog = dbutils.widgets.get('catalog')
schema = dbutils.widgets.get('schema')

# COMMAND ----------

df = spark.table(f'{catalog}.{schema}.chewy_churn_customers')
display(df)

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.functions import col, when

pet_type_map = {
  'dog': 0,
  'cat': 1,
  'bird': 2,
  'fish': 3,
  'reptile': 4,
}

mapping_expr = F.create_map([F.lit(x) for item in pet_type_map.items() for x in item])

df_features = (
  df
  .withColumn('pet_type_encoded', mapping_expr[col('pet_type')])
  .withColumn('subscription_active', col('subscription_active').cast('int'))
  .withColumn('churned', col('churned').cast('int'))
  .select(
    'customer_id',
    'subscription_active',
    'pet_type_encoded',
    'days_since_last_order',
    'total_orders_12m',
    'avg_order_value',
    'total_spend_12m',
    'customer_tenure_days',
    'support_tickets_6m',
    'website_visits_30d',
    'churned',
  )
)

display(df_features)

# COMMAND ----------

df_features.write.mode('overwrite').saveAsTable(f'{catalog}.{schema}.chewy_churn_features')

spark.sql(
  f'ALTER TABLE {catalog}.{schema}.chewy_churn_features '
  f'ADD CONSTRAINT chewy_churn_pk PRIMARY KEY (customer_id)'
)

# COMMAND ----------

train_df, eval_df = df_features.randomSplit([0.8, 0.2], seed=42)

eval_df.write.mode('overwrite').saveAsTable(f'{catalog}.{schema}.chewy_churn_eval')

# COMMAND ----------

features_count = spark.table(f'{catalog}.{schema}.chewy_churn_features').count()
eval_count = spark.table(f'{catalog}.{schema}.chewy_churn_eval').count()

print(f'chewy_churn_features count: {features_count}')
print(f'chewy_churn_eval count: {eval_count}')
