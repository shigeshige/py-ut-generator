"""
Generate test code tool


copyrigth https://github.com/shigeshige/py-ut-generator
"""
import argparse

from pyutgenerator import ast_util, files, templates


def parse_file(file_name, renew=False):
    """
    generate test code.
    """
    module = ast_util.create_ast(file_name)
    if not module:
        print('File not Found :' + str(file_name))
        return

    pkg, mdn = files.get_package_moduel(file_name)
    t_file = files.get_test_file_name(pkg, mdn)
    ttt = make_test_code(module, pkg, mdn, renew)

    files.write_file(t_file, ttt, not renew)


def make_test_code(module, pkg, mdn, renew):
    """
    make test code text.
    """

    t_funcs = ast_util.get_function(module)
    t_funcs_cls = ast_util.get_function_class(module)
    # test file name
    t_file = files.get_test_file_name(pkg, mdn)
    old_test = ast_util.create_ast(t_file)

    if renew:
        ttt = templates.parse_import(pkg, mdn)
        old_test = None
    else:
        ttt = ''
        if not old_test:
            ttt = templates.parse_import(pkg, mdn)

    for t_func in t_funcs:
        if ast_util.has_test_function(old_test, t_func):
            continue
        fpo = ast_util.make_func_obj(t_func, pkg, mdn, module)
        ttt += templates.parse_func(fpo)

    for t_func, clazz in t_funcs_cls:
        if ast_util.has_test_function(old_test, t_func):
            continue
        fpo = ast_util.make_func_obj(t_func, pkg, mdn, module, clazz)
        ttt += templates.parse_func(fpo)
    return ttt


def main():
    """
    main function.
    """
    pas = argparse.ArgumentParser()
    pas.add_argument("filename", help="input python filename")
    pas.add_argument("--overwrite", help="overwrite test code", action="store_true")
    args = pas.parse_args()
    print('input:' + args.filename)
    # print(args.ovewrite)
    parse_file(args.filename, args.overwrite)
    return


if __name__ == "__main__":
    main()
