from pathlib import Path
import subprocess
import os
import logging

from utils import languages, translate
from utils.audio import split_audio

from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips
import speech_recognition as sr
import pysrt
from PIL import Image, ImageDraw, ImageFont

WV_FOLDER = "current-trans"
VD_FLDR = f"temp/video/"

def transcribe_audio(audio, src, target_dest, dest='en'):
  spoken_text =  ''
  if src == "en":
    subprocess.run(["sh.exe", "./transcribe_english.sh", audio, target_dest]).returncode
    print("English transcription generated.")
    return 0
    
  else:
    chunks = split_audio(audio_path=audio)
    
    for chunk in chunks:
      rec = sr.Recognizer()
      with sr.WavFile(chunk) as source:              
          audio = rec.record(source)
      try:
        print("translating chunk...")
        spoken_text = rec.recognize_google(audio, language=src)
        translation = translate.translate_single(spoken_text, src, "en")
        with open(target_dest, "a") as f:
          f.write(translation.text + " ")
        
      except Exception as e:
        print(e)
        print("Error: Could not transcribe audio.")
        return -1
        
  print("English translation generated.")
  return 0
    

def extract_audio(video):
  if Path(WV_FOLDER).exists():
    if len(os.listdir(WV_FOLDER)) > 0:
      print("Error: Empty folder 'current-trans' and retry")
      return None
    
  Path(WV_FOLDER).mkdir(exist_ok=True)

  video_path = f"{VD_FLDR}/{video}"
  audio_clip = VideoFileClip(video_path).audio
  path = f"{WV_FOLDER}/{video[:-4]}.wav"
  audio_clip.write_audiofile(path)
  print("Audio extraction complete.")
  return path

def srt_time_to_seconds(srt_time):
    return srt_time.hours * 3600 + srt_time.minutes * 60 + srt_time.seconds + srt_time.milliseconds / 1000

def add_subtitles(video_path, subtitle_path): #TODO
  try:
    subtitles = pysrt.open(subtitle_path)
    folder = "current-trans/subtitles"
    os.makedirs(folder, exist_ok=True)

    subclips = []
    prev_end = 0

    with VideoFileClip(video_path) as myvideo:
      i = 0
      for st in subtitles:
        start_time = srt_time_to_seconds(st.start)
        end_time = srt_time_to_seconds(st.end)

        if start_time > prev_end:
          non_subclip = myvideo.subclip(prev_end, start_time)
          subclips.append(non_subclip)

        clip = myvideo.subclip(start_time, end_time)
        
        img = Image.new('RGB', (700, 150))
        fnt = ImageFont.truetype('api/assets/fonts/OpenSans-Regular.ttf', 30)
        d = ImageDraw.Draw(img)
        d.text((15, 25), st.text, font=fnt, fill=(255, 255, 255))
        img.save(f'{folder}/{i}.png')

        stclip = ImageClip(f'{folder}/{i}.png', duration=clip.duration)
        stclip = stclip.set_position(('center', 0.85), relative=True)
        subclips.append(CompositeVideoClip([clip, stclip]))

        prev_end = end_time

        i += 1

      if prev_end < myvideo.duration:
        subclips.append(myvideo.subclip(prev_end, myvideo.duration))
      final = concatenate_videoclips(subclips)
      final.write_videofile(f"{WV_FOLDER}/final.mp4", fps=myvideo.fps)
      print("Subtitles added.")
      # TODO save in cloudinary and get link
      for im in os.listdir(folder):
        os.remove(im)
      os.rmdir(folder)
      for file in os.listdir(WV_FOLDER):
        os.remove(file)
    
    return 0 # return link
  except Exception as e:
    print(f"{e}")
    return -1
  
def execute(video, source_language, dest_language="english"):
  src = languages.get_language_code(source_language)
  # dest = languages.get_language_code(dest_language)
  audio_path = extract_audio(video)
  if not audio_path:
    exit(1)
  print("Transcribing text...")
  result = transcribe_audio(audio_path, src, f"{WV_FOLDER}/en-translation.txt")
  if result == -1:
    exit(1)
  print("Generating subtitles...")
  subprocess.run(["sh.exe", "./transcribe_align_to_english.sh", audio_path, source_language]).returncode
  print("\nSubtitles generated.")
  print("\nAdding subtitles...")
  if add_subtitles(f"{video}", f"{WV_FOLDER}/en-subtitles.srt") == -1:
    os.rmdir("current-trans")
    return {'status': "error", 'message': "Error: Could not add subtitles to video"}
  return {'status': "success", 'link': ""}