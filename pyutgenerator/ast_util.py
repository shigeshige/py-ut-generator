"""
Generate test code tool

copyrigth https://github.com/shigeshige/py-ut-generator
"""

import ast
from typing import List, Optional, cast

from pyutgenerator import const, files
from pyutgenerator.objects import CallFunc, FuncArg, MockFunc, ParseFunc


def create_ast(file_name):
    """
    parse source file.
    """
    src = files.read_file(file_name)
    if not src:
        return None
    return ast.parse(src, file_name)


def get_function(module) -> List[ast.FunctionDef]:
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


def get_func_arg(func) -> List[FuncArg]:
    """
    関数の引数取得
    """
    prms = [FuncArg(a.arg, get_variable_values(func, a.arg))
            for a in func.args.args]
    return prms


def get_variable_values(func, name):
    """
    Get variable values in function.
    """

    ret = []
    for stm in ast.walk(func):
        if _equals(stm, const.AST_COMP):
            stm2 = cast(ast.Compare, stm)
            if (_equals(stm2.left, const.AST_NAME)
                    and stm2.left.id == name
                    and stm2.comparators):
                if _equals(stm2.comparators[0], const.AST_CONST):
                    # aaa > 0
                    ret.append(stm2.comparators[0].value)
                if _equals(stm2.comparators[0], const.AST_OPE):
                    # aaa > -1
                    ret.append(-stm2.comparators[0].operand.value)
            if (stm2.comparators
                    and _equals(stm2.comparators[0], const.AST_NAME)
                    and stm2.comparators[0].id == name
                    and _equals(stm2.left, const.AST_CONST)):
                # 1 > aaa
                ret.append(stm2.left.value)

    return ret


def get_calls(func) -> List[CallFunc]:
    """
    関数呼び出しを取得する
    """
    calls = []
    for stm in ast.walk(func):
        if _equals(stm, const.AST_CALL):
            stm2 = cast(ast.Call, stm)
            # print('---cal--')
            # call(hoge)
            cfo = None
            if _equals(stm2.func, const.AST_NAME):
                has_return = _has_return_call(stm, func)
                cfo = CallFunc('', stm2.func.id, has_return)
            # hoge.call(hoge)
            if (_equals(stm2.func, const.AST_ATTRIBUTE)
                    and _equals(stm2.func.value, const.AST_NAME)):
                has_return = _has_return_call(stm, func)
                cfo = CallFunc(stm2.func.value.id, stm2.func.attr, has_return)
            # hoge.hoge.call(hoge)
            if (_equals(stm2.func, const.AST_ATTRIBUTE)
                    and _equals(stm2.func.value, const.AST_ATTRIBUTE)
                    and _equals(stm2.func.value.value, const.AST_NAME)):
                has_return = _has_return_call(stm, func)
                cfo = CallFunc(
                    stm2.func.value.value.id, stm2.func.attr, has_return,
                    stm2.func.value.attr)
            if cfo:
                cfo.ats = stm
                calls.append(cfo)
    return calls


def get_funcs(module) -> List[ast.FunctionDef]:
    """
    get function list
    """
    return [
        cast(ast.FunctionDef, stm) for stm in ast.walk(module) if _equals(
            stm, const.AST_FUCNTION)]


def _has_return_call(call_obj, func):
    """
    call ast uses return value?
    """
    for stm in ast.walk(func):
        # bbb = aaa()
        if _equals(stm, const.AST_ASSIGN):
            for stm2 in ast.walk(stm.value):
                if stm2 is call_obj:
                    return True
        # bbb(aaa())
        if _equals(stm, const.AST_CALL):
            for stm2 in [j for i in stm.args for j in ast.walk(i)]:
                if stm2 is call_obj:
                    return True
        # if aaa():
        if _equals(stm, const.AST_IF) or _equals(stm, const.AST_WHILE):
            for stm2 in ast.walk(stm.test):
                if stm2 is call_obj:
                    return True
        # with aaa() as bbb
        if _equals(stm, const.AST_WITH):
            for stm2 in ast.walk(stm):
                if stm2 is call_obj:
                    return True
        # return aaa()
        if _equals(stm, const.AST_RETURN):
            for stm2 in ast.walk(stm):
                if stm2 is call_obj:
                    return True

    return False


