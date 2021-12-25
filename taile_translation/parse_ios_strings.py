import os

import chardet

from mobile_string import MobileString
from read_ini_utils import get_ios_strings_files, get_ios_project_path

"""
只获取该项目的英文翻译的字段和中文翻译的字段, 然后基于英文和中文去对比和比较
"""
ios_app_project_path = get_ios_project_path()


def get_all_files_list(path: str, all_file_list: list) -> list:
    app_file = os.walk(path)
    print("=========== file_full_path file_list app_file = ", app_file)
    for path, dir_list, file_list in app_file:
        for file in file_list:
            file_path = os.path.join(path, file)
            all_file_list.append(file_path)
            # print("=========== file_full_path file_list file = ", path, "    ", file)
        for dir_name in dir_list:
            get_all_files_list(dir_name, all_file_list)
    print("the strings file of the project, total " + str(all_file_list.__len__()))
    return all_file_list


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
    file_list = get_all_files_list(module_string_path + os.sep + module_name, [])
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


def read_strings_from_file(module_name: str, file_path):
    ios_string_list = []
    encoding = get_encoding(file_path)
    print("read_strings_from_file: encoding = ", encoding, " file_path " + file_path)
    """
    这些 Windows-1254 和 EUC-TW 编码统一归为 UTF-8 编码
    """
    if encoding == "Windows-1254" or encoding == "EUC-TW":
        encoding = "utf-8"
    relative_file_path = file_path.split(ios_app_project_path)[1]
    print("read_strings_from_file: encoding = ", encoding, " relative_file_path " + relative_file_path)

    with open(file=file_path, encoding=encoding) as f:
        file_string = f.readlines()

        for string in file_string:

            if string.strip().__eq__(""):
                continue
            if not string.startswith("\""):
                continue
            ios_string_id = ""
            ios_string_value = ""
            if str(string).__contains__("\" = \""):  # "MXCHIP_upgrade_skip" = "暂不升级"; 类型的
                ios_string_id = string.split("\" ")[0].replace("\"", "")
                ios_string_value = string.split("\" ")[1].replace("= ", "").replace(";", "").replace("\"", "")
            if str(string).__contains__("\"=\""):  # "MXCHIP_upgrade_skip"="暂不升级"; 类型的
                ios_string_id = string.split("\"=\"")[0].replace("\"", "")
                ios_string_value = string.split("\"=\"")[1].replace("= ", "").replace(";", "").replace("\"", "")
            print("module_name = ", module_name, ", ios_string_id = ", ios_string_id, ", ios_string_value = ",
                  ios_string_value)
            ios_string_value = ios_string_value.strip("\n")
            if relative_file_path.__contains__("zh.lproj") or relative_file_path.__contains__("zh-Hans.lproj"):
                ios_string = MobileString(module_name, string_id=ios_string_id,
                                          zh_cn=ios_string_value, is_ios_string=True,
                                          zh_cn_file=relative_file_path)
                ios_string_list.append(ios_string)

            if relative_file_path.__contains__("de.lproj"):
                ios_string = MobileString(module_name, string_id=ios_string_id,
                                          germany=ios_string_value, is_ios_string=True,
                                          germany_file=relative_file_path)
                ios_string_list.append(ios_string)

            if relative_file_path.__contains__("fr.lproj"):
                ios_string = MobileString(module_name, string_id=ios_string_id,
                                          french=ios_string_value, is_ios_string=True,
                                          french_file=relative_file_path)
                ios_string_list.append(ios_string)

            if relative_file_path.__contains__("es.lproj"):
                ios_string = MobileString(module_name, string_id=ios_string_id,
                                          spanish=ios_string_value, is_ios_string=True,
                                          spanish_file=relative_file_path)
                ios_string_list.append(ios_string)

            if relative_file_path.__contains__("de.lproj"):
                ios_string = MobileString(module_name, string_id=ios_string_id,
                                          germany=ios_string_value, is_ios_string=True,
                                          germany_file=relative_file_path)
                ios_string_list.append(ios_string)

            if relative_file_path.__contains__("ja.lproj"):
                ios_string = MobileString(module_name, string_id=ios_string_id,
                                          japan=ios_string_value, is_ios_string=True,
                                          japan_file=relative_file_path)
                ios_string_list.append(ios_string)

            if relative_file_path.__contains__("ko.lproj"):
                ios_string = MobileString(module_name, string_id=ios_string_id,
                                          korean=ios_string_value, is_ios_string=True,
                                          korean_file=relative_file_path)
                ios_string_list.append(ios_string)

            if relative_file_path.__contains__("en.lproj"):
                ios_string = MobileString(module_name, string_id=ios_string_id,
                                          english_us=ios_string_value, is_ios_string=True,
                                          english_us_file=relative_file_path)
                ios_string_list.append(ios_string)

            if relative_file_path.__contains__("ru.lproj"):
                ios_string = MobileString(module_name, string_id=ios_string_id,
                                          russia=ios_string_value, is_ios_string=True,
                                          russia_file=relative_file_path)
                ios_string_list.append(ios_string)
    return ios_string_list


