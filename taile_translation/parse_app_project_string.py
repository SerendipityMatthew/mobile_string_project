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
from ios_string import IOS_String
from parse_ios_strings import get_ios_project_string_dict, get_ios_project_string_dict_all
from parse_module import get_app_project_module, project_path
from read_ini_utils import get_android_strings_files, get_targe_language, get_generate_excel_file_name

multination_string_excel_file = "correct_translation.xlsx"
final_multination_string_excel_file = "hello_translation.xlsx"
mx_app_file_path = project_path

"""
项目的路径作为这个项目的名称
"""
project_name = mx_app_file_path.split(os.sep)[-1]

mxapp_smartplus_android_common = project_name + os.sep + "src"

module_name_list = get_app_project_module()


def get_all_strings_xml_file():
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
                if file_full_path.__contains__(".git"):
                    break
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
    print("parse_single_string: xml_file = " + str(xml_file))
    xml_file_doc = ElementTree.parse(xml_file)

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
            single_xml_file_string_dict[string_name_id] = string_name_value

    return single_xml_file_string_dict


def is_the_language(xml_file, res_prefix, values_dir):
    """

    :param xml_file:
    :param res_prefix:
    :param values_dir:  values-ko-rKR 形如这样的目录
    :return:
    """
    dash_last_index = values_dir.rindex("-")
    values_dir2 = values_dir[0:dash_last_index]
    if xml_file.__contains__(res_prefix + values_dir2):
        return True
    return False


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
    string_dict_da_rDK = {}
    string_dict_fi_rFI = {}
    string_dict_cs_rCZ = {}
    string_dict_sl_rSI = {}
    string_dict_pt_rPT = {}
    string_dict_zh_rTW = {}
    module_string_list = []
    file_separator = "/"
    if isWindowsSystem():
        file_separator = "\\"

    for string_file in all_string_list:
        module_name_str = module_name + file_separator

        if string_file.__contains__(module_name_str):
            page_start_string_list.append(string_file)
    wanted_string_list = []
    """
    过滤出配置文件里的所需要的 字符串文件
    """
    for xml_file in page_start_string_list:
        string_files = get_android_strings_files()
        if len(string_files) == 0:
            break
        for wanted_file in string_files:
            if xml_file.endswith(wanted_file):
                wanted_string_list.append(xml_file)

    for xml_file in wanted_string_list:
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
        if is_the_language(xml_file, res_prefix, "values-zh-rCN"):
            string_dict_zh_rCN.update(parse_single_string(xml_file))
        if is_the_language(xml_file, res_prefix, "values-en-rUS"):
            string_dict_en_rUS.update(parse_single_string(xml_file))
        if is_the_language(xml_file, res_prefix, "values-de-rDE"):
            string_dict_de_rDE.update(parse_single_string(xml_file))
        if is_the_language(xml_file, res_prefix, "values-fr-rFR"):
            string_dict_fr_rFR.update(parse_single_string(xml_file))
        if is_the_language(xml_file, res_prefix, "values-es-rES"):
            string_dict_es_rES.update(parse_single_string(xml_file))
        if is_the_language(xml_file, res_prefix, "values-ko-rKR"):
            string_dict_ko_rKR.update(parse_single_string(xml_file))
        if is_the_language(xml_file, res_prefix, "values-ru-rRU"):
            string_dict_ru_rRU.update(parse_single_string(xml_file))
        if is_the_language(xml_file, res_prefix, "values-ja-rJP"):
            string_dict_ja_rJP.update(parse_single_string(xml_file))
        if is_the_language(xml_file, res_prefix, "values-da-rDK"):
            string_dict_da_rDK.update(parse_single_string(xml_file))
        if is_the_language(xml_file, res_prefix, "values-fi-rFI"):
            string_dict_fi_rFI.update(parse_single_string(xml_file))
        if is_the_language(xml_file, res_prefix, "values-cs-rCZ"):
            string_dict_cs_rCZ.update(parse_single_string(xml_file))
        if is_the_language(xml_file, res_prefix, "values-sl-rSI"):
            string_dict_sl_rSI.update(parse_single_string(xml_file))
        if is_the_language(xml_file, res_prefix, "values-pt-rPT"):
            string_dict_pt_rPT.update(parse_single_string(xml_file))
        if is_the_language(xml_file, res_prefix, "values-zh-rTW"):
            string_dict_zh_rTW.update(parse_single_string(xml_file))

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

        try:
            tw = string_dict_zh_rTW[key]
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
        # print("taileString = " + str(taileString) + " android_id = " + key)
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
        if module_count == 0:
            continue
        end = count + module_count
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


