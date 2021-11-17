
import os


def read_file(file_name):
    """
    read utf8 txt file.
    """
    if not os.path.exists(file_name):
        return None

    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()
