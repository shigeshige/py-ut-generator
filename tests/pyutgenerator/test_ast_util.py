
import ast
from pyutgenerator.objects import MockFunc, Module
from unittest.mock import MagicMock, patch

import pytest

from pyutgenerator import ast_util, code_analysis
from tests.pyutgenerator.data import td_funcs


def _get_asts():
    return ast_util.create_ast(td_funcs.__file__)


def _get_func():
    asts = ast_util.create_ast(td_funcs.__file__)
    if asts:
        return asts.body[2]  # type: ignore
    return None


def _get_func2():
    asts = ast_util.create_ast(td_funcs.__file__)
    if asts:
        return asts.body[3]  # type: ignore
    return None


def test_create_ast():
    """
    test1
    """
    # plan
    file_name = td_funcs.__file__
    # do
    ret = ast_util.create_ast(file_name)

    # check
    assert ret


def test_get_function():
    """
    test
    """
    # plan
    asts = _get_asts()
    # do
    ret = ast_util.get_function(asts)

    # check
    assert ret[0].name == 'func1'
    assert ret[1].name == 'func2'


def test_get_function_class():
    """
    test
    """
    # plan
    asts = _get_asts()
    # do
    ret = ast_util.get_function_class(asts)

    # check
    assert ret[0][0].name == 'tf01'
    assert ret[0][1] == 'T001'
    assert ret[1][0].name == 'tf02'
    assert ret[1][1] == 'T001'


def test_has_test_function():
    """
    test
    """
    # plan
    test_module = _get_asts()
    func = _get_func()
    # do
    ret = ast_util.has_test_function(test_module, func)

    # check
    assert ret

    ret = ast_util.has_test_function([], func)

    # check
    assert not ret


def test_get_test_func():
    """
    test
    """
    # plan
    func_name = 'func1'
    # do

    ret = ast_util.get_test_func(func_name)

    # check
    assert ret == 'test_func1'


def test_has_return_val():
    """
    test
    """
    # plan
    func = _get_func()
    # do
    ret = ast_util.has_return_val(func)

    # check
    assert ret


def test_get_func_arg():
    """
    test
    """
    # plan
    func = _get_func2()

    # do
    ret = ast_util.get_func_arg(func, False, None)  # type: ignore

    # check
    assert [x.arg_name for x in ret] == ['prm1', 'prm2']


def test_get_calls():
    """
    test
    """
    # plan
    func = _get_func2()
    # do
    ret = ast_util.get_calls(func)

    # check
    assert ret[0].func_name == 'func1'


def test_get_funcs():
    """
    test
    """
    # plan
    asts = _get_asts()
    # do
    ret = ast_util.get_funcs(asts)

    # check
    assert ret[0].name == 'func1'


def test__has_return_call():
    """
    test
    """
    # plan
    call_obj = _get_func()
    func = _get_func2()
    # do
    ret = ast_util._has_return_call(call_obj, func)

    # check
    assert not ret  # TODO


def test_get_mocks():
    """
    test
    """
    # plan
    calls = ast_util.get_calls(_get_func2())
    asts = _get_asts()
    pkg = 'test'
    mdn = 'test2'
    # do
    ret = ast_util.get_mocks(calls, asts, Module(pkg, mdn))

    # check
    assert ret[0].mock_path == 'func1'
    assert ret[0].module.pakage_name == 'test'
    assert ret[0].module.module_name == 'test2'


def test_get_import_names():
    """
    test
    """
    # plan
    stm = [
        x for x in ast.walk(
            _get_asts()) if x.__class__.__name__ == 'Import'][0]  # type: ignore
    # do

    ret = ast_util.get_import_names(stm)  # type: ignore

    # check
    assert ret == 'os'


def test_make_func_obj():
    """
    test
    """
    # plan
    t_func = _get_func()
    pkg = 'pkg'
    mdn = 'module'
    asts = 'name'
    class_name = 'class'
    # do
    ret = code_analysis.make_func_obj(t_func, Module(pkg, mdn), asts, class_name)

    # check
    assert ret.name == 'func1'


def test_merge_mocks():
    mocks = [
        MockFunc('aaaa', True, Module(), 'bbb'),
        MockFunc('aaaa', True, Module(), 'bbb'),
        MockFunc('aaaa', True, Module(), 'bbb'),
    ]

    ret = ast_util.merge_mocks(mocks)
    assert ret[0].call_count == 3
