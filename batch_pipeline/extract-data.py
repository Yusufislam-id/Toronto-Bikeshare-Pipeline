import requests
import zipfile
import os

data_year = "2022"

base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
package_id = "bike-share-toronto-ridership-data"
data_folder = "./data"
zip_file_path = f"./data/bikeshare-ridership-{data_year}.zip"

# Get package information(json). Fetch package metadata from CKAN API.
def fetch_package_data(package_id):
    url = f"{base_url}/api/3/action/package_show"
    response = requests.get(url, params={"id": package_id})
    # ^ request.get({base_url}/api/3/action/package_show?id=bike-share-toronto-ridership-data)
    if response.status_code == 200:
        print("Success Fetch Data")
        return response.json()
    else:
        print("Failed Fetch Data. Status code:", response.status_code)
        return None

# Download data by year from package_data
def download_resource(data_year):
    package = fetch_package_data(package_id)

    # Ensure package is not None before proceeding
    if package is None or "result" not in package or "resources" not in package["result"]:
        print("Error: Unable to fetch package data.")
        return  # Safely break execution

    # Check zip data exist
    if os.path.exists(f"data/bikeshare-ridership-{data_year}.zip"):
        print(f'bikeshare-ridership-{data_year}.zip exist')
        return
    
    # Check zip data exist
    if os.path.exists(f"data/bikeshare-ridership-{data_year}"):
        print(f'bikeshare-ridership-{data_year} exist')
        return
    
    # Iterate through resources and download matching files
    for resource in package["result"]["resources"]:
        if not resource["datastore_active"]:
            resource_id = resource["id"]
            resource_name = resource["name"]
            resource_url = resource["url"]
            
            # Check for specific file name
            if f'bikeshare-ridership-{data_year}' in resource_name:  
                # Check and create folder if not exist
                if not os.path.exists(data_folder):
                    os.makedirs(data_folder)
                    print(f"Folder created: {data_folder}")

                response = requests.get(resource_url)
                # Save inside the data folder
                if response.status_code == 200:
                    file_extension = resource["format"].lower()
                    filename = f"{resource_name}.{file_extension}"
                    file_path = os.path.join(data_folder, filename)  

                    with open(file_path, "wb") as file:
                        file.write(response.content)
                    print(f"Saved as: {file_path}\n")
                else:
                    print(f"Failed to download {resource_name}\n")

# Extract zip
def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(zip_path)

# Fungsi untuk membersihkan folder dan menangani nested ZIP
def process_directory(directory):
    for root, _, files in os.walk(directory, topdown=False):  # Bottom-up traversal
        for file in files:
            file_path = os.path.join(root, file)

            # Jika menemukan ZIP, ekstrak dan proses ulang
            if file.endswith('.zip'):
                print(f"Extracting {file_path}")
                extract_zip(file_path, root)

        # Pastikan hanya file CSV yang tersisa
        for file in os.listdir(root):
            file_path = os.path.join(root, file)
            if os.path.isdir(file_path):
                continue  # Lewati folder
            if not file.endswith('.csv'):
                print(f"Removing non-CSV file: {file_path}")
                os.remove(file_path)

    # Cek ulang apakah masih ada ZIP yang tertinggal
    nested_zip_found = any(file.endswith('.zip') for _, _, files in os.walk(directory) for file in files)
    if nested_zip_found:
        print("Nested ZIP found, reprocessing...")
        process_directory(directory)  # Proses ulang jika masih ada ZIP


download_resource(data_year)
process_directory(data_folder)