"""
Generate test code tool

copyrigth https://github.com/shigeshige/py-ut-generator
"""

import ast
from pyutgenerator import ast_util, files, templates

from pyutgenerator.objects import Module, ParseFunc, RaiseEx


def check(file_name):
    """
    check source file.
    """
    src = files.read_file(file_name)
    if not src:
        return True
    return not bool(ast.parse(src, file_name))


def make_test_code(module: Module, renew: bool):
    """
    make test code text.
    """

    asts = ast_util.create_ast(module.file_name)

    t_funcs = ast_util.get_function(asts)
    t_funcs_cls = ast_util.get_function_class(asts)
    # test file name
    t_file = module.get_test_file_name()
    old_test = ast_util.create_ast(t_file)
    add_imports = []

    t_txt = ''
    mock_open_flg = False

    if renew:
        old_test = None

    # nomal func
    for t_func in t_funcs:
        if ast_util.has_test_function(old_test, t_func):
            continue
        fpo = make_func_obj(t_func, module, asts)
        add_imports.extend(fpo.imports)
        t_txt += templates.parse_func(fpo)
        if fpo.is_mock_open():
            mock_open_flg = True

    # class func
    for t_func, clazz in t_funcs_cls:
        if ast_util.has_test_function(old_test, t_func):
            continue
        fpo = make_func_obj(t_func, module, asts, clazz)
        add_imports.extend(fpo.imports)
        t_txt += templates.parse_func(fpo)
        if fpo.is_mock_open():
            mock_open_flg = True

    if renew:
        t_txt = templates.parse_import(module, mock_open_flg, set(add_imports)) + t_txt
    else:
        if not old_test:
            t_txt = templates.parse_import(module, mock_open_flg, set(add_imports)) + t_txt
    return t_txt


def has_test_function(test_module, func):
    """
    check test function already has.
    """
    if not test_module:
        return False

    for stm in ast.walk(test_module):
        if isinstance(stm, ast.FunctionDef):
            if ast_util.get_test_func(func.name) == stm.name:
                return True
    return False


def get_raise(t_func: ast.FunctionDef):
    """
    analyze raise.
    """
    rai = []
    for stm in ast.walk(t_func):
        if isinstance(stm, ast.Raise):
            if isinstance(stm.exc, ast.Call) and isinstance(stm.exc.func, ast.Name):
                # raise Exception('aaaaaaa')
                rai.append(RaiseEx(stm.exc.func.id))
    return rai


def make_func_obj(
        t_func: ast.FunctionDef, module: Module, asts, class_name='') -> ParseFunc:
    """
    関数解析
    """
    calls = ast_util.get_calls(t_func)
    calls = ast_util.analyze_call_for_call(calls, t_func)
    ast_util.calls_with(t_func, calls)
    pfo = ParseFunc(
        t_func.name, t_func,
        module,
        ast_util.get_func_arg(t_func, bool(class_name), asts),
        calls,
        ast_util.has_return_val(t_func))
    pfo.class_func = len(
        list(
            filter(
                lambda x: getattr(x, 'id', None) in [
                    'staticmethod', 'classmethod'],
                t_func.decorator_list))) != 0
    pfo.mocks = ast_util.get_mocks(calls, asts, module)
    pfo.mocks = ast_util.merge_mocks(pfo.mocks)
    pfo.raises = get_raise(t_func)
    pfo.class_name = class_name
    for x in pfo.args:
        for y in x.values:
            if not y.is_literal and y.imports:
                pfo.imports.append(y.imports)

    return pfo
