"""
copyrigth https://github.com/shigeshige/py-ut-generator
"""

import ast
import os
import pathlib


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()

def create_ast(file_name):
    """
    """
    src = read_file(file_name)
    return ast.parse(src, file_name)


def get_package_moduel(file_name):
    """
    パッケージ名とモジュール名を取得
    """
    modu = os.path.splitext(os.path.basename(file_name))[0]
    pth = pathlib.Path(file_name).absolute()
    pkg = os.path.dirname(str(pth.relative_to(pathlib.Path.cwd())))
    pkg = pkg.replace('\\', '.')
    pkg = pkg.replace('/', '.')
    if os.path.basename(file_name) == pkg:
        pkg = ''
    return pkg, modu
