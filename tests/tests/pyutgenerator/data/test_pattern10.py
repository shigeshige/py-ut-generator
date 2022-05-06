
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock



from tests.pyutgenerator.data import pattern10

def test_aaaa():
    # plan
    prm1 = None
    # do


    with pytest.raises(ValueError) as _ex1:
        ret = pattern10.aaaa(prm1)

        # check
        assert ret
    assert str(_ex1.value) == ""

def test_bbbb():
    # plan
    prm1 = None
    # do


    ret = pattern10.bbbb(prm1)

    # check
    assert ret
