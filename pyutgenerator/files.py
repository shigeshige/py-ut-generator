"""
Generate test code tool

copyrigth https://github.com/shigeshige/py-ut-generator
"""

import os
import pathlib

from pyutgenerator.objects import Module


def read_file(file_name):
    """
    read utf8 txt file.
    """
    if not os.path.exists(file_name):
        return None

    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(file_name, txt, append=False):
    """
    write txt file.
    and mkdir directory
    """
    mode = 'w'
    if append and os.path.exists(file_name):
        mode = 'a'
    if not txt:
        print('No output')
        return
    dirs = os.path.dirname(file_name)
    os.makedirs(dirs, exist_ok=True)
    with open(file_name, mode=mode, encoding='utf8') as fip:
        fip.write(txt)


def get_package_moduel(file_name) -> Module:
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
    return Module(pkg, modu)
