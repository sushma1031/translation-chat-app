import easyocr
from utils import languages, translate

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