from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder.appName("ParquetReader").getOrCreate()

# Read data from a Parquet file into a DataFrame
parquet_file_path = "hdfs://localhost:9820/output/data.parquet"
df = spark.read.parquet(parquet_file_path)
print(df.show())
# Stop SparkSession when done
spark.stop()
