"""
copyrigth https://github.com/shigeshige/py-ut-generator
"""

import os
import pathlib


def read_file(file_name):
    """
    read utf8 txt file.
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(file_name, txt):
    """
    write txt file.
    and mkdir directory
    """
    dirs = os.path.dirname(file_name)
    os.makedirs(dirs, exist_ok=True)
    with open(file_name, mode='w') as f:
        f.write(txt)


def get_package_moduel(file_name):
    """
    get package name and module name from file name.
    """
    modu = os.path.splitext(os.path.basename(file_name))[0]
    pth = pathlib.Path(file_name).absolute()
    pkg = os.path.dirname(str(pth.relative_to(pathlib.Path.cwd())))
    pkg = pkg.replace('\\', '.')
    pkg = pkg.replace('/', '.')
    if os.path.basename(file_name) == pkg:
        pkg = ''
    return pkg, modu


def get_test_file_name(pkg, mdn):
    """
    get test file name from input file.
    """
    return 'tests/' + pkg.replace('.', '/') + '/test_' + mdn + '.py'
