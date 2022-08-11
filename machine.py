import ffmpeg
import cloudstorage

async def copy_mp4(src_bucket_name, dest_bucket_name, filename, name):
    await cloudstorage.download(src_bucket_name, filename, filename)
    await cloudstorage.upload(dest_bucket_name, filename, filename)

async def convert_webm(src_bucket_name, dest_bucket_name, filename, name):
    await cloudstorage.download(src_bucket_name, filename, filename)
    stream = ffmpeg.input(filename)
    wemb = ffmpeg.output(stream, '/tmp/{name}.webm'.format(name=name))
    print("Converting to webm")
    ffmpeg.run(wemb)
    await cloudstorage.upload(dest_bucket_name, f"{name}.webm", f"{name}.webm")
    
async def convert_ogg(src_bucket_name, dest_bucket_name, filename, name):
    await cloudstorage.download(src_bucket_name, filename, filename)
    stream = ffmpeg.input(filename)
    ogg = ffmpeg.output(stream, '/tmp/{name}.ogg'.format(name=name))
    print("Converting to ogg")
    await cloudstorage.upload(dest_bucket_name, f"{name}.ogg", f"{name}.ogg")
    ffmpeg.run(ogg)

async def create_thumbnail(src_bucket_name, dest_bucket_name, filename, name):
    await cloudstorage.download(src_bucket_name, filename, filename)
    print("Creating thumbnail video")
    ffmpeg.input("/tmp/{name}.mp4".format(name=name), ss=2).output("/tmp/{name}-thumb.jpg", vframes=1).run()
    await cloudstorage.upload(dest_bucket_name, f"{name}-thumb.jpg", f"{name}-thumb.jpg")