import requests
import zipfile
import os

base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
package_id = "bike-share-toronto-ridership-data"
data_folder = "./data"
data_year = "2023"

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

    # Check data exist
    if os.path.exists(f"data/bikeshare-ridership-{data_year}.zip"):
        print(f'bikeshare-ridership-{data_year}.zip exist')
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

def extract_data(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(data_folder)
    os.remove(zip_path)