import os

import chardet

from google_trans_api import translate, translate_text
from lang_string import LangString
from mobile_string import MobileString
from read_ini_utils import get_ios_strings_files, get_ios_project_path, get_target_languages

"""
只获取该项目的英文翻译的字段和中文翻译的字段, 然后基于英文和中文去对比和比较
"""
ios_app_project_path = get_ios_project_path()


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
    ios_string_list = list(filter(lambda x: str(x).endswith(".strings"),
                                  file_list))
    print("the all strings file of ios project: ", len(ios_string_list))
    return ios_string_list


def get_filtered_strings_file(module_name, module_string_path):
    all_string_list = get_all_strings_file(module_name, module_string_path)
    wanted_file_list = get_ios_strings_files()
    print("get_filtered_strings_file, wanted_file_list ", len(wanted_file_list))
    filtered_file_list = []

    if len(wanted_file_list) == 0:
        filtered_file_list = all_string_list
    else:
        for all_string_file in all_string_list:
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
    string_dir = os.listdir(ios_app_project_path)
    list_a = []
    for dir1 in string_dir:
        isDir = os.path.isdir(ios_app_project_path + os.sep + dir1)
        print("get_all_module_name = ", dir1)
        if isDir:
            list_a.append(dir1)
    return list_a


string_file_dict = {}


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']


