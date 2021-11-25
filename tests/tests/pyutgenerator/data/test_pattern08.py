
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from pyutgenerator.const import FUNC_OPEN
from pyutgenerator import const

from tests.pyutgenerator.data import pattern08


def test_aaaa():
    # plan
    prm1 = ['V1', 'V2', const.FUNC_OPEN, FUNC_OPEN]
    # do

    ret = pattern08.aaaa(prm1[0])

    # check
    assert ret
