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
        if isinstance(stm, ast.FunctionDef):
            funcs.append(stm)
    return funcs


def get_function_class(module):
    """
    get function from class module.
    """
    funcs = []
    for stm in module.body:
        # class define
        if isinstance(stm, ast.ClassDef):
            for stm2 in stm.body:
                if isinstance(stm2, ast.FunctionDef):
                    funcs.append((stm2, stm.name))
    return funcs


def has_test_function(test_module, func):
    """
    check test function already has.
    """
    if not test_module:
        return False

    for stm in ast.walk(test_module):
        if isinstance(stm, ast.FunctionDef):
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
        if isinstance(stm, ast.Return):
            if stm.value:
                return True
    return False


def get_func_arg(func, is_class: bool) -> List[FuncArg]:
    """
    関数の引数取得
    """
    prms = [FuncArg(a.arg, get_variable_values(func, a.arg))
            for a in func.args.args]
    if is_class:
        return prms[1:]
    return prms


def get_variable_values(func, name):
    """
    Get variable values in function.
    """

    ret = []
    for stm in ast.walk(func):
        if isinstance(stm, ast.Compare):
            if (isinstance(stm.left, ast.Name)
                    and stm.left.id == name
                    and stm.comparators):
                if isinstance(stm.comparators[0], ast.Constant):
                    # aaa > 0
                    ret.append(stm.comparators[0].value)
                if (isinstance(stm.comparators[0], ast.UnaryOp)
                        and isinstance(stm.comparators[0].operand, ast.Constant)):
                    # aaa > -1
                    ret.append(-stm.comparators[0].operand.value)
            if (stm.comparators
                    and isinstance(stm.comparators[0], ast.Name)
                    and stm.comparators[0].id == name
                    and isinstance(stm.left, ast.Constant)):
                # 1 > aaa
                ret.append(stm.left.value)

    return ret


def get_calls(func) -> List[CallFunc]:
    """
    関数呼び出しを取得する
    """
    calls = []
    for stm in ast.walk(func):
        if isinstance(stm, ast.Call):
            # print('---cal--')
            # call(hoge)
            cfo = None
            if isinstance(stm.func, ast.Name):
                has_return = _has_return_call(stm, func)
                cfo = CallFunc('', stm.func.id, has_return)
            # hoge.call(hoge)
            if (isinstance(stm.func, ast.Attribute)
                    and isinstance(stm.func.value, ast.Name)):
                has_return = _has_return_call(stm, func)
                cfo = CallFunc(stm.func.value.id, stm.func.attr, has_return)
            # hoge.hoge.call(hoge)
            if (isinstance(stm.func, ast.Attribute)
                    and isinstance(stm.func.value, ast.Attribute)
                    and isinstance(stm.func.value.value, ast.Name)):
                has_return = _has_return_call(stm, func)
                cfo = CallFunc(
                    stm.func.value.value.id, stm.func.attr, has_return,
                    stm.func.value.attr)
            if (isinstance(stm.func, ast.Attribute)
                    and isinstance(stm.func.value, ast.Call)):
                has_return = _has_return_call(stm, func)
                cfo = CallFunc('', stm.func.attr, has_return)
            if cfo:
                cfo.ats = stm
                calls.append(cfo)
    return calls


def get_funcs(module) -> List[ast.FunctionDef]:
    """
    get function list
    """
    return [
        cast(ast.FunctionDef, stm) for stm in ast.walk(module) if isinstance(
            stm, ast.FunctionDef)]


def _get_parent(child: Optional[ast.AST], func: ast.AST) -> Optional[ast.AST]:

    if child is None:
        return None

    for stm in ast.walk(func):
        if hasattr(stm, 'value'):
            if getattr(stm, 'value') is child:
                return stm
    return None


def _is_same_origin(stm1: ast.AST, stm2: ast.AST, func: ast.AST) -> bool:
    """
    same origin val
    """
    name1 = None
    name2 = None
    if isinstance(stm1, ast.Assign) and isinstance(stm1.targets[0], ast.Name):
        name1 = stm1.targets[0].id
    if isinstance(stm1, ast.Attribute) and isinstance(stm1.value, ast.Name):
        name1 = stm1.value.id
    if isinstance(stm2, ast.Assign) and isinstance(stm2.targets[0], ast.Name):
        name2 = stm2.targets[0].id
    if isinstance(stm2, ast.Attribute) and isinstance(stm2.value, ast.Name):
        name2 = stm2.value.id

    return name1 is not None and name2 is not None and name1 == name2


