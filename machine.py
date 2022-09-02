import ffmpeg
import cloudstorage
import google.cloud.logging
import logging

async def copy_mp4(src_bucket_name, dest_bucket_name, filename):
    client = google.cloud.logging.Client()
    client.setup_logging()
    logging.info(f"Copying {filename} to {dest_bucket_name}")
    await cloudstorage.download(src_bucket_name, filename)
    await cloudstorage.upload(dest_bucket_name, filename, filename)
    logging.info(f"File {filename} successfully copied to {dest_bucket_name}")

async def convert_webm(dest_bucket_name, name):
    client = google.cloud.logging.Client()
    client.setup_logging()
    stream = ffmpeg.input("/tmp/{file}.mp4".format(file=name))
    webm = ffmpeg.output(stream, '/tmp/{name}.webm'.format(name=name))
    print("Converting to webm")
    logging.info(f"Converting {name}.mp4 to {name}.webm")
    ffmpeg.run(webm)
    await cloudstorage.upload(dest_bucket_name, f"{name}.webm", f"{name}.webm")
    print(f"File {name}.webm successfully converted and uploaded to {dest_bucket_name}")
    logging.info(f"File {name}.webm successfully converted and uploaded to {dest_bucket_name}")
    
async def convert_ogg(dest_bucket_name, name):
    client = google.cloud.logging.Client()
    client.setup_logging()
    stream = ffmpeg.input("/tmp/{file}.mp4".format(file=name))
    ogg = ffmpeg.output(stream, '/tmp/{name}.ogg'.format(name=name))
    print("Converting to ogg")
    logging.info(f"Converting {name}.mp4 to {name}.ogg")
    ffmpeg.run(ogg)
    await cloudstorage.upload(dest_bucket_name, f"{name}.ogg", f"{name}.ogg")
    print(f"File {name}.ogg successfully converted and uploaded to {dest_bucket_name}")
    logging.info(f"File {name}.ogg successfully converted and uploaded to {dest_bucket_name}")

async def create_thumbnail(dest_bucket_name, name):
    client = google.cloud.logging.Client()
    client.setup_logging()
    print(f"Creating thumbnail video for {name}.mp4")
    logging.info(f"Creating thumbnail video for {name}.mp4")
    ffmpeg.input("/tmp/{name}.mp4".format(name=name), ss=2).output("/tmp/{name}-thumb.jpg".format(name=name), vframes=1).run()
    await cloudstorage.upload(dest_bucket_name, f"{name}-thumb.jpg", f"{name}-thumb.jpg")
    print(f"File {name}-thumb.jpg successfully converted and uploaded to {dest_bucket_name}")
    logging.info(f"File {name}-thumb.jpg successfully converted and uploaded to {dest_bucket_name}")