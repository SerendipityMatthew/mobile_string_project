"""
https: // translate.googleapis.com
POST / v3beta1 / {parent = projects / *}:translateText

"""

import re
import html
from urllib import parse

import deepl
import requests
from googletrans import Translator

from read_ini_utils import is_translate_by_google

GOOGLE_TRANSLATE_URL = 'http://translate.google.cn/m?q=%s&tl=%s&sl=%s'

auth_key = "xxxxxx"


def get_translation_text_by_deepl(text: str, target_lang: str):
    deepl_translator = deepl.Translator(auth_key)

    result = deepl_translator.translate_text(text, target_lang=target_lang)
    translated_text = result.text
    print("the translated text is: ", translated_text)
    return translated_text


def translate_by_api(text: str, to_language="auto", text_language="auto"):
    """
    谷歌官方的 翻译库
    https://py-googletrans.readthedocs.io/en/latest/
    :param text:
    :param to_language:
    :param text_language:
    :return:
    """
    google_translator = Translator()
    return google_translator.translate(text, dest=to_language).text


def translate(text, to_language="auto", source_language="auto") -> str:
    source_language = "auto"
    """
    通过网页的方式翻译字符串， 似乎有请求次数的限制，切换成 api 接口的方式更好
    :param source_language: 
    :param text:
    :param to_language:
    :return:
    """
    text = parse.quote(text)
    url = GOOGLE_TRANSLATE_URL % (text, to_language, source_language)
    response = requests.get(url)
    data = response.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if len(result) == 0:
        return ""
    result_text = html.unescape(result[0])
    print("the translated text is: result_text = ", result_text)

    return result_text


def translate_text(text: str, dest_lang: str, source_lang: str = "") -> str:
    result = ''
    if is_translate_by_google():
        result = translate(text, dest_lang)
    else:
        deepl_trans = get_translation_text_by_deepl(text, target_lang=dest_lang)
        result = deepl_trans
    return result


# print(get_translation_text_by_deepl("保存", "JA"))
