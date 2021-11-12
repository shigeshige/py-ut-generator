Use Aage
============


Runs Tool
------------
::

    pyutgen "Input File Name"


Sample Input File
-------------------
::

    import os


    def aaaaa():
        """
        call and return
        """
        return os.path.exists('')



Sample Out Put Test Code
------------------------
::

    import pytest
    from unittest.mock import patch
    from unittest.mock import MagicMock

    from tests.pyutgenerator.data import pattern01

    def test_aaaaa():
        # plan

        # do
        with\
                patch('tests.pyutgenerator.data.pattern01.os.path') as m1:
            m1.return_value = None
            m1.exists = MagicMock(return_value=None)
            ret = pattern01.aaaaa()

            # check
            assert ret