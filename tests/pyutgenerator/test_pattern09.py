
import pytest
from unittest.mock import Mock, patch
from unittest.mock import MagicMock

from pyutgenerator import ast_util, code_analysis, files, run
from tests.pyutgenerator.data import pattern09


def test_output():
    """
    test
    """
    file_name = pattern09.__file__

    mmodule = files.get_package_moduel(file_name)
    t_file = mmodule.get_test_file_name()
    ttt1 = code_analysis.make_test_code(mmodule, True)

    ttt2 = files.read_file(t_file)

    assert ttt1 == ttt2


def test_aaaa():
    # plan
    prm1 = None
    # do
    with\
            patch('tests.pyutgenerator.data.pattern09.os.path') as m1:
        m1.return_value = None
        m1.exists = MagicMock(return_value=None)
        ret = pattern09.aaaa(prm1)

        # check
        assert ret
