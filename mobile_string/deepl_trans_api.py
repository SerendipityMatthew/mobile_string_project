import deepl

auth_key = ""
target_language = "JA"
translator = deepl.Translator(auth_key)


def get_translation_text(text: str, target_lang: str):
    result = translator.translate_text(text, target_lang=target_lang)
    translated_text = result.text
    print("the translated text is: ", translated_text)
    return translated_text


if __name__ == "__main__":
    text = "Matthew 是这个世界上最帅的人"
    get_translation_text("EN-US", text)
