import json
import time
import os
import shutil
import xmltodict
import pandas as pd
from pprint import pprint
from pathlib import Path

# ?   _       _    __                        _
# ?  |||__   (_)  / _|  _ __    ___    ___  | |_
# ?  ||'_ \  | | | |_  | '__|  / _ \  / __| | __|
# ?  |||_) | | | |  _| | |    | (_) | \__ \ | |_
# ?  |_.__/  |_| |_|   |_|     \___/  |___/  \__|


MY_USER = os.path.expanduser('~')

def goto(path):
    os.chdir(path)


def open_json(file_name):
    with open(file_name, "r", encoding="utf8") as f:
        return json.load(f)


def write_json(file_name, str):
    with open(file_name, "w", encoding="utf8") as f:
        json.dump(str, f, indent=4)
        f.close()


class BRAE(object):
    __slot__ = "companies"

    def p_companies():
        return {
            "empresa": {
                "NUMBER": "COMPANY NAME"                
            },
            "keys": {
                "COMPANY ID": "API KEY"                
            },
        }

    def __init__(self, companies=p_companies()):
        self.companies = companies


class types(object):
    __slot__ = "sufix"

    def p_sfx():
        return {
            ".xlsx": {
                "tipo": "Excel",
                "pd_function": "frame_xls(**kwargs)",
                "altern": "xls"
            },
            ".xls": {
                "tipo": "Excel",
                "pd_function": "read_excel",
                "altern": "xlsx"
            },
            ".json": {
                "tipo": "Json",
                "pd_function": "read_json",
                "altern": None
            },

        }

    def __init__(self, sufix=p_sfx()):
        self.sufix = sufix


def delay(x):
    time.sleep(x)
    print("...")


def sufix(file):
    return {file: file[file.rfind('.'):]}


def dropbox_path():
    cur_user = os.path.expanduser("~")
    dropbox_folder = os.path.join(cur_user, "PATH GOES HERE")
    nfe_total_f = os.path.join(dropbox_folder, "PATH GOES HERE")
    os.chdir(nfe_total_f)
    print(os.getcwd())
    delay(1)


def sumData_path():
    cur_user = os.path.expanduser("~")
    dropbox_folder = os.path.join(cur_user, "PATH GOES HERE")
    nfe_total_f = os.path.join(
        dropbox_folder, "PATH GOES HERE")
    os.chdir(nfe_total_f)
    print(os.getcwd())
    delay(1)


def nfe_pendingFolder():
    cur_user = os.path.expanduser("~")
    dropbox_folder = os.path.join(cur_user, "PATH GOES HERE")
    nfe_total_f = os.path.join(dropbox_folder, "PATH GOES HERE")
    os.chdir(nfe_total_f)
    print(os.getcwd())
    delay(1)


def list_files():
    return os.listdir()


def find(arg):
    _ = list_files()
    for i in _:
        if arg in i:
            return i


def p_join(path, target):
    return os.path.join(path, target)


def filter_list(list, arg):
    _ = []
    for item in list:
        if arg in item:
            _.append(item)
        else:
            pass
    return _


def frame_xls(file_name, sheet):
    return pd.read_excel(file_name, sheet_name=sheet, engine="openpyxl")


def open_csv(file_name, separator):
    return pd.read_csv(file_name, sep=separator, encoding="utf8")


def _split(path, position):
    for i in range(0, position):
        _ = os.path.split(path)
        path = _[0]    
    return path


def open_xml(file_name):
    with open(file_name, "r", encoding="UTF-8") as file:
        return json.loads(json.dumps(xmltodict.parse(file.read())))


def nice_p(object):
    pprint(object)


def recort(orign, destiny):
    try:
        try:
            shutil.copyfile(orign, destiny)
        except:
            os.makedirs(_split(destiny, 0))
            shutil.copyfile(orign, destiny)
    except:
        pass
    os.remove(orign)


def query(frame,col, val):
    return frame.query(f'{col}=="{val}"')




