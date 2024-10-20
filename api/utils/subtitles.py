from pathlib import Path
import subprocess
import os

from utils import languages, translate
from utils.audio import split_audio
from utils.cloud_store import download_media, upload_to_cld

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
    

def extract_audio(video, name):
  if Path(WV_FOLDER).exists():
    if len(os.listdir(WV_FOLDER)) > 0:
      print("Error: Empty folder 'current-trans' and retry")
      return None
    
  Path(WV_FOLDER).mkdir(exist_ok=True)

  # video_path = f"{VD_FLDR}/{video}"
  video_path = video
  temp = VideoFileClip(video_path)
  audio_clip = temp.audio
  path = f"{WV_FOLDER}/{name}.wav"
  audio_clip.write_audiofile(path)
  print("Audio extraction complete.")
  temp.close()
  return f"{name}.wav"

def srt_time_to_seconds(srt_time):
    return srt_time.hours * 3600 + srt_time.minutes * 60 + srt_time.seconds + srt_time.milliseconds / 1000

def add_subtitles(video_path, subtitle_path):
  try:
    subtitles = pysrt.open(subtitle_path)
    folder = "current-trans/subtitles"
    os.makedirs(folder, exist_ok=True)

    subclips = []
    prev_end = 0
    # abs_video_path = os.path.join(os.getcwd(), "uploads", video_path)
    os.path.normpath
    fnt = ImageFont.truetype('assets/fonts/OpenSans-Regular.ttf', 30)
    # os.chdir("uploads")

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
        
        d = ImageDraw.Draw(img)
        d.text((15, 25), st.text, font=fnt, fill=(255, 255, 255))
        img.save(f'{folder}/{i}.png')

        stclip = ImageClip(f'{folder}/{i}.png', duration=clip.duration)
        stclip = stclip.set_position(('center', 0.85), relative=True)
        subclips.append(CompositeVideoClip([clip, stclip]))

        prev_end = end_time

        i += 1

      if prev_end < myvideo.duration:
        if(myvideo.duration - prev_end) > 0.05:
          subclips.append(myvideo.subclip(prev_end, myvideo.duration))
      final = concatenate_videoclips(subclips)
      name = os.path.basename(video_path)[:-4]
      final.write_videofile(f"{WV_FOLDER}/{name}-final.mp4", fps=myvideo.fps)
      print("Subtitles added.")
      # TODO save in cloudinary and get link
    url = upload_to_cld(f"{WV_FOLDER}/{name}-final.mp4", "video")
    for im in os.listdir(folder):
      os.remove(os.path.join(folder, im))
    os.rmdir(folder)
    for file in os.listdir(WV_FOLDER):
      os.remove(os.path.join(WV_FOLDER, file))
    
    return url
  except Exception as e:
    print(f"{e}")
    return ""
  
def generate_st_and_upload(url, source_language, dest_language="english"):

  src = languages.get_language_code(source_language)
  # dest = languages.get_language_code(dest_language)
  video = f"uploads/v-{source_language}-1.mp4"
  if not download_media(url, video):
    return {"error": True, "message": "Could not download media"}
  try:
    audio_path = extract_audio(video, f"v-{source_language}-1")
    if not audio_path:
      return {'error': True, 'message': "Error: Could not extract audio"}
    print("Transcribing text...")
    result = transcribe_audio(f"{WV_FOLDER}/{audio_path}", src, f"{WV_FOLDER}/en-translation.txt")
    if result == -1:
      return {'error': True, 'message': "Error: Could not transcribe audio"}
    print("Generating subtitles...")
    subprocess.run(["sh.exe", "utils/transcribe_align_to_english.sh", audio_path, src]).returncode
    print("\nSubtitles generated.")
    print("\nAdding subtitles...")
    # print(os.getcwd())
    res = add_subtitles(f"{video}", f"{WV_FOLDER}/en-subtitles.srt")
    if not res:
      for file in os.listdir(WV_FOLDER):
        os.remove(file)
      return {'error': True, 'message': "Error: Could not add subtitles"}
    
    return {'success': True, 'result': res}
  except Exception as e:
    print(e)
    return {'message': f"{e}", "error": True}
  
if __name__ == "__main__":
  print("all imports are proper")

  