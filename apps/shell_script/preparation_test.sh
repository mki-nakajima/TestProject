#!/bin/bash
# ITの準備をするスクリプト
# 引数はテストケース番号
# テスト用ディレクトリ（テスト用ディレクトリ/テストケース番号/input）から、
# そっくりそのままコピーする（フルパス）
# テスト用ディレクトリが存在しない場合、inputに使用するディレクトリ一覧をコピーする
# その際、テスト用ディレクトリを作成する

# テストデータディレクトリ
test_root_dir=/Applications/Eclipse_4.7.0.app/Contents/workspace/TestProject/apps/shell_script

# inputに使用するディレクトリ
input_dir_list=(`cat ../input_target_dirs.txt`)

# 特定のディレクトリ以下のファイルをすべてフルパスで表示するコマンド
# ls -1 -d $(find `pwd`)

for dir_name in  "${input_dir_list[@]}"
do
  echo $dir_name
done

echo "Hello World!!"

target=/Applications/Eclipse_4.7.0.app/Contents/workspace/TestProject/apps/shell_script/test_data
ls -1 -d $(find ${target})