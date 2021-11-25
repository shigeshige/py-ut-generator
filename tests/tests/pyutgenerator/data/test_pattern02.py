
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock



from tests.pyutgenerator.data import pattern02

def test_p01():
    # plan

    # do
    with\
            patch('tests.pyutgenerator.data.pattern02.f01') as m1:
        m1.side_effect = [None, None]
        ret = pattern02.p01()

        # check
        assert ret

def test_f01():
    # plan
    prm1 = None
    # do


    ret = pattern02.f01(prm1)

    # check
    assert ret