def read_strings_from_file(module_name: str, file_path_a: str) -> list:
    ios_string_list = []
    encoding = get_encoding(file_path_a)
    print("read_strings_from_file: module_name = ", module_name, "file_path_a = ", file_path_a)
    """
    这些 Windows-1254 和 EUC-TW 编码统一归为 UTF-8 编码
    """
    if encoding == "Windows-1254" or encoding == "EUC-TW":
        encoding = "utf-8"
    relative_file_path = file_path_a.split(ios_app_project_path)[1]
    if str(relative_file_path).startswith("/"):
        relative_file_path = str(relative_file_path).lstrip("/")
    if str(relative_file_path).startswith("/"):
        relative_file_path = str(relative_file_path).lstrip("/")
    print("read_strings_from_file: encoding = ", encoding, " relative_file_path ", relative_file_path)
    relative_common_path_list = relative_file_path.split("/")[0:-2]
    file_name = relative_file_path.split("/")[-1]
    language_dir = relative_file_path.split("/")[-2]
    print("read_strings_from_file: encoding = ", encoding, " language_dir = ", language_dir)

    relative_common_path = ""

    if len(relative_common_path_list) != 0:
        for path in relative_common_path_list:
            relative_common_path += path + os.sep
    print("read_strings_from_file: encoding = ", encoding, " relative_common_path ", relative_common_path)

    with open(file=file_path_a, encoding=encoding) as f:
        file_string = f.readlines()

        for string_line in file_string:

            if string_line.strip().__eq__(""):
                continue
            if not string_line.startswith("\""):
                continue
            ios_string_id = ""
            ios_string_value = ""
            if str(string_line).__contains__(" = \""):  # "MXCHIP_upgrade_skip" = "暂不升级"; 类型的, 等号两端都有空格
                ios_string_id = string_line.split(" = \"")[0].replace("\"", "")
                ios_string_value = string_line.split("\" ")[1] \
                    .replace("= ", "") \
                    .replace(";", "") \
                    .replace("\"", "")
            if ios_string_id == "":
                if str(string_line).__contains__("\"=\""):  # "MXCHIP_upgrade_skip"="暂不升级"; 类型的 等号两端都没有空格
                    ios_string_id = string_line.split("\"=\"")[0].replace("\"", "")
                    ios_string_value = string_line.split("\"=\"")[1] \
                        .replace("= ", "") \
                        .replace(";", "").replace("\"", "")
            if ios_string_id == "":
                if str(string_line).__contains__("\"= \""):  # "MXCHIP_upgrade_skip"= "暂不升级"; 类型的 等号右端有空格, 左侧没有空格的
                    ios_string_id = string_line.split("\"= \"")[0].replace("\"", "")
                    ios_string_value = string_line.split("\"= \"")[1] \
                        .replace("= ", "") \
                        .replace(";", "").replace("\"", "")

            ios_string_value = ios_string_value.strip("\n")
            if language_dir.__contains__("zh.lproj") or language_dir.__contains__("zh-Hans.lproj"):
                lang_string = LangString(string_id=ios_string_id, common_path=relative_common_path,
                                         module_name=module_name,
                                         lang_dir="zh.lproj", file_name=file_name, content=ios_string_value)

                ios_string_list.append(lang_string)

            if language_dir.__contains__("de.lproj"):
                lang_string = LangString(string_id=ios_string_id, common_path=relative_common_path,
                                         module_name=module_name,
                                         lang_dir="de.lproj", file_name=file_name, content=ios_string_value)

                ios_string_list.append(lang_string)

            if language_dir.__contains__("fr.lproj"):
                lang_string = LangString(string_id=ios_string_id, common_path=relative_common_path,
                                         module_name=module_name,
                                         lang_dir="fr.lproj", file_name=file_name, content=ios_string_value)

                ios_string_list.append(lang_string)

            if language_dir.__contains__("es.lproj"):
                lang_string = LangString(string_id=ios_string_id, common_path=relative_common_path,
                                         module_name=module_name,
                                         lang_dir="es.lproj", file_name=file_name, content=ios_string_value)

                ios_string_list.append(lang_string)

            if language_dir.__contains__("de.lproj"):
                lang_string = LangString(string_id=ios_string_id, common_path=relative_common_path,
                                         module_name=module_name,
                                         lang_dir="de.lproj", file_name=file_name, content=ios_string_value)

                ios_string_list.append(lang_string)

            if language_dir.__contains__("ja.lproj"):
                lang_string = LangString(string_id=ios_string_id, common_path=relative_common_path,
                                         module_name=module_name,
                                         lang_dir="ja.lproj", file_name=file_name, content=ios_string_value)
                ios_string_list.append(lang_string)

            if language_dir.__contains__("ko.lproj"):
                lang_string = LangString(string_id=ios_string_id, common_path=relative_common_path,
                                         module_name=module_name,
                                         lang_dir="ko.lproj", file_name=file_name, content=ios_string_value)

                ios_string_list.append(lang_string)

            if language_dir.__contains__("en.lproj"):
                lang_string = LangString(string_id=ios_string_id, common_path=relative_common_path,
                                         module_name=module_name,
                                         lang_dir="en.lproj", file_name=file_name, content=ios_string_value)

                ios_string_list.append(lang_string)

            if language_dir.__contains__("ru.lproj"):
                lang_string = LangString(string_id=ios_string_id, common_path=relative_common_path,
                                         module_name=module_name,
                                         lang_dir="ru.lproj", file_name=file_name, content=ios_string_value)

                ios_string_list.append(lang_string)
    return ios_string_list


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
        if mobileString.zh_cn is not None and mobileString.zh_cn.get_full_path() != "":
            # try:
            zh_cn_lang_file_list = string_by_file_dict.get(mobileString.zh_cn.get_full_path())
            # except KeyError:
            #     zh_cn_lang_file_list = []
            if zh_cn_lang_file_list is None:
                zh_cn_lang_file_list = []

            zh_cn_lang_file_list.append(mobileString)
            string_by_file_dict[mobileString.zh_cn.get_full_path()] = zh_cn_lang_file_list
            # lang_file_list.clear()

        if mobileString.english_us is not None and mobileString.english_us.get_full_path() != "":
            lang_file_list = string_by_file_dict.get(mobileString.english_us.get_full_path())
            if lang_file_list is None:
                lang_file_list = []
            lang_file_list.append(mobileString)
            string_by_file_dict[mobileString.english_us.get_full_path()] = lang_file_list
            # lang_file_list.clear()

        if mobileString.spanish is not None and mobileString.spanish.get_full_path() != "":
            lang_file_list = string_by_file_dict.get(mobileString.spanish.get_full_path())
            if lang_file_list is None:
                lang_file_list = []
            lang_file_list.append(mobileString)
            string_by_file_dict[mobileString.spanish.get_full_path()] = lang_file_list
            # lang_file_list.clear()

        if mobileString.french is not None and mobileString.french.get_full_path() != "":
            lang_file_list = string_by_file_dict.get(mobileString.french.get_full_path())
            if lang_file_list is None:
                lang_file_list = []
            lang_file_list.append(mobileString)
            string_by_file_dict[mobileString.french.get_full_path()] = lang_file_list
            # lang_file_list.clear()

        if mobileString.russia is not None and mobileString.russia.get_full_path() != "":
            lang_file_list = string_by_file_dict.get(mobileString.russia.get_full_path())
            if lang_file_list is None:
                lang_file_list = []
            string_by_file_dict[mobileString.russia.get_full_path()] = lang_file_list.append(mobileString)
            # lang_file_list.clear()

        if mobileString.germany is not None and mobileString.germany.get_full_path() != "":
            lang_file_list = string_by_file_dict.get(mobileString.germany.get_full_path())
            if lang_file_list is None:
                lang_file_list = []
            string_by_file_dict[mobileString.germany.get_full_path()] = lang_file_list.append(mobileString)
            # lang_file_list.clear()

        if mobileString.korean is not None and mobileString.korean.get_full_path() != "":
            lang_file_list = string_by_file_dict.get(mobileString.korean.get_full_path())
            if lang_file_list is None:
                lang_file_list = []
            lang_file_list.append(mobileString)
            string_by_file_dict[mobileString.korean.get_full_path()] = lang_file_list
            # lang_file_list.clear()

        if mobileString.japan is not None and mobileString.japan.get_full_path() != "":
            lang_file_list = string_by_file_dict.get(mobileString.japan.get_full_path())
            if lang_file_list is None:
                lang_file_list = []
            lang_file_list.append(mobileString)
            string_by_file_dict[mobileString.japan.get_full_path()] = lang_file_list
            # lang_file_list.clear()
    return string_by_file_dict


