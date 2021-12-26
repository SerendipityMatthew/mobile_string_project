#!/usr/bin/env python3.6
# encoding: utf-8
'''
demo 文件
'''
import os

import xlwt


# workbook = xlwt.Workbook()
# worksheet = workbook.add_sheet('My sheet')
# # 合并第0行的第0列到第3列。
# font = xlwt.Font()
# font.blod = True
#
# pattern_top = xlwt.Pattern()
# pattern_top.pattern = xlwt.Pattern.SOLID_PATTERN
# pattern_top.pattern_fore_colour = 5
#
# style = xlwt.XFStyle()
# style.font = font
# alignment = xlwt.Alignment()
# alignment.horz = xlwt.Alignment.HORZ_CENTER
# alignment.vert = xlwt.Alignment.VERT_CENTER
# style.alignment = alignment
#
# # 合并第1行到第2行的第0列到第3列。
# worksheet.write_merge(0, 0, 0, 0, 'Second Merge', style)

# worksheet.write_merge(4, 6, 3, 6, 'My merge', style)

# workbook.save('Merge_cell.xls')
def remove_duplicate(list1) -> list:
    return list(set(list1))


def get_all_files_list(path: str, all_file_list: list) -> list:
    app_file = os.walk(path)
    print("=========== file_full_path file_list app_file = ", app_file)
    print("=========== file_full_path file_list path = ", path)
    for path, dir_list, file_list in app_file:
        for file in file_list:
            file_path = os.path.join(path, file)
            all_file_list.append(file_path)
            # print("=========== file_full_path file_list file = ", path, "    ", file)
        for dir_name in dir_list:
            get_all_files_list(path + os.sep + dir_name, all_file_list)
    return all_file_list


all = get_all_files_list("/Volumes/Matthew/code/mxchip/mxapp_smartplus_ios", [])
print("the strings file of the project, remove_duplicate, total = " + str((remove_duplicate(all)).__len__()))
