import os

import chardet

from google_trans_api import translate, translate_text
from mobile_string import MobileString
from parse_android_string import android_app_project_path
from read_ini_utils import get_android_strings_files, get_android_project_path, get_target_languages
from xml_utils import pretty_xml_to_file
import xml.etree.cElementTree as ElementTree

"""
只获取该项目的英文翻译的字段和中文翻译的字段, 然后基于英文和中文去对比和比较
"""
android_app_project_path = get_android_project_path()


def get_all_files_list(path: str, all_file_list: list) -> list:
    app_file = os.walk(path)
    print("=========== file_full_path file_list app_file = ", app_file)
    print("=========== file_full_path file_list path = ", path)
    for parent, dir_list, file_list in os.walk(path):
        for file in file_list:
            file_path_a = os.path.join(parent, file)
            all_file_list.append(file_path_a)
    return all_file_list


def remove_duplicate(list1) -> list:
    return list(set(list1))


def get_all_strings_file(module_name, module_string_path):
    """

    根据模块名和项目路径, 获得该模块的 Localizable.strings 文件
    :param module_name:
    :param module_string_path:
    :return:
    """
    """
        过滤出所有的符合条件的 strings 文件
    :return:
    """
    print("the all strings file of ios project: ", str(module_string_path + os.sep + module_name))

    file_list = remove_duplicate(get_all_files_list(module_string_path + os.sep + module_name, []))
    ios_string_list = list(filter(lambda x: str(x).endswith("strings.xml") or str(x).endswith("string.xml"),
                                  file_list))
    print("the all strings file of ios project: ", len(ios_string_list))
    return ios_string_list


def get_filtered_strings_file(module_name, module_string_path):
    all_string_list = get_all_strings_file(module_name, module_string_path)
    wanted_file_list = get_android_strings_files()
    print("get_filtered_strings_file, all_string_list ", len(all_string_list))
    print("get_filtered_strings_file, wanted_file_list ", len(wanted_file_list))
    filtered_file_list = []

    if len(wanted_file_list) == 0:
        filtered_file_list = all_string_list
    else:
        for all_string_file in all_string_list:
            print("========= all_string_file ", all_string_file)
            for string_file in wanted_file_list:
                if str(all_string_file).endswith(string_file):
                    filtered_file_list.append(all_string_file)
    print("the quantity of ios string file that we want: ", len(filtered_file_list))
    return filtered_file_list


def get_all_module_name():
    """
    根据目录获取该项目的所有的项目
    :return:
    """
    string_dir = os.listdir(android_app_project_path)
    list_a = []
    for dir1 in string_dir:
        isDir = os.path.isdir(android_app_project_path + os.sep + dir1)
        print("get_all_module_name = ", dir1)
        if isDir:
            list_a.append(dir1)
    return list_a


string_file_dict = {}


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']


