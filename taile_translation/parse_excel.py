from xml.etree.ElementTree import ElementTree, SubElement, Element

import pandas

from Taile_String import TaileString
from main import mxapp_smartplus_android_common
from xml_utils import generate_string_res

string_excel_file = "code_string_translation.xls"

sheet = pandas.read_excel(io=string_excel_file)

columns = sheet.columns.values
all_string_list = []
for idx, row in sheet.iterrows():
    module_name = ""
    android_id_str = ""
    chinese_str = ""
    default_lang_str = ""
    english_us = ""
    spanish_str = ""
    germany_str = ""
    french_str = ""
    russia_str = ""
    korean_str = ""
    japan_str = ""
    for column in columns:
        if "功能模块" == column:
            module_name = row[column]
        if "android 资源id" == column:
            android_id_str = row[column]
        if "中文" == column:
            chinese_str = row[column]
        if "默认语言" == column:
            default_lang_str = row[column]
        if "美式英语" == column:
            english_us = row[column]
        if "西班牙语" == column:
            spanish_str = row[column]
        if "德语" == column:
            germany_str = row[column]
        if "法语" == column:
            french_str = row[column]
        if "俄罗斯语" == column:
            russia_str = row[column]
        if "韩语" == column:
            korean_str = row[column]
        if "日语" == column:
            japan_str = row[column]

    taileString = TaileString(module_name, android_id=android_id_str, simplified_chinese=chinese_str,
                              default_lang=default_lang_str,
                              english_us=english_us, spanish=spanish_str, germany=germany_str,
                              french=french_str, russia=russia_str, korean=korean_str, japan=japan_str)
    all_string_list.append(taileString)

all_string_module_dict = dict()
page_start_module_list = []
page_ota_module_list = []
page_message_module_list = []
page_scene_module_list = []
page_me_module_list = []
page_account_module_list = []
page_device_add_module_list = []
page_device_add_sdk_module_list = []
page_device_account_module_list = []
page_device_module_list = []
page_share_module_list = []
mxchip_component_module_list = []
ilop_component_module_list = []
mxapp_smartplus_android_common_module_list = []
module_name_list = ["page-start", "page-scene",
                    "page-ota", "page-message", "page-me",
                    "page-device-add", "page-device-add-sdk",
                    "page-account", "page-device",
                    "mxchip-component", "ilop-component",
                    "page-share", mxapp_smartplus_android_common
                    ]
for string_list in all_string_list:
    if string_list.module_name.__eq__("page-start"):
        page_start_module_list.append(string_list)
    if string_list.module_name.__eq__("page-ota"):
        page_ota_module_list.append(string_list)
    if string_list.module_name.__eq__("page-me"):
        page_me_module_list.append(string_list)
    if string_list.module_name.__eq__("page-scene"):
        page_scene_module_list.append(string_list)
    if string_list.module_name.__eq__("page-device-add"):
        page_device_add_module_list.append(string_list)
    if string_list.module_name.__eq__("page-device-add-sdk"):
        page_device_add_sdk_module_list.append(string_list)
    if string_list.module_name.__eq__("page-message"):
        page_message_module_list.append(string_list)
    if string_list.module_name.__eq__("page-account"):
        page_account_module_list.append(string_list)
    if string_list.module_name.__eq__("page-device"):
        page_device_module_list.append(string_list)
    if string_list.module_name.__eq__("page-share"):
        page_share_module_list.append(string_list)
    if string_list.module_name.__eq__("ilop-component"):
        ilop_component_module_list.append(string_list)
    if string_list.module_name.__eq__("mxchip-component"):
        mxchip_component_module_list.append(string_list)
    if string_list.module_name.__eq__(mxapp_smartplus_android_common):
        mxapp_smartplus_android_common_module_list.append(string_list)

simplified_chinese_dict = {}
for page_start_string in page_start_module_list:
    print("==========   dddd  " + page_start_string.simplified_chinese)
    simplified_chinese_dict[page_start_string.android_id] = page_start_string.simplified_chinese

generate_string_res(simplified_chinese_dict,"pagge_start", file_name="string.xml")
