from googletrans import Translator

translator = Translator()

def translate_single(text, from_language, to_language):
    return translator.translate(text, src=from_language, dest=to_language)

def translate_batch(batch, to_language):
    return translator.translate(batch, dest=to_language)