import asyncio
import os

import speech_recognition as sr
from gtts import gTTS
from faster_whisper import WhisperModel

from utils import languages
from utils.cloud_store import download_media, upload_to_cld

# def split_audio(audio_path, folder=None):
#   audio = AudioSegment.from_wav(audio_path)  
#   if not folder:
#     folder = "audio_chunks"
#   else:
#     folder += "/audio_chunks"  
#   try: 
#     os.mkdir(folder) 
#   except FileExistsError: 
#     pass 
#   i = 0
#   count = 0
#   duration = 10000
#   audio_length = audio.duration_seconds * 1000
#   audio_chunk_paths = []
#   while(i+duration < audio_length):
#     chunk = audio[i:(i+duration)]
#     print(f"saving chunk-{count}.wav") 
#     chunk.export(f"{folder}/chunk-{count}.wav", bitrate ='192k', format ="wav")
#     audio_chunk_paths.append(f"{folder}/chunk-{count}.wav") 
#     i += duration
#     count += 1
#   if(i<audio_length):
#     chunk = audio[i:audio_length]
#     print(f"saving chunk-{count}.wav") 
#     chunk.export(f"{folder}/chunk-{count}.wav", bitrate ='192k', format ="wav")
#     audio_chunk_paths.append(f"{folder}/chunk-{count}.wav")
#   return audio_chunk_paths

def text_to_voice(text_data, to_language, name):
  dest = languages.get_language_code(to_language)
  myobj = gTTS(text=text_data, lang=dest, slow=False)
  myobj.save(f"translated/{name}-translated.mp3")
  return f"translated/{name}-translated.mp3"

def transcribe_audio(audio_file, src):
  spoken_text =  ''
  if src == "en":
    model = WhisperModel("small", local_files_only=True)
    segments, _ = model.transcribe(audio_file, language="en")  # 'language' is set to 'en' for English
    transcription = ""
    for segment in segments:
        spoken_text += segment.text
  else:
    try:
      rec = sr.Recognizer()
      with sr.WavFile(audio_file) as source:              
          audio = rec.record(source)
      spoken_text = rec.recognize_google(audio)   
    except Exception as e:
      print(e)
  
  return spoken_text

def translate_and_upload_audio(url, source_language, dest_language):
  print("Translating...")
  save_path = os.path.join("uploads", f"a-{source_language}-1.wav")
  if not download_media(url, save_path):
    return {"error": True, "message": "Could not download media"}
  sp_text = ''
  sp_text = transcribe_audio(save_path, source_language)
  try:
    res = translate_text(sp_text, source_language, dest_language)
    if res.get('success', False):
      # print("here")
      voice = text_to_voice(res["result"], dest_language, f"a-{source_language}-1")
      # print(save_path[:-4])
      url = upload_to_cld(voice, "audio")
      os.remove(voice)
      print("Audio translated successfully!")
      return {'success': True, 'result': url}
    return res
  except Exception as e:
    print(e)
    return {'message': f"{e}", "error": True}
  
if __name__ == "__main__":
  print("all imports are proper")
  