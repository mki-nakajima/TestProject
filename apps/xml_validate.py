# -*- coding: utf-8 -*-
"""
機能名：XMLファイルフォーマットチェック機能

概要：XMLのフォーマットがルールに則ったものかチェックする
        求められている機能：
            １．XMLのタグ構成が設計通りかどうか
            ２．設計には、
                    １．タグの親子関係
                    ２．存在が必須かどうか（必ず1つ存在、0個以上存在、など）
                    ３．型（半角数値のみ、全角英数・記号、など）
                がある
            ３．これらをチェックし、

  1 中嶋    2019/04/10 初版作成
"""
import re
import traceback
import csv
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring

# 文字コード
DEFAULT_CHARSET = "utf-8"
# 設定ファイルの要素数
TAG_EXISTS_COLUMN_COUNT = 3
TAG_VALUE_COLUMN_COUNT = 4
# 設定ファイルのインデックス
TAG_EXISTS_TARGET_TAG_POS = 0
TAG_EXISTS_EXPECTED_TAG_POS = 1
TAG_EXISTS_EXPECTED_TAG_CONTENT_MODEL_POS = 2
TAG_VALUE_TARGET_TAG_POS = 0
TAG_VALUE_REGEXP_POS = 1
TAG_VALUE_ALLOW_BLANK_POS = 2
TAG_VALUE_DEFAULT_POS = 3
# 繰り返し記号
ZERO_OR_MORE = "*"
ONE_OR_MORE = "+"
# 空白許可の値
ALLOW_BLANK = "1"
# 許容する値（正規表現）
# 全角半角文字数値記号なんでもOK
REGEXP_ALL_OK = ""


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
    print("START VALIADTE UNIFICATION.\n")
    # XMLファイル読込
    xml_file = None
    try:
        xml_file = parse(xml_file_path)
    except Exception:
        print("xml read failed.")
        print(traceback.format_exc())
        return False
    root_element = xml_file.getroot()
    print("------------ original -------------")
    print(tostring(root_element, encoding="unicode"))
    print("------------ original -------------")

    # 設定ファイルを読み込む
    # 内容をすべてリストに格納する
    conf_csv_lines = []
    with open(validate_config, "r", encoding="utf-8") as conf_file:
        conf_reader = csv.reader(conf_file, delimiter="\t")
        # 再帰的に設定ファイルの値を使用するので、いったんすべてリストに格納する
        for line in conf_reader:
            conf_csv_lines.append(line)
    # 設定ファイル内容を基にチェックする
    for conf_line in conf_csv_lines:
        # タブ区切りの要素数で処理体系が変わるため、判定する
        if len(conf_line) == TAG_EXISTS_COLUMN_COUNT:
            # タグの存在をチェックする
            validate_tag_exists(root_element,
                                conf_line,
                                conf_csv_lines,
                                auto_fix)
        elif len(conf_line) == TAG_VALUE_COLUMN_COUNT:
            # タグの値をチェックする
            validate_tag_value(root_element, conf_line)
        else:
            print("Invalid Format:" + "\t".join(conf_line))

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
    print("FINISH VALIADTE UNIFICATION.")


def validate_tag_exists(root_element, conf_line, conf_csv_lines, auto_fix):
    '''
    タグの親子関係をチェックするメソッド

    設定データのフォーマットと現在のファイルが一致するかチェックする
    一致しない場合エラー終了

    @param object ルートエレメント
    @param string[] 設定ファイルの一行のデータ
    @return boolean チェック結果
    '''
    # チェック対象のタグ取得
    target_tag = conf_line[TAG_EXISTS_TARGET_TAG_POS]
    # チェック対象のタグの直下にあるはずのタグリスト取得（カンマ区切りの文字列）
    expected_tag = conf_line[TAG_EXISTS_EXPECTED_TAG_POS]
    # あるはずのタグリストの内容モデル（1個あるとか0個以上あるとか）
    expected_tag_content_model\
        = conf_line[TAG_EXISTS_EXPECTED_TAG_CONTENT_MODEL_POS]

    # チェック対象のタグを検索・処理
    target_tag_list = root_element.findall(target_tag)
    # 先のチェックで使用するリスト
    expected_tag_list = expected_tag.split(",")
    expected_tag_content_model_list = expected_tag_content_model.split(",")
    for tag in target_tag_list:
        # 直下の子要素にどんなタグをいくつ持っているか調べる
        tag_count_dict = {}
        for c_tag in tag:
            if c_tag.tag not in expected_tag_list:
                # 想定していないタグを持っている場合、削除する
                tag.remove(c_tag)
            else:
                # 想定しているものは数える
                tag_count = tag_count_dict.get(c_tag.tag, 0)
                tag_count_dict[c_tag.tag] = (tag_count + 1)

        # 直下のタグをチェックする
        for expected_tag_name, expected_tag_content_model\
                in enumerate(expected_tag_list,
                             expected_tag_content_model_list):
            print("expected:" + expected_tag_name)
            print("content_model:" + expected_tag_content_model)
            if expected_tag_name in tag_count_dict:
                # 想定するタグが既に存在する場合、数をチェックする
                if expected_tag_content_model == ZERO_OR_MORE:
                    # 内容モデルが0以上を表す"*"の場合
                    # 要素がなくても問題ないので何もしない
                    pass
                elif expected_tag_content_model == ONE_OR_MORE\
                        and tag_count_dict.get(expected_tag_name) < 1:
                    # 内容モデルが1以上を表す"+"かつ、子要素のタグが1より少ない場合
                    print("Tag[" + expected_tag_name + "] is Nothing.")
                    # タグを追加するか
                    if auto_fix:
                        c_tag = create_child_tag(tag, conf_csv_lines)
                        SubElement(tag, c_tag)
                    else:
                        # エラー出力
                        print("エラー")
                        return False
                elif expected_tag_content_model\
                        > tag_count_dict.get(expected_tag_name):
                    # 内容モデルが要素数を表す数値で、カウント結果より多い場合
                    # タグを追加する
                    print("Tag[" + expected_tag_name + "] is not Enough.")
                    # タグを追加するか
                    if auto_fix:
                        c_tag = create_child_tag(tag, conf_csv_lines)
                        SubElement(tag, c_tag)
                    else:
                        # エラー出力
                        print("エラー")
                        return False
                elif expected_tag_content_model\
                        < tag_count_dict.get(expected_tag_name):
                    # 内容モデルが要素数を表す数値で、カウント結果より多い場合
                    # エラーとする
                    print("エラー")
                    return False
                else:
                    # エラー出力
                    print("エラー？")
                    return False
            elif auto_fix:
                # タグを追加する
                c_tag = create_child_tag(tag, conf_csv_lines)
                SubElement(tag, c_tag)