def _has_return_call(call_obj, func):
    """
    call ast uses return value?
    """
    for stm in ast.walk(func):
        # bbb = aaa()
        if isinstance(stm, ast.Assign):
            for stm2 in ast.walk(stm.value):
                if stm2 is call_obj:
                    return True
        # bbb(aaa())
        if isinstance(stm, ast.Call):
            for stm2 in [j for i in stm.args for j in ast.walk(i)]:
                if stm2 is call_obj:
                    return True
        # if aaa():
        if isinstance(stm, ast.If) or isinstance(stm, ast.While):
            for stm2 in ast.walk(stm.test):
                if stm2 is call_obj:
                    return True
        # with aaa() as bbb
        if isinstance(stm, ast.With):
            for stm2 in ast.walk(stm):
                if stm2 is call_obj:
                    return True
        # return aaa()
        if isinstance(stm, ast.Return):
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
        return MockFunc(
            pkg + '.' + mdn + '.' + clf.func_name, clf.has_return)
    return None


def get_mocks(calls: List[CallFunc], module, pkg, mdn):
    """
    呼び出し先のモックを作成する。
    """
    mocks: List[MockFunc] = []
    for clf in calls:
        ope_flg = False
        for stm in ast.walk(module):
            if isinstance(stm, ast.Import):
                names = get_import_names(stm)
                if names == clf.func_name and not clf.module:
                    # import xxx
                    ope_flg = True
                elif names == clf.module:
                    # import xxx -> xxx.yyy.clf()
                    if clf.module2:
                        mck = MockFunc(
                            pkg + '.' + mdn + '.' +
                            clf.module + '.' + clf.module2, clf.has_return, clf.func_name)
                        mck.call_func = clf
                        mocks.append(mck)
                    else:
                        # import xxx -> xxx.clf()
                        mck = MockFunc(
                            clf.module + '.' +
                            clf.func_name, clf.has_return)
                        mck.call_func = clf
                        mocks.append(mck)
                    ope_flg = True
            if isinstance(stm, ast.ImportFrom):
                mck = _create_mock_func(stm, clf, pkg, mdn)
                if mck is not None:
                    mocks.append(mck)
        if ope_flg:
            continue
        for stm in get_function(module):
            # def xxx():
            if not clf.module and clf.func_name == stm.name:
                mck = MockFunc(pkg + '.' + mdn + '.' + clf.func_name, clf.has_return)
                mck.call_func = clf
                mocks.append(mck)
                ope_flg = True
        if not ope_flg and clf.func_name in const.BUILDINS:
            if const.FUNC_OPEN == clf.func_name:
                mck = MockFunc(pkg + '.' + mdn + '.' + clf.func_name, clf.has_return)
                mck.call_func = clf
                mck.open_flg = True
                mocks.append(mck)

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
                if mk1.call_func and mk2.call_func:
                    mk2.call_func.call_calls.extend(
                        [k for k in mk1.call_func.call_calls if (
                            k.func_name not in [j.func_name for j in mk2.call_func.call_calls])])
                    #    [k for k in  if mk2.callFunc.func_name != k.func_name])
                same = True
                break
        if not same:
            ret.append(mk1)

    return ret


def calls_with(t_func: ast.FunctionDef, calls: List[CallFunc]):
    """
    analyze call with.
    """
    for stm in ast.walk(t_func):
        if isinstance(stm, ast.With):
            for call in calls:
                for stm3 in ast.walk(stm.items[0]):
                    if stm3 is call.ats:
                        # with call() as xx:
                        call.is_with = True


def analyze_call_for_call(calls: List[CallFunc], t_func: ast.FunctionDef):
    """
    analyze call returns call
    """
    rets = []
    for call1 in calls:
        flg = False
        for call2 in calls:
            if (call1.ats and isinstance(call1.ats.func, ast.Attribute)
                    and call1.ats.func.value is call2.ats):
                flg = True
                # c02().c01()
                if call1.func_name not in [k.func_name for k in call2.call_calls]:
                    call2.call_calls.append(call1)
            # ccc = c02(); ccc.c01()
            par = _get_parent(call2.ats, t_func)
            if par is not None and call1.ats and _is_same_origin(par, call1.ats.func, t_func):
                flg = True
                if call1.func_name not in [k.func_name for k in call2.call_calls]:
                    call2.call_calls.append(call1)
        if not flg:
            rets.append(call1)
    return rets


def get_import_names(stm: ast.Import):
    """
    join import names.
    """
    return '.'.join([x.name for x in stm.names])


def make_func_obj(
        t_func: ast.FunctionDef, package, module_name, module, class_name='') -> ParseFunc:
    """
    関数解析
    """
    calls = get_calls(t_func)
    calls = analyze_call_for_call(calls, t_func)
    calls_with(t_func, calls)
    pfo = ParseFunc(
        t_func.name, t_func,
        module_name,
        package,
        get_func_arg(t_func, class_name),
        calls,
        has_return_val(t_func))
    pfo.class_func = len(
        list(
            filter(
                lambda x: getattr(x, 'id', None) in [
                    'staticmethod', 'classmethod'],
                t_func.decorator_list))) != 0
    pfo.mocks = get_mocks(calls, module, package, module_name)
    pfo.mocks = merge_mocks(pfo.mocks)
    pfo.class_name = class_name
    return pfo
