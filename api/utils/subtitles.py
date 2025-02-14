from pathlib import Path
import os

from utils import languages
from utils.cloud_store import download_media, upload_to_cld

import ffmpeg

WV_FOLDER = "current-trans"
VD_FLDR = f"temp/video/"

def transcribe_audio(audio, src, dest='en'):
  from faster_whisper import WhisperModel
  try:
    model = WhisperModel("small", local_files_only=True,compute_type="float32")
    segments = []
    if src == 'en':
      segments, _ = model.transcribe(audio)
    else:
      segments, _ = model.transcribe(audio, language=src, task="translate")
    print("English translation generated.")
    return segments
  except Exception as e:
    print("Error transcribing audio:", e)
    return None

def extract_audio(video, name):
  if Path(WV_FOLDER).exists():
    if len(os.listdir(WV_FOLDER)) > 0:
      clear_folder()
  else:  
    Path(WV_FOLDER).mkdir(exist_ok=True)
  
  path = f"{WV_FOLDER}/{name}.wav"
  stream = ffmpeg.input(video)
  stream = ffmpeg.output(stream, path, loglevel="quiet")
  ffmpeg.run(stream, overwrite_output=True)

  return f"{name}.wav"

def format_time(seconds):
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    milliseconds = round((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time

def generate_subtitle_file(segments):
    subtitle_file = f"{WV_FOLDER}/en-subtitles.srt"
    text = ""
    try:
      for index, segment in enumerate(segments):
          segment_start = format_time(segment.start)
          segment_end = format_time(segment.end)
          text += f"{str(index+1)} \n"
          text += f"{segment_start} --> {segment_end} \n"
          text += f"{segment.text} \n"
          text += "\n"
          
      with open(subtitle_file, "w") as f:
        f.write(text)
      print("\nSubtitles generated.")
      return True
    except Exception as e:
      print(e)
      return False

def add_subtitles(video_path, subtitle_path):
  try:
    video_input_stream = ffmpeg.input(video_path)
    name = os.path.basename(video_path)[:-4]
    output_video = f"{WV_FOLDER}/{name}-final.mp4"
    stream = ffmpeg.output(video_input_stream, output_video, vf=f"subtitles={subtitle_path}", loglevel="quiet")
    ffmpeg.run(stream, overwrite_output=True)
    print("Subtitles added.")

    url = upload_to_cld(f"{WV_FOLDER}/{name}-final.mp4", "video")
    return url
  except Exception as e:
    print(e)
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
    if not result:
      return {'error': True, 'message': "Error: Could not transcribe audio"}
    print("Generating subtitles...")
    if not generate_subtitle_file(result):
      return {'error': True, 'message': "Error: Could not generate subtitles"}
    print("\nAdding subtitles...")
    # print(os.getcwd())
    res = add_subtitles(video, f"{WV_FOLDER}/en-subtitles.srt")
    if not res:
      return {'error': True, 'message': "Error: Could not add subtitles"}
    clear_folder()
    return {'success': True, 'result': res}
  except Exception as e:
    print(e)
    clear_folder()
    return {'message': f"{e}", "error": True}

def clear_folder():
  temp_files = os.listdir(WV_FOLDER)
  for f in temp_files:
    os.remove(f"{WV_FOLDER}/{f}")
  
if __name__ == "__main__":
  print("all imports are proper")

  