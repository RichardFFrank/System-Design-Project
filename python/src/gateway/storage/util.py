import pika, json


def upload(f, fs, channel, access):
    
    # upload file to mongoDB database.
    try:
        file_id = fs.put(file) # mongoDB returns the fileID
        if (file_id):
            print("Put file on mongoDB: " + file_id)
        
    except Exception as err:
        print(err)
        return "internal server error", 500

    # on successful upload, put message in rabbitMQ queue to be processed.
    
    message = {
        "video_fid": str(file_id),
        "mp3_fid": None,
        "username": access["username"],
    }
    
    try:
        print("here")
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body= json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        print("published to rabbitMQ")
        
    except Exception as err:
        print(err)
        fs.delete(fid)
        return "internal server error", 500
