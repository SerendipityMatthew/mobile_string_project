# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os as os
import xml.etree.cElementTree as ElementTree

from xlrd.sheet import Sheet

from Taile_String import TaileString
import pandas as pandas

import xlrd
import xlwt
from xlutils.copy import copy


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


multination_string_excel_file = "/correct_translation.xlsx"
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


def parse_module_string(module_name: str, all_string_list):
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


"""
为规范表格里的文字的 样式
"""


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


"""
    最终生成一个 excel 表格
"""


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
        for index1 in range(count, end):
            android_string = single_module_name_list[index1 - count]
            print("index1 = " + str(index1))
            for col_index1 in range(12):
                sheet.col(col_index1).width = 256 * 40
                if col_index1 == 0:
                    continue
                sheet.col(col_index1).height = 40 * 40
            sheet.write(index1, 1, android_string.android_id, style=other_style)
            sheet.write(index1, 2, android_string.ios_id)
            sheet.write(index1, 3, android_string.simplified_chinese)
            sheet.write(index1, 4, android_string.default_lang)
            sheet.write(index1, 5, android_string.english_us)
            sheet.write(index1, 6, android_string.spanish)
            sheet.write(index1, 7, android_string.germany)
            sheet.write(index1, 8, android_string.french)
            sheet.write(index1, 9, android_string.russia)
            sheet.write(index1, 10, android_string.korean)
            sheet.write(index1, 11, android_string.japan)

        count = end
        # sheet.write_merge(module_count, module_count - 1, 0, 0, single_module_name_list[i].module_name)

    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")


def read_all_strings_from_android_xml():
    all_string_list = read_all_strings_xml()
    all_string = []
    for module in module_name_list:
        var = parse_module_string(module, all_string_list)
        for hello in var:
            all_string.append(hello)

    return all_string


"""
    读取 android 项目下的 所有的 strings.xml 等字符串文件, 然后生成一个 excel 表格.
"""


def read_all_strings_generate_excel():
    all_string = read_all_strings_from_android_xml()

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


"""
读取合并所有的单元格
"""


def get_merged_cells(sheet: Sheet):
    return sheet.merged_cells


"""
读取合并所有的单元格的值, 这里我们只需要 col_index = 1 的值,就行了. 其他的无所谓
"""


def get_merged_cells_value(sheet: Sheet, row_index, col_index):
    """
    先判断给定的单元格，是否属于合并单元格；
    如果是合并单元格，就返回合并单元格的内容
    :return:
    """
    merged = get_merged_cells(sheet)
    for (rlow, rhigh, clow, chigh) in merged:
        if (row_index >= rlow and row_index < rhigh):
            if (col_index >= clow and col_index < chigh):
                cell_value = sheet.cell_value(rlow, clow)

                # print('该单元格[%d,%d]属于合并单元格，值为[%s]' % (row_index, col_index, cell_value))
                return cell_value
                break
    return None


"""
从 correct_translation.xlsx 文件里读出所有的字符串
服务协议  ----> mxapp_smartplus_android/src
注册功能   ----> page-account
登录功能   ----> ilop-component
忘记/修改密码   ---> page-account
首页     ----> ilop-componen  page-device
家庭管理  ----> page-device
智能   -----> page-scene
我的   -----> page-me
个人设置 ----> page-me
设置    ---> page-ota page-me ilop-component
消息中心  ---->page-message
问题反馈    --->ilop-componen
设备共享   -----> page-share
使用帮助   ---->   page-me
关于我们    ----> page-me  ilop-component
添加设备   ----> page-device-add  ilop-component
虚拟按钮   ----> page-scene
设备详情
"""


def read_multination_string_company_excel():
    with xlrd.open_workbook(multination_string_excel_file) as excel_workbook:
        worksheet = excel_workbook.sheet_by_name('Sheet1')
        multination_string_list = []
        for row_index in range(worksheet.nrows):
            if row_index == 0:
                continue
            module_name = ""
            function_desc = ""
            simplified_chinese = ""
            english_us = ""
            for col_index in range(worksheet.ncols):
                # print(worksheet.cell_value(row_index, col_index))
                cell_value = worksheet.cell_value(row_index, col_index)
                if col_index == 1:
                    module_name = get_merged_cells_value(worksheet, row_index, col_index)
                if col_index == 2:
                    function_desc = cell_value
                if col_index == 4:
                    simplified_chinese = cell_value
                if col_index == 5:
                    english_us = cell_value

            taileString = TaileString(module_name=module_name, function_desc=function_desc,
                                      simplified_chinese=simplified_chinese, english_us=english_us)
            multination_string_list.append(taileString)

        for taileString in multination_string_list:
            # print(taileString)
            pass

        return multination_string_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    """
    大致的流程描述
    1. 按照模块 读取 android 源代码里的 String
    2. 读取修正的 excel 表格里的 字符串资源
    3. 交叉对比里面的文件, 并且赋值正确的功能描述
    4. 写入到全新的, 字段全面的 excel 表格里
    
    """
    correct_string_list = read_multination_string_company_excel()
    android_code_string_list = read_all_strings_from_android_xml()

    for correct_string in correct_string_list:
        for code_string in android_code_string_list:
            if str(code_string.simplified_chinese).__eq__(str(correct_string.simplified_chinese)):
                if str(code_string.english_us).__eq__(str(correct_string.english_us)):
                    code_string.function_desc = correct_string.function_desc
                    print(code_string)
