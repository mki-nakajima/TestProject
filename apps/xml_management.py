'''
Created on 2019/01/14

@author: shunsuke
'''

import os
import shutil
from xml.etree import ElementTree

DEFAULT_TARGET_DIR = "/static/xml"
DEFAULT_TARGET_FILE = "/sample_xml_01.xml"
DEFAULT_TARGET_FILE_PATH = DEFAULT_TARGET_DIR + DEFAULT_TARGET_FILE
TEMP_FILE_PATH = DEFAULT_TARGET_DIR + "/sample_xml_tmp.xml"

def read_xml_file(target_file_path=DEFAULT_TARGET_FILE_PATH):
    target_file_path = os.getcwd() + target_file_path
    tree = ElementTree.parse(target_file_path)
    # dirタグ
    dir_text = tree.find('class/point').text
    print(dir_text)

    # nameタグ
    names = tree.findall('class/name')
    for name in names:
        print(name.text)

def write_xml_file(target_file_path=TEMP_FILE_PATH):
    target_file_path = os.getcwd() + target_file_path
    if os.path.isfile(target_file_path):
        os.remove(target_file_path)
    shutil.copy2(os.getcwd() + DEFAULT_TARGET_FILE_PATH, target_file_path)

    # xmlファイルの読み込み
    tree = ElementTree.parse(target_file_path)
    # 特定のタグの値を変更
    new_change = tree.find('change')
    new_change.text = "新しい値"
    # 対象の複数タグの値を変更
    classes = tree.findall('class')
    for class_tag in classes:
        name = class_tag.find('name')
        print(name.text)
        name.text = name.text + ' mod'
        print(name.text)

    # 上書き保存
    tree.write(target_file_path, 'utf-8', True)


if __name__ == '__main__':
    read_xml_file()
    write_xml_file()
