# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os as os
import xml.etree.cElementTree as ElementTree
from Taile_String import TaileString
import pandas as pandas

import xlrd
import xlwt
from xlutils.copy import copy


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


mx_app_file_path = "/Volumes/Mathew/code/mxchip/mxapp_smartplus_android"

module_name_list = ["page-start", "page-scene", "page-scan",
                    "page-ota", "page-message", "page-me",
                    "page-device-add", "page-device-add-sdk",
                    "page-account", "page-device",
                    "mxchip-component", "ilop-component",
                    "page-share", "mxapp_smartplus_android/src"
                    ]


def read_all_strings_xml():
    app_file = os.walk(mx_app_file_path)
    string_file_list = []
    for path, dir_list, file_list in app_file:
        for dir_name in dir_list:
            file_path = os.path.join(path, dir_name)
            for dir_path in os.listdir(file_path):
                file_full_path = os.path.join(file_path, dir_path)
                if file_full_path.__contains__(".xml") and file_full_path.__contains__("main/res/values"):
                    string_file_list.append(file_full_path)

    return string_file_list


def parse_module_string(module_name: str):
    page_start_string_list = []
    string_dict_ko_rKR = {}
    string_dict_none = {}
    string_dict_zh_rCN = {}
    string_dict_en_rUS = {}
    string_dict_de_rDE = {}
    string_dict_fr_rFR = {}
    string_dict_es_rES = {}
    string_dict_ru_rRU = {}
    string_dict_ja_rJP = {}
    module_string_list = []
    for string_file in all_string_list:
        if string_file.__contains__(module_name + "/"):
            page_start_string_list.append(string_file)

    for xml_file in page_start_string_list:
        if xml_file.endswith("dimen.xml"):
            continue
        if xml_file.endswith("color.xml"):
            continue
        if xml_file.endswith("start_style.xml"):
            continue
        if xml_file.endswith("styles.xml"):
            continue
        if xml_file.endswith("dimens.xml"):
            continue
        if xml_file.endswith("attrs.xml"):
            continue
        if xml_file.endswith("demin.xml"):
            continue
        if xml_file.endswith("widget_actions.xml"):
            continue
        if xml_file.endswith("yccardview.xml"):
            continue
        if xml_file.endswith("ids.xml"):
            continue
        if xml_file.endswith("colors.xml"):
            continue
        if xml_file.endswith("attr.xml"):
            continue
        if xml_file.endswith("deviceadd_colors.xml"):
            continue
        if xml_file.endswith("ilop_mine_colors.xml"):
            continue
        if xml_file.endswith("ilop_ota_dialog_style.xml"):
            continue
        if xml_file.endswith("account_style.xml"):
            continue
        if xml_file.endswith("device_style.xml"):
            continue
        # print(xml_file)
        if xml_file.__contains__("res/values/"):
            xml_file_doc = ElementTree.parse(xml_file)
            for child in xml_file_doc.getroot():
                string_dict_none[child.attrib["name"]] = str(child.text)
        if xml_file.__contains__("res/values-zh-rCN"):
            xml_file_doc = ElementTree.parse(xml_file)
            for child in xml_file_doc.getroot():
                string_dict_zh_rCN[child.attrib["name"]] = str(child.text)
        if xml_file.__contains__("res/values-en-rUS"):
            xml_file_doc = ElementTree.parse(xml_file)
            for child in xml_file_doc.getroot():
                string_dict_en_rUS[child.attrib["name"]] = str(child.text)
        if xml_file.__contains__("res/values-de-rDE"):
            xml_file_doc = ElementTree.parse(xml_file)
            for child in xml_file_doc.getroot():
                string_dict_de_rDE[child.attrib["name"]] = str(child.text)
        if xml_file.__contains__("res/values-fr-rFR"):
            xml_file_doc = ElementTree.parse(xml_file)
            for child in xml_file_doc.getroot():
                string_dict_fr_rFR[child.attrib["name"]] = str(child.text)

        if xml_file.__contains__("res/values-es-rES"):
            xml_file_doc = ElementTree.parse(xml_file)
            for child in xml_file_doc.getroot():
                string_dict_es_rES[child.attrib["name"]] = str(child.text)
        if xml_file.__contains__("res/values-ko-rKR"):
            xml_file_doc = ElementTree.parse(xml_file)
            for child in xml_file_doc.getroot():
                string_dict_ko_rKR[child.attrib["name"]] = str(child.text)

        if xml_file.__contains__("res/values-ru-rRU"):
            xml_file_doc = ElementTree.parse(xml_file)
            for child in xml_file_doc.getroot():
                string_dict_ru_rRU[child.attrib["name"]] = str(child.text)

        if xml_file.__contains__("res/values-ja-rJP"):
            xml_file_doc = ElementTree.parse(xml_file)
            for child in xml_file_doc.getroot():
                string_dict_ja_rJP[child.attrib["name"]] = str(child.text)

    # 从中选择出最大的
    # print(string_dict_none.__len__())
    # print(string_dict_zh_rCN.__len__())
    # print(string_dict_en_rUS.__len__())
    # print(string_dict_es_rES.__len__())
    # print(string_dict_fr_rFR.__len__())
    # print(string_dict_de_rDE.__len__())
    # print(string_dict_ko_rKR.__len__())
    # print(string_dict_ru_rRU.__len__())
    # print(string_dict_ja_rJP.__len__())

    for key in string_dict_none.keys():
        default_lang = string_dict_none[key]
        simplified_chinese = ""
        english_us = ""
        spanish = ""
        french = ""
        germany = ""
        korean = ""
        russia = ""
        japan = ""

        try:
            simplified_chinese = string_dict_zh_rCN[key]
        except KeyError:
            pass

        try:
            english_us = string_dict_en_rUS[key]
        except KeyError:
            pass

        try:
            spanish = string_dict_es_rES[key]
        except KeyError:
            pass

        try:
            french = string_dict_fr_rFR[key]
        except KeyError:
            pass

        try:
            germany = string_dict_de_rDE[key]
        except KeyError:
            pass
        try:
            korean = string_dict_ko_rKR[key]
        except KeyError:
            pass

        try:
            russia = string_dict_ru_rRU[key]
        except KeyError:
            pass

        try:
            japan = string_dict_ja_rJP[key]
        except KeyError:
            pass

        taileString = TaileString(
            module_name=module_name,
            android_id=key,
            ios_id="",
            default_lang=default_lang,
            simplified_chinese=simplified_chinese,
            english_us=english_us,
            french=french,
            spanish=spanish,
            korean=korean,
            russia=russia,
            germany=germany,
            japan=japan,
        )
        module_string_list.append(taileString)
    return module_string_list


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


