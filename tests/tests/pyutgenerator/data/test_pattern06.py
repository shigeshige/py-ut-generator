
import pytest
from unittest.mock import patch
from unittest.mock import mock_open
from unittest.mock import MagicMock

from tests.pyutgenerator.data import pattern06

def test_read_file():
    # plan
    file_name = None
    # do
    with\
            patch('tests.pyutgenerator.data.pattern06.os.path') as m1,\
            patch('tests.pyutgenerator.data.pattern06.open', mock_open(read_data='')) as m2:
        m1.return_value = None
        m1.exists = MagicMock(return_value=None)
        ret = pattern06.read_file(file_name)

        # check
        assert ret
