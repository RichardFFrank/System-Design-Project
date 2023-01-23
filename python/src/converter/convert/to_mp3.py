import pika
import json
import tempfile
import os
from bson.objectid import ObjectId
import moviepy.editor


def start(message, fs_videos, fs_mp3s, channel):
    # deserialize message document to object.
    message = json.loads(message)

    # create empty temp file
    temp_file = tempfile.NamedTemporaryFile()

    # get video contents
    video_contents = fs_videos.get(ObjectId(message["video_fid"]))
    print("we're in the mp3 converter.")
    # add video contents to empty file
    temp_file.write(video_contents.read())

    # create audio from temp video file
    audio = moviepy.editor.VideoFileClip(tf.name).audio

    temp_file.close()

    temp_path = temp_file.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(temp_path)

    # save file to mongo
    write_file = open(temp_path, "rd")
    data = write_file.read()
    fid = fs_mp3s.put(data)
    write_file.close()
    os.remove(temp_path)

    # update message
    message["mp3_fid"] = str(fid)

    # add message to mp3 queue

    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),

            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        fs_mp3s.delete(fid)
        return "failed to publish message"
