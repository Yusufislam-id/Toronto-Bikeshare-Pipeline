import requests
import zipfile
import os
from pathlib import Path

# Configuration
BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
PACKAGE_ID = "bike-share-toronto-ridership-data"
DATA_FOLDER = Path("./data")
YEAR = 2023  # Change this to the year you want to download


def fetch_package_data(package_id):
    """Fetch package metadata from CKAN API."""
    url = f"{BASE_URL}/api/3/action/package_show"
    response = requests.get(url, params={"id": package_id})
    return response.json() if response.status_code == 200 else None


def download_file(resource):
    """Download a single file from the given resource."""
    resource_name = resource.get("name", "unknown")
    resource_url = resource.get("url", "")
    file_extension = resource.get("format", "").lower()

    if resource_url:
        DATA_FOLDER.mkdir(exist_ok=True)
        file_path = DATA_FOLDER / f"{resource_name}.{file_extension}"

        try:
            response = requests.get(resource_url)
            response.raise_for_status()
            file_path.write_bytes(response.content)
            print(f"✅ Saved: {file_path}")
            return file_path  # Return the downloaded file path
        except requests.RequestException as e:
            print(f"❌ Error downloading {resource_name}: {e}")
    
    return None


def download_data_by_year(year):
    """Download ridership data for a specific year and return downloaded files."""
    package_data = fetch_package_data(PACKAGE_ID)
    if not package_data:
        print("❌ Failed to fetch package data.")
        return []
    
    resources = package_data.get("result", {}).get("resources", [])
    filtered_resources = [res for res in resources if str(year) in res.get("name", "").lower()]
    
    if not filtered_resources:
        print(f"⚠️ No data found for the year {year}.")
        return []

    print(f"🔍 Found {len(filtered_resources)} file(s) for {year}. Downloading...")
    downloaded_files = [download_file(resource) for resource in filtered_resources if not resource.get("datastore_active", False)]
    
    return [file for file in downloaded_files if file]  # Remove None values


def extract_zip(zip_path, extract_to):
    """Extract a zip file and remove it after extraction."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"📂 Extracted: {zip_path} -> {extract_to}")
        zip_path.unlink()  # Remove the zip file after extraction
    except zipfile.BadZipFile:
        print(f"❌ Invalid ZIP file: {zip_path}")


def process_directory(directory):
    """Extract zip files and remove non-CSV files in the directory."""
    for item in directory.glob("**/*"):  # Recursively check all files
        if item.suffix == ".zip":
            print(f"📦 Extracting {item}")
            extract_zip(item, item.parent)
    
    # Remove non-CSV files
    for item in directory.glob("**/*"):
        if item.is_file() and item.suffix != ".csv":
            print(f"🗑️ Removing non-CSV file: {item}")
            item.unlink()


if __name__ == "__main__":
    downloaded_files = download_data_by_year(YEAR)
    if downloaded_files:
        print("🛠️ Processing extracted files...")
        process_directory(DATA_FOLDER)
    else:
        print("⚠️ No files downloaded, skipping extraction.")
