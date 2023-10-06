import sys

from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder.appName("ParquetReader").getOrCreate()
hdfs_url = sys.argv[1]
# Read data from a Parquet file into a DataFrame
parquet_file_path = hdfs_url
df = spark.read.parquet(parquet_file_path)
print(df.show())
# Stop SparkSession when done
spark.stop()
