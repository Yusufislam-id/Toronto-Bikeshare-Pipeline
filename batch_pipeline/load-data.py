import os
from google.cloud import storage

def upload_folder_to_gcs(bucket_name, folder_path, destination_folder):
    """
    Uploads all CSV files in a local folder to a GCS bucket.

    :param bucket_name: Name of the GCS bucket
    :param folder_path: Local folder path containing CSV files
    :param destination_folder: Destination path in GCS
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):  # Upload only CSV files
            local_file_path = os.path.join(folder_path, file_name)
            destination_blob_name = f"{destination_folder}/{file_name}"  # GCS path

            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(local_file_path)

            print(f"Uploaded {local_file_path} to gs://{bucket_name}/{destination_blob_name}")


upload_folder_to_gcs("toronto-bikeshare", "./data/bikeshare-ridership-2022", "bikeshare-ridership-2022")
