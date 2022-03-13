import os

import pandas

from Taile_String import TaileString
from read_ini_utils import get_language_key_list, get_language_dir_list, get_chinese_title_list, \
    get_language_chinese_title_key_list, get_chinese_title
from xml_utils import generate_android_res
from ios_string import IOS_String

string_excel_file = "Android_ios_megered_string_001.xls"


def parse_excel_file():
    if not os.path.exists(string_excel_file):
        print("请先用 parse_app_project_string 程序生成 相应格式化的 excel 表格")
        return
    if not os.path.isfile(string_excel_file):
        print("code_string_translation_01.xls 不是一个文件")
        return

    sheet = pandas.read_excel(io=string_excel_file)

    columns = sheet.columns.values
    list = []
    for idx, row in sheet.iterrows():
        module_name = ""
        android_id_str = ""
        chinese_str = ""
        default_lang_str = ""
        chinese_simple_str = ""
        ios_id_str = ""
        english_us = ""

        language_map = dict()
        for column in columns:
            column_value = row[column]
            column_title = str(column)
            print("column_value = " + str(column_value))
            if pandas.isna(column_value):
                print("the column value is nan, we set the nan to space")

                column_value = ""
            if "原中文字符串" == column:
                module_name = column_value
            if "android 模块和资源id" == column:
                android_id_str = column_value
            if "中文（简体)" == column:
                chinese_simple_str = column_value
            if "ios 模块和资源id" == column:
                ios_id_str = column_value
            if "英语" == column:
                english_us = column_value
            for chinese_title in get_chinese_title_list():
                if column_title.__contains__(chinese_title):
                    for language_key in get_language_chinese_title_key_list():
                        if get_chinese_title(language_key) == chinese_title:
                            print("the language_key = %s, chinese_title = %s, the content is = %s" % (
                                language_key, chinese_title, column_value))
                            language_map[language_key] = column_value

        trimmed_android_id = str(android_id_str).strip().replace("\n", "")
        if trimmed_android_id != "":
            trimmed_android_id_list = trimmed_android_id.split("&")
            for android_module_res_id_item in trimmed_android_id_list:
                if android_module_res_id_item == "":
                    continue
                print("-------------  android_module_res_id_item = ", android_module_res_id_item)
                android_module = android_module_res_id_item.split("#")[0]
                android_id = android_module_res_id_item.split("#")[1]
                taileString = TaileString(android_module, android_id=android_id,
                                          simplified_chinese=chinese_simple_str,
                                          default_lang=default_lang_str,
                                          english_us=english_us,
                                          )
                taileString.__dict__.update(language_map)
                list.append(taileString)

        trimmed_ios_id = str(ios_id_str).strip().replace("\n", "")

        if trimmed_ios_id != "":
            trimmed_ios_id_list = trimmed_ios_id.split("&")
            for module_res_id_item in trimmed_ios_id_list:
                if module_res_id_item == "":
                    continue
                print("-------------  hello = ", module_res_id_item)
                module_name = module_res_id_item.split("#")[0]
                ios_id = module_res_id_item.split("#")[1]
                ios_string = IOS_String(value=english_us, string_id=ios_id, module_name=module_name, file_name="",
                                        chinese_simple_str=chinese_simple_str)
                list.append(ios_string)
    return list


"""
根据模块的名称动态的生成变量名称:
形如 page_start_string_list
"""


def get_module_string(module_name: str, string_list: list):
    single_module_list = []
    print("string_list = " + str(string_list))
    for string in string_list:
        if string is not None and string.module_name.__eq__(module_name):
            single_module_list.append(string)
    return single_module_list


def get_android_string(string_list: list) -> list:
    """
    获取 android 的字符串
    :param string_list:
    :return:
    """
    temp_module_name_list = []
    for string in string_list:
        if type(string) is TaileString:
            temp_module_name_list.append(string)
    module_name_list_a = list(set(temp_module_name_list))
    return module_name_list_a


