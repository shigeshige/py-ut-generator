"""
テストコードの生成ツール

copyrigth https://github.com/shigeshige/py-ut-generator
"""

import sys

from pyutgenerator import files, ast_util


def parse_file(file_name):
    modu = ast_util.create_ast(file_name)
    funcs = ast_util.get_function(modu)
    pkg, mdn = files.get_package_moduel(file_name)
    ts_file = files.get_test_file_name(pkg, mdn)

    ttt = ast_util.parse_import(modu, pkg, mdn)
    for f1 in funcs:
        ttt += ast_util.parse_func(f1, pkg, mdn, modu)
    files.write_file(ts_file, ttt)


def output(file_name, txt):
    pass


def main():
    f = sys.argv[1]
    parse_file(f)
    return


if __name__ == "__main__":
    main()
