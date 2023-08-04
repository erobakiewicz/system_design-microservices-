import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor as mp


def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    # temporary file
    temp_file = tempfile.NamedTemporaryFile()
    # video content
    out = fs_videos.get(ObjectId(message.get('video_fid')))
    # add video contents to empty file
    temp_file.write(out.read())
    # convert video to audio (mp3)
    audio = mp.VideoFileClip(temp_file.name).audio
    temp_file.close()

    # write audio to its own file
    temp_file_path = tempfile.gettempdir() + f'/{message.get("video_fid")}.mp3'
    audio.write_audiofile(temp_file_path)

    # save file to mongodb
    file = open(temp_file_path, 'rb')
    data = file.read()
    fid = fs_mp3s.put(data)
    file.close()
    os.remove(temp_file_path)

    message['mp3_fid'] = str(fid)

    try:
        channel.basic_publish(
            exchange='', routing_key=os.environ.get('MP3_QUEUE'),
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
        )
    except Exception as e:
        fs_mp3s.delete(fid)
        return {'message': str(e)}
