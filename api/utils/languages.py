from googletrans import LANGUAGES

language_mapping = {name: code for code, name in LANGUAGES.items()}

values = list(LANGUAGES.values())

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)