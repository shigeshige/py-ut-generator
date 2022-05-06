
import pytest
from unittest.mock import Mock, patch
from unittest.mock import MagicMock

from pyutgenerator import ast_util, code_analysis, files, run
from tests.pyutgenerator.data import pattern05


def test_aaa():
    file_name = pattern05.__file__
    module = ast_util.create_ast(file_name)

    mmodule = files.get_package_moduel(file_name)
    t_file = mmodule.get_test_file_name()
    ttt1 = code_analysis.make_test_code(mmodule, True)

    t_funcs = ast_util.get_function(module)
    fpo = code_analysis.make_func_obj(t_funcs[0], mmodule, module)

    assert fpo.calls[1].call_calls


def test_output():
    """
    test
    """
    file_name = pattern05.__file__

    mmodule = files.get_package_moduel(file_name)
    t_file = mmodule.get_test_file_name()
    ttt1 = code_analysis.make_test_code(mmodule, True)

    ttt2 = files.read_file(t_file)

    assert ttt1 == ttt2