def read_strings_from_file(module_name: str, file_path):
    android_string_list = []
    encoding = get_encoding(file_path)
    print("read_strings_from_file: encoding = ", encoding, " file_path " + file_path)
    print("read_strings_from_file: encoding = ", encoding, " file_path " + android_app_project_path)
    """
    这些 Windows-1254 和 EUC-TW 编码统一归为 UTF-8 编码
    """
    if encoding == "Windows-1254" or encoding == "EUC-TW":
        encoding = "utf-8"
    relative_file_path = file_path.split(android_app_project_path)[1]
    if str(relative_file_path).startswith("/"):
        relative_file_path = str(relative_file_path).lstrip("/")
    if str(relative_file_path).startswith("/"):
        relative_file_path = str(relative_file_path).lstrip("/")
    print("read_strings_from_file: encoding = ", encoding, " relative_file_path " + relative_file_path)
    single_xml_file_string_dict = {}
    print("read_strings_from_file: xml_file = " + str(file_path))
    xml_file_doc = ElementTree.parse(file_path)

    for child in xml_file_doc.getroot():
        if str(child.tag).__eq__("string-array"):
            string_array_item_list = []
            for string_array_item in child.iter():
                string_array_item_list.append(string_array_item.text)
            single_xml_file_string_dict[child.attrib["name"]] = "|".join(string_array_item_list)

        else:
            string_name_id = child.attrib["name"]
            string_name_value = child.text
            if string_name_value is None:
                string_name_value = ""
            if relative_file_path.__contains__("values-zh-rCN") \
                    or relative_file_path.__contains__("/res/values/"):
                android_string = MobileString(module_name, string_id=string_name_id,
                                              zh_cn=string_name_value, is_android_string=True,
                                              zh_cn_file=relative_file_path)
                android_string_list.append(android_string)

            if relative_file_path.__contains__("values-de-rDE"):
                android_string = MobileString(module_name, string_id=string_name_id,
                                              germany=string_name_value, is_android_string=True,
                                              germany_file=relative_file_path)
                android_string_list.append(android_string)

            if relative_file_path.__contains__("values-fr-rFR"):
                android_string = MobileString(module_name, string_id=string_name_id,
                                              french=string_name_value, is_android_string=True,
                                              french_file=relative_file_path)
                android_string_list.append(android_string)

            if relative_file_path.__contains__("values-es-rES"):
                android_string = MobileString(module_name, string_id=string_name_id,
                                              spanish=string_name_value, is_android_string=True,
                                              spanish_file=relative_file_path)
                android_string_list.append(android_string)

            if relative_file_path.__contains__("values-de-rDE"):
                android_string = MobileString(module_name, string_id=string_name_id,
                                              germany=string_name_value, is_android_string=True,
                                              germany_file=relative_file_path)
                android_string_list.append(android_string)

            if relative_file_path.__contains__("values-ja-rJP"):
                android_string = MobileString(module_name, string_id=string_name_id,
                                              japan=string_name_value, is_android_string=True,
                                              japan_file=relative_file_path)
                android_string_list.append(android_string)

            if relative_file_path.__contains__("values-ko-rKR"):
                android_string = MobileString(module_name, string_id=string_name_id,
                                              korean=string_name_value, is_android_string=True,
                                              korean_file=relative_file_path)
                android_string_list.append(android_string)

            if relative_file_path.__contains__("values-en-rUS"):
                android_string = MobileString(module_name, string_id=string_name_id,
                                              english_us=string_name_value, is_android_string=True,
                                              english_us_file=relative_file_path)
                android_string_list.append(android_string)

            if relative_file_path.__contains__("values-ru-rRU"):
                android_string = MobileString(module_name, string_id=string_name_id,
                                              russia=string_name_value, is_android_string=True,
                                              russia_file=relative_file_path)
                android_string_list.append(android_string)
    return android_string_list


def merge_mobile_string_object(cache_string: MobileString, append_string: MobileString):
    """
    合并字符串, 强制规定 append_string 是合并到 cache_string 的
    :param cache_string:
    :param append_string:
    :return:
    """
    if cache_string.string_id is None:
        if append_string.string_id != "":
            cache_string.string_id = append_string.string_id
    if cache_string.zh_cn == "":
        if append_string.zh_cn != "":
            cache_string.zh_cn = append_string.zh_cn
            cache_string.zh_cn_file = append_string.zh_cn_file
    if cache_string.russia == "":
        if append_string.russia != "":
            cache_string.russia = append_string.russia
            cache_string.russia_file = append_string.russia_file
    if cache_string.germany == "":
        if append_string.germany != "":
            cache_string.germany = append_string.germany
            cache_string.germany_file = append_string.germany_file

    if cache_string.english_us == "":
        if append_string.english_us != "":
            cache_string.english_us = append_string.english_us
            cache_string.english_us_file = append_string.english_us_file

    if cache_string.korean == "":
        if append_string.korean != "":
            cache_string.korean = append_string.korean
            cache_string.korean_file = append_string.korean_file

    if cache_string.japan == "":
        print(" append_string.japan  = ", append_string.japan)
        if append_string.japan != "":
            cache_string.japan = append_string.japan
            cache_string.japan_file = append_string.japan_file

    if cache_string.french == "":
        if append_string.french != "":
            cache_string.french = append_string.french
            cache_string.french_file = append_string.french_file

    if cache_string.spanish == "":
        if append_string.spanish != "":
            cache_string.spanish = append_string.spanish
            cache_string.spanish_file = append_string.spanish_file

    return cache_string


