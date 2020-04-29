"""

copyrigth https://github.com/shigeshige/py-ut-generator
"""

import ast

from pyutgenerator import const, templates


def get_function(modeles):
    """
    file:///./pyutgenerator/const.py
    """
    funcs = []
    for stm in modeles.body:
        if _equals(stm, const.AST_FUCNTION):
            funcs.append(stm)
    return funcs


def parse_import(modu, pkg, mdn):
    """
    """
    owenr = f'from {pkg} import {mdn}'
    if not pkg:
        owenr = f'import {mdn}'

    return templates.parse_import(owenr)


def parse_func(func, pkg, mdn, modu):
    """
    呼び出し関数の解析と出力
    """
    has_return = has_return_val(func)
    print(func.name)
    calls = get_calls(func)
    mocks = get_mocks(calls, modu)
    args = get_func_arg(func)
    inits = '\n'.join([templates.parse_varis(arg, 'None') for arg in args])
    name = func.name
    return templates.parse_func(name, pkg, mdn, inits, has_return, args)


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
            if stm.func.__class__.__name__ == const.AST_NAME:
                calls.append(['', stm.func.id])
            if _equals(
                    stm.func,
                    const.AST_ATTRIBUTE) and _equals(
                    stm.func.value,
                    const.AST_NAME):
                calls.append([stm.func.value.id, stm.func.attr])
            # TODO: has return
    return calls


def get_mocks(calls, modu):
    """
    呼び出し先のモックを作成する。
    """
    mocks = []
    for c in calls:
        for stm in ast.walk(modu):
            if _equals(stm, const.AST_IMPORT):
                if names_str(stm) == c[0]:
                    print(stm)
                elif expression:
                    pass
    return mocks


def names_str(stm):
    return '.'.join([x.name for x in stm.names])


def _equals(stm, class_name):
    """
    クラス名の確認
    """
    return stm.__class__.__name__ == class_name
