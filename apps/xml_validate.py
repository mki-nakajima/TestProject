# -*- coding: utf-8 -*-
"""
機能名：XMLファイルフォーマットチェック機能

概要：XMLのフォーマットがルールに則ったものかチェックする

  1 中嶋    2019/04/10 初版作成
"""

import traceback
import csv
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring

# 文字コード
DEFAULT_CHARSET = "utf-8"
# 設定ファイルのインデックス
TARGET_TAG_NAME_POS = 0
EXPECTED_TAG_NAME_POS = 1
EXPECTED_TAG_CONTENT_MODEL_POS = 2


def validate_unification_xml(xml_file_path, validate_config, auto_fix=True):
    '''
    XMLファイルバリデーションチェックメソッド

    処理内容
    引数のXMLファイルを、引数の設定に基づいてチェックする
    反しているものは、都度タグを追加する
    @param string  コピー元ディレクトリ
    @param string  コピー元ディレクトリ
    @param boolean 自動修復するかしないか
    @return param string  結果？
    '''
    # XMLファイル読込
    try:
        xml_file = parse(xml_file_path)
    except Exception:
        print("xml read failed.")
        print(traceback.format_exc())
        return False
    root_element = xml_file.getroot()
    print(tostring(root_element, encoding="unicode"))
    print("root tag:" + root_element.tag)

    # 設定ファイルを読み込む
    conf_file = open(validate_config, "r", encoding="utf-8")
    conf_reader = csv.reader(conf_file, delimiter="\t")
    # 設定ファイルを基にチェックする
    for conf_line in conf_reader:
        # チェック対象のタグ取得
        target_tag = conf_line[TARGET_TAG_NAME_POS]
        # チェック対象のタグの直下にあるはずのタグリスト取得（カンマ区切りの文字列）
        expected_tag_list = conf_line[EXPECTED_TAG_NAME_POS]
        # あるはずのタグリストの内容モデル（1個あるとか0個以上あるとか）
        expected_tag_content_model = conf_line[EXPECTED_TAG_CONTENT_MODEL_POS]
        print("------------------------------------------------------")
        print(target_tag + "/" + expected_tag_list + "/" + expected_tag_content_model)
        # チェック対象のタグを検索・処理
        target_tag_list = root_element.findall(target_tag)
        print(target_tag + " len:" + str(len(root_element.findall(target_tag))))
        for tag in target_tag_list:
            # 直下の子要素にどんなタグをいくつ持っているか調べる
            tag_count_dict = {}
            for c_tag in tag:
                tag_count = tag_count_dict.get(c_tag.tag, 0)
                tag_count_dict[c_tag.tag] = (tag_count + 1)
            print(tag_count_dict)
            # 直下にあるはずのタグを持っているかチェックする
            for expected_tag_name in expected_tag_list.split(","):
                print("expected:" + expected_tag_name)
                if tag_count_dict.get(expected_tag_name, 0) <= 0:
                    print("Tag[" + expected_tag_name + "] is Nothing.")
                    if auto_fix:
                        SubElement(tag, expected_tag_name)
            print(tostring(root_element, encoding="unicode"))

    # XMLファイル保存
    try:
        if auto_fix:
            file_name_front = "." + xml_file_path.split(".")[1]
            file_name_back = xml_file_path.split(".")[2]
            xml_file.write(file_name_front + "_mod." + file_name_back,
                           DEFAULT_CHARSET,
                           xml_declaration=True)
    except Exception:
        print("XML save failed.")
        print(traceback.format_exc())
        return False


if __name__ == '__main__':
    print("XML file validate start.")
    sample_xml_path = "./static/xml_validate/sample_01.xml"
    validate_config = "./static/xml_validate/sample_01.csv"

    validate_result = False
    try:
        validate_result = validate_unification_xml(sample_xml_path,
                                                   validate_config)
    except Exception:
        print("xml validate failed.")
        print(traceback.format_exc())

    print("XML file validate finish.")