def _create_mock_func(stm, clf: CallFunc, pkg, mdn) -> Optional[MockFunc]:
    """
    create mocks
    """
    # from xxx import yyy
    if clf.module in list(map(lambda x: x.name, stm.names)):
        return MockFunc(
            stm.module +
            '.' +
            clf.module +
            '.' +
            clf.func_name,
            clf.has_return)
    # from xxx.xxx import yyy
    if clf.func_name in list(map(lambda x: x.name, stm.names)):
        if clf.module:
            return MockFunc(
                stm.module +
                '.' +
                clf.module +
                '.' +
                clf.func_name,
                clf.has_return)
        else:
            return MockFunc(
                pkg + '.' + mdn + '.' + clf.func_name, clf.has_return)
    return None


def get_mocks(calls: List[CallFunc], module, pkg, mdn):
    """
    呼び出し先のモックを作成する。
    """
    mocks: List[MockFunc] = []
    for clf in calls:
        import_flg = False
        for stm in ast.walk(module):
            if _equals(stm, const.AST_IMPORT):
                names = get_import_names(stm)
                if names == clf.func_name and not clf.module:
                    # import xxx
                    import_flg = True
                elif names == clf.module:
                    # import xxx -> xxx.yyy.clf()
                    if clf.module2:
                        mocks.append(
                            MockFunc(
                                pkg +
                                '.' +
                                mdn +
                                '.' +
                                clf.module +
                                '.' +
                                clf.module2,
                                clf.has_return,
                                clf.func_name))
                    else:
                        # import xxx -> xxx.clf()
                        mocks.append(
                            MockFunc(
                                clf.module +
                                '.' +
                                clf.func_name,
                                clf.has_return))
                    import_flg = True
            if _equals(stm, const.AST_IMPORT_FROM):
                mck = _create_mock_func(stm, clf, pkg, mdn)
                if mck is not None:
                    mocks.append(mck)
        if import_flg:
            continue
        for stm in get_function(module):
            # def xxx():
            if not clf.module and clf.func_name == stm.name:
                mocks.append(
                    MockFunc(
                        pkg + '.' + mdn +
                        '.' + clf.func_name, clf.has_return))

    return mocks


def merge_mocks(mocks: List[MockFunc]):
    """
    merge same mock call.
    """
    ret: List[MockFunc] = []
    for mk1 in mocks:
        same = False
        for mk2 in ret:
            if mk1.mock_path == mk2.mock_path and mk1.func_name == mk2.func_name:
                mk2.call_count += 1
                same = True
                break
        if not same:
            ret.append(mk1)

    return ret


def get_import_names(stm: ast.Import):
    """
    join import names.
    """
    return '.'.join([x.name for x in stm.names])


def _equals(stm, class_name) -> bool:
    """
    check class name.
    """
    return stm.__class__.__name__ == class_name


def make_func_obj(
        t_func: ast.FunctionDef, package, module_name, module, class_name='') -> ParseFunc:
    """
    関数解析
    """

    pfo = ParseFunc(
        t_func.name, t_func,
        module_name,
        package,
        get_func_arg(t_func),
        get_calls(t_func),
        has_return_val(t_func))
    pfo.class_func = len(
        list(
            filter(
                lambda x: getattr(x, 'id', None) in [
                    'staticmethod', 'classmethod'],
                t_func.decorator_list))) != 0
    pfo.mocks = get_mocks(pfo.calls, module, package, module_name)
    pfo.mocks = merge_mocks(pfo.mocks)
    pfo.class_name = class_name
    return pfo
