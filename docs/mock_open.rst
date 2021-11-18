Mock Open File
==============


Mock Open Code
-------------------

It's difficult to mock the open function directly.
Please use unittest.mock.mock_open
It is easy to use and customize.

::

    import os


    def read_file(file_name):
        """
        read utf8 txt file.
        """
        if not os.path.exists(file_name):
            return None

        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()




Output Test Code
------------------------
::

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


Customize Test Code
--------------------
::

    import pytest
    from unittest.mock import patch
    from unittest.mock import mock_open
    from unittest.mock import MagicMock

    from tests.pyutgenerator.data import pattern06

    def test_read_file():
        # plan
        file_name = 'aaaa.txt'
        # do
        with\
                patch('tests.pyutgenerator.data.pattern06.os.path') as m1,\
                patch('tests.pyutgenerator.data.pattern06.open', mock_open(read_data='content')) as m2:
            m1.return_value = None
            m1.exists = MagicMock(return_value=True)
            ret = pattern06.read_file(file_name)

            # check
            assert ret == 'content'