def other_cell_style():
    style = xlwt.easyxf('font:height 720;')
    font = xlwt.Font()
    font.blod = True
    font.height = 20 * 20
    style.font = font
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_LEFT
    # alignment.vert = xlwt.Alignment.VERT_CENTER
    style.alignment = alignment
    return style


#
# dict { module_name : }
#
def write_excel_xls(path, sheet_name, value):
    length = value.__len__()  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    print("========== length " + str(length))
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    count = 0
    # 遍历 所有的 字符串资源
    for key in value.keys():
        single_module_name_list = value[key]
        print(key + "[[[[[[ " + str(single_module_name_list.__len__()))
        print("xxxxxxxxx " + str(single_module_name_list.__len__()))
        # 写入一个模块的资源
        module_count = single_module_name_list.__len__()
        print("========= count = " + str(count))
        print("========= module_count = " + str(module_count))
        end = count + module_count
        print("========= end = " + str(end))
        cell_style = module_name_cell_style()
        sheet.write_merge(count, end - 1, 0, 0, key, style=cell_style)
        for col_index in range(12):
            sheet.col(col_index).width = 256 * 40
            if col_index == 0:
                continue
            sheet.col(col_index).height = 40 * 40
        other_style = other_cell_style()
        for index in range(count, end):
            string = single_module_name_list[index - count]
            print("index = " + str(index))
            for col_index in range(12):
                sheet.col(col_index).width = 256 * 40
                if col_index == 0:
                    continue
                sheet.col(col_index).height = 40 * 40
            sheet.write(index, 1, string.android_id, style=other_style)
            sheet.write(index, 2, string.ios_id)
            sheet.write(index, 3, string.simplified_chinese)
            sheet.write(index, 4, string.default_lang)
            sheet.write(index, 5, string.english_us)
            sheet.write(index, 6, string.spanish)
            sheet.write(index, 7, string.germany)
            sheet.write(index, 8, string.french)
            sheet.write(index, 9, string.russia)
            sheet.write(index, 10, string.korean)
            sheet.write(index, 11, string.japan)

        count = end
        # sheet.write_merge(module_count, module_count - 1, 0, 0, single_module_name_list[i].module_name)

    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    all_string_list = read_all_strings_xml()
    all_string = []
    for module in module_name_list:
        var = parse_module_string(module)
        for hello in var:
            all_string.append(hello)

    all_string_dict = {}
    taileStringHeaderlist = []
    taileStringHeader = TaileString(
        module_name="功能模块",
        android_id="android 资源id",
        ios_id="ios 资源id",
        simplified_chinese="中文",
        default_lang="默认语言",
        english_us="美式英语",
        spanish="西班牙语",
        germany="德语",
        french="法语",
        russia="俄罗斯语",
        korean="韩语",
        japan="日语"

    )
    taileStringHeaderlist.insert(0, taileStringHeader)
    print(all_string.__len__())
    all_string_dict["模块名称"] = taileStringHeaderlist
    write_excel_xls("translation.xlsx", "taile", all_string_dict)

    for module_name in module_name_list:
        page_start_string_list = []
        for index in range(all_string.__len__()):
            if all_string[index].module_name.__eq__(module_name):
                print("mmmmmmmm " + all_string[index].__str__())
                page_start_string_list.append(all_string[index])

        all_string_dict[module_name] = page_start_string_list

    for module in all_string_dict.keys():
        for string in all_string_dict[module]:
            # print(string)
            pass
    write_excel_xls("translation.xlsx", "taile", all_string_dict)
