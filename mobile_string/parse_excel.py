import os

import pandas

from Taile_String import TaileString
from read_ini_utils import get_language_key_list, get_language_dir_list, get_chinese_title_list, \
    get_language_chinese_title_key_list, get_chinese_title, get_parse_string_type
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
        #  我要遍历一行的每个列里的数据,
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
        trimmed_ios_id = str(ios_id_str).strip().replace("\n", "")
        string_type_list = get_parse_string_type()
        for string_type in string_type_list:
            trimmed_id_list = []
            string_type_str = str(string_type).lower()
            if string_type_str == "android":
                trimmed_id_list = trimmed_android_id.split("&")
            elif string_type_str == "ios":
                trimmed_id_list = trimmed_ios_id.split("&")

            print("trimmed_id_list = ")
            if len(trimmed_id_list) == 0:
                break

            for module_res_id_item in trimmed_id_list:
                if module_res_id_item == "":
                    continue
                print("------------- string_type_str = %s module_res_id_item = %s " % (
                    string_type_str, module_res_id_item))
                module_id_group = module_res_id_item.split("#")
                taileString: TaileString
                if len(module_id_group) == 1:
                    string_id = module_id_group[0]
                    if string_type_str == "android":
                        taileString = TaileString("android_app", android_id=string_id,
                                                  simplified_chinese=chinese_simple_str,
                                                  default_lang=default_lang_str,
                                                  english_us=english_us,
                                                  )
                        taileString.__dict__.update(language_map)
                        list.append(taileString)
                    elif string_type_str == "ios":
                        taileString = TaileString("ios_app", ios_id=string_id,
                                                  simplified_chinese=chinese_simple_str,
                                                  default_lang=default_lang_str,
                                                  english_us=english_us,
                                                  )
                        taileString.__dict__.update(language_map)
                        list.append(taileString)
                elif len(module_id_group) == 2:

                    string_module = module_id_group[0]
                    string_id = module_id_group[1]
                    if string_type_str == "android":
                        taileString = TaileString(string_module, android_id=string_id,
                                                  simplified_chinese=chinese_simple_str,
                                                  default_lang=default_lang_str,
                                                  english_us=english_us,
                                                  )
                        taileString.__dict__.update(language_map)
                        list.append(taileString)
                    elif string_type_str == "ios":
                        taileString = TaileString(string_module, ios_id=string_id,
                                                  simplified_chinese=chinese_simple_str,
                                                  default_lang=default_lang_str,
                                                  english_us=english_us,
                                                  )
                        taileString.__dict__.update(language_map)
                        list.append(taileString)

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


def get_mobile_string_by_type(string_list: list, string_type: str) -> list:
    """
    获取 android 的字符串
    :param string_type:
    :param string_list:
    :return:
    """
    print("module_name_list_a = len(string_list) = ", len(string_list))
    print("module_name_list_a = string_type = ", string_type)

    temp_module_name_list = []
    if str(string_type) == "android":
        for string in string_list:
            if str(string.android_id) != "":
                temp_module_name_list.append(string)
    elif str(string_type) == "ios":
        for string in string_list:
            if str(string.ios_id) != "":
                temp_module_name_list.append(string)
    module_name_list_a = list(set(temp_module_name_list))
    print("module_name_list_a = len(module_name_list_a) = ", len(module_name_list_a))
    return module_name_list_a


def generate_ios_res(string_dict: dict, filePath: str, file_name: str):
    is_not_empty = False
    for value in string_dict.values():
        if value is not "":
            is_not_empty = True
    """
    如果 这个 map 里面的 每一个 key 对应的 value 都是空的, 那么就表示不需要写这个语言的文件。
    """
    if not is_not_empty:
        return
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    with open(filePath + file_name, mode="w+") as f:
        for ios_string_key in string_dict.keys():
            if ios_string_key == "":
                continue
            ios_string = string_dict[ios_string_key]
            if ios_string == "":
                continue
            print("ios_string_key = ", ios_string_key)
            #  去掉左右两边的引号
            ios_string_key = str(ios_string_key).replace("\"", "")

            string_line = "\"" + ios_string_key + "\"" + " = " + "\"" + ios_string + "\";\n"
            f.write(string_line)


def generate_module_string_to_ios_file(module_name, module_string_list, xml_file_name="Localizable.strings"):
    module_name_path = "./ios_app/" + module_name

    lang_key_list = get_language_key_list()

    all_language_dict = {}
    # 遍历所需要的语言列表
    for language_key in lang_key_list:
        string_dict = {}
        for taile_string in module_string_list:
            print("============ page_start_string  = ", taile_string)
            if taile_string.module_name == module_name:
                # 获取需要需要的属性对应的语言字符串
                try:
                    string_dict[taile_string.ios_id] = getattr(taile_string, language_key)
                except AttributeError:
                    print("there is no attribute %s for object %s = " % (language_key, taile_string))

        all_language_dict[language_key] = string_dict

    if len(all_language_dict) != 0:
        trimmed_string_dict = {}

        for language_key, str_dict in all_language_dict.items():
            # 1 表示 iOS 的路径， 0 表示 Android 的路径
            ios_dir = str(get_language_dir_list(language_key)[1]).replace("\n", "").strip()
            if len(str_dict) == 0:
                continue
            for stringA in str_dict.keys():
                value = str_dict[stringA]
                if value != "":
                    trimmed_string_dict[stringA] = value
                print("--------------- string_dict[stringA] ", )
            if len(trimmed_string_dict) != 0:
                generate_ios_res(str_dict, module_name_path + "/" + ios_dir + "/",
                                 file_name=xml_file_name)


def generate_module_string_to_xml(module_name, module_string_list, xml_file_name="strings.xml"):
    """
    生成单个模块的字符串到 strings.xml 文件
    :param xml_file_name:   写入到文件名称
    :param module_name:  模块名称
    :param module_string_list: 这个模块的字符串 list
    :return:
    """
    module_name_path = "./android_app/" + module_name
    print("generate_module_string_to_xml: module_name_path = ", module_name_path)
    lang_key_list = get_language_key_list()

    all_language_dict = {}
    # 遍历所需要的语言列表
    for language_key in lang_key_list:
        string_dict = {}
        for taile_string in module_string_list:
            print("============ page_start_string  = ", taile_string)
            if taile_string.module_name == module_name:
                # 获取需要需要的属性对应的语言字符串
                try:
                    string_dict[taile_string.android_id] = getattr(taile_string, language_key)
                except AttributeError:
                    print("there is no attribute %s for object %s = " % (language_key, taile_string))
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


def generate_string_file(string_list: list):
    string_type_list = get_parse_string_type()

    for string_type in string_type_list:
        if str(string_type) == "android":
            android_string_list = get_mobile_string_by_type(string_list, str(string_type))
            android_module_name_list = []
            for android_string in android_string_list:
                android_module_name_list.append(android_string.module_name)

            print("=============== android_string_list.size = ", len(android_string_list))
            module_list = list(set(android_module_name_list))
            for module_name_A in module_list:
                generate_module_string_to_xml(module_name_A, android_string_list, )
        if str(string_type).lower() == "ios":
            ios_string_list = get_mobile_string_by_type(string_list, str(string_type))
            ios_module_name_list = []

            for ios_string in ios_string_list:
                ios_module_name_list.append(ios_string.module_name)
            module_list = list(set(ios_module_name_list))
            print("=============== module_list.size = ", len(module_list))

            for module_name_A in module_list:
                generate_module_string_to_ios_file(module_name_A, ios_string_list, )


if __name__ == "__main__":
    all_string_list = parse_excel_file()
    generate_string_file(all_string_list)
