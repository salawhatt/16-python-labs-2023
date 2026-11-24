import argparse
import os
import sys
import shutil
import winreg
import winreg as wrg


def rename(path):
    if not os.path.isfile(path):
        sys.exit("This file doesn't exist")
    print('Enter a new file name along with the extension: ')
    new_name = input()
    if path.find("\\", 0, 3) == -1:
        os.rename(path, new_name)
    else:
        old_name = os.path.basename(path)
        os.rename(path, path.replace(old_name, new_name))


def read(path):
    if not os.path.isfile(path):
        sys.exit("This file doesn't exist")
    text_file = open(path, "r")
    print(text_file.read())


def write(path):
    if not os.path.isfile(path):
        sys.exit("This file doesn't exist")
    with open(path, 'a+') as file:
        print("Enter text:")
        file.write(input())


def create(path):
    if os.path.isfile(path):
        sys.exit("File already exists")
    with open(path, 'w+') as file:
        sys.exit("File created")


def delete(path):
    if not os.path.isfile(path):
        sys.exit("This file doesn't exist")
    os.remove(path)


def copy(path, destination):
    if not os.path.isdir(destination):
        sys.exit("Directory/catalog doesn't exist")
    elif os.path.isfile(destination + '\\' + os.path.basename(path)):
        sys.exit("File already exists")
    elif path.find("\\", 0, 3) == -1:
        shutil.copy(os.path.abspath(path), destination)
    else:
        shutil.copy(path, destination)


def create_key(path_key, name_key):
    cur_proc_object = wrg.OpenKeyEx(wrg.HKEY_CURRENT_USER, path_key)
    new_key = wrg.CreateKey(cur_proc_object, name_key)
    if new_key:
        wrg.CloseKey(new_key)


def write_key(path_key, name_key, value_key, value_name):
    cur_proc_object = wrg.OpenKeyEx(wrg.HKEY_CURRENT_USER, path_key)
    new_key = wrg.CreateKey(cur_proc_object, name_key)
    wrg.SetValueEx(new_key, value_name, 0, winreg.REG_SZ, value_key)
    if new_key:
        wrg.CloseKey(new_key)


def delete_key(path_key, name_key):
    cur_proc_object = wrg.OpenKeyEx(wrg.HKEY_CURRENT_USER, path_key)
    key = wrg.CreateKey(cur_proc_object, name_key)
    wrg.DeleteKey(key, "")


def processing_arguments(file_action, reg_action, path, destination, path_key, name_key, value_key, value_name):
    if file_action is not None:
        if path is None:
            sys.exit("File path or name not entered")
        elif file_action == 'read':
            read(path)
        elif file_action == 'write':
            write(path)
        elif file_action == 'rename':
            rename(path)
        elif file_action == 'create':
            create(path)
        elif file_action == 'delete':
            delete(path)
        elif file_action == 'copy':
            copy(path, destination)

    elif reg_action is not None:
        if reg_action == 'write':
            write_key(path_key, name_key, value_key, value_name)
        elif reg_action == 'create':
            create_key(path_key, name_key)
        elif reg_action == 'delete':
            delete_key(path_key, name_key)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-fs", "--file_sys", type=str, help='file system actions',
                        choices=['read', 'write', 'copy', 'rename', 'create', 'delete'])
    parser.add_argument("-p", "--path", type=str, help='path to the file', metavar='', default='NewFile.txt')
    parser.add_argument("-d", "--destination", type=str, help='file destination', metavar='')
    parser.add_argument("-rg", "--register", type=str, help='register actions', choices=['write', 'create', 'delete'])
    parser.add_argument("-pk", "--path_key", type=str, help='path to registry key', default=r'Software\\', metavar='')
    parser.add_argument("-nk", "--name_key", type=str, help='new key name', metavar='')
    parser.add_argument("-vk", "--value_key", type=str, help='key value', metavar='')
    parser.add_argument("-vn", "--value_name", type=str, help='name value', metavar='')
    args = parser.parse_args()
    processing_arguments(args.file_sys, args.register, args.path, args.destination, args.path_key, args.name_key, args.value_key, args.value_name)


main()
