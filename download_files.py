
import requests
import os
from moviepy.editor import *
from pytube import YouTube

from pydub import AudioSegment
#the given code takes input the type of file i.e audio or video and depending on type it will extract from the above and save it
#as a .wav file
def download_audio(url, output_path):
    
    response = requests.get(url)
    if response.status_code == 200:
        
        filename = os.path.basename(url)
        local_path = os.path.join(output_path, filename)

        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"Audio file downloaded and saved as {local_path}")
    else:
        print(f"Failed to download audio. Status code: {response.status_code}")


def download_audio_from_video(url, output_path):
   
    if not os.path.exists(output_path):
        os.makedirs(output_path)

  
    yt = YouTube(url)

    
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

  
    print(f"Downloading audio from: {yt.title}")
    audio_file = audio_stream.download(output_path)

 
    base, ext = os.path.splitext(audio_file)
    wav_file = f"{base}.wav"

    
    audio = AudioSegment.from_file(audio_file)
    audio.export(wav_file, format="wav")

   
    os.remove(audio_file)

    print(f"Audio has been downloaded and saved as: {wav_file}")


audio_dir = r"./audio"
os.makedirs(audio_dir,exist_ok= True)

def download_from_link(type,url):
    if type == 1:
        download_audio(url,audio_dir)
    else:
        download_audio_from_video(url,audio_dir)

#the above are some example urls
url = ['https://www.youtube.com/watch?v=DjuCoQbJ4ZA','https://www.youtube.com/watch?v=ry9SYnV3svc&pp=ygUTc2hvcnQgZW5naXNoIHZpZGVvcw%3D%3D','https://www.youtube.com/watch?v=h1WdbfoHeac&pp=ygUccHl0aG9uIGluIHRlbHVndSBmdWxsIGNvdXJzZQ%3D%3D',
'https://www.youtube.com/watch?v=XHzQvq-ltAo&pp=ygUbcHl0aG9uIGluIGhpbmRpIGZ1bGwgY291cnNl','https://storage.googleapis.com/aai-web-samples/langchain_agents_webinar.opus','https://youtu.be/OZIRAavoGng?list=PLjVLYmrlmjGcQfNj_SLlLV4Ytf39f8BF7']

type = int(input("Enter 1 for audio 2 for video:  "))
url_link = input('enter the audio/video link:  ')

link = url_link.replace("'", "")

download_from_link(type, link)

