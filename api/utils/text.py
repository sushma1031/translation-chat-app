from utils import languages, translate

def translate_text(text, src, dest):
  s_code = languages.get_language_code(src)
  d_code = languages.get_language_code(dest)
  return translate.translate_single(text, s_code, d_code)