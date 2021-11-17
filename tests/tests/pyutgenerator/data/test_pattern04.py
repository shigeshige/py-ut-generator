
import pytest
from unittest.mock import patch
from unittest.mock import mock_open
from unittest.mock import MagicMock

from tests.pyutgenerator.data import pattern04

def test_aaa():
    # plan

    # do
    with\
            patch('tests.pyutgenerator.data.pattern04.bbb') as m1:
        m1.return_value = MagicMock()
        m1.return_value.__enter__ = MagicMock()
        pattern04.aaa()

        # check


def test_bbb():
    # plan

    # do
    with\
            patch('tests.pyutgenerator.data.pattern04.open', mock_open(read_data='')) as m1:

        ret = pattern04.bbb()

        # check
        assert ret
