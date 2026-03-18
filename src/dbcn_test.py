# new line
# from databricks.connect import DatabricksSession

# Here is a demo of spark session with databricks connect.
# Need to add some unit tests here
spark = DatabricksSession.builder.profile('dev').serverless().getOrCreate()

# let's separate these into there own functions
print('now running in whatever it chooses as default')
print(spark.conf.get('spark.databricks.workspaceUrl'))
print(spark.conf.get('spark.databricks.clusterUsageTags.clusterId'))
spark.table('samples.nyctaxi.trips').show(10, False)
display(spark.sql('select * from samples.nyctaxi.trips limit 10'))

# Lets add some plotly in the future
