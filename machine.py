import ffmpeg
import cloudstorage

async def copy_mp4(src_bucket_name, dest_bucket_name, filename):
    await cloudstorage.download(src_bucket_name, filename)
    await cloudstorage.upload(dest_bucket_name, filename, filename)

async def convert_webm(dest_bucket_name, name):
    stream = ffmpeg.input("/tmp/{file}.mp4".format(file=name))
    wemb = ffmpeg.output(stream, '/tmp/{name}.webm'.format(name=name))
    print("Converting to webm")
    ffmpeg.run(wemb)
    await cloudstorage.upload(dest_bucket_name, f"{name}.webm", f"{name}.webm")
    print(f"File {name}.webm successfully converted and uploaded to {dest_bucket_name}")
    
async def convert_ogg(dest_bucket_name, name):
    stream = ffmpeg.input("/tmp/{file}.mp4".format(file=name))
    ogg = ffmpeg.output(stream, '/tmp/{name}.ogg'.format(name=name))
    print("Converting to ogg")
    await cloudstorage.upload(dest_bucket_name, f"{name}.ogg", f"{name}.ogg")
    ffmpeg.run(ogg)
    print(f"File {name}.ogg successfully converted and uploaded to {dest_bucket_name}")

async def create_thumbnail(dest_bucket_name, name):
    print("Creating thumbnail video")
    ffmpeg.input("/tmp/{name}.mp4".format(name=name), ss=2).output("/tmp/{name}-thumb.jpg", vframes=1).run()
    await cloudstorage.upload(dest_bucket_name, f"{name}-thumb.jpg", f"{name}-thumb.jpg")
    print(f"File {name}-thumb.jpg successfully converted and uploaded to {dest_bucket_name}")