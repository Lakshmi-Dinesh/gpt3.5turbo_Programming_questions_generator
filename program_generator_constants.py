"""
@author: Lakshmi Dinesh
A module that manages all the constants for the application.
Application engine customization made possible though this.
"""
DEBUG_CONSOLE_LOG = False

ENGINE = "gpt-3.5-turbo-0301"
JSON_LOG_FILE = "./out/logs/json_log.txt"
ROOT_DIR = "./out/"
LOG_DIR = "./out/logs/"
DIR_PATH_PYTHON = "./out/Python/"
DIR_PATH_JAVA = "./out/Java/"

PREFIX = "Generate "
POSTFIX = " level programming question(s) in "

LVL_QUESTIONS = {
    'Beginner': [i for i in range(1, 11)],
    'Intermediate': [i for i in range(1, 9)],
    'Advanced': [i for i in range(1, 6)],
    'Combined': [i for i in range(3, 19, 3)]
}

TOPICS = {
    'Python': {'Beginner': ['Strings', 'Lists', 'Tuples', 'Dictionaries', 'Functions', 'Classes', 'File handling',
                            'Exception handling'],
               'Intermediate': ['Datastructures', 'File handling', 'Classes', 'Decorators', 'Exception handling',
                                'Data visualization'],
               'Advanced': ['Datastructures', 'Search and sort algorithms', 'Data analysis', 'Data visualization',
                            'RegEx'],
               'Combined': ['Datastructures', 'File handling', 'Recursion']
               },
    'Java': {'Beginner': ['Strings', 'Arrays', 'Sets', 'Maps', 'Methods', 'Classes', 'File handling',
                          'Exception handling'],
             'Intermediate': ['ArrayLists', 'LinkedLists', 'HashMaps', 'Sets', 'File handling', 'Exception handling',
                              'Collections'],
             'Advanced': ['Datastructures', 'Search and sort algorithms', 'RegEx', 'Lambda functions'],
             'Combined': ['Datastructures', 'File handling', 'Recursion']
             }
}
