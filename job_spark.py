from pyspark.sql.functions import mean, max, min, col, count
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("ExerciseSpark")
    .getOrCreate()
)

# Ler os dados do ENEM 2020

enem = (
    spark
    .read
    .format("csv")
    .option("header", True)
    .option("delimiter", ";")
    .option("encoding", "UTF-8")
    .load("s3://datalake-maxwell-igti-mba/raw-data/enem/")
)

(
    enem
    .write
    .mode("overwrite")
    .format("parquet")
    .partitionBy("year")
    .save("s3://datalake-maxwell-igti-mba/staging/enem")
)