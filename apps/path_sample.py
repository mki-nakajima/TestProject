'''
Created on 2018/12/09

@author: shunsuke
'''


import glob
import configparser
import re
import os

def path_init(path):
    global _settings_path, _rootdir, _objConf
    _settings_path = path
    _objConf = configparser.ConfigParser()
    _objConf.read(_settings_path, "UTF-8")
    _rootdir = get_conf("settings", "rootdir")


def get_conf(section, option):
    setting_value = _objConf.get(section, option)
    return setting_value


def get_pathlist(status, analysis_id, *target):
    regfmt = os.path.join(_rootdir,
                          status + '_' + analysis_id,
                          "*/*/*/*/*/*/",
                          *target)
    path_list = glob.glob(regfmt, recursive=False)
    return path_list


if __name__ == '__main__':
    print('start.')
    print(get_pathlist('status', '123'))
