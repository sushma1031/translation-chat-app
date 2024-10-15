import asyncio
import os
from pydub import AudioSegment 

import speech_recognition as sr
from utils import languages, translate
from gtts import gTTS

from pathlib import Path
import subprocess


def split_audio(audio_path, folder=None):
  audio = AudioSegment.from_wav(audio_path)
  
  if not folder:
    folder = "../audio_chunks"
  else:
    folder += "/audio_chunks"
  
  try: 
    os.mkdir(folder) 
  except FileExistsError: 
    pass 

  i = 0
  count = 0
  duration = 10000
  audio_length = audio.duration_seconds * 1000
  audio_chunk_paths = []
  while(i+duration < audio_length):
    chunk = audio[i:(i+duration)]
    print(f"saving chunk-{count}.wav") 

    chunk.export(f"{folder}/chunk-{count}.wav", bitrate ='192k', format ="wav")
    audio_chunk_paths.append(f"{folder}/chunk-{count}.wav") 

    i += duration
    count += 1

  if(i<audio_length):
    chunk = audio[i:audio_length]
    print(f"saving chunk-{count}.wav") 

    chunk.export(f"{folder}/chunk-{count}.wav", bitrate ='192k', format ="wav")
    audio_chunk_paths.append(f"{folder}/chunk-{count}.wav")

  return audio_chunk_paths

async def text_to_voice(text_data, to_language, name):
  dest = languages.get_language_code(to_language)
  myobj = gTTS(text=text_data, lang=dest, slow=False)
  Path("../translated").mkdir(exist_ok=True)
  myobj.save(f"{Path.cwd()}/../translated/{name}-translated.mp3")
  # TODO save in cloudinary

def transcribe_audio(audio_file):
  spoken_text =  ''
  try:
    rec = sr.Recognizer()
    with sr.WavFile(audio_file) as source:              
        audio = rec.record(source)
    spoken_text = rec.recognize_google(audio)   
  except Exception as e:
    print(e)
  
  return spoken_text

def translate_audio(audio_file, source_language, dest_language):
  src = languages.get_language_code(source_language)
  dest = languages.get_language_code(dest_language)
  spoken_text =  ''
  if src == "en":
    subprocess.run(["sh.exe", "./transcribe_english.sh", audio_file, f"{audio_file}-result.txt"]).returncode
    try:
      with open(f"{audio_file}-result.txt", "r") as f:
        spoken_text = f.read()
    except Exception as e:
       print(e)
    os.remove(f"{audio_file}-result.txt")

  else:
    try:
      rec = sr.Recognizer()
      with sr.WavFile(audio_file) as source:              
          audio = rec.record(source)
      spoken_text = rec.recognize_google(audio)   
    except Exception as e:
      print(e)

  try:
    return translate.translate_single(spoken_text, src, dest)
  except Exception as e:
      print(e)