def divide_string_dict_by_file(string_dict: dict) -> dict:
    """
    将 android 的字符串 按照所要写的路径, 重新划分一下, 这样就可以一次性写一个文件
    :param string_dict:
    :return:
    """
    string_by_file_dict = {}
    # global zh_cn_lang_file_list
    for mobile_string_id in string_dict.keys():
        mobileString: MobileString = string_dict.get(mobile_string_id)
        if mobileString is None:
            continue
        print("lang_file_l ist mobileString =", mobileString)
        if mobileString.zh_cn_file != "":
            # try:
            zh_cn_lang_file_list = string_by_file_dict.get(mobileString.zh_cn_file)
            # except KeyError:
            #     zh_cn_lang_file_list = []
            if zh_cn_lang_file_list is None:
                zh_cn_lang_file_list = []

            zh_cn_lang_file_list.append(mobileString)
            string_by_file_dict[mobileString.zh_cn_file] = zh_cn_lang_file_list
            # lang_file_list.clear()

        if mobileString.english_us_file != "":
            lang_file_list = string_by_file_dict.get(mobileString.english_us_file)
            if lang_file_list is None:
                lang_file_list = []
            lang_file_list.append(mobileString)
            string_by_file_dict[mobileString.english_us_file] = lang_file_list
            # lang_file_list.clear()

        if mobileString.spanish_file != "":
            lang_file_list = string_by_file_dict.get(mobileString.spanish_file)
            if lang_file_list is None:
                lang_file_list = []
            lang_file_list.append(mobileString)
            string_by_file_dict[mobileString.spanish_file] = lang_file_list
            # lang_file_list.clear()

        if mobileString.french_file != "":
            lang_file_list = string_by_file_dict.get(mobileString.french_file)
            if lang_file_list is None:
                lang_file_list = []
            lang_file_list.append(mobileString)
            string_by_file_dict[mobileString.french_file] = lang_file_list
            # lang_file_list.clear()

        if mobileString.russia_file != "":
            lang_file_list = string_by_file_dict.get(mobileString.russia_file)
            if lang_file_list is None:
                lang_file_list = []
            string_by_file_dict[mobileString.russia_file] = lang_file_list.append(mobileString)
            # lang_file_list.clear()

        if mobileString.germany_file != "":
            lang_file_list = string_by_file_dict.get(mobileString.germany_file)
            if lang_file_list is None:
                lang_file_list = []
            string_by_file_dict[mobileString.germany_file] = lang_file_list.append(mobileString)
            # lang_file_list.clear()

        if mobileString.korean_file != "":
            lang_file_list = string_by_file_dict.get(mobileString.korean_file)
            if lang_file_list is None:
                lang_file_list = []
            lang_file_list.append(mobileString)
            string_by_file_dict[mobileString.korean_file] = lang_file_list
            # lang_file_list.clear()

        if mobileString.japan_file != "":
            lang_file_list = string_by_file_dict.get(mobileString.japan_file)
            if lang_file_list is None:
                lang_file_list = []
            lang_file_list.append(mobileString)
            string_by_file_dict[mobileString.japan_file] = lang_file_list
            # lang_file_list.clear()
    return string_by_file_dict


def get_android_string_dict_by_string_id() -> dict:
    """
    以 string_id 为 key 的 字符串 dict
    :return:
    """
    module_list = get_all_module_name()
    android_module_string_dict = {}
    print("the all ios module size is ", len(module_list))

    for module in module_list:
        print("the all ios module size is  module = ", module)
        string_file_list = get_filtered_strings_file(module, android_app_project_path)
        if len(string_file_list) == 0:
            continue
        module_string_list = []
        for file in string_file_list:
            list_c = read_strings_from_file(module, file)
            for c in list_c:
                module_string_list.append(c)

        print("the module_string_list size is, ", len(module_string_list))
        android_module_string_dict[module] = module_string_list
    print("the all ios module string dict is ", len(android_module_string_dict))
    string_dict_by_id = {}
    for module in android_module_string_dict.keys():
        for string in android_module_string_dict[module]:
            cache_string = string_dict_by_id.get(string.string_id)
            if cache_string is None:
                string_dict_by_id[string.string_id] = string
            else:
                merge_cache_string = merge_mobile_string_object(cache_string, string)
                string_dict_by_id[string.string_id] = merge_cache_string
    print("get_ios_string_dict_by_string_id, the all string is = ", len(string_dict_by_id))
    return string_dict_by_id


def get_ios_string_dict_by_module() -> dict:
    """
    通过模块把字符串划分开
    :return:
    """
    string_dict_by_id = get_android_string_dict_by_string_id()
    module_string_dict = {}
    for android_string_id in string_dict_by_id.keys():
        module = string_dict_by_id[android_string_id].module_name
        module_string_list_A = module_string_dict.get(module)
        if module_string_list_A is None:
            module_string_list_A = []
        module_string_dict[module] = module_string_list_A.append(string_dict_by_id[android_string_id])
    print("the all module string ", len(module_string_dict))

    return module_string_dict


