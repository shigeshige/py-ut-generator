
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from tests.pyutgenerator.data import pattern05

def test_aaa():
    # plan

    # do
    with\
            patch('tests.pyutgenerator.data.pattern05.bbb') as m1:
        m1.return_value = MagicMock()
        m1.return_value.eee = MagicMock(return_value=None)
        m1.return_value.ddd = MagicMock(return_value=None)
        pattern05.aaa()

        # check


def test_bbb():
    # plan

    # do


    ret = pattern05.bbb()

    # check
    assert ret

def test_ccc():
    # plan

    # do


    ret = pattern05.ccc()

    # check
    assert ret

def test_ddd():
    # plan

    # do


    target = pattern05.C1()
    ret = target.ddd()

    # check
    assert ret

def test_eee():
    # plan

    # do


    target = pattern05.C1()
    ret = target.eee()

    # check
    assert ret
