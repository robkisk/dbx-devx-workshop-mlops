# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # Chewy Churn - Synthetic Data Generation
# MAGIC
# MAGIC Generates ~10,000 rows of synthetic customer data for churn prediction.
# MAGIC Target churn rate is ~20% with realistic behavioral correlations.

# COMMAND ----------

dbutils.widgets.text('catalog', '', 'Catalog')
dbutils.widgets.text('schema', '', 'Schema')

catalog = dbutils.widgets.get('catalog')
schema = dbutils.widgets.get('schema')

print(f'Using catalog: {catalog}, schema: {schema}')

# COMMAND ----------

import numpy as np
import uuid
from pyspark.sql.types import (
  StructType,
  StructField,
  StringType,
  BooleanType,
  IntegerType,
  FloatType,
)

# COMMAND ----------

np.random.seed(42)
n_customers = 10_000

# ---------- base features ----------
customer_ids = [str(uuid.uuid4()) for _ in range(n_customers)]

pet_types = np.random.choice(
  ['dog', 'cat', 'bird', 'fish', 'reptile'],
  size=n_customers,
  p=[0.45, 0.30, 0.10, 0.10, 0.05],
)

customer_tenure_days = np.random.exponential(scale=600, size=n_customers).astype(int)
customer_tenure_days = np.clip(customer_tenure_days, 30, 3650)

subscription_active = np.random.choice(
  [True, False], size=n_customers, p=[0.70, 0.30]
)

# ---------- behavioral features ----------
total_orders_12m = np.random.poisson(lam=8, size=n_customers)
total_orders_12m = np.clip(total_orders_12m, 0, 50)

avg_order_value = np.random.normal(loc=55.0, scale=20.0, size=n_customers).astype(
  np.float32
)
avg_order_value = np.clip(avg_order_value, 5.0, 200.0)

total_spend_12m = (total_orders_12m * avg_order_value).astype(np.float32)

days_since_last_order = np.random.exponential(scale=30, size=n_customers).astype(int)
days_since_last_order = np.clip(days_since_last_order, 0, 365)

support_tickets_6m = np.random.poisson(lam=1.5, size=n_customers)
support_tickets_6m = np.clip(support_tickets_6m, 0, 20)

website_visits_30d = np.random.poisson(lam=12, size=n_customers)
website_visits_30d = np.clip(website_visits_30d, 0, 100)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Compute churn probability via logistic function
# MAGIC
# MAGIC Signals that increase churn likelihood:
# MAGIC - More support tickets
# MAGIC - Fewer recent orders
# MAGIC - Inactive subscription
# MAGIC - Lower tenure
# MAGIC - More days since last order

# COMMAND ----------

def logistic(x):
  return 1.0 / (1.0 + np.exp(-x))

# build a linear score from behavioral features
# coefficients are intentionally strong so the model can learn clear patterns
z = (
  -0.5                                                  # intercept (targets ~35% churn for strong signal)
  + 0.8 * support_tickets_6m                            # more tickets → more churn
  - 0.4 * total_orders_12m                              # fewer orders → more churn
  - 2.0 * subscription_active.astype(float)             # inactive sub → more churn
  - 0.003 * customer_tenure_days                        # lower tenure → more churn
  + 0.03 * days_since_last_order                        # longer gap → more churn
  - 0.05 * website_visits_30d                           # fewer visits → more churn
)

churn_prob = logistic(z)
churned = np.random.binomial(1, churn_prob).astype(bool)

actual_churn_rate = churned.mean()
print(f'Generated churn rate: {actual_churn_rate:.2%} (target ~20%)')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Build Spark DataFrame and write to Unity Catalog

# COMMAND ----------

spark_schema = StructType([
  StructField('customer_id', StringType(), False),
  StructField('subscription_active', BooleanType(), False),
  StructField('pet_type', StringType(), False),
  StructField('days_since_last_order', IntegerType(), False),
  StructField('total_orders_12m', IntegerType(), False),
  StructField('avg_order_value', FloatType(), False),
  StructField('total_spend_12m', FloatType(), False),
  StructField('customer_tenure_days', IntegerType(), False),
  StructField('support_tickets_6m', IntegerType(), False),
  StructField('website_visits_30d', IntegerType(), False),
  StructField('churned', BooleanType(), False),
])

rows = [
  (
    customer_ids[i],
    bool(subscription_active[i]),
    str(pet_types[i]),
    int(days_since_last_order[i]),
    int(total_orders_12m[i]),
    float(avg_order_value[i]),
    float(total_spend_12m[i]),
    int(customer_tenure_days[i]),
    int(support_tickets_6m[i]),
    int(website_visits_30d[i]),
    bool(churned[i]),
  )
  for i in range(n_customers)
]

df = spark.createDataFrame(rows, schema=spark_schema)

# COMMAND ----------

table_name = f'{catalog}.{schema}.chewy_churn_customers'

(
  df.write
  .mode('overwrite')
  .saveAsTable(table_name)
)

print(f'Wrote {df.count()} rows to {table_name}')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Summary

# COMMAND ----------

row_count = spark.table(table_name).count()
churn_count = spark.table(table_name).filter('churned = true').count()
churn_rate = churn_count / row_count

print(f'Total rows:  {row_count:,}')
print(f'Churned:     {churn_count:,}')
print(f'Churn rate:  {churn_rate:.2%}')