def get_source_text(mobile_string: MobileString) -> str:
    """
    输入一个 mobilestring 对象, 选择合适的
    :param mobile_string:
    :return:
    """
    if mobile_string.zh_cn is not None and mobile_string.zh_cn != "":
        return mobile_string.zh_cn
    elif mobile_string.zh_tw is not None and mobile_string.zh_tw != "":
        return mobile_string.zh_tw
    elif mobile_string.english_us is not None and mobile_string.english_us != "":
        return mobile_string.english_us
    elif mobile_string.french is not None and mobile_string.french != "":
        return mobile_string.french
    elif mobile_string.spanish is not None and mobile_string.spanish != "":
        return mobile_string.spanish
    elif mobile_string.germany is not None and mobile_string.germany != "":
        return mobile_string.germany


def get_source_text_file_path(mobile_string: MobileString) -> str:
    """
    优先选择中文字符串的文件路径作为共同的路径, 以后会优化为该语言的读取的文件路径,如果没有才选择其他的语言
    :param mobile_string:
    :return:
    """
    full_file_path = ""
    if mobile_string.zh_cn is not None and mobile_string.zh_cn != "":
        full_file_path = mobile_string.zh_cn_file
    elif mobile_string.zh_tw is not None and mobile_string.zh_tw != "":
        full_file_path = mobile_string.zh_tw_file
    elif mobile_string.english_us is not None and mobile_string.english_us != "":
        full_file_path = mobile_string.english_us_file
    elif mobile_string.french is not None and mobile_string.french != "":
        full_file_path = mobile_string.french_file
    elif mobile_string.spanish is not None and mobile_string.spanish != "":
        full_file_path = mobile_string.spanish_file
    elif mobile_string.germany is not None and mobile_string.germany != "":
        full_file_path = mobile_string.germany_file
    if full_file_path == "":
        full_file_path = mobile_string.english_us_file

    if full_file_path.startswith("/"):
        full_file_path.lstrip("/")
    if full_file_path.startswith("/"):
        full_file_path.lstrip("/")
    return full_file_path


def get_common_string_file_path(mobile_string: MobileString) -> str:
    file_path = get_source_text_file_path(mobile_string)
    print("get_common_string_file_path: file_path = ", file_path)
    print("get_common_string_file_path: file_path = ", mobile_string)
    file_name = file_path.split("/")[-1]
    lang_dir = file_path.split("/")[-2]

    common_file_path = file_path.replace(lang_dir + "/" + file_name, "")
    print("get_common_string_file_path: common_file_path = ", common_file_path)
    if common_file_path.startswith("/"):
        common_file_path = common_file_path.lstrip("/")
    if common_file_path.startswith("/"):
        common_file_path = common_file_path.lstrip("/")
    if common_file_path.endswith("/"):
        common_file_path = common_file_path.rstrip("/")
    print("get_common_string_file_path: trimmed common_file_path = ", common_file_path)

    return common_file_path


def get_string_file_name(mobile_string: MobileString) -> str:
    """
    获取字符串的文件名称
    :param mobile_string:
    :return:
    """
    file_path = get_source_text_file_path(mobile_string)
    file_name = file_path.split("/")[-1]
    return file_name


def get_pending_translate_ios_string_dict() -> dict:
    string_dict_by_id = get_android_string_dict_by_string_id()
    for string_id in string_dict_by_id.keys():
        ios_string: MobileString = string_dict_by_id[string_id]
        print("get_pending_translate_ios_string_dict(), android_string = ", ios_string)
        if ios_string is None:
            continue
        if ios_string.string_id is None or ios_string.string_id == "":
            continue
        for target_lang in get_target_languages():
            common_file_path = get_common_string_file_path(ios_string)
            print("get_pending_translate_ios_string_dict: common_file_path = ", common_file_path)
            common_file_pat_with_sep = common_file_path + os.sep
            if common_file_path == "":
                common_file_pat_with_sep = ""
            file_name = get_string_file_name(ios_string)
            source_text = get_source_text(ios_string)
            print("get_pending_translate_ios_string_dict: source_text = ", source_text)
            if source_text is None:
                continue
            if target_lang == "ZH-CN":
                ios_string.english_us = translate(source_text, "en", "zh-CN")
                ios_string.zh_cn_file = common_file_path + os.sep + "values-zh-rCN" + os.sep + file_name
            if target_lang == "EN-US":
                ios_string.english_us = translate(source_text, "en", "zh-CN")
                ios_string.english_us_file = common_file_path + os.sep + "values-en-rUS" + os.sep + file_name
            if target_lang == "JA":
                ios_string.japan = translate_text(source_text, "JA", "zh-CN")
                ios_string.japan_file = common_file_pat_with_sep + "values-ja-rJP" + os.sep + file_name
            if target_lang == "KO":
                ios_string.korean = translate(source_text, "ko", "zh-CN")
                ios_string.korean_file = common_file_path + os.sep + "values-ko-rKR" + os.sep + file_name
            print("android_string  === ", ios_string)
        string_dict_by_id[string_id] = ios_string
    return string_dict_by_id


