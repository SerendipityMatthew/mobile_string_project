import os
from xml.dom import minidom
from xml.etree import ElementTree  # 导入ElementTree模块

import pandas
from deprecated import deprecated

"""
 这个文件主要是用来生成 android 的 string.xml 文件的, 并且格式化该文件
"""

"""
格式化 xml 文件, 这个方式已经废弃了, 并不可靠, 他会将中文写成数字的问题
"""


@deprecated(version="1.0", reason="这个方式已经废弃了, 并不可靠, 他会将中文写成数字的问题")
def pretty_xml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作


def pretty_xml_to_file(source_file, file_path):
    """
    正在使用的格式化xml文件的方法
    """
    import xml.dom.minidom
    dom = xml.dom.minidom.parse(source_file)  # or xml.dom.minidom.parseString(xml_string)
    pretty_xml_as_string = dom.toprettyxml()
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    path = file_path + os.sep + source_file

    with open(path, "w") as f:
        f.write(pretty_xml_as_string)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def generate_string_res(string_value_dict, file_path: str, file_name: str):
    """
    将 android 的字符串 写成 android的 strings.xml 的格式
    """
    from xml.etree.ElementTree import Element, SubElement, ElementTree

    root = Element('resources')
    # 生成第一个子节点 head]
    print("string_value_dict = " + str(string_value_dict))
    for name_key in string_value_dict:
        head = SubElement(root, 'string')
        string_value = string_value_dict[name_key]
        # print("string_value = " + string_value)
        if pandas.isna(string_value):
            print("string_value is nan = " + string_value)
            string_value = ""
        head.attrib["name"] = name_key
        string_value_str = str(string_value)

        print("=========== string_value = " + string_value_str)
        head.text = string_value_str
    tree = ElementTree(root)
    print("generate_string_res: tree = " + str(tree))
    print("generate_string_res: file_name = " + str(file_name))
    tree.write(file_name, encoding='utf-8')
    pretty_xml_to_file(file_name, file_path)


def test_xml_generator():
    """
    用来测试 generate_string_res 和 pretty_xml_to_file 方法是否正确执行的
    """
    name_key_value = {"Matthew": "Mona", "Mona": "1111"}
    generate_string_res(name_key_value, "pretty_xml_to_file_test.xml", "pretty_xml_to_file_test.xml")

# test_xml_generator()
