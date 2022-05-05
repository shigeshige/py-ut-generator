
import pytest
from unittest.mock import Mock, patch
from unittest.mock import MagicMock

from pyutgenerator import ast_util, files, run
from tests.pyutgenerator.data import pattern07


def test_output():
    """
    test
    """
    file_name = pattern07.__file__
    module = ast_util.create_ast(file_name)

    mmodule = files.get_package_moduel(file_name)
    t_file = mmodule.get_test_file_name()
    ttt1 = run.make_test_code(module, mmodule, True)

    ttt2 = files.read_file(t_file)

    assert ttt1 == ttt2
