INPUT_DIR = "\input"

# Define the target for the ETL process
setup: create_venv activate_venv install_requirements
etl: fetch_data transform_data load_data

create_venv:
	python -m venv venv

activate_venv:
	source .\venv\Scripts\activate

install_requirements:
	pip install -r requirements.txt
# Target to fetch data from the OpenFDA API
fetch_data:
	python fetch_data.py $(INPUT_DIR)

# Target to transform the fetched data using PySpark RDDs
transform_data:
	spark-submit transform_and_load_data.py $(INPUT_DIR)

# Target to load the transformed data into a Spark table
load_data:
	spark-submit load_data.py

# Define a target for cleaning up temporary files (optional)
clean:
	Remove-Item -Path $(INPUT_DIR)/*.json