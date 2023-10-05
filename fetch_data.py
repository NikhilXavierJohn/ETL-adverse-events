import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import requests

# Define the OpenFDA API query URLs for different drug categories
categories = [
    "nonsteroidal+anti-inflammatory+drug",
    "Thiazide+Diuretic",
    "Tumor+Necrosis+Factor+Blocker",
]
base_url = "https://api.fda.gov/drug/event.json?"

# Create a directory to store fetched data
output_dir = sys.argv[1]
os.makedirs(output_dir, exist_ok=True)


def create_data_json(category):
    url = f"{base_url}search=patient.drug.openfda.pharm_class_epc:{category}&limit=100"
    print(f"Getting data for {category.replace('+','_')}")
    # Send a GET request to the OpenFDA API
    response = requests.get(url)

    if response.status_code == 200:
        # If the request is successful, parse the JSON response
        data = response.json()

        # Define the output file path based on the category
        output_file = os.path.join(output_dir, f"{category.replace('+','_')}.json")
        # Write the fetched data to a JSON file
        with open(output_file, "w") as f:
            json.dump(data, f)
        return f"Stored {category.replace('+','_')}.json"
    else:
        # Print an error message if the request fails
        print(
            f"Failed to fetch data for {category.replace('+','_')}. Status code: {response.status_code}"
        )
        return None


with ThreadPoolExecutor() as executor:
    futures = [executor.submit(create_data_json, category) for category in categories]
results = [future.result() for future in futures if future is not None]
print(results)