def read_all_strings_from_android_xml() -> list:
    all_string_list = get_all_strings_xml_file()
    all_string = []
    for module_name in module_name_list:
        module_string_list = parse_module_string(module_name, all_string_list)
        for string in module_string_list:
            all_string.append(string)

    return all_string


def taile_string_comp(taile_str1: TaileString, taile_str2: TaileString):
    if taile_str1.page_start > taile_str2.page_start:
        return True
    return False


def sort_string_list(all_string):
    all_string_dict = {}
    taileStringHeaderlist = []
    taileStringHeader = TaileString(
        module_name="功能模块",
        function_desc="功能描述",
        page_start="所在页面",
        android_id="android 资源id",
        ios_module="ios 所在模块",
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
    module_name_list.append("----")
    for module_name in module_name_list:
        page_start_string_list = []
        # print("sort_string_list: module_name =" + module_name)
        for index in range(all_string.__len__()):
            if all_string[index].module_name.__eq__(module_name):
                page_start_string_list.append(all_string[index])
        page_start_string_list.sort()
        all_string_dict[module_name] = page_start_string_list

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


def setStyle():
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    # 字体类型：比如宋体、仿宋也可以是汉仪瘦金书繁
    font.name = 'Times New Roman'
    # 设置字体颜色
    font.colour_index = 14
    # 字体大小
    font.height = 200
    # 定义格式
    style.font = font

    return style


def setStyleFontColor():
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    # 字体类型：比如宋体、仿宋也可以是汉仪瘦金书繁
    font.name = 'Times New Roman'
    # 设置字体颜色
    font.colour_index = 39
    # 字体大小
    font.height = 200
    # 定义格式
    style.font = font

    return style


def write_code_string_excel_xls(path: str, sorted_string_map: dict):
    length = sorted_string_map.__len__()  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet("code_string")  # 在工作簿中新建一个表格
    count = 0
    cell_style = module_name_cell_style()
    # 遍历 所有的 字符串资源
    for key in sorted_string_map.keys():
        single_module_name_list = sorted_string_map[key]
        # print("key  = " + key + ", the length: " + str(single_module_name_list.__len__()))
        # 写入一个模块的资源
        module_count = single_module_name_list.__len__()
        # print("========= module_count = " + str(module_count))
        if module_count == 0:
            continue
        end = count + module_count
        # sheet.write_merge(count, end - 1, 0, 0, key, style=cell_style)
        for col_index in range(single_module_name_list[0].__dict__.keys().__sizeof__()):
            sheet.col(col_index).width = 256 * 40
            if col_index == 0:
                continue
            sheet.col(col_index).height = 40 * 40
        other_style = other_cell_style()
        fontStyle = setStyle()
        fontColorStyle = setStyleFontColor()
        for index1 in range(count, end):
            android_string = single_module_name_list[index1 - count]
            for col_index1 in range(12):
                sheet.col(col_index1).width = 256 * 40
                if col_index1 == 0:
                    continue
                sheet.col(col_index1).height = 40 * 40
            sheet.write(index1, 0, android_string.module_name)
            sheet.write(index1, 1, android_string.ios_module)
            sheet.write(index1, 2, android_string.android_id)

            # sheet.write(index1, 3, android_string.ios_id)
            if android_string.module_name.strip() == "----":
                sheet.write(index1, 3, android_string.ios_id, fontColorStyle)
            else:
                sheet.write(index1, 3, android_string.ios_id)

            sheet.write(index1, 4, android_string.simplified_chinese)
            sheet.write(index1, 5, android_string.default_lang)
            if android_string.ios_id.strip() == "":
                sheet.write(index1, 6, android_string.english_us, fontStyle)
            else:
                sheet.write(index1, 6, android_string.english_us)

            sheet.write(index1, 7, android_string.spanish)
            sheet.write(index1, 8, android_string.germany)
            sheet.write(index1, 9, android_string.french)
            sheet.write(index1, 10, android_string.russia)
            sheet.write(index1, 11, android_string.korean)
            sheet.write(index1, 12, android_string.japan)

        count = end
        # sheet.write_merge(module_count, module_count - 1, 0, 0, single_module_name_list[i].module_name)

    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")


def parse_string() -> list:
    """
    大致的流程描述
    1. 按照模块 读取 android 源代码里的 String
    2. 读取修正的 excel 表格里的 字符串资源
    3. 交叉对比里面的文件, 并且赋值正确的功能描述
    4. 写入到全新的, 字段全面的 excel 表格里

    """
    # correct_string_list = read_multination_string_excel(sheetName='Sheet1')
    android_code_string_list = read_all_strings_from_android_xml()
    return android_code_string_list


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def android_all_string() -> dict:
    """
    android 相同的中文相同字符串合并
    :return:
    """
    android_strings_list = parse_string()
    taile_string_dict = {}
    for taile_string in android_strings_list:
        print("=========== " + str(taile_string))

        try:
            same_key_value = taile_string_dict[taile_string.default_lang]
        except:
            same_key_value = None
        print("------------- " + taile_string.default_lang + " ------ " +
              str(same_key_value))
        if same_key_value is None:
            taile_string_dict[taile_string.default_lang] = [taile_string]
        else:
            # 这么写是错误的
            # taile_string_dict[taile_string.default_lang] = same_key_value.append(
            #     taile_string)
            taile_string_dict[taile_string.default_lang].append(
                taile_string)
    # for key in taile_string_dict.keys():
    #     print("========= key = " + str(key) + " value = " + str(taile_string_dict.get(key)))
    return taile_string_dict


def get_all_ios_string() -> dict:
    return get_ios_project_string_dict_all()


def hello():
    android_string_list = parse_string()
    ios_string_dict = get_ios_project_string_dict()
    for hello in ios_string_dict.keys():
        print("jjjjjjjjjjjjj = " + str(ios_string_dict.get(hello).__len__()))
    print("============== ios_string_dict = " + str(ios_string_dict.__len__()))
    print("============== android_code_string_list = " + str(android_string_list.__len__()))
    merge_ios_android_string_list = []
    for string_index in range(android_string_list.__len__()):
        android_string = android_string_list[string_index]
        for ios_module in ios_string_dict.keys():
            module_string_list = ios_string_dict.get(ios_module)
            print("============== module_string_list len = " + str(module_string_list.__len__()))

            for ios_string in module_string_list:
                ios_compare_string = ios_string.value.strip()

                android_compare_string = android_string.simplified_chinese.strip()
                if android_compare_string.__len__() == 0:
                    android_compare_string = android_string.default_lang

                if android_compare_string.lower() == ios_compare_string.lower():
                    android_string.ios_module = ios_string.module_name
                    android_string.ios_id = ios_string.string_id
                    merge_ios_android_string_list.append(ios_string)
                    android_string_list[string_index] = android_string

                else:
                    print("android_compare_string = " + str(android_compare_string) + ", ios_compare_string = " + str(
                        ios_compare_string))
                    android_zh_string = android_string.simplified_chinese
                    android_zh_string.__contains__(",")
    all_ios_string_list = []
    for ios_module in ios_string_dict.keys():
        module_string_list = ios_string_dict.get(ios_module)
        for ios_string in module_string_list:
            all_ios_string_list.append(ios_string)
    # list(set(listB).difference(set(listA)))

    diff_ios_list = list(set(all_ios_string_list).difference(set(merge_ios_android_string_list)))
    print("============== diff_ios_list = " + str(diff_ios_list.__len__()))
    for ios_string in diff_ios_list:
        ios_string_convert = TaileString(module_name="----",
                                         ios_module=ios_string.module_name,
                                         simplified_chinese=ios_string.value,
                                         ios_id=ios_string.string_id, english_us="")
        android_string_list.append(ios_string_convert)

    sorted_string_map = sort_string_list(android_string_list)

    write_code_string_excel_xls("code_string_translation.xls", sorted_string_map)


def remove_duplicate(list1) -> list:
    return list(set(list1))


def merge_android_and_ios_string() -> dict:
    """
     将 android 的 字符串和额 ios 的字符串 根据 中文字符串合并到同一个 dict 里面去
    :return:
    """
    all_ios_string_dict = get_all_ios_string()
    all_android_string_dict = android_all_string()
    #  android ios 存放的字符串的 字典, 在这里合并
    megered_string_dict = {}

    # 遍历所有的 ios_string_dict
    for ios_string_key in all_ios_string_dict.keys():
        # 遍历所有的 android_string_dict
        for android_string_key in all_android_string_dict.keys():
            try:
                mergered_string_list = megered_string_dict[android_string_key]
            except:
                mergered_string_list = None
            # android_string_list = all_android_string_dict.get(android_string_key)

            # ios 和 Android 的中文字符串是一样的
            if str(android_string_key).strip() == str(ios_string_key).strip():
                #  如果之前没有元素存放进去, 那么就默认的给一个 空的 list
                if mergered_string_list is None:
                    megered_string_dict[android_string_key] = []
                megered_string_dict[android_string_key].extend(all_ios_string_dict.get(ios_string_key))
                megered_string_dict[android_string_key].extend(all_android_string_dict.get(android_string_key))

                #  去掉 list 中的重复的

                megered_string_dict[android_string_key] = remove_duplicate(megered_string_dict[android_string_key])

            else:

                if mergered_string_list is None:
                    megered_string_dict[android_string_key] = []
                megered_string_dict[android_string_key].extend(all_android_string_dict.get(android_string_key))

                if megered_string_dict.get(ios_string_key) is None:
                    megered_string_dict[ios_string_key] = []
                megered_string_dict[ios_string_key].extend(all_ios_string_dict.get(ios_string_key))

                if megered_string_dict.get(ios_string_key) is None:
                    megered_string_dict[ios_string_key] = []
                megered_string_dict[ios_string_key].extend(all_ios_string_dict.get(ios_string_key))
                #  去掉 list 中的重复的
                megered_string_dict[android_string_key] = remove_duplicate(megered_string_dict[android_string_key])
                megered_string_dict[ios_string_key] = remove_duplicate(megered_string_dict[ios_string_key])
    for megered_string_key in megered_string_dict.keys():
        megered_string_dict[megered_string_key].extend(remove_duplicate(megered_string_dict.get(megered_string_key)))
    return megered_string_dict


def generate_string_excel(string_dict):
    path = get_generate_excel_file_name()
    length = string_dict.__len__()  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    print("========== length " + str(length))
    sheet = workbook.add_sheet("code_string", cell_overwrite_ok=True)  # 在工作簿中新建一个表格
    cell_style = module_name_cell_style()
    # 写文件的头
    sheet.write(0, 0, "中文字符串")
    sheet.write(0, 1, get_targe_language())  # 韩语字符串
    sheet.write(0, 2, "android 模块和资源id")
    sheet.write(0, 3, "ios 模块和资源id")  # 韩语字符串
    # 遍历 所有的 字符串资源
    index = 1
    for string_key in string_dict.keys():
        single_module_name_list = string_dict[string_key]
        print("key  = " + string_key + ", the length: " + str(single_module_name_list.__len__()))
        # 写入一个模块的资源
        single_module_name_list = string_dict[string_key]
        # 写入一个模块的资源
        # Column1    Column2             (Column3)                    (Column14)
        # 中文字符串   韩语字符串      (android module-android id)      (ios module - ios id)
        sheet.write(index, 0, string_key)
        sheet.write(index, 1, "")  # 韩语字符串
        android_module_res_id = ""
        ios_module_res_id = ""
        for string in single_module_name_list:
            if type(string) is TaileString:
                android_module_res_id = android_module_res_id + "&" + string.module_name + "#" + string.android_id
            if type(string) is IOS_String:
                ios_module_res_id = ios_module_res_id + "&" + string.module_name + "#" + string.string_id
        sheet.write(index, 2, android_module_res_id)
        sheet.write(index, 3, ios_module_res_id)  # 韩语字符串
        index += 1

    workbook.save(path)  # 保存工作簿


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    all_string_dict = merge_android_and_ios_string()
    for key in all_string_dict.keys():
        print("========= all_string_dict key = " + str(key) + " value = " + str(
            remove_duplicate(all_string_dict.get(key))))
    generate_string_excel(all_string_dict)
