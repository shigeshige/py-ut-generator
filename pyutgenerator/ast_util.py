"""

copyrigth https://github.com/shigeshige/py-ut-generator
"""

import ast

from pyutgenerator import const, templates, files


def create_ast(file_name):
    """
    """
    src = files.read_file(file_name)
    return ast.parse(src, file_name)


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
    # print(func.name)
    calls = get_calls(func)
    mocks = get_mocks(calls, modu)
    args = get_func_arg(func)
    inits = '\n'.join([templates.parse_varis(arg, 'None') for arg in args])
    name = func.name
    checks = ''
    if has_return:
        checks = templates.parse_assert(['ret'])
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
        import_flg = False
        for stm in ast.walk(modu):
            if _equals(stm, const.AST_IMPORT):
                if names_str(stm) == c[1] and not c[0]:
                    # import xxx
                    # print(names_str(stm))
                    import_flg = True
                elif names_str(stm) == c[0]:
                    mocks.append([c[0] + '.' + c[1]])
                    import_flg = True
            if _equals(stm, const.AST_IMPORT_FROM):
                # print(stm)
                if c[0] in list(map(lambda x: x.name, stm.names)):
                    mocks.append([stm.module + '.' + c[0] + '.' + c[1]])
    return mocks


def names_str(stm):
    return '.'.join([x.name for x in stm.names])


def _equals(stm, class_name):
    """
    クラス名の確認
    """
    return stm.__class__.__name__ == class_name