def merge_mobile_string_object(cache_string: MobileString, append_string: MobileString):
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

    print("merge_mobile_string_object cache_string = ", cache_string)
    return cache_string


def get_ios_string_dict_by_string_id() -> dict:
    module_list = get_all_module_name()
    ios_module_string_dict = {}
    for module in module_list:
        string_file_list = get_filtered_strings_file(module, ios_app_project_path)
        module_string_list = []
        for file in string_file_list:
            list_c = read_strings_from_file(module, file)
            for c in list_c:
                module_string_list.append(c)

        print("the module_string_list size is, ", len(module_string_list))
        ios_module_string_dict[module] = module_string_list
    print("the all ios module string dict is ", len(ios_module_string_dict))
    string_dict_by_id = {}
    for module in ios_module_string_dict.keys():
        for string in ios_module_string_dict[module]:
            cache_string = string_dict_by_id.get(string.string_id)
            if cache_string is None:
                string_dict_by_id[string.string_id] = string
            else:
                merge_cache_string = merge_mobile_string_object(cache_string, string)
                string_dict_by_id[string.string_id] = merge_cache_string

    return string_dict_by_id


def get_ios_string_dict_by_module() -> dict:
    module_list = get_all_module_name()
    ios_module_string_dict = {}
    for module in module_list:
        string_file_list = get_filtered_strings_file(module, ios_app_project_path)
        module_string_list = []
        for file in string_file_list:
            list_c = read_strings_from_file(module, file)
            for c in list_c:
                module_string_list.append(c)

        print("the module_string_list size is, ", len(module_string_list))
        ios_module_string_dict[module] = module_string_list
    print("the all ios module string dict is ", len(ios_module_string_dict))
    string_dict_by_id = {}
    for module in ios_module_string_dict.keys():
        for string in ios_module_string_dict[module]:
            cache_string = string_dict_by_id.get(string.string_id)
            if cache_string is None:
                string_dict_by_id[string.string_id] = string
            else:
                merge_cache_string = merge_mobile_string_object(cache_string, string)
                string_dict_by_id[string.string_id] = merge_cache_string

    module_string_dict = {}
    for ios_string_id in string_dict_by_id.keys():
        module = string_dict_by_id[ios_string_id].module_name
        module_string_list_A = module_string_dict.get(module)
        if module_string_list_A is None:
            module_string_list_A = []
        module_string_dict[module] = module_string_list_A.append(string_dict_by_id[ios_string_id])
        print("ios_string_id  ======= ", string_dict_by_id[ios_string_id])
    return module_string_dict


def get_ios_project_string_dict_all() -> dict:
    """
    获得的是以 中文字符串 为 key, value 是 ios_string 对象组成的 list的 dict
    :return:
    """
    module_list = get_all_module_name()
    ios_string_list = []
    for module_name in module_list:
        string_file_list = get_all_strings_file(module_name, ios_app_project_path)
        string_file_list = list(set(string_file_list))

        for file in string_file_list:
            file_list = get_ios_strings_files()
            if len(file_list) == 0:
                break
            for wanted_ios_file in file_list:
                if file.endswith(wanted_ios_file):
                    ios_string_list.extend(read_strings_from_file(module_name, file))

    ios_string_list = filter(lambda x: str(x).__contains__("Base.lproj") or str(x).__contains__("zh.lproj"),
                             ios_string_list)
    ios_string_dict = {}
    for ios_string in ios_string_list:
        strip_value = str(ios_string.value).strip().strip("\n")

        # if not str(ios_string.string_id).startswith("SYM_"):
        #     continue
        # print("ios string   ios_string = " + str(ios_string.string_id))
        try:
            ios_string_list = ios_string_dict[strip_value]
        except:
            ios_string_list = None
        if ios_string_list is None:
            ios_string_dict[strip_value] = [ios_string]
        else:
            ios_string_list.append(ios_string)
            ios_string_dict[strip_value] = ios_string_list

    return ios_string_dict


def strip_null_value_string_dict():
    ios_module_string = get_ios_string_dict_by_module()
    module_string = {}
    for (module_name, value) in ios_module_string.items():
        list_d = ios_module_string.get(module_name)
        if list_d.__len__() == 0:
            continue
        print("list_d = " + str(list_d.__len__()) + ", module_name = " + module_name)
        module_string[module_name] = list_d
        for d in list_d:
            print("ddddd = " + str(d))
    return module_string


if __name__ == '__main__':
    print("get_ios_project_string_dict_by_module() ", len(get_ios_string_dict_by_module()))
