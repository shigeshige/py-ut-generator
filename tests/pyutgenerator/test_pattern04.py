
import pytest
from unittest.mock import Mock, patch
from unittest.mock import MagicMock

from pyutgenerator import ast_util, files, run
from tests.pyutgenerator.data import pattern04


def test_aaa():
    file_name = pattern04.__file__
    module = ast_util.create_ast(file_name)

    mmodule = files.get_package_moduel(file_name)
    t_file = mmodule.get_test_file_name()
    ttt1 = run.make_test_code(module, mmodule, True)

    t_funcs = ast_util.get_function(module)
    fpo = ast_util.make_func_obj(t_funcs[0], mmodule, module)

    assert fpo.calls[0].is_with


def test_output():
    """
    test
    """
    file_name = pattern04.__file__
    module = ast_util.create_ast(file_name)

    mmodule = files.get_package_moduel(file_name)
    t_file = mmodule.get_test_file_name()
    ttt1 = run.make_test_code(module, mmodule, True)

    ttt2 = files.read_file(t_file)

    assert ttt1 == ttt2
