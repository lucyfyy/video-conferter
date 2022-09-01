import ffmpeg
import cloudstorage
import logging

async def copy_mp4(src_bucket_name, dest_bucket_name, filename):
    logging.debug(f"Copying {filename} to {dest_bucket_name}")
    await cloudstorage.download(src_bucket_name, filename)
    await cloudstorage.upload(dest_bucket_name, filename, filename)
    logging.debug(f"File {filename} successfully copied to {dest_bucket_name}")

async def convert_webm(dest_bucket_name, name):
    stream = ffmpeg.input("/tmp/{file}.mp4".format(file=name))
    webm = ffmpeg.output(stream, '/tmp/{name}.webm'.format(name=name))
    print("Converting to webm")
    logging.debug(f"Converting {name}.mp4 to {name}.webm")
    ffmpeg.run(webm)
    await cloudstorage.upload(dest_bucket_name, f"{name}.webm", f"{name}.webm")
    print(f"File {name}.webm successfully converted and uploaded to {dest_bucket_name}")
    logging.debug(f"File {name}.webm successfully converted and uploaded to {dest_bucket_name}")
    
async def convert_ogg(dest_bucket_name, name):
    stream = ffmpeg.input("/tmp/{file}.mp4".format(file=name))
    ogg = ffmpeg.output(stream, '/tmp/{name}.ogg'.format(name=name))
    print("Converting to ogg")
    logging.debug(f"Converting {name}.mp4 to {name}.ogg")
    ffmpeg.run(ogg)
    await cloudstorage.upload(dest_bucket_name, f"{name}.ogg", f"{name}.ogg")
    print(f"File {name}.ogg successfully converted and uploaded to {dest_bucket_name}")
    logging.debug(f"File {name}.ogg successfully converted and uploaded to {dest_bucket_name}")

async def create_thumbnail(dest_bucket_name, name):
    print(f"Creating thumbnail video for {name}.mp4")
    logging.debug(f"Creating thumbnail video for {name}.mp4")
    ffmpeg.input("/tmp/{name}.mp4".format(name=name), ss=2).output("/tmp/{name}-thumb.jpg".format(name=name), vframes=1).run()
    await cloudstorage.upload(dest_bucket_name, f"{name}-thumb.jpg", f"{name}-thumb.jpg")
    print(f"File {name}-thumb.jpg successfully converted and uploaded to {dest_bucket_name}")
    logging.debug(f"File {name}-thumb.jpg successfully converted and uploaded to {dest_bucket_name}")