def get_ios_string(string_list: list) -> list:
    """
    获取 ios 的字符串
    :param string_list:
    :return:
    """
    temp_module_name_list = []
    for string in string_list:
        if type(string) is IOS_String:
            temp_module_name_list.append(string)
    module_name_list_a = list(set(temp_module_name_list))
    return module_name_list_a


def generate_ios_res(string_dict: dict, filePath: str, file_name: str):
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    with open(filePath + file_name, mode="w+") as f:
        for ios_string_key in string_dict.keys():
            if ios_string_key == "":
                continue
            ios_string = string_dict[ios_string_key]
            if ios_string == "":
                continue
            string_line = "\"" + ios_string_key + "\"" + " = " + "\"" + ios_string + "\";\n"
            f.write(string_line)


def generate_module_string_to_ios_file(module_name, module_string_list, xml_file_name="Localizable.strings"):
    module_name_path = "./ios_app/" + module_name
    string_dict = {}

    #  获取简体中文的字符串
    for taile_string in module_string_list:
        print("============ page_start_string  = ", taile_string)
        if taile_string.module_name == module_name:
            # 获取需要需要的属性
            lang_key_list = get_language_key_list()
            for language_key in lang_key_list:
                string_dict[taile_string.string_id] = getattr(taile_string, language_key)
    print(" simplified_chinese_dict = " + str(len(string_dict)))
    if len(string_dict) != 0:
        trimmed_string_dict = {}
        for stringA in string_dict.keys():
            value = string_dict[stringA]
            if value != "":
                trimmed_string_dict[stringA] = value
            print("--------------- string_dict[stringA] ", )
        if len(trimmed_string_dict) != 0:
            generate_ios_res(string_dict,
                             module_name_path + "/" + "zh.proj" + "/",
                             file_name=xml_file_name)

    string_dict.clear()


def generate_module_string_to_xml(module_name, module_string_list, xml_file_name="strings.xml"):
    """
    生成单个模块的字符串到 strings.xml 文件
    :param xml_file_name:   写入到文件名称
    :param module_name:  模块名称
    :param module_string_list: 这个模块的字符串 list
    :return:
    """
    module_name_path = "./android_app/" + module_name

    lang_key_list = get_language_key_list()

    all_language_dict = {}
    # 遍历所需要的语言列表
    for language_key in lang_key_list:
        string_dict = {}
        for taile_string in module_string_list:
            print("============ page_start_string  = ", taile_string)
            if taile_string.module_name == module_name:
                # 获取需要需要的属性对应的语言字符串
                string_dict[taile_string.android_id] = getattr(taile_string, language_key)
        all_language_dict[language_key] = string_dict

    if len(all_language_dict) != 0:
        trimmed_string_dict = {}

        for language_key, str_dict in all_language_dict.items():
            android_dir = str(get_language_dir_list(language_key)[0]).replace("\n", "").strip()
            if len(str_dict) == 0:
                continue
            for stringA in str_dict.keys():
                value = str_dict[stringA]
                if value != "":
                    trimmed_string_dict[stringA] = value
                print("--------------- string_dict[stringA] ", )
            if len(trimmed_string_dict) != 0:
                generate_android_res(str_dict, module_name_path + "/src/main/res/" + android_dir,
                                     file_name=xml_file_name)


if __name__ == "__main__":
    all_string_list = parse_excel_file()

    android_string_list = get_android_string(all_string_list)
    android_module_name_list = []
    for android_string in android_string_list:
        android_module_name_list.append(android_string.module_name)

    print("=============== android_string_list.size = ", len(android_string_list))
    module_list = list(set(android_module_name_list))
    for module_name_A in module_list:
        generate_module_string_to_xml(module_name_A, android_string_list, )
    # ios_string_list = get_ios_string(all_string_list)
    # ios_module_name_list = []
    # for ios_string in ios_string_list:
    #     ios_module_name_list.append(ios_string.module_name)
    # module_list = list(set(ios_module_name_list))
    # for module_name_A in module_list:
    #     generate_module_string_to_ios_file(module_name_A, ios_string_list, )
