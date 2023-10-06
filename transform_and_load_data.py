import json
import os
import sys

from pyspark import SparkConf, SparkContext
from pyspark.sql import Row, SparkSession
from pyspark.sql.types import ArrayType, StringType, StructField, StructType

# Initialize Spark
conf = SparkConf().setAppName("AdverseEventETL")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

# Define input directories
input_dir = sys.argv[1]
hdfs_url = sys.argv[2]
cpu_count = int(os.cpu_count())
# Load JSON files as RDDs and merge them
data_rdds = []
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        file_path = os.path.join(input_dir, filename)
        data_rdd = sc.textFile(file_path,minPartitions=cpu_count).map(lambda x: json.loads(x))
        data_rdds.append(data_rdd)

merged_data_rdd = sc.union(data_rdds)

# Extract specific fields using RDD transformations
selected_fields_rdd = merged_data_rdd.flatMap(
    lambda record: [
        (
            result.get("safetyreportid"),  # Extract safetyreportid
            result.get("seriousnessdeath"),  # Extract seriousnessdeath
            result.get("sender", {}).get(
                "senderorganization"
            ),  # Extract senderorganization
            result.get("patient", {}).get("patientonsetage"),  # Extract patientonsetage
            result.get("patient", {}).get("patientsex"),  # Extract patientsex
            result.get("patient", {}).get("reaction"),  # Extract reaction
            result.get("patient", {})
            .get("patientdeath", {})
            .get("patientdeathdate"),  # Extract patientdeathdate
        )
        for result in record.get("results", [])
    ]
)

schema = StructType(
    [
        StructField("safetyreportid", StringType(), True),
        StructField("seriousnessdeath", StringType(), True),
        StructField("senderorganization", StringType(), True),
        StructField("patientonsetage", StringType(), True),
        StructField("patientsex", StringType(), True),
        StructField(
            "reaction",
            ArrayType(
                StructType([StructField("reactionmeddrapt", StringType(), True)])
            ),
            True,
        ),
        StructField("patientdeathdate", StringType(), True),
    ]
)
# Create an RDD of Row objects to represent the data

row_rdd = selected_fields_rdd.map(
    lambda x: Row(
        safetyreportid=x[0],
        seriousnessdeath=x[1],
        senderorganization=x[2],
        patientonsetage=x[3],
        patientsex=x[4],
        reaction=x[5],
        patientdeathdate=x[6],
    )
)

# # Create a DataFrame from the RDD of Row objects
data_df = spark.createDataFrame(row_rdd, schema=schema)

# # Create a temporary Spark table (view) from the DataFrame
data_df.createOrReplaceTempView("adverse_events")
# # display the Dataframe
print(data_df.show())

# # write the dataframe to a parquet in a HDFS system
data_df.write.mode("overwrite").parquet(hdfs_url)
# # Stop SparkContext
sc.stop()
