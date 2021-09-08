"""
Generate test code tool



copyrigth https://github.com/shigeshige/py-ut-generator
"""
import argparse

import sys


from pyutgenerator import files, ast_util


def parse_file(file_name, renew=False):
    """
    generate test code.
    """
    module = ast_util.create_ast(file_name)
    if not module:
        print('File not Found :' + str(file_name))
        return
    funcs = ast_util.get_function(module)
    cls_funcs = ast_util.get_function_class(module)
    pkg, mdn = files.get_package_moduel(file_name)
    ts_file = files.get_test_file_name(pkg, mdn)
    old_test = ast_util.create_ast(ts_file)
    append = old_test is not None
    if renew:
        append = False
        old_test = None
    if append:
        ttt = ''
    else:
        ttt = ast_util.parse_import(module, pkg, mdn)

    for func in funcs:
        if ast_util.has_test_function(old_test, func):
            continue
        ttt += ast_util.parse_func(func, pkg, mdn, module)

    for func, clazz in cls_funcs:
        if ast_util.has_test_function(old_test, func):
            continue
        ttt += ast_util.parse_func(func, pkg, mdn, module, clazz)

    files.write_file(ts_file, ttt, append)


def output(file_name, txt):
    pass


def main():
    """
    main function.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="input python filename")
    parser.add_argument("--ovewrite", help="overwrite test code", action="store_true")
    args = parser.parse_args()
    print(args.filename)
    print(args.ovewrite)
    parse_file(args.filename, args.ovewrite)
    return


if __name__ == "__main__":
    main()