def get_raw_ios_string_dict() -> dict:
    """
    读取的 .strings  文件，获得是最原声的字符串，在这里相同的 string_id 的字符串并没有整理到一起来
    :return:
    """
    module_list = get_all_module_name()
    ios_module_string_dict = {}
    print("the ios module size is ", len(module_list))

    for module in module_list:
        string_file_list = get_filtered_strings_file(module, ios_app_project_path)
        if len(string_file_list) == 0:
            continue
        try:
            module_string_list = ios_module_string_dict[module]
        except KeyError:
            module_string_list = []
        for file in string_file_list:
            list_c = read_strings_from_file(module, file)
            if len(list_c) == 0:
                continue
            for c in list_c:
                module_string_list.append(c)

        print("the size of this module ", module, " string is: ", len(module_string_list))
        """
        去掉没有字符串的模块
        """
        if len(module_string_list) == 0:
            continue
        ios_module_string_dict[module] = module_string_list.copy()
    print("the all ios module string dict is ", len(ios_module_string_dict))
    return ios_module_string_dict


def merge_lang_to_mobile_string(identity_key_string_list: list) -> MobileString:
    """
    对于 lang_string 有相同的 identity_key 合并成同一个 mobile_string
    :return: 返回一个 mobile_string 对象
    """
    module = identity_key_string_list[0].module_name
    string_id = identity_key_string_list[0].string_id
    mobile_string = MobileString(module_name=module, string_id=string_id,
                                 is_ios_string=True, is_android_string=False
                                 )
    for lang_string in identity_key_string_list:
        if lang_string.lang_dir == "zh.lproj":
            mobile_string.zh_cn = lang_string
        if lang_string.lang_dir == "en.lproj":
            mobile_string.english_us = lang_string

        if lang_string.lang_dir == "de.lproj":
            mobile_string.germany = lang_string
        if lang_string.lang_dir == "fr.lproj":
            mobile_string.french = lang_string

        if lang_string.lang_dir == "ko.lproj":
            mobile_string.korean = lang_string
        if lang_string.lang_dir == "es.lproj":
            mobile_string.spanish = lang_string

        if lang_string.lang_dir == "ru.lproj":
            mobile_string.russia = lang_string
        if lang_string.lang_dir == "ja.lproj":
            mobile_string.japan = lang_string
    return mobile_string


