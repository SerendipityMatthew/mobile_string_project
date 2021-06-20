# coding:utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os as os
import xml.etree.cElementTree as ElementTree

import xlrd
import xlwt
from xlrd.sheet import Sheet
import platform

from Taile_String import TaileString
from parse_module import get_app_project_module


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


multination_string_excel_file = "correct_translation.xlsx"
final_multination_string_excel_file = "hello_translation.xlsx"
mx_app_file_path = "/Volumes/Mathew/code/mxchip/mxapp_smartplus_android"
mxapp_smartplus_android_common = "mxapp_smartplus_android" + os.sep + "src"
# module_name_list = ["page-message"]

module_name_list = ["page-start", "page-scene", "page-scan",
                    "page-ota", "page-message", "page-me",
                    "page-device-add", "page-device-add-sdk",
                    "page-account", "page-device",
                    "mxchip-component", "ilop-component",
                    "page-share", mxapp_smartplus_android_common
                    ]
page_list = ["服务协议", "注册功能", "登录功能",
             "忘记/修改密码", "首页", "家庭管理",
             "智能", "我的", "个人设置",
             "设置", "消息中心", "问题反馈",
             "使用帮助", "设备共享", "关于我们",
             "添加设备", "虚拟按钮",
             ]


def read_all_strings_xml():
    """
        过滤出所有的符合条件的 strings 文件
    :return:
    """
    app_file = os.walk(mx_app_file_path)
    string_file_list = []
    for path, dir_list, file_list in app_file:
        for dir_name in dir_list:
            file_path = os.path.join(path, dir_name)
            for dir_path in os.listdir(file_path):
                file_full_path = os.path.join(file_path, dir_path)
                values_string_path = "main/res/values"
                if isWindowsSystem():
                    values_string_path = "main\\res\\values"
                if file_full_path.__contains__(".xml"):
                    if file_full_path.__contains__(values_string_path):
                        string_file_list.append(file_full_path)

    return string_file_list


def isWindowsSystem():
    system = platform.system()
    if system.__eq__("Windows"):
        return True
    return False