def validate_tag_value(root_element, conf_line):
    '''
    タグの値をチェックするメソッド
    タグの値に関する設定をチェックする

    処理内容（下記例）
    引数1のコピー元ディレクトリ内の情報を、引数2のコピー先にコピーします。
    コピー先のディレクトリが存在しない場合、フォルダを作成します。
        １．コピー先のディレクトリを作成する。
        ２．shutil.copytreeでディレクトリの情報をコピーする。
        ３．結果を返却する。
    @param string  コピー元ディレクトリ
    @return param string  コピー先ディレクトリ
    @raises boolean  処理結果(True:コピー成功、False:コピー失敗)
    '''
    target_tag_name = conf_line[TAG_VALUE_TARGET_TAG_POS]
    target_tag_list = root_element.findall(target_tag_name)
    conf_line[TAG_VALUE_ALLOW_BLANK_POS]
    regexp_pattern = conf_line[TAG_VALUE_REGEXP_POS]
    conf_line[TAG_VALUE_TARGET_TAG_POS]
    result = False
    # どんな文字でもアリならチェックする意味ないので正常終了
    if conf_line[TAG_VALUE_REGEXP_POS] == REGEXP_ALL_OK:
        result = True
    else:
        # 正規表現にマッチしているかチェックする
        for target_tag in target_tag_list:
            if re.match(regexp_pattern, target_tag.text) is None:
                raise Exception("定義に一致しません。[regexp:" + regexp_pattern + "/text:" + target_tag.text + "]")
        result = True
    return result


def create_child_tag(target_tag_name, conf_csv_lines):
    '''
    子要素タグ追加メソッド

    引数のタグ名を設定ファイルから検索し、子要素があれば、自身を実行する
    値の設定があれば、設定する
    @param object チェック対象のタグ
    @param object 設定ファイル
    @return object 作成した子要素エレメント
    '''
    for conf_line in conf_csv_lines:
        if target_tag_name == conf_line[TAG_EXISTS_TARGET_TAG_POS]:
            tmp_tag_name = target_tag_name.split("/")[-1]
            if len(conf_line) == TAG_EXISTS_COLUMN_COUNT:
                # 子要素があるので自信を実行する
                for c_tag_name\
                        in conf_line[TAG_EXISTS_EXPECTED_TAG_POS].split(","):
                    c_tag = create_child_tag(
                        target_tag_name + "/" + c_tag_name,
                        conf_csv_lines
                    )
                    tag = Element(tmp_tag_name)
                    SubElement(tag, c_tag)
            elif len(conf_line) == TAG_VALUE_COLUMN_COUNT:
                # タグの値の設定なので、タグを追加する
                if conf_line[TAG_VALUE_ALLOW_BLANK_POS] == ALLOW_BLANK:
                    tag = Element(tmp_tag_name)
                    tag.text = conf_line[TAG_VALUE_DEFAULT_POS]
                else:
                    print("エラー")
                    raise Exception(
                        "空白許可していないタグは自動生成不可能です。[" + target_tag_name + "/" + tmp_tag_name + "]")
    return tag


if __name__ == '__main__':
    print("XML file validate start.\n")
    sample_xml_path = "./static/xml_validate/sample_01.xml"
    validate_config = "./static/xml_validate/sample_01.csv"

    validate_result = False
    print("XML:" + sample_xml_path)
    print("CONF:" + validate_config + "\n")
    try:
        validate_result = validate_unification_xml(sample_xml_path,
                                                   validate_config)
    except Exception:
        print("xml validate failed.")
        print(traceback.format_exc())

    print("XML file validate finish.")