def get_ios_string_dict_by_identity_key() -> dict:
    """
    把字符串按照 identity_key 划分
    :return:
    """
    string_dict_by_identity_key = {}
    module_strings_dict = get_ios_string_dict_by_module()
    for module_name in module_strings_dict.keys():
        module_strings_list = module_strings_dict.get(module_name)
        for ios_string in module_strings_list:
            string_dict_by_identity_key[ios_string.get_identity_key()] = ios_string
    return string_dict_by_identity_key


def get_ios_string_dict_by_zh_cn() -> dict:
    """
    把字符串按照 identity_key 划分
    :return:
    """
    string_dict_by_zh_cn = {}
    module_strings_dict = get_ios_string_dict_by_module()
    for module_name in module_strings_dict.keys():
        module_strings_list = module_strings_dict.get(module_name)
        for ios_string in module_strings_list:
            string_dict_by_zh_cn[ios_string.get_identity_key()] = ios_string
    return string_dict_by_zh_cn


def get_ios_string_dict_by_module() -> dict:
    """
    通过模块把字符串划分开, 同时对于同一个模块的字符串， 相同的 string_id， 但是不同的语言进行
    :return:
    """
    raw_string_dic = get_raw_ios_string_dict()
    module_string_dict = {}
    for module_name in raw_string_dic.keys():
        try:
            module_string_list = module_string_dict.get(module_name)
        except KeyError:
            module_string_list = []
        if module_string_list is None:
            module_string_list = []
        single_module_raw_string_list = raw_string_dic.get(module_name)
        print("get_ios_string_dict_by_module, module = ", module_name, "len(single_module_raw_string_list) = ",
              len(single_module_raw_string_list))
        module_string_dict_by_identity_key = {}
        for lang_string in single_module_raw_string_list:
            string_identity_key = lang_string.get_identity_key()
            try:
                mobile_string_list = module_string_dict_by_identity_key.get(string_identity_key)
            except KeyError:
                mobile_string_list = []
            if mobile_string_list is None:
                mobile_string_list = []
            mobile_string_list.append(lang_string)
            module_string_dict_by_identity_key[string_identity_key] = mobile_string_list
        for identity_key in module_string_dict_by_identity_key.keys():
            string_list = module_string_dict_by_identity_key.get(identity_key)
            if string_list is None or len(string_list) == 0:
                continue
            module_string_list.append(merge_lang_to_mobile_string(string_list))
            module_string_dict[module_name] = module_string_list

    print("the all module string ", len(module_string_dict))
    for module_name in module_string_dict:
        module_string_list_a = module_string_dict[module_name]
        for mobile_string in module_string_list_a:
            pass
            # print("==================== mobile_string = ", mobile_string)
    return module_string_dict


def get_source_text(mobile_string: MobileString) -> str:
    """
    输入一个 mobilestring 对象, 选择合适的
    :param mobile_string:
    :return:
    """
    if mobile_string.zh_cn is not None and mobile_string.zh_cn != "":
        return mobile_string.zh_cn.content
    elif mobile_string.zh_tw is not None and mobile_string.zh_tw != "":
        return mobile_string.zh_tw.content
    elif mobile_string.english_us is not None and mobile_string.english_us != "":
        return mobile_string.english_us.content
    elif mobile_string.french is not None and mobile_string.french != "":
        return mobile_string.french.content
    elif mobile_string.spanish is not None and mobile_string.spanish != "":
        return mobile_string.spanish.content
    elif mobile_string.germany is not None and mobile_string.germany != "":
        return mobile_string.germany.content


