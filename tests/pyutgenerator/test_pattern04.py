
import pytest
from unittest.mock import Mock, patch
from unittest.mock import MagicMock

from pyutgenerator import ast_util, files, run
from tests.pyutgenerator.data import pattern04


def test_aaa():
    file_name = pattern04.__file__
    module = ast_util.create_ast(file_name)

    pkg, mdn = files.get_package_moduel(file_name)
    t_file = files.get_test_file_name(pkg, mdn)
    ttt1 = run.make_test_code(module, pkg, mdn, True)

    t_funcs = ast_util.get_function(module)
    fpo = ast_util.make_func_obj(t_funcs[0], pkg, mdn, module)

    assert fpo.calls[0].is_with


def test_output():
    """
    test
    """
    file_name = pattern04.__file__
    module = ast_util.create_ast(file_name)

    pkg, mdn = files.get_package_moduel(file_name)
    t_file = files.get_test_file_name(pkg, mdn)
    ttt1 = run.make_test_code(module, pkg, mdn, True)

    ttt2 = files.read_file(t_file)

    assert ttt1 == ttt2
