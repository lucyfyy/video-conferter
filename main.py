import machine
import delete
import logging
import cloudstorage
import google.cloud.logging

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
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

        ifexists = cloudstorage.cek_if_exists(objectId, dest_bucket)

        if ext == "mp4" and ifexists == False:
            client = google.cloud.logging.Client()
            client.setup_logging()
            delete.tmp(objectId)
            machine.copy_mp4(bucketId, dest_bucket, objectId)
            machine.convert_webm( dest_bucket, name)
            machine.convert_ogg(dest_bucket, name)
            machine.create_thumbnail( dest_bucket, name)
            delete.tmp(objectId)
            ress = f"File {objectId} successfull converted" 
            print(ress)
            logging.info(ress)
            return jsonify(ress), 200
        elif ext == "mp4" and ifexists == True:
            client = google.cloud.logging.Client()
            client.setup_logging()
            ress = f"File {objectId} is already exists in {dest_bucket}"
            print(ress)
            logging.info(ress)
            return jsonify(ress), 200
        else:
            client = google.cloud.logging.Client()
            client.setup_logging()
            ress = f"File {ext} is not supported"
            print(ress)
            logging.info(ress)
            return jsonify(ress), 200
        
    except BaseException as e:
        client = google.cloud.logging.Client()
        client.setup_logging()
        print(ress)
        logging.error(ress)
        return jsonify(ress), 200

@app.route("/", methods=["GET"])
def test():
    return jsonify("video-processing-api"), 200

if __name__=='__main__':
    app.run(host="0.0.0.0", port="8080", threaded=True, debug=True)
