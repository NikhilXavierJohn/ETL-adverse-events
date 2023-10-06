## Table of Contents
- [ Question 1 ](#question-1)
- [ Question 2](#question-2)
- [ Question 3](#question-3)
- [ Question 4](#question-4)



## Question 1

How would you efficiently extract the fields related to adverse events using PySpark from the datasets available at the provided link?

### Solution

To efficiently extract the fields related to adverse events using PySpark from the datasets available at the provided link,

1. **Get data from Api:** The code fetch_data uses Threading  i.e a ThreadPoolExecutor that run API calls in parallel, the API called is for the three drugs that were asked for. This then reads the data into a json format and stores it in separate json files in a local storage.

2. **Initialize Spark:** The transform_and_load_data.py code starts by initializing a SparkConf and SparkContext. This step is necessary to use PySpark for distributed data processing.

3. **Load JSON Files as RDDs:** It loads the JSON files from the input directory and creates an RDD for each file. This step reads the data into memory, and if one has a large dataset, one might consider using a more scalable approach, like reading from HDFS or a distributed file system.

4. **Merge Data RDDs:** The code merges all the RDDs into a single RDD using the `sc.union()` method. This is a reasonable approach as long as the combined data fits into memory.

5. **Extract Specific Fields using RDD Transformations:** The code then extracts specific fields using RDD transformations. This step is efficient as it leverages the distributed processing power of Spark.

6. **Define Schema and Create DataFrame:** The code defines a schema for the extracted data and creates a DataFrame from the RDD of Row objects. This step is necessary for performing SQL-like operations on the data.

7. **Create Temporary Spark Table (View):** It creates a temporary Spark table (view) from the DataFrame, allowing one to run SQL queries on the data using Spark SQL. This is an efficient way to perform complex data analysis tasks.

8. **Write Data to Parquet Format:** The code writes the processed data to Parquet format into a HDFS. Parquet is a columnar storage format that is efficient for both reading and writing data. Writing to a distributed file system (like HDFS) is a good choice for scalability.

9. **Stop SparkContext:** Finally, the SparkContext is stopped to release resources.


## Question 2

How would you design the data partitioning strategy for optimizing performance in Spark?

### Solution
In the provided code, there are a few considerations to design a data partitioning strategy for optimizing performance in Spark:

1. **Input Data Partitioning:** The input data is read from multiple JSON files located in the `input_dir`. To optimize performance, we have used a partitioning strategy that aligns with the number of available CPU cores or executor instances. 

   ```python
   cpu_count = int(os.cpu_count())
   data_rdds = []
   for filename in os.listdir(input_dir):
       if filename.endswith(".json"):
           file_path = os.path.join(input_dir, filename)
           data_rdd = sc.textFile(file_path, minPartitions=cpu_count).map(lambda x: json.loads(x))
           data_rdds.append(data_rdd)
   ```

2. **Output Data Partitioning:** When writing the processed data to Parquet, thenumber of partitions are automatically set by spark based on the size of the data and also the capability of the machine. 

   ```python
   data_df.write.mode("overwrite").parquet(hdfs_url)
   ```

## Question 3

How would you create a Spark table and store the extracted data in an open-source platform?

### Solution
To create a Spark table and store the extracted data in an open-source platform like HDFS, one can follow these steps based on the code submitted:

1. **Create a Spark DataFrame:** a DataFrame named `data_df`is created in the code. This DataFrame represents the extracted data from the adverse event JSON files.

2. **Create a Temporary Spark Table (View):** A temporary Spark table (view) is created from the DataFrame using the `createOrReplaceTempView` method. 

   ```python
   data_df.createOrReplaceTempView("adverse_events")
   ```

   Now, one can refer to this Spark table by the name "adverse_events" in their Spark SQL queries.

3. **Store Data in HDFS:** To store the data in HDFS, one can use the `write` method on their DataFrame to save it in Parquet format. One can specify the HDFS path where they want to save the data.

   ```python
   data_df.write.mode("overwrite").parquet(hdfs_url)
   ```

   Here, `hdfs://localhost:9820/output/data.parquet` or the path set in the makefile is the HDFS path where the Parquet data will be saved. Make sure that the specified path exists and is writable.

This code will write the data from the `data_df` DataFrame to HDFS in Parquet format, making it available for further processing or analysis on your Hadoop cluster.

## Question 4

How would you use Makefile to manage the ETL process and dependencies?

### Solution

The submitted Makefile is a set of rules that can be used to manage the ETL (Extract, Transform, Load) process and its dependencies. 

1. **Create a Virtual Environment:** To create a virtual environment, one can run the following command in their terminal:
   ```
   make create_venv
   ```

2. **Activate the Virtual Environment:** To activate the virtual environment, one can run the following command:
   ```
   make activate_venv
   ```

3. **Install Requirements:** To install the Python dependencies from the `requirements.txt` file into the virtual environment, one can use the following command:
   ```
   make install_requirements
   ```

4. **Fetch Data:** To fetch data from the OpenFDA API, one can run:
   ```
   make fetch_data
   ```

5. **Transform Data:** To transform the fetched data using PySpark RDDs, one can run:
   ```
   make transform_data
   ```
   This target depends on the `fetch_data` target

6. **Load Data:** To load the transformed data into a Spark table, one can run:
   ```
   make load_data
   ```
   This target depends on the `transform_data` target, ensure that the transformation is complete before loading the data.

7. **Read Data (Optional):** To read the data from HDFS, one can run:
   ```
   make read_data
   ```
   This target can be useful if one wants to read and process the data further. It depends on the `transform_data` target.

8. **Clean (Optional):** To clean up temporary files, one can run:
   ```
   make clean
   ```
   This target is optional and can be used to remove any temporary files generated during the ETL process.

9. **Alternatively:** To run ETL jobs one after the other automatically, one can run:
    ```
    make etl
    ```