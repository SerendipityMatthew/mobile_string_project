import os

import pandas

from Taile_String import TaileString
from xml_utils import generate_string_res

string_excel_file = "code_string_translation.xls"


def parse_excel_file():
    if not os.path.exists(string_excel_file):
        print("请先用 parse_app_project_string 程序生成 相应格式化的 excel 表格")
        return
    if not os.path.isfile(string_excel_file):
        print("code_string_translation.xls 不是一个文件")
        return

    sheet = pandas.read_excel(io=string_excel_file)

    columns = sheet.columns.values
    list = []
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
            column_value = row[column]
            print("column_value = " + str(column_value))
            if pandas.isna(column_value):
                print("the column value is nan, we set the nan to space")

                column_value = ""
            if "功能模块" == column:
                module_name = column_value
            if "android 资源id" == column:
                android_id_str = column_value
            if "中文" == column:
                chinese_str = column_value
            if "默认语言" == column:
                default_lang_str = column_value
            if "美式英语" == column:
                english_us = column_value
            if "西班牙语" == column:
                spanish_str = column_value
            if "德语" == column:
                germany_str = column_value
            if "法语" == column:
                french_str = column_value
            if "俄罗斯语" == column:
                russia_str = column_value
            if "韩语" == column:
                korean_str = column_value
            if "日语" == column:
                japan_str = column_value

        taileString = TaileString(module_name, android_id=android_id_str, simplified_chinese=chinese_str,
                                  default_lang=default_lang_str,
                                  english_us=english_us, spanish=spanish_str, germany=germany_str,
                                  french=french_str, russia=russia_str, korean=korean_str, japan=japan_str)
        list.append(taileString)
    return list


"""
根据模块的名称动态的生成变量名称:
形如 page_start_string_list
"""

import parse_module

module_name_list = parse_module.get_app_project_module()
all_string_list = parse_excel_file()

for taile_string in all_string_list:
    print(taile_string)


def get_module_string(module_name: str, string_list: list):
    single_module_list = []
    print("string_list = " + str(string_list))
    for string in string_list:
        if string.module_name.__eq__(module_name):
            single_module_list.append(string)
    return single_module_list


def parse_all_string_list():
    for module_name in module_name_list:
        get_module_string(module_name, all_string_list)


def generate_module_string_to_xml(module_name, module_string_list, xml_file_name="strings.xml"):
    """
    生成单个模块的字符串到 strings.xml 文件
    :param xml_file_name:   写入到文件名称
    :param module_name:  模块名称
    :param module_string_list: 这个模块的字符串 list
    :return:
    """
    module_name = parse_module.project_name + os.sep + "app" + os.sep + module_name

    string_dict = {}
    for page_start_string in module_string_list:
        string_dict[page_start_string.android_id] = page_start_string.simplified_chinese
    print(" simplified_chinese_dict = " + str(string_dict.__len__()))
    if string_dict.__len__() != 0:
        generate_string_res(string_dict, module_name + "/src/main/res/" + "values-zh-rCN",
                            file_name=xml_file_name)

    string_dict.clear()

    for page_start_string in module_string_list:
        string_dict[page_start_string.android_id] = page_start_string.english_us
    if string_dict.__len__() != 0:
        generate_string_res(string_dict, module_name + "/src/main/res/" + "values-en-rUS",
                            file_name=xml_file_name)

    string_dict.clear()
    for page_start_string in module_string_list:
        string_dict[page_start_string.android_id] = page_start_string.korean
    if string_dict.__len__() != 0:
        generate_string_res(string_dict, module_name + "/src/main/res/" + "values-ko-rKR",
                            file_name=xml_file_name)

    string_dict.clear()
    for page_start_string in module_string_list:
        string_dict[page_start_string.android_id] = page_start_string.japan
    if string_dict.__len__() != 0:
        generate_string_res(string_dict, module_name + "/src/main/res/" + "values-ja-rJP",
                            file_name=xml_file_name)

    string_dict.clear()
    for page_start_string in module_string_list:
        string_dict[page_start_string.android_id] = page_start_string.germany

    if string_dict.__len__() != 0:
        generate_string_res(string_dict, module_name + "/src/main/res/" + "values-de-rDE",
                            file_name=xml_file_name)

    string_dict.clear()
    for page_start_string in module_string_list:
        string_dict[page_start_string.android_id] = page_start_string.french
    if string_dict.__len__() != 0:
        generate_string_res(string_dict, module_name + "/src/main/res/" + "values-fr-rFR",
                            file_name=xml_file_name)

    string_dict.clear()
    for page_start_string in module_string_list:
        string_dict[page_start_string.android_id] = page_start_string.french
    if string_dict.__len__() != 0:
        generate_string_res(string_dict, module_name + "/src/main/res/" + "values-ru-rRU",
                            file_name=xml_file_name)
    string_dict.clear()

    for page_start_string in module_string_list:
        string_dict[page_start_string.android_id] = page_start_string.spanish
    if string_dict.__len__() != 0:
        generate_string_res(string_dict, module_name + "/src/main/res/" + "values-es-rES",
                            file_name=xml_file_name)
    string_dict.clear()

    for page_start_string in module_string_list:
        string_dict[page_start_string.android_id] = page_start_string.default_lang
    if string_dict.__len__() != 0:
        generate_string_res(string_dict, module_name + "/src/main/res/" + "values", file_name=xml_file_name)


for name in module_name_list:
    module_string_list = get_module_string(name, all_string_list)
    generate_module_string_to_xml(name, module_string_list)
