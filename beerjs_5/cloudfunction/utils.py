from google.cloud import storage
from google.cloud import bigquery
import logging

TEMP_FOLDER = "/tmp/"

def download_file_from_storage(bucket, file_path):
    file_name = file_path.split("/")[-1]
    local_file_path = TEMP_FOLDER+file_name
    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.blob(file_path)
    blob.download_to_filename(local_file_path)
    return local_file_path