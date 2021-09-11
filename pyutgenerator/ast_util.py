"""
Generate test code tool

copyrigth https://github.com/shigeshige/py-ut-generator
"""

import ast
from typing import List

from pyutgenerator import const, files
from pyutgenerator.objects import CallFunc, MockFunc, ParseFunc


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


def get_function_class(module):
    """
    get function from class module.
    """
    funcs = []
    for stm in module.body:
        # class define
        if _equals(stm, const.AST_CLASS):
            for stm2 in stm.body:
                if _equals(stm2, const.AST_FUCNTION):
                    funcs.append((stm2, stm.name))
    return funcs


def has_test_function(test_module, func):
    """
    check test function already has.
    """
    if not test_module:
        return False

    for stm in ast.walk(test_module):
        if _equals(stm, const.AST_FUCNTION):
            if get_test_func(func.name) == stm.name:
                return True
    return False



def get_test_func(func_name):
    """
    test function name.
    """
    return const.STR_PRE_FUNC + func_name


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


def get_calls(func) -> List[CallFunc]:
    """
    関数呼び出しを取得する
    """
    calls = []
    for stm in ast.walk(func):
        if _equals(stm, const.AST_CALL):
            # print('---cal--')
            # call(hoge)
            if _equals(stm.func, const.AST_NAME):
                has_return = _has_return_call(stm, func)
                calls.append(CallFunc('', stm.func.id, has_return))
            # hoge.call(hoge)
            if _equals(
                    stm.func,
                    const.AST_ATTRIBUTE) and _equals(
                        stm.func.value,
                        const.AST_NAME):
                has_return = _has_return_call(stm, func)
                calls.append(CallFunc(stm.func.value.id, stm.func.attr, has_return))
            # hoge.hoge.call(hoge)
            if _equals(
                    stm.func, const.AST_ATTRIBUTE) and _equals(
                        stm.func.value, const.AST_ATTRIBUTE) and _equals(
                        stm.func.value.value, const.AST_NAME):
                has_return = _has_return_call(stm, func)
                calls.append(
                    CallFunc(
                        stm.func.value.attr, stm.func.attr, has_return,
                        stm.func.value.value.id))
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


def _create_mock_func(stm, cf: CallFunc, pkg, mdn):
    # from xxx import yyy
    if cf.module in list(map(lambda x: x.name, stm.names)):
        return MockFunc(
            stm.module + '.' + cf.module + '.' + cf.func_name, cf.has_return)
    # from xxx.xxx import yyy
    if cf.func_name in list(map(lambda x: x.name, stm.names)):
        if cf.module:
            return MockFunc(
                stm.module + '.' + cf.module + '.' + cf.func_name, cf.has_return)
        else:
            return MockFunc(
                pkg + '.' + mdn + '.' + cf.func_name, cf.has_return)
    return None


def get_mocks(calls: List[CallFunc], module, pkg, mdn):
    """
    呼び出し先のモックを作成する。
    """
    mocks: List[MockFunc] = []
    for c in calls:
        import_flg = False
        for stm in ast.walk(module):
            if _equals(stm, const.AST_IMPORT):
                if names_str(stm) == c.func_name and not c.module:
                    # import xxx
                    import_flg = True
                elif names_str(stm) == c.module:
                    if c.module2:
                        mocks.append(
                            MockFunc(
                                pkg + '.' + mdn + '.' + c.module2,
                                c.has_return, c.func_name))
                    else:
                        mocks.append(MockFunc(c.module + '.' + c.func_name, c.has_return))
                    import_flg = True
            if _equals(stm, const.AST_IMPORT_FROM):
                mck = _create_mock_func(stm, c, pkg, mdn)
                if mck is not None:
                    mocks.append(mck)
        if import_flg:
            continue
        for stm in get_function(module):
            # def xxx():
            if not c.module and c.func_name == stm.name:
                mocks.append(MockFunc(pkg + '.' + mdn + '.' + c.func_name, c.has_return))

    return mocks


def names_str(stm):
    """
    join names
    """
    return '.'.join([x.name for x in stm.names])


def _equals(stm, class_name):
    """
    check class name.\
    """
    return stm.__class__.__name__ == class_name


def make_func_obj(t_func, pkg, mdn, module, class_name='') -> ParseFunc:
    """
    関数解析
    """

    pfo = ParseFunc(
        t_func.name, t_func,
        mdn,
        pkg,
        get_func_arg(t_func),
        get_calls(t_func),
        has_return_val(t_func))
    pfo.class_func = len(
        list(
            filter(
                lambda x: getattr(x, 'id', None) in [
                    'staticmethod', 'classmethod'],
                t_func.decorator_list))) != 0
    pfo.mocks = get_mocks(pfo.calls, module, pkg, mdn)
    pfo.class_name = class_name
    return pfo
