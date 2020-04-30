"""
Generate test code tool

copyrigth https://github.com/shigeshige/py-ut-generator
"""

import sys

from pyutgenerator import files, ast_util


def parse_file(file_name):
    """
    generate test code.
    """
    module = ast_util.create_ast(file_name)
    funcs = ast_util.get_function(module)
    pkg, mdn = files.get_package_moduel(file_name)
    ts_file = files.get_test_file_name(pkg, mdn)

    ttt = ast_util.parse_import(module, pkg, mdn)
    for func in funcs:
        ttt += ast_util.parse_func(func, pkg, mdn, module)
    files.write_file(ts_file, ttt)


def output(file_name, txt):
    pass


def main():
    """
    main function.
    """
    f_name = sys.argv[1]
    parse_file(f_name)
    return


if __name__ == "__main__":
    main()
