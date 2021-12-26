"""
https: // translate.googleapis.com
POST / v3beta1 / {parent = projects / *}:translateText

"""

import re
import html
from urllib import parse
import requests
from googletrans import Translator

GOOGLE_TRANSLATE_URL = 'http://translate.google.cn/m?q=%s&tl=%s&sl=%s'


def translate_by_api(text: str, to_language="auto", text_language="auto"):
    """
    谷歌官方的 翻译库
    https://py-googletrans.readthedocs.io/en/latest/
    :param text:
    :param to_language:
    :param text_language:
    :return:
    """
    translator = Translator()
    # translator.translate('안녕하세요.')
    # <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
    # <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
    return translator.translate(text, dest=to_language).text


def translate(text, to_language="auto", text_language="auto"):
    """
    通过网页的方式翻译字符串， 似乎有请求次数的限制，切换成 api 接口的方式更好
    :param text:
    :param to_language:
    :param text_language:
    :return:
    """
    text = parse.quote(text)
    url = GOOGLE_TRANSLATE_URL % (text, to_language, text_language)
    response = requests.get(url)
    data = response.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if len(result) == 0:
        return ""

    return html.unescape(result[0])


print(translate_by_api("许万金是这个世界上最帅的人", "ko", "zh-CN"))
