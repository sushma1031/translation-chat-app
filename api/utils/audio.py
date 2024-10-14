import sys
import os
from pydub import AudioSegment 

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

if __name__ == "__main__":
  split_audio(audio_path=f"../audio/{sys.argv[1]}")