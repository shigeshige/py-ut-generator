
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock



from tests.pyutgenerator.data import pattern09

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
