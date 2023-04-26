"""
@author: Lakshmi Dinesh
A utility module with functions that can be used by multiple classes within the application
"""

import os.path
import textwrap
import time
import traceback
from time import sleep
import os
import datetime
from tkinter import messagebox as mb
from program_generator_constants import DIR_PATH_PYTHON, DIR_PATH_JAVA, LOG_DIR


def wrap_line(text):
    wrapper = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
    return wrapper.fill(text)


def wrap_content(paragraph):
    lines = paragraph.splitlines(True)
    wrapped_para = ""
    for line in lines:
        if len(line) > 100:
            wrapped_para += wrap_line(line) + "\n"
        else:
            wrapped_para += line
    return wrapped_para


def create_file_name():
    timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    return timestamp + '.txt'


def create_log_dir():
    try:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
    except Exception as e:
        print(f"ERROR: in output directory creation: {e}")
        traceback.print_exc()


def create_dir_path(lang, level, topic):
    dir_path_1 = DIR_PATH_PYTHON if lang == 'Python' else DIR_PATH_JAVA
    dir_path = os.path.join(dir_path_1, f'{level}/{topic}/')
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except Exception as e:
            print(f"ERROR: in output directory ({dir_path}) creation: {e}")
            traceback.print_exc()
    return dir_path


def create_file_path(dir_path, file_name):
    file_path = os.path.join(dir_path, file_name)
    return file_path


def wait_for_file(file_path):
    while not os.path.isfile(file_path):
        sleep(0.5)
    return True


def save_to_file(file_path, content):
    f_path = file_path
    try:
        with open(f_path, 'w') as fileObj:
            fileObj.write(content)
            fileObj.flush()
            time.sleep(0.5)
            return True
    except FileNotFoundError:
        print("ERROR: File not found")
        return False
    except PermissionError:
        print("ERROR: File permission denied")
        return False
    except TypeError:
        print("ERROR:Invalid file name")
        return False
    except Exception as e:
        print(f"Unexpected error encountered with file write: {e}")
        traceback.print_exc()
        return False


def validate_name(f_name, l_name):
    if "" == (f_name or l_name):
        show_message('Error', 'At least one of the name fields should not be left empty!')
        return False
    return True


def show_message(message_type, text):
    mb.showwarning(title=message_type, message=text)
