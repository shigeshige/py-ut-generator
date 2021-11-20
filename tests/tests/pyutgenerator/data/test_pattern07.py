
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from tests.pyutgenerator.data import pattern07

def test_aaaaa():
    # plan
    dic = {'K1': 'V1', 'K4': None, 'K2': None, 'K3': None}
    # do


    ret = pattern07.aaaaa(dic)

    # check
    assert ret