def get_source_text_file_path(mobile_string: MobileString) -> str:
    """
    优先选择中文字符串的文件路径作为共同的路径, 以后会优化为该语言的读取的文件路径,如果没有才选择其他的语言
    :param mobile_string:
    :return:
    """
    full_file_path = ""
    if mobile_string.zh_cn is not None and mobile_string.zh_cn != "":
        full_file_path = mobile_string.zh_cn.get_full_path()
    elif mobile_string.zh_tw is not None and mobile_string.zh_tw != "":
        full_file_path = mobile_string.zh_tw.get_full_path()
    elif mobile_string.english_us is not None and mobile_string.english_us != "":
        full_file_path = mobile_string.english_us.get_full_path()
    elif mobile_string.french is not None and mobile_string.french != "":
        full_file_path = mobile_string.french.get_full_path()
    elif mobile_string.spanish is not None and mobile_string.spanish != "":
        full_file_path = mobile_string.spanish.get_full_path()
    elif mobile_string.germany is not None and mobile_string.germany != "":
        full_file_path = mobile_string.germany.get_full_path()
    if full_file_path.startswith("/"):
        full_file_path.lstrip("/")
    if full_file_path.startswith("/"):
        full_file_path.lstrip("/")
    return full_file_path


def get_common_string_file_path(mobile_string: MobileString) -> str:
    file_path = get_source_text_file_path(mobile_string)
    print("get_common_string_file_path: file_path = ", file_path)
    print("get_common_string_file_path: mobile_string = ", mobile_string)
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
    string_dict_by_id = get_ios_string_dict_by_identity_key()
    for string_id in string_dict_by_id.keys():
        ios_string: MobileString = string_dict_by_id[string_id]
        print("get_pending_translate_ios_string_dict(), android_string = ", str(ios_string))
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

            if target_lang == "ZH-CN":
                # ios_string.english_us = translate(source_text, "en", "zh-CN")
                ios_string.zh_cn_file = common_file_path + os.sep + "zh.lproj" + os.sep + file_name
            if target_lang == "EN-US":
                # ios_string.english_us = translate(source_text, "en", "zh-CN")
                ios_string.english_us_file = common_file_path + os.sep + "en.lproj" + os.sep + file_name
            if target_lang == "JA":
                # ios_string.japan = translate_text(source_text, "JA", "zh-CN")
                ios_string.japan_file = common_file_pat_with_sep + "ja.lproj" + os.sep + file_name
            if target_lang == "KO":
                # ios_string.korean = translate(source_text, "ko", "zh-CN")
                ios_string.korean_file = common_file_path + os.sep + "ko.lproj" + os.sep + file_name
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
                string_value_str = str(string_value.japan.content)
            if target_language == "EN-US":
                string_value_str = str(string_value.english_us.content)
            if target_language == "ZH-CN":
                string_value_str = str(string_value.zh_cn.content)
            if target_language == "KO":
                string_value_str = str(string_value.korean.content)
            if string_value_str == "":
                continue
            string_line = "\"" + ios_string_key + "\"" + " = " + "\"" + string_value_str + "\";\n"
            print("generate_ios_res: string_line: string_line = ", string_line)
            f.write(string_line)


if __name__ == '__main__':
    # get_ios_string_dict_by_identity_key()

    # print("ios_string_dict_by_id = ", ios_string_dict_by_id[ios_string_key])
    pending_translation_ios_string_dict = get_pending_translate_ios_string_dict()
    divider_by_file = divide_string_dict_by_file(pending_translation_ios_string_dict)
    print("=================== len(divider_by_file) = ", len(divider_by_file))
    for file_key in divider_by_file.keys():
        print("================ file_key = ", file_key)
        string_list = divider_by_file.get(file_key)

        string_list_dict = {}
        if string_list is None:
            continue
        if len(string_list) == 0:
            continue
        """
        重新规整一下字符串, 放在字典里面
        """
        print("================ len(string_list) = ", len(string_list))

        for string in string_list:
            string_list_dict[string.string_id] = string
        for target_lang in get_target_languages():
            if target_lang == "ZH-CN":
                if str(file_key).__contains__("zh.lproj"):
                    generate_ios_res(string_list_dict, "ZH-CN", file_key)
            if target_lang == "EN-US":
                if str(file_key).__contains__("en.lproj"):
                    generate_ios_res(string_list_dict, "EN-US", file_key)
            if target_lang == "JA":
                if str(file_key).__contains__("ja.lproj"):
                    generate_ios_res(string_list_dict, "JA", file_key)
            if target_lang == "KO":
                if str(file_key).__contains__("ko.lproj"):
                    generate_ios_res(string_list_dict, "KO", file_key)
