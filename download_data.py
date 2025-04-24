import requests
import zipfile
import io

# URL of the ZIP file
url = "https://www.cdc.gov/brfss/annual_data/2023/files/LLCP2023XPT.zip"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Create a ZipFile object from the response content
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        # List the files in the ZIP archive
        zip_files = zip_ref.namelist()
        print("Files in the ZIP archive:", zip_files)

        # Example of how to read a specific file inside the zip without extracting it to disk
        with zip_ref.open(zip_files[0]) as file:
            # Assuming the file is a text-based file, you can read it directly.
            # For example, if it's a CSV, you can read it into a pandas DataFrame:
            import pandas as pd
            df = pd.read_sas(file,format='xport')
            print(df.head())
else:
    print(f"Failed to download the file. Status code: {response.status_code}")
