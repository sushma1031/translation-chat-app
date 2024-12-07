def load_translator():
    from googletrans import Translator
    return Translator()

def translate_single(text, from_language, to_language, translator):
    return translator.translate(text, src=from_language, dest=to_language).text

def translate_batch(batch, to_language, translator):
    return translator.translate(batch, dest=to_language)