def generate_ios_res(string_dict: dict, target_language: str, filePath: str):
    suffix = filePath.split("/")[-1]
    file_path_dir = filePath.replace(suffix, "")
    print("=========== filePath ", filePath, ", suffix = ", suffix)
    print("=========== filePath ", filePath, ", target_language , ", target_language)
    print("=========== file_path_dir ", file_path_dir, ", target_language , ", target_language)
    if os.path.exists(file_path_dir):
        pass
    else:
        os.makedirs(name=file_path_dir)
    print("generate_ios_res: string_line: len(string_dict) = ", len(string_dict))

    with open(filePath, mode="w+") as f:
        for ios_string_key in string_dict.keys():
            print("generate_ios_res: string_line: ios_string_key = ", ios_string_key)
            if ios_string_key == "":
                continue
            string_value = string_dict[ios_string_key]
            print("generate_ios_res: string_line: target_language = ", target_language)

            if target_language == "JA":
                string_value_str = str(string_value.japan)
            if target_language == "EN-US":
                string_value_str = str(string_value.english_us)
            if target_language == "ZH-CN":
                string_value_str = str(string_value.zh_cn)
            if target_language == "KO":
                string_value_str = str(string_value.korean)
            if string_value_str == "":
                continue
            string_line = "\"" + ios_string_key + "\"" + " = " + "\"" + string_value_str + "\";\n"
            print("generate_ios_res: string_line: string_line = ", string_line)
            f.write(string_line)


def generate_android_res(string_value_dict: dict, target_language: str, save_str_file_path: str):
    """
    将 android 的字符串 写成 android的 strings.xml 的格式
    如何生成这些 android 的字符串,将这些字符串按照不同的语言, 不同模块再次划分一下, 比较好, 也就是写到同一个文件里的, 放到一个 dict 里面
    """
    from xml.etree.ElementTree import Element, SubElement, ElementTree
    print("generate_android_res save_str_file_path = " + str(save_str_file_path))
    file_name = save_str_file_path.split("/")[-1]
    file_path_dir = save_str_file_path.replace(file_name, "")
    if os.path.exists(file_path_dir):
        pass
    else:
        os.makedirs(name=file_path_dir)
    root = Element('resources')
    # 生成第一个子节点 head]
    print("string_value_dict = " + str(string_value_dict))
    for name_key in string_value_dict:
        string_value: MobileString = string_value_dict[name_key]
        if string_value is None:
            print("string_value is nan = ", string_value)
        string_value_str = str(string_value.english_us)
        if target_language == "JA":
            string_value_str = str(string_value.japan)
        if target_language == "EN-US":
            string_value_str = str(string_value.english_us)
        if target_language == "ZH-CN":
            string_value_str = str(string_value.zh_cn)
        if target_language == "KO":
            string_value_str = str(string_value.korean)
        if string_value_str == "":
            continue

        head = SubElement(root, 'string')
        head.attrib["name"] = name_key
        head.text = string_value_str
    tree = ElementTree(root)
    tree.write(save_str_file_path, encoding='utf-8')
    pretty_xml_to_file(save_str_file_path, "./")


if __name__ == '__main__':
    pending_translation_ios_string_dict = get_pending_translate_ios_string_dict()
    divider_by_file = divide_string_dict_by_file(pending_translation_ios_string_dict)
    print("=================== len(divider_by_file) = ", len(divider_by_file))
    for file_key in divider_by_file.keys():
        print("================ file_key = ", file_key)
        string_list = divider_by_file.get(file_key)
        print("================ len(string_list) = ", len(string_list))

        string_list_dict = {}
        if string_list is None:
            continue
        if len(string_list) == 0:
            continue
        """
        重新规整一下字符串, 放在字典里面
        """

        for string in string_list:
            string_list_dict[string.string_id] = string
        for target_lang in get_target_languages():
            if target_lang == "ZH-CN":
                if str(file_key).__contains__("values-zh-rCN"):
                    generate_android_res(string_list_dict, "ZH-CN", file_key)
            if target_lang == "EN-US":
                if str(file_key).__contains__("values-en-rUS"):
                    generate_android_res(string_list_dict, "EN-US", file_key)
            if target_lang == "JA":
                if str(file_key).__contains__("values-ja-rJP"):
                    generate_android_res(string_list_dict, "JA", file_key)
            if target_lang == "KO":
                if str(file_key).__contains__("values-ko-rKR"):
                    generate_android_res(string_list_dict, "KO", file_key)
