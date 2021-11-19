Mock Open File
==============


Mock Open Code
-------------------

It's difficult to mock the open function directly.
Please use unittest.mock.mock_open
It is easy to use and customize.

 unittest.mock.mock_open(mock=None, read_data=None)

    A helper function to create a mock to replace the use of open(). It works for open() called directly or used as a context manager.

    The mock argument is the mock object to configure. If None (the default) then a MagicMock will be created for you, with the API limited to methods or attributes available on standard file handles.

    read_data is a string for the read(), readline(), and readlines() methods of the file handle to return. Calls to those methods will take data from read_data until it is depleted. The mock of these methods is pretty simplistic: every time the mock is called, the read_data is rewound to the start. If you need more control over the data that you are feeding to the tested code you will need to customize this mock for yourself. When that is insufficient, one of the in-memory filesystem packages on PyPI can offer a realistic filesystem for testing.

    Changed in version 3.4: Added readline() and readlines() support. The mock of read() changed to consume read_data rather than returning it on each call.

    Changed in version 3.5: read_data is now reset on each call to the mock.


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
