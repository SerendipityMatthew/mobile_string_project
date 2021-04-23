#!/usr/bin/env python3.6
# encoding: utf-8
'''
demo 文件
'''
import xlwt

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('My sheet')
# 合并第0行的第0列到第3列。
font = xlwt.Font()
font.blod = True

pattern_top = xlwt.Pattern()
pattern_top.pattern = xlwt.Pattern.SOLID_PATTERN
pattern_top.pattern_fore_colour = 5

style = xlwt.XFStyle()
style.font = font
alignment = xlwt.Alignment()
alignment.horz = xlwt.Alignment.HORZ_CENTER
alignment.vert = xlwt.Alignment.VERT_CENTER
style.alignment = alignment

# 合并第1行到第2行的第0列到第3列。
worksheet.write_merge(0, 0, 0, 0, 'Second Merge', style)

# worksheet.write_merge(4, 6, 3, 6, 'My merge', style)

workbook.save('Merge_cell.xls')
