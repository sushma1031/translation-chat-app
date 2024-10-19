import easyocr
from utils import languages, translate
from utils.cloud_store import download_media

import os

def load_ocr_model(langs):
  language_codes = [languages.get_language_code(l) for l in langs]
  if 'en' not in language_codes:
    language_codes.append('en')
  reader = easyocr.Reader(language_codes, gpu=False)
  print("Model loaded successfully.")
  return reader

def extract_image_text(image_path, reader):
  result = reader.readtext(image_path)
  text = [r[1] for r in result]
  return text

def translate_img_text(image, src, dest):
    print("Loading model...")
    reader = load_ocr_model([src, 'english'])
    print("Extracting text...")
    extracted_text = extract_image_text(image, reader)
    print("Translating text...")
    results = translate.translate_batch(extracted_text, dest)
    translations = [translation.text for translation in results]
    return translations

def download_and_translate_img(url, source_language, dest_language):
  save_path = os.path.join("uploads", f"i-{source_language}-1.jpg")
  if not download_media(url, save_path):
    return {"error": True, "message": "Could not download media"}
  try:
    res = translate_img_text(save_path, source_language, dest_language)
    return {'success': True, 'result': res}
  except Exception as e:
    print(e)
    return {'message': f"{e}", "error": True}
  
if __name__ == "__main__":
  print("all imports are proper")