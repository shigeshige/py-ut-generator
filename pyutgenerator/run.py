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
    if not module:
        print('File not Found :' + str(file_name))
        return
    funcs = ast_util.get_function(module)
    pkg, mdn = files.get_package_moduel(file_name)
    ts_file = files.get_test_file_name(pkg, mdn)
    old_test = ast_util.create_ast(ts_file)
    append = old_test is not None
    if append:
        ttt = ''
    else:
        ttt = ast_util.parse_import(module, pkg, mdn)

    for func in funcs:
        if ast_util.has_test_function(old_test, func):
            continue
        ttt += ast_util.parse_func(func, pkg, mdn, module)
    files.write_file(ts_file, ttt, append)


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