def parse_single_string(xml_file):
    single_xml_file_string_dict = {}
    xml_file_doc = ElementTree.parse(xml_file)
    print("parse_single_string: xml_file = " + str(xml_file))

    for child in xml_file_doc.getroot():
        if str(child.tag).__eq__("string-array"):
            string_array_item_list = []
            for string_array_item in child.iter():
                print("==== xxxxx yyyy ======= " + str(string_array_item.text))
                string_array_item_list.append(string_array_item.text)
            single_xml_file_string_dict[child.attrib["name"]] = "|".join(string_array_item_list)

        else:
            string_name_id = child.attrib["name"]
            string_name_value = child.text
            if xml_file.__contains__("openaccount_ui.xml"):
                if xml_file.__contains__("page-account/"):
                    print("=============== string_name_id = " + string_name_id)

            if string_name_value is None:
                string_name_value = ""
            single_xml_file_string_dict[string_name_id] = string_name_value

    return single_xml_file_string_dict


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
    file_separator = "/"
    if isWindowsSystem():
        file_separator = "\\"
    print("===========ddddddddddddd========" + str(all_string_list.__len__()))
    for string_file in all_string_list:
        module_name_str = module_name + file_separator

        if string_file.__contains__(module_name_str):
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
        if xml_file.endswith("ilop_message_switchbtn_styles.xml"):
            continue

        if xml_file.endswith("app_styles.xml"):
            continue
        if xml_file.endswith("ids.xml"):
            continue

        if xml_file.endswith("arrays.xml"):
            continue
        # print(xml_file)
        res_prefix = "res/"
        if isWindowsSystem():
            res_prefix = "res\\"
        if xml_file.__contains__(res_prefix + "values" + os.sep):
            string_dict_none.update(parse_single_string(xml_file))
        if xml_file.__contains__(res_prefix + "values-zh-rCN"):
            string_dict_zh_rCN.update(parse_single_string(xml_file))
        if xml_file.__contains__(res_prefix + "values-en-rUS"):
            string_dict_en_rUS.update(parse_single_string(xml_file))
        if xml_file.__contains__(res_prefix + "values-de-rDE"):
            string_dict_de_rDE.update(parse_single_string(xml_file))
        if xml_file.__contains__(res_prefix + "values-fr-rFR"):
            string_dict_fr_rFR.update(parse_single_string(xml_file))

        if xml_file.__contains__(res_prefix + "values-es-rES"):
            string_dict_es_rES.update(parse_single_string(xml_file))

        if xml_file.__contains__(res_prefix + "values-ko-rKR"):
            string_dict_ko_rKR.update(parse_single_string(xml_file))

        if xml_file.__contains__(res_prefix + "values-ru-rRU"):
            string_dict_ru_rRU.update(parse_single_string(xml_file))

        if xml_file.__contains__(res_prefix + "values-ja-rJP"):
            string_dict_ja_rJP.update(parse_single_string(xml_file))

    # 从中选择出最大的
    print(string_dict_none.__len__())
    print("@@@@@@@@@@@@ " + str(string_dict_none))
    # print(string_dict_en_rUS.__len__())
    # print(string_dict_es_rES.__len__())
    # print(string_dict_fr_rFR.__len__())
    print("每个语言的字符串个个数")
    print(string_dict_de_rDE.__len__())
    print(string_dict_ko_rKR.__len__())
    print(string_dict_ru_rRU.__len__())
    print(string_dict_ja_rJP.__len__())

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
        print("--------------- " + key)
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

        isStringArray = simplified_chinese.__contains__("|")
        print(" is string array = " + str(isStringArray))
        taileString = TaileString(
            module_name=module_name,
            android_id=key,
            ios_id="",
            isStringArray=isStringArray,
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
        print("taileString = " + str(taileString) + " android_id = " + key)
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
    cell_style = module_name_cell_style()
    # 遍历 所有的 字符串资源
    for key in value.keys():
        single_module_name_list = value[key]
        print("key  = " + key + ", the length: " + str(single_module_name_list.__len__()))
        # 写入一个模块的资源
        module_count = single_module_name_list.__len__()
        print("========= module_count = " + str(module_count))
        if module_count == 0:
            continue
        end = count + module_count
        print("========= count = " + str(count))
        print("========= end = " + str(end))
        sheet.write_merge(count, end - 1, 0, 0, key, style=cell_style)
        for col_index in range(single_module_name_list[0].__dict__.keys().__sizeof__()):
            sheet.col(col_index).width = 256 * 40
            if col_index == 0:
                continue
            sheet.col(col_index).height = 40 * 40
        other_style = other_cell_style()
        for index1 in range(count, end):
            android_string = single_module_name_list[index1 - count]
            # print("index1 = " + str(index1))
            for col_index1 in range(12):
                sheet.col(col_index1).width = 256 * 40
                if col_index1 == 0:
                    continue
                sheet.col(col_index1).height = 40 * 40
            sheet.write(index1, 1, android_string.module_name)
            sheet.write(index1, 2, android_string.function_desc)
            sheet.write(index1, 3, android_string.android_id)
            sheet.write(index1, 4, android_string.ios_id)
            sheet.write(index1, 5, android_string.simplified_chinese)
            sheet.write(index1, 6, android_string.default_lang)
            sheet.write(index1, 7, android_string.english_us)
            sheet.write(index1, 8, android_string.spanish)
            sheet.write(index1, 9, android_string.germany)
            sheet.write(index1, 10, android_string.french)
            sheet.write(index1, 11, android_string.russia)
            sheet.write(index1, 12, android_string.korean)
            sheet.write(index1, 13, android_string.japan)

        count = end
        # sheet.write_merge(module_count, module_count - 1, 0, 0, single_module_name_list[i].module_name)

    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")


def read_all_strings_from_android_xml():
    all_string_list = read_all_strings_xml()
    all_string = []
    print("hhhhhhhh = " + str(module_name_list.__len__()))
    for module_name in module_name_list:
        print("bbbbbbbbbbbbb: module = " + str(module_name))
        var = parse_module_string(module_name, all_string_list)
        for hello in var:
            all_string.append(hello)

    return all_string


def taile_string_comp(taile_str1: TaileString, taile_str2: TaileString):
    if taile_str1.page_start > taile_str2.page_start:
        return True
    return False


"""
对 list 内的元素, 进行排序, 
"""
sorted_by_module = True


def sort_string_list(all_string):
    all_string_dict = {}
    taileStringHeaderlist = []
    taileStringHeader = TaileString(
        module_name="功能模块",
        function_desc="功能描述",
        page_start="所在页面",
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
    """
     写第一行文件
    """

    """
    排序字段  模块名称 ---> 启动页面
    
    """
    if sorted_by_module:
        for module_name in module_name_list:
            page_start_string_list = []
            print("sort_string_list: module_name =" + module_name)
            for index in range(all_string.__len__()):
                if all_string[index].module_name.__eq__(module_name):
                    print("mmmmmmmm " + all_string[index].__str__())
                    page_start_string_list.append(all_string[index])
            page_start_string_list.sort()
            all_string_dict[module_name] = page_start_string_list
    else:
        for page_name in page_list:
            page_start_string_list = []
            print("sort_string_list: page_name =" + page_name)
            for index in range(all_string.__len__()):
                if all_string[index].page_start.__eq__(page_name):
                    print("page_name =  " + all_string[index].__str__())
                    page_start_string_list.append(all_string[index])
            page_start_string_list.sort()
            all_string_dict[page_name] = page_start_string_list
    return all_string_dict


"""
    读取 android 项目下的 所有的 strings.xml 等字符串文件, 然后生成一个 excel 表格.
"""


def read_all_strings_generate_excel():
    all_string = read_all_strings_from_android_xml()
    print(all_string.__len__())
    all_string_dict_temp = sort_string_list(all_string)

    print(all_string_dict_temp.keys().__sizeof__())

    write_excel_xls("translation.xlsx", "taile", all_string_dict_temp)


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
        if rlow <= row_index < rhigh:
            if clow <= col_index < chigh:
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
首页     ----> ilop-component  page-device
家庭管理  ----> page-device
智能   -----> page-scene
我的   -----> page-me
个人设置 ----> page-me
设置    ---> page-ota page-me ilop-component
消息中心  ---->page-message
问题反馈    --->ilop-component
设备共享   -----> page-share
使用帮助   ---->   page-me
关于我们    ----> page-me  ilop-component
添加设备   ----> page-device-add  ilop-component
虚拟按钮   ----> page-scene
设备详情
"""


def read_multination_string_excel(sheetName: str):
    print("================ sheetName = " + sheetName)
    with xlrd.open_workbook(multination_string_excel_file) as excel_workbook:
        worksheet = excel_workbook.sheet_by_name(sheetName)
        multination_string_list = []
        for row_index in range(worksheet.nrows):
            print("row_index = " + str(row_index))
            if row_index == 0:
                continue
            module_name = ""
            function_desc = ""
            simplified_chinese = ""
            english_us = ""
            for col_index in range(worksheet.ncols):
                cell_value = worksheet.cell_value(row_index, col_index)
                print("cell_value = " + str(cell_value))
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
            print(taileString)

    return multination_string_list


"""
读取最终版本的 字符串的excel 文件, 他有最全的字段
"""


def read_final_multination_string_company_excel(sheetName: str):
    with xlrd.open_workbook(final_multination_string_excel_file) as excel_workbook:
        worksheet = excel_workbook.sheet_by_name(sheetName)
        multination_string_list = []
        for row_index in range(worksheet.nrows):
            if row_index == 0:
                continue
            module_name = ""
            function_desc = ""
            android_id = ""
            ios_id = ""
            simplified_chinese = ""
            default_lang = ""
            english_us = ""
            spanish = ""
            germany = ""
            french = ""
            russia = ""
            korean = ""
            japan = ""
            page_start = ""
            for col_index in range(worksheet.ncols):
                # print(worksheet.cell_value(row_index, col_index))
                cell_value = worksheet.cell_value(row_index, col_index)
                print("cell_value = " + cell_value)
                if col_index == 1:
                    module_name = get_merged_cells_value(worksheet, row_index, col_index)
                if col_index == 2:
                    page_start = cell_value
                if col_index == 3:
                    function_desc = cell_value
                if col_index == 4:
                    android_id = cell_value
                if col_index == 5:
                    ios_id = cell_value
                if col_index == 6:
                    simplified_chinese = cell_value
                if col_index == 7:
                    default_lang = cell_value
                if col_index == 8:
                    english_us = cell_value
                if col_index == 9:
                    spanish = cell_value

                if col_index == 10:
                    germany = cell_value
                if col_index == 11:
                    french = cell_value
                if col_index == 12:
                    russia = cell_value
                if col_index == 13:
                    korean = cell_value
                if col_index == 14:
                    japan = cell_value

            taileString = TaileString(module_name=module_name, function_desc=function_desc,
                                      page_start=page_start, default_lang=default_lang,
                                      android_id=android_id, ios_id=ios_id,
                                      germany=germany, french=french, russia=russia,
                                      korean=korean, japan=japan, spanish=spanish,
                                      simplified_chinese=simplified_chinese, english_us=english_us)
            multination_string_list.append(taileString)

        for taileString in multination_string_list:
            print(taileString)

        return multination_string_list


"""
交叉对比 代码当中 string 和 正确翻译的 excel 文件中的 string
"""

collect_all_xxxx = []


def cross_compare_the_then_get_one(android_code_string_list, correct_string,
                                   code_module_name,
                                   chinese_and_english: bool):
    string_list = []
    for code_string in android_code_string_list:
        # if str(code_string.english_us).__eq__("Ok"):
        #     continue
        # if str(code_string.english_us).__eq__("OK"):
        #     continue
        # if str(code_string.english_us).__eq__("Cancel"):
        #     continue
        print("cross_compare_the_then_get_one = code_module_name = " + code_module_name)
        print("cross_compare_the_then_get_one = code_string.module_name = " + code_string.module_name)
        if code_string.module_name.__eq__(code_module_name):
            print("===========================================")
            print("=========================================== code_string.english_us = " + code_string.english_us)
            """
             对于特殊字符串, 去掉一些符号,然后比较, 比如去掉 中文的 "《"
            """
            modify_code_english = code_string.english_us \
                .replace("《", "") \
                .replace("？", "?") \
                .replace("?", "") \
                .replace("\n", "") \
                .replace("  ", "") \
                .replace("》", "") \
                .replace("\\", "") \
                .replace("\n", "") \
                .replace("\t", "") \
                .replace(", ", ",") \
                .strip().lower()
            modify_correct_english = correct_string.english_us \
                .replace("《", "") \
                .replace("》", "") \
                .replace("？", "?") \
                .replace("?", "") \
                .replace("\n", "") \
                .replace("  ", "") \
                .replace("\\", "") \
                .replace("\t", "") \
                .replace("\n", "") \
                .replace(", ", ",") \
                .strip().lower()

            modify_code_chinese = code_string.simplified_chinese.replace("《", "").replace("》", "").strip()
            modify_correct_chinese = correct_string.simplified_chinese.replace("《", "").replace("》", "").strip()
            print("modify_code_chinese = " + modify_code_chinese)
            print("modify_correct_chinese = " + modify_correct_chinese)
            print("modify_correct_chinese code_string = " + str(code_string))
            print("modify_correct_chinese code_string.isStringArray = " + str(code_string.isStringArray))
            print("english us   correct one:  modify_code_english = " + modify_code_english)
            print("english us   correct one:  modify_correct_english = " + modify_correct_english)
            if not code_string.isStringArray and modify_code_english.__eq__(modify_correct_english):
                print("[[[[[[[[[[[[[[[[[[[[[[[[[")
                if chinese_and_english:
                    if modify_code_chinese.__eq__(modify_correct_chinese):
                        collect_all_xxxx.append(correct_string)
                        code_string.page_start = correct_string.module_name
                        code_string.function_desc = correct_string.function_desc
                        print("code_string = " + str(code_string))
                        print("correct_string = " + str(correct_string))
                        string_list.append(code_string)
                else:
                    collect_all_xxxx.append(correct_string)
                    code_string.page_start = correct_string.module_name
                    code_string.function_desc = correct_string.function_desc
                    print("code_string = " + str(code_string))
                    print("correct_string = " + str(correct_string))
                    string_list.append(code_string)
            elif code_string.isStringArray:
                """
                数组类型的
                """
                code_array_string = code_string.english_us.split("|")[0].strip()

                if code_array_string.__eq__(correct_string.english_us):
                    collect_all_xxxx.append(correct_string)
                    code_string.page_start = correct_string.module_name
                    code_string.function_desc = correct_string.function_desc
                    print("code_string = " + str(code_string))
                    string_list.append(code_string)
            else:
                """
                    长句子, 比较第一句话是否相同
                """
                if modify_correct_english.__contains__("."):
                    correct_first_line = modify_correct_english.split(".")[0].strip()
                    code_first_line = modify_code_english.split(".")[0].strip()
                    if code_first_line.__eq__(correct_first_line):
                        collect_all_xxxx.append(correct_string)
                        code_string.page_start = correct_string.module_name
                        code_string.function_desc = correct_string.function_desc
                        print("code_string = " + str(code_string))
                        string_list.append(code_string)

    print("++++++++++++++++++ " + str(string_list.__len__()))

    return string_list


def parse_array_string(single_module_list: list):
    single_module_array_list = []
    for string in single_module_list:
        if string.isStringArray:
            chinese_array_string = string.simplified_chinese.split("|")
            default_array_string = string.default_lang.split("|")
            english_array_string = string.english_us.split("|")
            spanish_array_string = string.spanish.split("|")
            germany_array_string = string.germany.split("|")
            french_array_string = string.french.split("|")
            russia_array_string = string.russia.split("|")
            korean_array_string = string.korean.split("|")
            japan_array_string = string.japan.split("|")
            for index in range(len(chinese_array_string)):
                simplified_chinese = chinese_array_string[index]
                default_lang = ""
                if index < len(default_array_string):
                    default_lang = default_array_string[index]

                english_us = ""
                if index < len(default_array_string):
                    english_us = english_array_string[index]
                spanish = ""
                if index < len(spanish_array_string):
                    spanish = spanish_array_string[index]

                french = ""
                if index < len(french_array_string):
                    french = french_array_string[index]

                russia = ""
                if index < len(russia_array_string):
                    russia = russia_array_string[index]
                korean = ""
                if index < len(korean_array_string):
                    korean = korean_array_string[index]
                japan = ""
                if index < len(japan_array_string):
                    japan = japan_array_string[index]
                germany = ""
                if index < len(germany_array_string):
                    germany = germany_array_string[index]

                taileString = TaileString(
                    module_name=string.module_name,
                    isStringArray=False,
                    page_start=string.page_start,
                    android_id=string.android_id,
                    ios_id="",
                    function_desc=string.function_desc,
                    simplified_chinese=simplified_chinese,
                    default_lang=default_lang,
                    english_us=english_us,
                    spanish=spanish,
                    french=french,
                    russia=russia,
                    korean=korean,
                    japan=japan,
                    germany=germany,
                )
                single_module_array_list.append(taileString)
        else:
            single_module_array_list.append(string)
    return single_module_array_list


def write_code_string_excel_xls(path: str, sorted_string_map: dict):
    length = sorted_string_map.__len__()  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    print("========== length " + str(length))
    sheet = workbook.add_sheet("code_string")  # 在工作簿中新建一个表格
    count = 0
    cell_style = module_name_cell_style()
    # 遍历 所有的 字符串资源
    for key in sorted_string_map.keys():
        single_module_name_list = sorted_string_map[key]
        print("key  = " + key + ", the length: " + str(single_module_name_list.__len__()))
        # 写入一个模块的资源
        module_count = single_module_name_list.__len__()
        print("========= module_count = " + str(module_count))
        if module_count == 0:
            continue
        end = count + module_count
        print("========= count = " + str(count))
        print("========= end = " + str(end))
        sheet.write_merge(count, end - 1, 0, 0, key, style=cell_style)
        for col_index in range(single_module_name_list[0].__dict__.keys().__sizeof__()):
            sheet.col(col_index).width = 256 * 40
            if col_index == 0:
                continue
            sheet.col(col_index).height = 40 * 40
        other_style = other_cell_style()
        for index1 in range(count, end):
            android_string = single_module_name_list[index1 - count]
            # print("index1 = " + str(index1))
            for col_index1 in range(12):
                sheet.col(col_index1).width = 256 * 40
                if col_index1 == 0:
                    continue
                sheet.col(col_index1).height = 40 * 40
            sheet.write(index1, 1, android_string.module_name)
            sheet.write(index1, 2, android_string.function_desc)
            sheet.write(index1, 3, android_string.android_id)
            sheet.write(index1, 4, android_string.ios_id)
            sheet.write(index1, 5, android_string.simplified_chinese)
            sheet.write(index1, 6, android_string.default_lang)
            sheet.write(index1, 7, android_string.english_us)
            sheet.write(index1, 8, android_string.spanish)
            if str(key).__eq__("page-account"):
                print("write_code_string_excel_xls: android_string.germany = " + android_string.germany)
            sheet.write(index1, 9, android_string.germany)
            sheet.write(index1, 10, android_string.french)
            sheet.write(index1, 11, android_string.russia)
            sheet.write(index1, 12, android_string.korean)
            sheet.write(index1, 13, android_string.japan)

        count = end
        # sheet.write_merge(module_count, module_count - 1, 0, 0, single_module_name_list[i].module_name)

    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")


def parse_string():
    """
    大致的流程描述
    1. 按照模块 读取 android 源代码里的 String
    2. 读取修正的 excel 表格里的 字符串资源
    3. 交叉对比里面的文件, 并且赋值正确的功能描述
    4. 写入到全新的, 字段全面的 excel 表格里

    """
    # correct_string_list = read_multination_string_excel(sheetName='Sheet1')
    android_code_string_list = read_all_strings_from_android_xml()
    for taile_string in android_code_string_list:
        if taile_string.module_name.__eq__("page-account"):
            print("hhhhhhhhh = " + taile_string.germany)
    sorted_string_map = sort_string_list(android_code_string_list)
    print("=============== fffffff  " + str(sorted_string_map.__len__()))
    write_code_string_excel_xls("code_string_translation.xls", sorted_string_map)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # read_all_strings_generate_excel(
    parse_string()
    # correct_string_list = read_final_multination_string_company_excel("taile")
    # for xxx in correct_string_list:
    #     print(xxx)
