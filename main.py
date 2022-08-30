import machine
import delete
import asyncio
import cloudstorage
import sys

from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
async def main():
    try:
        envelope = request.get_json()
        if not envelope:
            msg = "no Pub/Sub message received"
            print(f"error: {msg}")
            return f"Bad Request: {msg}", 400

        if not isinstance(envelope, dict) or "message" not in envelope:
            msg = "invalid Pub/Sub message format"
            print(f"error: {msg}")
            return f"Bad Request: {msg}", 400

        json_parse = envelope["message"]
        value = json_parse["attributes"]
        bucketId = value["bucketId"]
        objectId = value["objectId"]
        a = objectId.rsplit(".", 1)
        name = a[0]
        ext = a[1]
        dest_bucket = "medicplus-storage-bucket"

        print("Event Time: {}".format(value["eventTime"]))
        print("Event type: {}".format(value["eventType"]))
        print(f"Source Bucket: {bucketId}")
        print(f"Destination Bucket: {dest_bucket}")
        print(f"File: {objectId}")

        ifexists = await cloudstorage.cek_if_exists(objectId, dest_bucket)

        if ext == "mp4" and ifexists == False:
            await delete.tmp(objectId)
            await machine.copy_mp4(bucketId, dest_bucket, objectId)
            await machine.convert_webm(bucketId, dest_bucket, objectId, name)
            await machine.convert_ogg(bucketId, dest_bucket, objectId, name)
            await machine.create_thumbnail(bucketId, dest_bucket, objectId, name)
            await delete.tmp(objectId)
            sys.stdout.flush()
            return (f"File {objectId} successfull converted", 204)
        elif ext == "mp4" and ifexists == True:
            e = f"File {objectId} is already exists in {dest_bucket}"
            return (e, 404)
        else:
            e = f"File {ext} is not supported"
            print(e)
            return (e, 404)
        
    except BaseException as e:
        print(e)
        sys.stdout.flush()
        return (e, 400)

@app.route("/", methods=["GET"])
async def test():
    return ("video-processing-api", 200)

if __name__=='__main__':
    app.run(host="0.0.0.0", port="8080", threaded=True, debug=True)
