from google.cloud import storage

async def download(src_bucket_name, source_blob_name, destination_file_name):
     print("Downloading {filename}".format(filename=source_blob_name))
     storage_client = storage.Client()
     bucket = storage_client.bucket(src_bucket_name)
     blob = bucket.blob(source_blob_name)

     blob.download_to_filename("/tmp/{file}".format(file=source_blob_name))
     print(
          "Downloaded {file} from bucket {bucket} to /tmp/{file}".format(file=source_blob_name, bucket=src_bucket_name)
     )

async def upload(dest_bucket_name, source_file_name, destination_blob_name):
     print("Uploading {filename}".format(filename=source_file_name))
     storage_client = storage.Client()
     bucket = storage_client.bucket(dest_bucket_name)
     blob = bucket.blob(destination_blob_name)

     blob.upload_from_filename("/tmp/{file}".format(file=source_file_name))
     print(
          "Uploaded {file} to bucket {bucket} from /tmp/{file}".format(file=source_file_name, bucket=dest_bucket_name)
     )

async def cek_if_exists(source_file_name, dest_bucket_name):
     print(f"Checking file {source_file_name} if exists")
     storage_client = storage.Client()
     bucket = storage_client.bucket(dest_bucket_name)
     result = storage.Blob("video"+source_file_name, bucket).exists(storage_client)
     return result