'''
Created on 2018/12/22

@author: shunsuke
'''
import sys
import os
import shutil


# 作業する所までのパス
WORK_BASE_DIR = '/tmp'
# 作業ディレクトリ
WORK_DIRS = ['/123', '/456/aaa', '/789/45b/67c']


def create_dir():
    # 基準のディレクトリ
    base_dir = os.getcwd()
    # ディレクトリ作成
    for work_dir in WORK_DIRS:
        target = base_dir + WORK_BASE_DIR + work_dir
        os.makedirs(target, exist_ok=True)


def remove_dir():
    print('delete stop.')
#     shutil.rmtree('.' + WORK_BASE_DIR)
#     os.makedirs('.' + WORK_BASE_DIR)

#     # 基準のディレクトリ
#     base_dir = os.getcwd()
#     # ディレクトリ移動
#     os.chdir(base_dir + WORK_BASE_DIR)
#     # ディレクトリ削除
#     for work_dir in WORK_DIRS:
#         print('delete .' + work_dir)
#         shutil.rmtree('.' + work_dir)

if __name__ == '__main__':
    # 引数チェック
    if len(sys.argv) < 2:
        print('please exec mode')
        # 終了
        sys.exit()

    # 開始メッセージ
    print('START.')

    # 起動モード取得
    exec_mode = sys.argv[1]
    if exec_mode == '1':
        print('Dir create start.')
        create_dir()
        print('Dir create finish.')
    elif exec_mode == '2':
        print('Dir remove start.')
        remove_dir()
        print('Dir remove finish.')
    else:
        print('Not supported exec_mode:' + exec_mode)

    # 終了メッセージ
    print('FINISH.')
