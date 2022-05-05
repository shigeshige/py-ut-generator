"""
Generate test code tool


copyrigth https://github.com/shigeshige/py-ut-generator
"""
import argparse

from pyutgenerator import ast_util, files, templates
from pyutgenerator.objects import Module


def parse_file(file_name, renew=False):
    """
    generate test code.
    """
    modules = ast_util.create_ast(file_name)
    if not modules:
        print('File not Found :' + str(file_name))
        return

    module = files.get_package_moduel(file_name)
    t_file = module.get_test_file_name()
    ttt = make_test_code(modules, module, renew)

    files.write_file(t_file, ttt, not renew)


def make_test_code(asts, module: Module, renew):
    """
    make test code text.
    """

    t_funcs = ast_util.get_function(asts)
    t_funcs_cls = ast_util.get_function_class(asts)
    # test file name
    t_file = module.get_test_file_name()
    old_test = ast_util.create_ast(t_file)
    add_imports = []

    ttt = ''
    mock_open_flg = False

    if renew:
        old_test = None

    for t_func in t_funcs:
        if ast_util.has_test_function(old_test, t_func):
            continue
        fpo = ast_util.make_func_obj(t_func, module, asts)
        add_imports.extend(fpo.imports)
        ttt += templates.parse_func(fpo)
        if fpo.is_mock_open():
            mock_open_flg = True

    for t_func, clazz in t_funcs_cls:
        if ast_util.has_test_function(old_test, t_func):
            continue
        fpo = ast_util.make_func_obj(t_func, module, asts, clazz)
        add_imports.extend(fpo.imports)
        ttt += templates.parse_func(fpo)
        if fpo.is_mock_open():
            mock_open_flg = True

    if renew:
        ttt = templates.parse_import(module, mock_open_flg, set(add_imports)) + ttt
    else:
        if not old_test:
            ttt = templates.parse_import(module, mock_open_flg, set(add_imports)) + ttt
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


if __name__ == "__main__":
    main()
