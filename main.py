import functions_framework
import machine
import delete
import asyncio

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def main(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    src_bucket = data["bucket"]
    file = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]
    a = file.rsplit(".", 1)
    name = a[0]
    ext = a[1]
    dest_bucket = "meidcplus-storage-bucket/video"

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Source Bucket: {src_bucket}")
    print(f"Destination Buucket: {dest_bucket}")
    print(f"File: {file}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    if __name__ == "__main__":
        asyncio.run(processing(ext, src_bucket, dest_bucket, file, name))

async def processing(ext, src_bucket, dest_bucket, file, name):
    if ext == "mp4":
        await machine.copy_mp4(src_bucket, dest_bucket, file)
        await machine.convert_webm(src_bucket, dest_bucket, file, name)
        await machine.convert_ogg(src_bucket, dest_bucket, file, name)
        await machine.create_thumbnail(src_bucket, dest_bucket, file, name)
        delete.tmp(file)
    else:
        print("File extension is not supported")