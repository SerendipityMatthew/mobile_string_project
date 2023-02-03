import xlwt

from mobile_string import MobileString
from parse_android_string import get_android_string_dict_by_identity_key, remove_duplicate
from parse_ios_strings import get_ios_string_dict_by_identity_key
from read_ini_utils import get_generate_excel_file_name


def get_merged_string_dict() -> dict:
    """
    合并 android 和 ios 的字符串，以中文字符串 key
    :return:
    """
    android_string_dict = get_android_string_dict_by_identity_key()
    merged_string_dict = dict()

    for android_string_key in android_string_dict:
        """
        遍历 Android 的字符串
        """

        android_string = android_string_dict.get(android_string_key)
        if android_string.default_lang is not None and android_string.default_lang.content is not None:
            content = android_string.default_lang.content
            try:
                same_key_string_list = merged_string_dict[content]
            except:
                same_key_string_list = []

            same_key_string_list.append(android_string)
            same_key_string_list = remove_duplicate(same_key_string_list)
            """
            以中文字符串为 key, 
            """
            merged_string_dict[content] = same_key_string_list

    ios_string_list = get_ios_string_dict_by_identity_key()
    for ios_string_key in ios_string_list:
        """
           遍历 iOS 的字符串
           """
        ios_string = ios_string_list.get(ios_string_key)

        if ios_string.zh_cn is not None and ios_string.zh_cn.content is not None:
            content = ios_string.zh_cn.content
            try:
                same_key_string_list = merged_string_dict[content]
            except:
                same_key_string_list = []
            same_key_string_list.append(ios_string)
            same_key_string_list = remove_duplicate(same_key_string_list)
            merged_string_dict[content] = same_key_string_list

    print("get_merged_string: len(merged_string_dict) = ", len(merged_string_dict))

    return merged_string_dict


def module_name_cell_style():
    style = xlwt.easyxf('font:height 720;')
    font = xlwt.Font()
    font.blod = True
    font.height = 20 * 20
    style.font = font
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style.alignment = alignment
    return style


def generate_excel_file(string_dict: dict):
    path = get_generate_excel_file_name()
    length = string_dict.__len__()  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    print("========== length " + str(length))
    sheet = workbook.add_sheet("android iOS 合并字符串", cell_overwrite_ok=True)  # 在工作簿中新建一个表格
    cell_style = module_name_cell_style()
    # 写文件的头
    sheet.write(0, 0, "中文字符串")
    sheet.write(0, 1, "英语")
    sheet.write(0, 2, "android 模块和资源id")
    sheet.write(0, 3, "ios 模块和资源id")  # 韩语字符串
    # 遍历 所有的 字符串资源
    index = 1
    for string_key in string_dict.keys():
        single_module_name_list = string_dict[string_key]
        print("key  = " + string_key + ", the length: " + str(single_module_name_list.__len__()))
        """
        # 写入一个模块的资源
        # Column1    Column2             (Column3)                    (Column14)
        # 中文字符串   目标语言列      (android module-android id)      (ios module - ios id)
        """
        sheet.write(index, 0, string_key)
        sheet.write(index, 1, )
        module_and_string_id = ""

        for mobile_string in single_module_name_list:
            if type(mobile_string) is MobileString:
                module_and_string_id = "&" + mobile_string.module_name + "#" + mobile_string.string_id
            if mobile_string.is_android_string:
                sheet.write(index, 2, module_and_string_id)
            if mobile_string.is_ios_string:
                sheet.write(index, 3, module_and_string_id)

        index += 1

    workbook.save(path)  # 保存工作簿


if __name__ == '__main__':
    merged_dict = get_merged_string_dict()
    generate_excel_file(merged_dict)
    for string_list_key in merged_dict:
        string_list = merged_dict[string_list_key]
        # print("============ string_list = ", remove_duplicate(string_list), ", string_list_key = ", string_list_key)
