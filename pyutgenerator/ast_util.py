"""

copyrigth https://github.com/shigeshige/py-ut-generator
"""

import ast

from pyutgenerator import const, templates, files


def create_ast(file_name):
    """
    parse source file.
    """
    src = files.read_file(file_name)
    if not src:
        return None
    return ast.parse(src, file_name)


def get_function(module):
    """
    get function from module.
    """
    funcs = []
    for stm in module.body:
        if _equals(stm, const.AST_FUCNTION):
            funcs.append(stm)
    return funcs


def has_test_function(test_module, func):
    """
    check test function already has.
    """
    if not test_module:
        return False

    for stm in ast.walk(test_module):
        if _equals(stm, const.AST_FUCNTION):
            if templates.get_test_func(func.name) == stm.name:
                return True
    return False


def parse_import(module, pkg, mdn):
    """
    """
    owenr = f'from {pkg} import {mdn}'
    if not pkg:
        owenr = f'import {mdn}'

    return templates.parse_import(owenr)


def parse_func(func, pkg, mdn, module):
    """
    呼び出し関数の解析と出力
    """
    has_return = has_return_val(func)
    # print(func.name)
    calls = get_calls(func)
    mocks = get_mocks(calls, module, pkg, mdn)
    args = get_func_arg(func)
    inits = '\n'.join([templates.parse_varis(arg, 'None') for arg in args])
    name = func.name
    checks = ''
    if has_return:
        checks = templates.parse_assert(['ret'], mocks)
    return templates.parse_func(
        name,
        pkg,
        mdn,
        inits,
        has_return,
        args,
        mocks,
        checks)


def has_return_val(func):
    """
    返却値があるか？
    """
    for stm in ast.walk(func):
        if _equals(stm, const.AST_RETURN):
            if stm.value:
                return True
    return False


def get_func_arg(func):
    """
    関数の引数取得
    """
    prms = [a.arg for a in func.args.args]
    return prms


def get_calls(func):
    """
    関数呼び出しを取得する
    """
    calls = []
    for stm in ast.walk(func):
        if _equals(stm, const.AST_CALL):
            # print('---cal--')
            if _equals(stm.func, const.AST_NAME):
                has_return = _has_return_call(stm, func)
                calls.append(['', stm.func.id, has_return])
            if _equals(
                    stm.func,
                    const.AST_ATTRIBUTE) and _equals(
                        stm.func.value,
                        const.AST_NAME):
                has_return = _has_return_call(stm, func)
                calls.append([stm.func.value.id, stm.func.attr, has_return])
    return calls


def _get_funcs(module):
    """
    get function list
    """
    return [stm for stm in ast.walk(module) if _equals(stm, const.AST_FUCNTION)]


def _has_return_call(call_obj, func):
    """
    call ast uses return value?
    """
    for stm in ast.walk(func):
        if _equals(stm, const.AST_ASSIGN):
            for stm2 in ast.walk(stm.value):
                if stm2 is call_obj:
                    return True
        if _equals(stm, const.AST_CALL):
            for stm2 in [j for i in stm.args for j in ast.walk(i)]:
                if stm2 is call_obj:
                    return True
        if _equals(stm, const.AST_IF) or _equals(stm, const.AST_WHILE):
            for stm2 in ast.walk(stm.test):
                if stm2 is call_obj:
                    return True
        if _equals(stm, const.AST_WITH):
            for stm2 in ast.walk(stm.items):
                if stm2 is call_obj:
                    return True
    return False


def get_mocks(calls, module, pkg, mdn):
    """
    呼び出し先のモックを作成する。
    """
    mocks = []
    for c in calls:
        import_flg = False
        for stm in ast.walk(module):
            if _equals(stm, const.AST_IMPORT):
                if names_str(stm) == c[1] and not c[0]:
                    # import xxx
                    import_flg = True
                elif names_str(stm) == c[0]:
                    mocks.append([c[0] + '.' + c[1], c[2]])
                    import_flg = True
            if _equals(stm, const.AST_IMPORT_FROM):
                # from xxx inport yyy
                if c[0] in list(map(lambda x: x.name, stm.names)):
                    mocks.append([stm.module + '.' + c[0] + '.' + c[1], c[2]])
        if import_flg:
            continue
        for stm in get_function(module):
            # def xxx():
            if not c[0] and c[1] == stm.name:
                mocks.append([pkg + '.' + mdn + '.' + c[1], c[2]])

    return mocks


def names_str(stm):
    return '.'.join([x.name for x in stm.names])


def _equals(stm, class_name):
    """
    check class name.\
    """
    return stm.__class__.__name__ == class_name
