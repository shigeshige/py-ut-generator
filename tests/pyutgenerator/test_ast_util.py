
import ast
from pyutgenerator.objects import MockFunc
from unittest.mock import MagicMock, patch

import pytest

from pyutgenerator import ast_util
from tests.pyutgenerator.data import td_funcs


def _get_module():
    return ast_util.create_ast(td_funcs.__file__)


def _get_func():
    return ast_util.create_ast(td_funcs.__file__).body[2]


def _get_func2():
    return ast_util.create_ast(td_funcs.__file__).body[3]


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
    module = _get_module()
    # do
    ret = ast_util.get_function(module)

    # check
    assert ret[0].name == 'func1'
    assert ret[1].name == 'func2'


def test_get_function_class():
    """
    test
    """
    # plan
    module = _get_module()
    # do
    ret = ast_util.get_function_class(module)

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
    test_module = _get_module()
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
    ret = ast_util.get_func_arg(func)

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
    module = _get_module()
    # do
    ret = ast_util.get_funcs(module)

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
    module = _get_module()
    pkg = 'test'
    mdn = 'test2'
    # do
    ret = ast_util.get_mocks(calls, module, pkg, mdn)

    # check
    assert ret[0].mock_path == 'test.test2.func1'


def test_get_import_names():
    """
    test
    """
    # plan
    stm = [
        x for x in ast.walk(
            _get_module()) if x.__class__.__name__ == 'Import'][0]
    # do

    ret = ast_util.get_import_names(stm)

    # check
    assert ret == 'os'


def test__equals():
    """
    test
    """
    # plan
    stm = _get_func()
    class_name = 'FunctionDef'
    # do
    ret = ast_util._equals(stm, class_name)
    # check
    assert ret


def test_make_func_obj():
    """
    test
    """
    # plan
    t_func = _get_func()
    pkg = 'pkg'
    mdn = 'module'
    module = 'name'
    class_name = 'class'
    # do
    ret = ast_util.make_func_obj(t_func, pkg, mdn, module, class_name)

    # check
    assert ret.name == 'func1'


def test_merge_mocks():
    mocks = [
        MockFunc('aaaa', True, 'bbb'),
        MockFunc('aaaa', True, 'bbb'),
        MockFunc('aaaa', True, 'bbb'),
    ]

    ret = ast_util.merge_mocks(mocks)
    assert ret[0].call_count == 3
