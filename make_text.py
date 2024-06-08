import librosa
import os
from transformers import WhisperProcessor, WhisperForConditionalGeneration

from tqdm.auto import tqdm

def load_audio_set_sample_rate(file_path):
    
    waveform, sample_rate = librosa.load(file_path, sr=None, mono=True)

    if not sample_rate == 16000:
       
        tensor_waveform = librosa.resample(waveform, orig_sr=sample_rate, target_sr=16000)
    else:
        tensor_waveform = waveform

    return tensor_waveform, 16000

audio_dir = r"./audio"
#the output text will be stored in thsi file
text_dir = r"./text"
os.makedirs(text_dir,exist_ok= True)
#i am using whisper tiny model for transcription
model_name = "openai/whisper-tiny"
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name)
transcriptions_dict = {}

#as the above is long time to be converted lets discuss about the video which is already transcribed
#it is a python hindi tutorial

audio_file = "/media/krishna/New Volume/roshini_assign/audio/एग्ज़िट पोल का एग्ज़िट पोल  Exit Poll ka Exit Poll.wav"#replace the path of the rquired audio file here
print(f"processing {audio_file}")
audio_path = os.path.join(audio_dir, audio_file)


audio, sample_rate = load_audio_set_sample_rate(audio_path)  


chunk_size = sample_rate * 20 
chunks = [audio[i:i+chunk_size] for i in range(0, len(audio), chunk_size)]
#splitting audios into chunks as to give input for whisper model and thne save the output as txt
transcriptions = []
for index, chunk in enumerate(tqdm(chunks)):
    input_features = processor(chunk, sampling_rate=16000, return_tensors="pt").input_features
    predicted_ids = model.generate(input_features)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    transcriptions.append(transcription)

full_transcription = ' '.join(transcriptions)


basefile_name = os.path.splitext(audio_file)[0]
transcriptions_dict[basefile_name] = full_transcription


text_file_path = os.path.join(text_dir, basefile_name + ".txt")
with open(text_file_path, 'w') as text_file:
    text_file.write(full_transcription)
print(f"Transcription saved to {text_file_path}")
print("-")