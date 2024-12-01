from utils import languages, translate

def translate_text(text, src, dest):
  s_code = languages.get_language_code(src)
  d_code = languages.get_language_code(dest)
  try:
    res = translate.translate_single(text, s_code, d_code)
    return {'success': True, 'result': res}
  except Exception as e:
    print(e)
    return {'message': f"{e}", "error": True}
  
if __name__ == "__main__":
  print("all imports are proper")