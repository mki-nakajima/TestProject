'''
Created on 2018/12/24

@author: shunsuke
'''
import os
import shutil

# 定数
# 作業する所までのパス
TMP_DIR = '/tmp'
# コピー元のディレクトリ
BASE_WORK_DIR = './address'
# コピー先のディレクトリ
WORK_DIR = './address_test'


def copy_test_dir_before_test():
    # テスト用の作業ディレクトリをコピーする
    # 基準のディレクトリ
    base_dir = os.getcwd()
    # コピー先に移動する
    os.chdir(base_dir + TMP_DIR)
    # ディレクトリをコピーする
    shutil.copytree(BASE_WORK_DIR, WORK_DIR)


def remove_test_dir_after_test():
    # テスト用の作業ディレクトリを削除する
#     # 基準のディレクトリ
#     base_dir = os.getcwd()
    # 作業用ディレクトリを削除する
    shutil.rmtree(WORK_DIR)
